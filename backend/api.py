from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="bl4ckops-osint-backend")

app.add_middleware(
    CORSMiddleware,
    # For local network development allow all origins (safe for LAN dev). Change to specific origins for production.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunRequest(BaseModel):
    module: str
    target: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None
    mode: Optional[str] = "simulate"  # simulate | live
    authorization_confirm: Optional[str] = None
    # safety controls
    results_per_query: Optional[int] = 10
    pause_seconds: Optional[float] = 2.0

class LogEntry(BaseModel):
    timestamp: str
    type: str  # info | success | error | result
    message: str
    link: Optional[str] = None


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def make_result_log(message: str, link: Optional[str] = None) -> LogEntry:
    return LogEntry(timestamp=now_iso(), type="result", message=message, link=link)


def make_info(message: str) -> LogEntry:
    return LogEntry(timestamp=now_iso(), type="info", message=message)


# Minimal local dork builder to mimic existing CLI scripts
def build_dorks_for_module(module: str, target: Optional[str]) -> List[str]:
    t = (target or "example").strip()
    # If target already looks like a hostname (contains a dot), use as-is; otherwise append .com
    domain = t if ("." in t) else f"{t}.com"
    dorks: List[str] = []
    if module == "files":
        exts = ["pdf", "txt", "doc", "docx", "xls", "xlsx", "ppt", "htm", "html", "zip", "tar", "mp4", "jpg", "png"]
        for e in exts:
            dorks.append(f"site:{domain} filetype:{e}")
    elif module == "mails":
        hosts = ["gmail", "hotmail.com", "yandex.com", "yahoo.com", "gmx.com", "zoho.com", "aol.com", "email.com"]
        for h in hosts:
            dorks.append(f"site:{domain} intext:@{h}")
    elif module == "numbers":
        code = target or ""
        dorks.append(f"site:{domain} intext:Whatsapp {code}")
    elif module == "person":
        # expects extra: {"name":"...","surname":"...","phone":"..."}
        # For the API we keep simple
        dorks.append(f"intext:{t}")
    else:
        # fallback: treat module as custom dork
        dorks.append(module)

    return dorks


@app.post("/run", response_model=List[LogEntry])
def run_module(req: RunRequest):
    """Run a module. By default runs in `simulate` mode. Set `mode: live` and
    provide `authorization_confirm: "I confirm I have authorization"` to run live searches or deobfuscation.
    """
    logs: List[LogEntry] = []
    logs.append(make_info("BL4CKOPS-OSINT PY BACKEND STARTED"))
    logs.append(make_info(f"Requested module: {req.module}"))

    target = req.target or (req.extra.get("target") if req.extra else None)

    # Build dorks similar to CLI
    try:
        dorks = build_dorks_for_module(req.module, target)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Simulate mode: echo dorks and provide example links
    if (req.mode or "").lower() != "live":
        for d in dorks:
            logs.append(make_info(f"Simulating dork: {d}"))
            example_link = f"https://www.google.com/search?q={d.replace(' ', '+')}"
            logs.append(make_result_log(f"Found (simulated) results for: {d}", link=example_link))

        logs.append(make_info("MODULE RUN COMPLETE (simulated)"))
        return logs

    # Live mode: require explicit authorization phrase
    if req.authorization_confirm != "I confirm I have authorization":
        raise HTTPException(status_code=403, detail="Live mode requires explicit authorization_confirm field.")

    # Perform live queries with rate limiting
    try:
        from googlesearch import search as gsearch
    except Exception:
        gsearch = None

    # SerpAPI support: prefer SerpAPI if key present (either env SERPAPI_KEY or req.extra['serpapi_key'])
    import os
    serpapi_key_env = os.environ.get("SERPAPI_KEY")
    serpapi_available = False
    serpapi_key_in_request = None
    if req.extra and isinstance(req.extra, dict):
        serpapi_key_in_request = req.extra.get("serpapi_key")
    serpapi_key = serpapi_key_in_request or serpapi_key_env
    if serpapi_key:
        try:
            from serpapi import GoogleSearch
            serpapi_available = True
        except Exception:
            serpapi_available = False

    for d in dorks:
        logs.append(make_info(f"Running live dork: {d}"))
        if gsearch is None:
            logs.append(make_result_log("googlesearch not installed; cannot perform live queries"))
            continue
        # If SerpAPI key is available, use SerpAPI (more reliable)
        if serpapi_available and serpapi_key:
            # allow request-scoped proxy via req.extra['proxy'] (e.g. 'http://host:port')
            proxy = None
            if req.extra and isinstance(req.extra, dict):
                proxy = req.extra.get("proxy")
            # If proxy provided, set HTTP(S)_PROXY environment variables temporarily
            old_http_proxy = os.environ.get("HTTP_PROXY")
            old_https_proxy = os.environ.get("HTTPS_PROXY")
            if proxy:
                os.environ["HTTP_PROXY"] = proxy
                os.environ["HTTPS_PROXY"] = proxy
            try:
                params = {
                    "engine": "google",
                    "q": d,
                    "api_key": serpapi_key,
                    "num": req.results_per_query or 10,
                }
                search = GoogleSearch(params)
                try:
                    result = search.get_dict()
                except Exception as e:
                    logs.append(make_result_log(f"SerpAPI error: {e}"))
                    result = None
                if result and isinstance(result, dict):
                    organs = result.get("organic_results") or result.get("organic_results", [])
                    count = 0
                    for item in organs:
                        if isinstance(item, dict):
                            link = item.get("link") or item.get("url") or item.get("position")
                            if link:
                                logs.append(make_result_log(link, link=link))
                                count += 1
                                if count >= (req.results_per_query or 10):
                                    break
                    if count == 0:
                        logs.append(make_result_log("SerpAPI returned no organic results."))
                else:
                    logs.append(make_result_log("SerpAPI returned unexpected response format."))
            finally:
                # restore env
                if old_http_proxy is not None:
                    os.environ["HTTP_PROXY"] = old_http_proxy
                else:
                    os.environ.pop("HTTP_PROXY", None)
                if old_https_proxy is not None:
                    os.environ["HTTPS_PROXY"] = old_https_proxy
                else:
                    os.environ.pop("HTTPS_PROXY", None)
            # done with SerpAPI for this dork
            continue

        # Try several calling styles for different googlesearch implementations
        def try_search_calls():
            # Try variant 1: common googlesearch-python signature
            try:
                count = 0
                for url in gsearch(d, tld="com", num=req.results_per_query or 10, stop=req.results_per_query or 10, pause=req.pause_seconds or 2.0):
                    yield url
                    count += 1
                    if count >= (req.results_per_query or 10):
                        return
            except TypeError:
                pass
            except Exception as e:
                logs.append(make_info(f"Variant 1 error: {e}"))

            # Try variant 2: no tld kw
            try:
                count = 0
                for url in gsearch(d, num=req.results_per_query or 10, stop=req.results_per_query or 10, pause=req.pause_seconds or 2.0):
                    yield url
                    count += 1
                    if count >= (req.results_per_query or 10):
                        return
            except TypeError:
                pass
            except Exception as e:
                logs.append(make_info(f"Variant 2 error: {e}"))

            # Try variant 3: simple signature returning list or generator with single arg
            try:
                res = gsearch(d, req.results_per_query or 10)
                # If it's a list or generator
                if hasattr(res, '__iter__'):
                    count = 0
                    for url in res:
                        yield url
                        count += 1
                        if count >= (req.results_per_query or 10):
                            return
                else:
                    return
            except Exception as e:
                logs.append(make_info(f"Variant 3 error: {e}"))

            # Try variant 4: googlesearch module variant with num_results and sleep_interval
            try:
                res = gsearch(d, num_results=(req.results_per_query or 10), sleep_interval=(req.pause_seconds or 2.0))
                if hasattr(res, '__iter__'):
                    count = 0
                    for url in res:
                        yield url
                        count += 1
                        if count >= (req.results_per_query or 10):
                            return
                else:
                    return
            except Exception as e:
                logs.append(make_info(f"Variant 4 error: {e}"))

        found_any = False
        try:
            for url in try_search_calls():
                found_any = True
                logs.append(make_result_log(f"{url}", link=url))
        except Exception as e:
            logs.append(make_result_log(f"Search error: {e}"))

        if not found_any:
            logs.append(make_result_log("No results returned or search implementation incompatible."))

    # If module indicates deobfuscation and a local file path is provided, run multilayer
    if req.module.lower() in ("deobfuscate", "multilayer", "deobf") and req.extra and req.extra.get("file"):
        file_path = req.extra.get("file")
        logs.append(make_info(f"Attempting deobfuscation on: {file_path}"))
        try:
            from multilayer import MalwareDeobfuscator
            deob = MalwareDeobfuscator(file_path, output_dir="deobfuscated_output")
            success = deob.run_full_deobfuscation()
            logs.append(make_info(f"Deobfuscation finished: success={bool(success)}"))
        except Exception as e:
            logs.append(make_result_log(f"Deobfuscation failed: {e}"))

    logs.append(make_info("MODULE RUN COMPLETE (live)"))
    return logs


@app.get("/health")
def health():
    return {"status": "ok", "time": now_iso()}
