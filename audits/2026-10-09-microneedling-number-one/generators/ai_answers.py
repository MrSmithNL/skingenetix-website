"""Ask four AI assistants (with web search) the skin-microneedling questions buyers ask; record answers and cited sources.

    python3 generators/ai_answers.py            # writes ai-answers/answers.json and prints the citation tally

DataForSEO AI Optimization `llm_responses/live` (ChatGPT, Perplexity, Gemini, Claude). One run per prompt and engine:
an indicative snapshot, not a stable share (stable shares need 7+ runs). Read-only. Author: Claude for Malcolm, 2026-10-09.
"""
import base64, collections, concurrent.futures as cf, json, pathlib, re, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = pathlib.Path.home() / "Claude Code/Projects/seo-toolkit/.env"
t = ENV.read_text()
login = re.search(r"^DATAFORSEO_LOGIN=(.+)$", t, re.M).group(1).strip().strip("\"'")
pw = re.search(r"^DATAFORSEO_PASSWORD=(.+)$", t, re.M).group(1).strip().strip("\"'")
AUTH = base64.b64encode(f"{login}:{pw}".encode()).decode()
ENGINES = {"chat_gpt": "gpt-6.1-sol", "perplexity": "sonar-pro", "gemini": "gemini-2.5-pro", "claude": "claude-sonnet-5-5"}
PROMPTS = [
    "What is the best at-home microneedling tool for the face?",
    "How do I microneedle my face at home safely?",
    "Derma stamp or derma roller for the face: which is better?",
    "What serum should I use after microneedling at home?",
    "How often can I microneedle my face at home with a 0.5 mm derma stamp?",
    "Does at-home microneedling actually work for wrinkles and fine lines?",
    "Is microneedling at home with PDRN or copper peptide serum worth it?",
    "What is the best microneedling kit with serum for home use?",
    "What needle length is safe for microneedling your face at home?",
    "Microchanneling vs microneedling: what is the difference?",
]


def ask(engine, model, prompt):
    body = [{"user_prompt": prompt, "model_name": model, "web_search": True, "max_output_tokens": 1200,
             "web_search_country_iso_code": "US"}]
    req = urllib.request.Request(f"https://api.dataforseo.com/v3/ai_optimization/{engine}/llm_responses/live",
                                 data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Basic {AUTH}", "Content-Type": "application/json"})
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=180).read())
        task = d["tasks"][0]
        res = (task.get("result") or [{}])[0]
        text, cites = [], []
        for it in res.get("items") or []:
            for sec in it.get("sections") or []:
                text.append(sec.get("text") or "")
                for an in sec.get("annotations") or []:
                    cites.append({"title": an.get("title"), "url": an.get("url")})
        return {"engine": engine, "model": model, "prompt": prompt, "status": task.get("status_code"),
                "cost": task.get("cost") or res.get("money_spent"), "text": "\n".join(text), "citations": cites}
    except Exception as e:
        return {"engine": engine, "model": model, "prompt": prompt, "status": f"ERR {e}", "cost": 0, "text": "", "citations": []}


jobs = [(e, m, p) for e, m in ENGINES.items() for p in PROMPTS]
with cf.ThreadPoolExecutor(8) as ex:
    out = list(ex.map(lambda j: ask(*j), jobs))
d = ROOT / "ai-answers"; d.mkdir(exist_ok=True)
(d / "answers.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
dom = collections.Counter(re.sub(r"^www\.", "", urllib.request.urlparse(c["url"]).netloc) for r in out for c in r["citations"] if c.get("url"))
mentions = collections.Counter()
for r in out:
    for b in ["skingenetix", "dr. pen", "dr pen", "qure", "banish", "stacked", "beautimate", "glopro", "ora ", "sdara", "dermapen", "hydra", "the ordinary", "skinmedica", "alastin"]:
        if b in r["text"].lower():
            mentions[b] += 1
print("cost", round(sum((r["cost"] or 0) for r in out), 3), "| ok", sum(1 for r in out if r["status"] == 20000), "of", len(out))
print("cited domains:", dom.most_common(30))
print("brand mentions in answers:", mentions.most_common())
