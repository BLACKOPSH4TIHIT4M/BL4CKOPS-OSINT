#!/usr/bin/env python3
"""
Python Malware Deobfuscator
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
        
        # Extract Fernet key
        key_match = re.search(r'__mikey__\s*=\s*["\']([^"\']+)["\']', code)
        if key_match:
            data['fernet_key_b64'] = key_match.group(1)
            data['fernet_key'] = base64.b64decode(data['fernet_key_b64'])
            print(f"[+] Extracted Fernet key: {data['fernet_key_b64'][:50]}...")
        
        # Extract encrypted payload (hex string)
        payload_match = re.search(r'mydata\s*=\s*["\']([0-9a-fA-F]+)["\']', code)
        if payload_match:
            data['encrypted_hex'] = payload_match.group(1)
            print(f"[+] Extracted encrypted payload: {len(data['encrypted_hex'])} chars")
        
        return data
    
    def decrypt_fernet_layer(self, encrypted_hex: str, fernet_key: bytes) -> bytes:
        """Decrypt Fernet encryption layer"""
        try:
            from cryptography.fernet import Fernet
            
            # Hex to bytes
            encrypted_bytes = bytes.fromhex(encrypted_hex)
            print(f"[+] Layer 1: Converted hex to bytes ({len(encrypted_bytes)} bytes)")
            
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
    
    def decompile_bytecode(self, code_obj: Any) -> Optional[str]:
        """Attempt to decompile bytecode back to Python source"""
        try:
            import uncompyle6
            from io import StringIO
            
            output = StringIO()
            uncompyle6.decompile_file(code_obj, output)
            source = output.getvalue()
            print(f"[+] Bytecode decompiled to source ({len(source)} chars)")
            return source
        except ImportError:
            print("[!] uncompyle6 not installed. Install with: pip install uncompyle6")
            return None
        except Exception as e:
            print(f"[-] Decompilation failed: {e}")
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
    
    def run_full_deobfuscation(self) -> bool:
        """Run complete deobfuscation pipeline"""
        print(f"\n{'='*70}")
        print(f"Python Malware Deobfuscator")
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
        
        # Stage 1: Extract encrypted data
        print("[*] Stage 1: Extracting encrypted data...")
        extracted = self.extract_encrypted_data(obfuscated_code)
        if not extracted.get('encrypted_hex') or not extracted.get('fernet_key'):
            print("[-] Failed to extract required data")
            return False
        
        # Stage 2: Decrypt Fernet layer
        print("\n[*] Stage 2: Decrypting layers...")
        decrypted = self.decrypt_fernet_layer(
            extracted['encrypted_hex'],
            extracted['fernet_key']
        )
        if not decrypted:
            return False
        self.save_results("02_fernet_decrypted", decrypted, "bin")
        
        # Stage 3: Decode Base64
        decoded_b64 = self.decode_base64_layer(decrypted)
        if not decoded_b64:
            return False
        self.save_results("03_base64_decoded", decoded_b64, "bin")
        
        # Stage 4: Decode Base32
        decoded_b32 = self.decode_base32_layer(decoded_b64)
        if not decoded_b32:
            return False
        self.save_results("04_base32_decoded", decoded_b32, "bin")
        
        # Stage 5: Decompress zlib
        decompressed = self.decompress_zlib_layer(decoded_b32)
        if not decompressed:
            return False
        self.save_results("05_zlib_decompressed", decompressed, "bin")
        
        # Stage 6: Unmarshal bytecode
        print("\n[*] Stage 3: Unmarshaling bytecode...")
        code_obj = self.unmarshal_bytecode(decompressed)
        if not code_obj:
            return False
        
        # Stage 7: Disassemble bytecode
        print("\n[*] Stage 4: Disassembling bytecode...")
        disassembled = self.disassemble_bytecode(code_obj)
        if disassembled:
            self.save_results("06_disassembled", disassembled, "txt")
        
        # Stage 8: Attempt decompilation
        print("\n[*] Stage 5: Attempting decompilation...")
        try:
            # Try to decompile
            import uncompyle6
            from io import StringIO
            import tempfile
            
            # Save bytecode to temp file
            with tempfile.NamedTemporaryFile(suffix='.pyc', delete=False) as tmp:
                tmp.write(decompressed)
                tmp_path = tmp.name
            
            # Decompile
            output = StringIO()
            uncompyle6.main.decompile_file(tmp_path, output)
            decompiled = output.getvalue()
            
            if decompiled:
                self.save_results("07_decompiled_source", decompiled, "py")
                
                # Analyze behavior
                print("\n[*] Stage 6: Analyzing malicious behavior...")
                self.analyze_code_behavior(decompiled)
            
            # Cleanup
            import os
            os.unlink(tmp_path)
            
        except ImportError:
            print("[!] Install uncompyle6 for full decompilation: pip install uncompyle6")
            print("[!] Attempting alternative decompilation...")
            
            # Alternative: just show what we can extract
            if hasattr(code_obj, 'co_consts'):
                print(f"\n[*] Code object constants:")
                for i, const in enumerate(code_obj.co_consts):
                    print(f"  [{i}] {type(const).__name__}: {repr(const)[:100]}")
            
            if hasattr(code_obj, 'co_names'):
                print(f"\n[*] Code object names:")
                print(f"  {code_obj.co_names}")
        
        print(f"\n{'='*70}")
        print(f"[+] Deobfuscation complete!")
        print(f"[+] Results saved to: {self.output_dir}")
        print(f"{'='*70}\n")
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Python Malware Deobfuscator - Production-grade analysis tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deobfuscator.py malware.py
  python deobfuscator.py malware.py -o analysis_output
  
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
