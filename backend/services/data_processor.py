import json
import pandas as pd
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class DataProcessor:
    @staticmethod
    def validate_host_data(host_data: Dict[str, Any]) -> bool:
        """Validate if host data has minimum required fields."""
        required_fields = ['ip']
        return all(field in host_data for field in required_fields)
    
    @staticmethod
    def clean_host_data(hosts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean and normalize host data."""
        cleaned_hosts = []
        
        for host in hosts:
            if DataProcessor.validate_host_data(host):
                # Extract services info
                services = host.get('services', [])
                ports = [s.get('port') for s in services if s.get('port')]
                protocols = [s.get('protocol') for s in services if s.get('protocol')]
                
                # Extract vulnerabilities
                vulnerabilities = []
                for service in services:
                    if 'vulnerabilities' in service:
                        vulnerabilities.extend(service['vulnerabilities'])
                
                # Extract malware info
                malware_detected = None
                for service in services:
                    if 'malware_detected' in service:
                        malware_detected = service['malware_detected']
                        break
                
                # Extract key fields and normalize
                cleaned_host = {
                    'ip': host.get('ip'),
                    'ports': ports,
                    'protocols': list(set(protocols)) if protocols else [],
                    'service_count': len(services),
                    'country': DataProcessor._extract_country(host),
                    'city': DataProcessor._extract_city(host),
                    'asn': DataProcessor._extract_asn(host),
                    'organization': DataProcessor._extract_organization(host),
                    'hostname': DataProcessor._extract_hostname(host),
                    'vulnerabilities': vulnerabilities,
                    'vulnerability_count': len(vulnerabilities),
                    'malware_detected': malware_detected,
                    'risk_level': DataProcessor._extract_risk_level(host),
                    'has_critical_vulns': any(v.get('severity') == 'critical' for v in vulnerabilities)
                }
                cleaned_hosts.append(cleaned_host)
            else:
                logger.warning(f"Skipping invalid host data: {host}")
        
        return cleaned_hosts
    
    @staticmethod
    def _extract_service_name(host: Dict[str, Any]) -> Optional[str]:
        """Extract service name from host data."""
        services = host.get('services', [])
        if services and len(services) > 0:
            return services[0].get('service_name') or services[0].get('protocol')
        return host.get('service_name')
    
    @staticmethod
    def _extract_country(host: Dict[str, Any]) -> Optional[str]:
        """Extract country from host data."""
        location = host.get('location', {})
        return location.get('country') or location.get('country_code')
    
    @staticmethod
    def _extract_city(host: Dict[str, Any]) -> Optional[str]:
        """Extract city from host data."""
        location = host.get('location', {})
        return location.get('city')
    
    @staticmethod
    def _extract_asn(host: Dict[str, Any]) -> Optional[int]:
        """Extract ASN from host data."""
        autonomous_system = host.get('autonomous_system', {})
        return autonomous_system.get('asn')
    
    @staticmethod
    def _extract_organization(host: Dict[str, Any]) -> Optional[str]:
        """Extract organization from host data."""
        autonomous_system = host.get('autonomous_system', {})
        return autonomous_system.get('name') or autonomous_system.get('organization')
    
    @staticmethod
    def _extract_hostname(host: Dict[str, Any]) -> Optional[str]:
        """Extract hostname from host data."""
        dns = host.get('dns', {})
        return dns.get('hostname')
    
    @staticmethod
    def _extract_risk_level(host: Dict[str, Any]) -> Optional[str]:
        """Extract risk level from host data."""
        threat_intel = host.get('threat_intelligence', {})
        return threat_intel.get('risk_level')
    
    @staticmethod
    def get_summary_stats(hosts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate basic statistics about the host data."""
        if not hosts:
            return {}
        
        df = pd.DataFrame(hosts)
        
        # Calculate vulnerability stats
        total_vulns = sum(h.get('vulnerability_count', 0) for h in hosts)
        critical_hosts = sum(1 for h in hosts if h.get('has_critical_vulns', False))
        malware_hosts = sum(1 for h in hosts if h.get('malware_detected'))
        
        stats = {
            'total_hosts': len(hosts),
            'unique_ips': df['ip'].nunique() if 'ip' in df else 0,
            'unique_countries': df['country'].nunique() if 'country' in df else 0,
            'total_services': sum(h.get('service_count', 0) for h in hosts),
            'total_vulnerabilities': total_vulns,
            'critical_vulnerability_hosts': critical_hosts,
            'malware_detected_hosts': malware_hosts,
            'top_countries': df['country'].value_counts().head(5).to_dict() if 'country' in df else {},
            'top_organizations': df['organization'].value_counts().head(5).to_dict() if 'organization' in df else {},
            'risk_levels': df['risk_level'].value_counts().to_dict() if 'risk_level' in df else {}
        }
        
        return stats