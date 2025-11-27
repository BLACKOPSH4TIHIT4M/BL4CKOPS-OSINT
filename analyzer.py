#!/usr/bin/env python3
"""
Amera.py Code Analyzer
Tool untuk menganalisis dan breakdown file amera.py
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Set

class AmeraAnalyzer:
    """Analyze Amera.py Google Dorking tool"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.code = ""
        self.analysis = {}
        
    def load_file(self):
        """Load file content"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.code = f.read()
            print(f"[+] Loaded file: {self.file_path}")
            print(f"[+] File size: {len(self.code)} characters\n")
            return True
        except Exception as e:
            print(f"[-] Error loading file: {e}")
            return False
    
    def extract_imports(self) -> Set[str]:
        """Extract all import statements"""
        imports = set()
        
        # Standard imports
        patterns = [
            r'^import\s+([\w,\s]+)',
            r'^from\s+([\w.]+)\s+import',
        ]
        
        for line in self.code.split('\n'):
            for pattern in patterns:
                match = re.match(pattern, line.strip())
                if match:
                    imports.add(match.group(1).split()[0])
        
        return imports
    
    def extract_functions(self) -> List[Dict]:
        """Extract all function definitions"""
        functions = []
        
        pattern = r'^def\s+(\w+)\s*\([^)]*\):'
        
        for line_num, line in enumerate(self.code.split('\n'), 1):
            match = re.match(pattern, line)
            if match:
                func_name = match.group(1)
                functions.append({
                    'name': func_name,
                    'line': line_num,
                    'signature': line.strip()
                })
        
        return functions
    
    def extract_google_dorks(self) -> List[Dict]:
        """Extract all Google Dork patterns used"""
        dorks = []
        
        # Pattern untuk variabel yang berisi dork
        pattern = r'data\d*\s*=\s*["\']([^"\']+)["\']'
        
        for line_num, line in enumerate(self.code.split('\n'), 1):
            matches = re.findall(pattern, line)
            for match in matches:
                if any(keyword in match.lower() for keyword in 
                       ['site:', 'filetype:', 'intext:', 'intitle:', 'inurl:', 'related:', 'link:', 'info:']):
                    dorks.append({
                        'dork': match,
                        'line': line_num,
                        'type': self.classify_dork(match)
                    })
        
        return dorks
    
    def classify_dork(self, dork: str) -> str:
        """Classify type of Google Dork"""
        dork_lower = dork.lower()
        
        if 'filetype:' in dork_lower:
            return 'File Search'
        elif 'intext:password' in dork_lower or 'password' in dork_lower:
            return 'Password Search'
        elif '@' in dork_lower or 'email' in dork_lower:
            return 'Email Search'
        elif 'intext:' in dork_lower:
            return 'Text Search'
        elif 'site:' in dork_lower:
            return 'Site-specific Search'
        elif 'intitle:' in dork_lower:
            return 'Title Search'
        elif 'inurl:' in dork_lower:
            return 'URL Search'
        else:
            return 'Other'
    
    def analyze_security_risks(self) -> Dict:
        """Analyze security and privacy risks"""
        risks = {
            'credential_theft': [],
            'personal_info': [],
            'file_exposure': [],
            'api_keys': [],
        }
        
        code_lower = self.code.lower()
        
        # Check for credential-related searches
        if 'password' in code_lower or 'username' in code_lower:
            risks['credential_theft'].append('Searches for passwords and usernames')
        
        # Check for personal info
        if 'email' in code_lower or 'phone' in code_lower or 'whatsapp' in code_lower:
            risks['personal_info'].append('Scrapes emails and phone numbers')
        
        # Check for file types
        file_types = re.findall(r'filetype:(\w+)', code_lower)
        if file_types:
            risks['file_exposure'] = list(set(file_types))
        
        # Check for API keys
        if 'api' in code_lower or 'key' in code_lower:
            risks['api_keys'].append('Searches for API keys')
        
        return risks
    
    def extract_target_sites(self) -> Set[str]:
        """Extract targeted websites/platforms"""
        sites = set()
        
        # Social media platforms
        social_patterns = [
            'instagram.com',
            'facebook.com',
            'twitter.com',
            'linkedin.com',
        ]
        
        for pattern in social_patterns:
            if pattern in self.code.lower():
                sites.add(pattern)
        
        return sites
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("="*70)
        print("AMERA.PY ANALYSIS REPORT")
        print("="*70)
        
        # Imports
        print("\n[*] IMPORTED LIBRARIES:")
        imports = self.extract_imports()
        for imp in sorted(imports):
            print(f"  - {imp}")
        
        # Functions
        print(f"\n[*] FUNCTIONS FOUND: {len(self.extract_functions())}")
        functions = self.extract_functions()
        for func in functions[:10]:  # Show first 10
            print(f"  - {func['name']}() at line {func['line']}")
        if len(functions) > 10:
            print(f"  ... and {len(functions) - 10} more")
        
        # Google Dorks
        print("\n[*] GOOGLE DORKS ANALYSIS:")
        dorks = self.extract_google_dorks()
        
        # Group by type
        dork_types = {}
        for dork in dorks:
            dtype = dork['type']
            if dtype not in dork_types:
                dork_types[dtype] = []
            dork_types[dtype].append(dork)
        
        for dtype, dork_list in dork_types.items():
            print(f"\n  {dtype}: {len(dork_list)} dorks")
            for dork in dork_list[:3]:  # Show first 3 of each type
                print(f"    - {dork['dork'][:60]}...")
        
        # Security Risks
        print("\n[*] SECURITY & PRIVACY RISKS:")
        risks = self.analyze_security_risks()
        
        for risk_type, risk_list in risks.items():
            if risk_list:
                print(f"\n  {risk_type.upper().replace('_', ' ')}:")
                for risk in risk_list:
                    print(f"    - {risk}")
        
        # Target sites
        print("\n[*] TARGETED PLATFORMS:")
        sites = self.extract_target_sites()
        for site in sorted(sites):
            print(f"  - {site}")
        
        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Total Functions: {len(functions)}")
        print(f"Total Google Dorks: {len(dorks)}")
        print(f"Risk Level: HIGH (Reconnaissance Tool)")
        print("\nPURPOSE: Google Dorking & OSINT for information gathering")
        print("USE CASE: Reconnaissance phase of penetration testing")
        print("WARNING: Can be used for malicious purposes")
        print("="*70)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Amera.py Code Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('file', help='Path to amera.py file')
    
    args = parser.parse_args()
    
    analyzer = AmeraAnalyzer(args.file)
    
    if analyzer.load_file():
        analyzer.generate_report()


if __name__ == '__main__':
    main()
