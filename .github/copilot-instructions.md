# Copilot instructions for BL4CKOPS_REVEALED

These notes help an AI coding assistant become productive quickly in this repository.

## Big picture
- Purpose: small collection of CLI OSINT tools and a Python deobfuscator. Key scripts: `bl4ckops_osint.py` (interactive OSINT), `multilayer.py` (deobfuscator), and `analyzer.py` (static extractor for dorks/imports).
- Data flow: interactive CLI -> construct Google dork strings (variables named `data`, `data2`, ... ) -> `googlesearch.search()` or direct `requests`+`BeautifulSoup` -> printed output and optional saved artifacts under `deobfuscated_output/`.

## Entrypoints & common commands
- Install deps: `pip install -r requirements.txt` or activate the bundled venv `source bin/activate` then install.
- Run interactive OSINT: `python bl4ckops_osint.py`
- Run deobfuscator: `python multilayer.py <obfuscated.py> -o deobfuscated_output`.
- Run analyzer: `python analyzer.py bl4ckops_osint.py` (use to extract dorks/imports quickly).

## Project-specific patterns
- Repetitive Google-dork assembly: dorks are created in many functions using sequential variable names (`data`, `data2`, ...). When refactoring, centralize into a helper like `run_dork(query, tld='co.in')`.
- UI: heavy use of `colorama` for colored prompts and `input()` for interactive flow. Keep color calls in the UI layer (menu functions).
- Long-running waits: scripts use `time.sleep()` and `tqdm` loops to simulate progress — tests or automation should mock or skip these sleeps.

## Integration points & optional deps
- Required for basic use: `googlesearch`, `beautifulsoup4`, `requests`, `lxml`, `tqdm`, `colorama`.
- Optional but recommended for deobfuscation: `cryptography` (Fernet) and `uncompyle6` for decompilation.

## Safety & running guidance
- This repo contains tools that search for and surface sensitive data. Only run against targets you are authorized to test and preferably within an isolated environment.
- Run `multilayer.py` only inside a sandbox — it processes potentially malicious bytecode and writes intermediate files to `deobfuscated_output/`.

## How an AI should make changes
- Avoid bulk reformatting. Make focused edits: replace repeated dork patterns by extracting a helper and update a couple of calling sites first.
- Keep all UI references consistent to the BL4CKOPS_REVEALED branding.
- Provide runnable examples in PR descriptions (command to run + expected short snippet of output).

## Files to reference
- `bl4ckops_osint.py` — primary interactive OSINT CLI (search patterns and prompts).
- `multilayer.py` — staged deobfuscation pipeline and where optional heavy deps are used.
- `analyzer.py` — useful reference for extracting imports/functions/dorks and producing reports.

If you want, I can now: (1) centralize the repeated Google-search logic into a helper, (2) add a small non-interactive runner for automated testing, or (3) create unit tests that mock `googlesearch.search()` — tell me which you'd prefer.
