#!/usr/bin/env python3
"""
Python Malware Deobfuscator - Fixed Version
Production-grade tool for analyzing obfuscated Python malware
WARNING: Only use in isolated/sandboxed environment!
"""

import base64
import zlib
import marshal
import dis
import ast
import re
import sys
from typing import Optional, Dict, Any
from pathlib import Path

class MalwareDeobfuscator:
    """Deobfuscate multi-layer encrypted Python malware"""
    
    def __init__(self, input_file: str, output_dir: str = "deobfuscated_output"):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = {}
        
    def extract_encrypted_data(self, code: str) -> Dict[str, str]:
        """Extract encryption key and encrypted payload from obfuscated code"""
        data = {}
        
        print("[*] Trying different extraction patterns...")
        
        # Pattern 1: Standard variable assignment with quotes
        key_patterns = [
            r'__mikey__\s*=\s*["\']([^"\']+)["\']',
            r'__mikey__\s*=\s*b?["\']([^"\']+)["\']',
            r'key\s*=\s*["\']([^"\']+)["\']',
            r'fernet_key\s*=\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in key_patterns:
            key_match = re.search(pattern, code, re.IGNORECASE)
            if key_match:
                try:
                    data['fernet_key_b64'] = key_match.group(1)
                    data['fernet_key'] = base64.b64decode(data['fernet_key_b64'])
                    print(f"[+] Extracted Fernet key: {data['fernet_key_b64'][:50]}...")
                    break
                except:
                    continue
        
        # Pattern 2: Encrypted payload patterns
        payload_patterns = [
            r'mydata\s*=\s*["\']([0-9a-fA-F]+)["\']',
            r'data\s*=\s*["\']([0-9a-fA-F]+)["\']',
            r'payload\s*=\s*["\']([0-9a-fA-F]+)["\']',
            r'encrypted\s*=\s*["\']([0-9a-fA-F]+)["\']',
            # Multi-line string
            r'mydata\s*=\s*["\']([0-9a-fA-F\s]+)["\']',
        ]
        
        for pattern in payload_patterns:
            payload_match = re.search(pattern, code, re.IGNORECASE | re.DOTALL)
            if payload_match:
                hex_data = payload_match.group(1).replace(' ', '').replace('\n', '')
                if len(hex_data) > 100:  # Reasonable payload size
                    data['encrypted_hex'] = hex_data
                    print(f"[+] Extracted encrypted payload: {len(data['encrypted_hex'])} chars")
                    break
        
        # If patterns fail, try to find ANY long hex string
        if 'encrypted_hex' not in data:
            print("[*] Pattern matching failed, searching for hex strings...")
            hex_strings = re.findall(r'["\']([0-9a-fA-F]{200,})["\']', code, re.DOTALL)
            if hex_strings:
                data['encrypted_hex'] = hex_strings[0].replace(' ', '').replace('\n', '')
                print(f"[+] Found hex string: {len(data['encrypted_hex'])} chars")
        
        # If still nothing, try base64 encoded data
        if 'encrypted_hex' not in data:
            print("[*] Searching for base64 encoded data...")
            b64_strings = re.findall(r'["\']([A-Za-z0-9+/=]{200,})["\']', code, re.DOTALL)
            if b64_strings:
                data['encrypted_b64'] = b64_strings[0].replace(' ', '').replace('\n', '')
                print(f"[+] Found base64 string: {len(data['encrypted_b64'])} chars")
        
        # Debug: Show what we found
        print(f"\n[DEBUG] Extracted data keys: {list(data.keys())}")
        
        return data
    
    def decrypt_fernet_layer(self, encrypted_data: str, fernet_key: bytes, is_hex: bool = True) -> bytes:
        """Decrypt Fernet encryption layer"""
        try:
            from cryptography.fernet import Fernet
            
            # Convert to bytes
            if is_hex:
                encrypted_bytes = bytes.fromhex(encrypted_data)
                print(f"[+] Layer 1: Converted hex to bytes ({len(encrypted_bytes)} bytes)")
            else:
                encrypted_bytes = base64.b64decode(encrypted_data)
                print(f"[+] Layer 1: Decoded base64 to bytes ({len(encrypted_bytes)} bytes)")
            
            # Fernet decrypt
            cipher = Fernet(fernet_key)
            decrypted = cipher.decrypt(encrypted_bytes)
            print(f"[+] Layer 2: Fernet decrypted ({len(decrypted)} bytes)")
            
            return decrypted
        except Exception as e:
            print(f"[-] Fernet decryption failed: {e}")
            return None
    
    def decode_base64_layer(self, data: bytes) -> bytes:
        """Decode Base64 layer"""
        try:
            decoded = base64.b64decode(data)
            print(f"[+] Layer 3: Base64 decoded ({len(decoded)} bytes)")
            return decoded
        except Exception as e:
            print(f"[-] Base64 decoding failed: {e}")
            return None
    
    def decode_base32_layer(self, data: bytes) -> bytes:
        """Decode Base32 layer"""
        try:
            decoded = base64.b32decode(data)
            print(f"[+] Layer 4: Base32 decoded ({len(decoded)} bytes)")
            return decoded
        except Exception as e:
            print(f"[-] Base32 decoding failed: {e}")
            return None
    
    def decompress_zlib_layer(self, data: bytes) -> bytes:
        """Decompress zlib compressed data"""
        try:
            decompressed = zlib.decompress(data)
            print(f"[+] Layer 5: Zlib decompressed ({len(decompressed)} bytes)")
            return decompressed
        except Exception as e:
            print(f"[-] Zlib decompression failed: {e}")
            return None
    
    def unmarshal_bytecode(self, data: bytes) -> Any:
        """Unmarshal Python bytecode"""
        try:
            code_obj = marshal.loads(data)
            print(f"[+] Layer 6: Marshal loaded (code object)")
            return code_obj
        except Exception as e:
            print(f"[-] Marshal loading failed: {e}")
            return None
    
    def disassemble_bytecode(self, code_obj: Any) -> str:
        """Disassemble Python bytecode to readable format"""
        try:
            import io
            output = io.StringIO()
            dis.dis(code_obj, file=output)
            disassembled = output.getvalue()
            print(f"[+] Bytecode disassembled ({len(disassembled)} chars)")
            return disassembled
        except Exception as e:
            print(f"[-] Bytecode disassembly failed: {e}")
            return None
    
    def analyze_code_behavior(self, code: str) -> Dict[str, list]:
        """Analyze code for suspicious patterns"""
        patterns = {
            'imports': re.findall(r'import\s+(\w+)', code),
            'network': re.findall(r'(requests|urllib|socket|http\.client)\.\w+', code),
            'file_operations': re.findall(r'(open|read|write|remove|unlink)\s*\(', code),
            'subprocess': re.findall(r'(subprocess|os\.system|os\.popen|eval|exec)\s*\(', code),
            'encryption': re.findall(r'(base64|crypto|fernet|aes|rsa)\.\w+', code),
            'persistence': re.findall(r'(startup|registry|cron|systemd)\.\w+', code),
        }
        
        print("\n[*] Behavioral Analysis:")
        for category, matches in patterns.items():
            if matches:
                print(f"  - {category.upper()}: {set(matches)}")
        
        return patterns
    
    def save_results(self, stage: str, data: Any, extension: str = "txt"):
        """Save intermediate results to files"""
        output_file = self.output_dir / f"stage_{stage}.{extension}"
        
        try:
            if isinstance(data, bytes):
                with open(output_file, 'wb') as f:
                    f.write(data)
            else:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(str(data))
            print(f"[+] Saved: {output_file}")
        except Exception as e:
            print(f"[-] Failed to save {output_file}: {e}")
    
    def auto_detect_and_decrypt(self, data: bytes) -> Optional[bytes]:
        """Auto-detect encryption layers and decrypt"""
        
        # Try different decryption chains
        chains = [
            ['base64', 'base32', 'zlib'],
            ['base64', 'zlib'],
            ['base32', 'zlib'],
            ['zlib'],
            ['base64'],
            ['base32'],
        ]
        
        for chain in chains:
            try:
                current = data
                for method in chain:
                    if method == 'base64':
                        current = base64.b64decode(current)
                    elif method == 'base32':
                        current = base64.b32decode(current)
                    elif method == 'zlib':
                        current = zlib.decompress(current)
                
                # Check if result looks like marshalled code
                try:
                    test_obj = marshal.loads(current)
                    print(f"[+] Success with chain: {' -> '.join(chain)}")
                    return current
                except:
                    continue
            except:
                continue
        
        return None
    
    def run_full_deobfuscation(self) -> bool:
        """Run complete deobfuscation pipeline"""
        print(f"\n{'='*70}")
        print(f"Python Malware Deobfuscator - Fixed Version")
        print(f"{'='*70}\n")
        print(f"[*] Input file: {self.input_file}")
        print(f"[*] Output directory: {self.output_dir}\n")
        
        # Read obfuscated code
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                obfuscated_code = f.read()
            print(f"[+] Loaded obfuscated code ({len(obfuscated_code)} chars)\n")
        except Exception as e:
            print(f"[-] Failed to read input file: {e}")
            return False
        
        # Save original
        self.save_results("00_original", obfuscated_code, "py")
        
        # Stage 1: Extract encrypted data
        print("[*] Stage 1: Extracting encrypted data...")
        extracted = self.extract_encrypted_data(obfuscated_code)
        
        if not extracted:
            print("[-] No encrypted data found")
            return False
        
        # Stage 2: Decrypt Fernet layer (if key exists)
        print("\n[*] Stage 2: Decrypting layers...")
        
        if 'fernet_key' in extracted and ('encrypted_hex' in extracted or 'encrypted_b64' in extracted):
            is_hex = 'encrypted_hex' in extracted
            encrypted_data = extracted.get('encrypted_hex') or extracted.get('encrypted_b64')
            
            decrypted = self.decrypt_fernet_layer(encrypted_data, extracted['fernet_key'], is_hex)
            if not decrypted:
                print("[!] Fernet decryption failed, trying without Fernet...")
                # Try direct decoding
                if is_hex:
                    decrypted = bytes.fromhex(encrypted_data)
                else:
                    decrypted = base64.b64decode(encrypted_data)
        else:
            print("[!] No Fernet key found, trying direct decoding...")
            if 'encrypted_hex' in extracted:
                decrypted = bytes.fromhex(extracted['encrypted_hex'])
            elif 'encrypted_b64' in extracted:
                decrypted = base64.b64decode(extracted['encrypted_b64'])
            else:
                print("[-] No encrypted data to process")
                return False
        
        if not decrypted:
            return False
        
        self.save_results("02_decrypted", decrypted, "bin")
        
        # Stage 3: Auto-detect and decode layers
        print("\n[*] Stage 3: Auto-detecting encoding layers...")
        final_data = self.auto_detect_and_decrypt(decrypted)
        
        if not final_data:
            print("[!] Auto-detection failed, trying manual layers...")
            # Manual fallback
            try:
                decoded_b64 = self.decode_base64_layer(decrypted)
                if decoded_b64:
                    decoded_b32 = self.decode_base32_layer(decoded_b64)
                    if decoded_b32:
                        final_data = self.decompress_zlib_layer(decoded_b32)
            except:
                pass
        
        if not final_data:
            print("[-] Could not decode all layers")
            return False
        
        self.save_results("05_final_decoded", final_data, "bin")
        
        # Stage 4: Unmarshal bytecode
        print("\n[*] Stage 4: Unmarshaling bytecode...")
        code_obj = self.unmarshal_bytecode(final_data)
        if not code_obj:
            return False
        
        # Stage 5: Disassemble bytecode
        print("\n[*] Stage 5: Disassembling bytecode...")
        disassembled = self.disassemble_bytecode(code_obj)
        if disassembled:
            self.save_results("06_disassembled", disassembled, "txt")
        
        # Stage 6: Extract info from code object
        print("\n[*] Stage 6: Extracting code object information...")
        self.extract_code_info(code_obj)
        
        print(f"\n{'='*70}")
        print(f"[+] Deobfuscation complete!")
        print(f"[+] Results saved to: {self.output_dir}")
        print(f"{'='*70}\n")
        
        return True
    
    def extract_code_info(self, code_obj):
        """Extract information from code object"""
        info = []
        
        info.append("="*70)
        info.append("CODE OBJECT ANALYSIS")
        info.append("="*70)
        
        if hasattr(code_obj, 'co_names'):
            info.append(f"\n[*] Names used: {len(code_obj.co_names)}")
            for name in code_obj.co_names[:50]:  # First 50
                info.append(f"  - {name}")
        
        if hasattr(code_obj, 'co_consts'):
            info.append(f"\n[*] Constants: {len(code_obj.co_consts)}")
            for i, const in enumerate(code_obj.co_consts[:20]):  # First 20
                const_str = repr(const)[:100]
                info.append(f"  [{i}] {type(const).__name__}: {const_str}")
        
        if hasattr(code_obj, 'co_varnames'):
            info.append(f"\n[*] Variable names: {code_obj.co_varnames}")
        
        if hasattr(code_obj, 'co_filename'):
            info.append(f"\n[*] Original filename: {code_obj.co_filename}")
        
        info_text = "\n".join(info)
        print(info_text)
        self.save_results("07_code_info", info_text, "txt")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Python Malware Deobfuscator - Fixed Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 deobfuscator_fixed.py malware.py
  python3 deobfuscator_fixed.py malware.py -o analysis_output
  
WARNING: Only use in isolated/sandboxed environment!
        """
    )
    
    parser.add_argument('input_file', help='Path to obfuscated Python file')
    parser.add_argument('-o', '--output', default='deobfuscated_output',
                       help='Output directory (default: deobfuscated_output)')
    
    args = parser.parse_args()
    
    # Run deobfuscation
    deobfuscator = MalwareDeobfuscator(args.input_file, args.output)
    success = deobfuscator.run_full_deobfuscation()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
