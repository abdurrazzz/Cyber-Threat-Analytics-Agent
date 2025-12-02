from groq import Groq
import json
import logging
from typing import Dict, List, Any
from config import Config

logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        
    def create_summarization_prompt(self, hosts: List[Dict], summary_type: str = "detailed") -> str:
        """Create prompt for host data summarization based on summary type."""
        
        # Base data
        host_data = json.dumps(hosts, indent=2)
        
        if summary_type == "brief":
            prompt = f"""Analyze this Censys host data and provide a BRIEF executive summary (3-4 paragraphs max).

{host_data}

Focus on:
- Total hosts and locations
- Most critical vulnerabilities (CVE IDs only)
- Any malware detected
- Overall risk level

Keep it concise and high-level. No detailed explanations."""

        elif summary_type == "technical":
            prompt = f"""Analyze this Censys host data and provide a DETAILED TECHNICAL analysis for security engineers.

{host_data}

Include:
1. Complete vulnerability breakdown (all CVEs with CVSS scores, exploit status)
2. Service enumeration (protocols, ports, banners, software versions)
3. Certificate analysis (self-signed, issuers, fingerprints)
4. Malware technical details (C2 infrastructure, threat actor TTPs)
5. Network infrastructure (ASNs, DNS, hosting providers)
6. Specific exploitation paths and attack vectors
7. Technical remediation steps with commands/procedures

Use technical terminology. Be comprehensive and detailed."""

        else:  # detailed (default)
            prompt = f"""Analyze this Censys host data and provide a DETAILED security analysis for SOC analysts.

{host_data}

Provide a structured analysis including:
1. **Overview**: Host count, geographic distribution, organizations
2. **Vulnerability Analysis**: 
   - CVEs with severity levels and CVSS scores
   - Known exploited vulnerabilities (KEVs)
   - Affected hosts
3. **Malware & Threats**: 
   - Detected malware families
   - Threat actor associations
   - C2 infrastructure
4. **Service Exposure**: 
   - Running services and protocols
   - Authentication status
   - Misconfigurations
5. **Risk Assessment**: Overall security posture
6. **Recommendations**: Prioritized action items

Balance technical detail with readability. Be specific about CVE IDs and threat actors."""

        return prompt

    def summarize_hosts(self, hosts: List[Dict], summary_type: str = "detailed") -> Dict[str, Any]:
        """Generate AI-powered summary using Groq."""
        try:
            prompt = self.create_summarization_prompt(hosts, summary_type)
            
            logger.info(f"Generating {summary_type} summary...")
            
            # Adjust token limits based on summary type
            if summary_type == "brief":
                max_tokens = 500
            elif summary_type == "technical":
                max_tokens = 2000
            else:
                max_tokens = 1500
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a cybersecurity analyst providing a {summary_type} security analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            
            summary_text = response.choices[0].message.content
            
            # Extract insights - adjust based on summary type
            if summary_type == "brief":
                insights_prompt = f"""From this brief analysis, list exactly 3 key security concerns as bullet points:

{summary_text}

Format as:
- [First concern]
- [Second concern]
- [Third concern]

One sentence each."""
                num_insights = 3
            else:
                insights_prompt = f"""From this security analysis, extract exactly 5 key insights as bullet points:

{summary_text}

Format as:
- [First key insight]
- [Second key insight]
- [Third key insight]
- [Fourth key insight]
- [Fifth key insight]

One concise sentence each. Focus on most critical findings."""
                num_insights = 5
            
            insights_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": insights_prompt}],
                max_tokens=300,
                temperature=0.2
            )
            
            insights_text = insights_response.choices[0].message.content
            key_insights = [
                insight.strip().lstrip('•-* ').lstrip('**').rstrip('**').strip()
                for insight in insights_text.split('\n') 
                if insight.strip() and any(c in insight for c in ['-', '•', '*'])
            ][:num_insights]
            
            # Risk assessment
            risk_prompt = f"""Based on this analysis, provide a {summary_type} security risk assessment (2-3 sentences):

{summary_text}

Focus on overall risk level and priority actions needed."""
            
            risk_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": risk_prompt}],
                max_tokens=200,
                temperature=0.2
            )
            
            risk_assessment = risk_response.choices[0].message.content.strip()
            
            logger.info(f"Successfully generated {summary_type} summary")
            
            return {
                "summary": summary_text,
                "key_insights": key_insights if key_insights else [f"{summary_type.capitalize()} analysis completed - see summary for details"],
                "risk_assessment": risk_assessment,
                "host_count": len(hosts)
            }
            
        except Exception as e:
            logger.error(f"AI summarization failed: {str(e)}")
            raise Exception(f"Failed to generate summary: {str(e)}")