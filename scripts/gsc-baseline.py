#!/usr/bin/env python3
"""Search Console baseline for skingenetix.com — what we already rank for.

Usage:
    python3 scripts/gsc-baseline.py [--days 90] [--limit 50] [--json out.json]

Why this exists: the publishing gate. Before writing any article for a target
keyword, check whether an existing page already ranks top 10 for it — if so,
improve that page instead of creating a competitor for it. Hairgenetix lost a
1,504-clicks/month article to exactly that mistake (docs/research-2026-*.md §8).

Read-only. Requires ~/.config/ga4/service-account.json with the property shared.
"""
import argparse, datetime as dt, json, pathlib, sys, warnings
warnings.filterwarnings("ignore")
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY = pathlib.Path.home() / ".config/ga4/service-account.json"
SITE = "sc-domain:skingenetix.com"
BASE = "https://www.skingenetix.com"


def service():
    creds = service_account.Credentials.from_service_account_file(
        str(KEY), scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    return build("searchconsole", "v1", credentials=creds)


def query(svc, dims, start, end, limit=1000, filters=None):
    body = {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": limit}
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]
    return svc.searchanalytics().query(siteUrl=SITE, body=body).execute().get("rows", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--json", help="write the full result to this path")
    a = ap.parse_args()

    # GSC lags ~2 days; asking for today silently returns nothing.
    end = dt.date.today() - dt.timedelta(days=2)
    start = end - dt.timedelta(days=a.days)
    svc = service()
    s, e = start.isoformat(), end.isoformat()
    print(f"  property {SITE}   window {s} → {e}")

    days = query(svc, ["date"], s, e, 1000)
    clicks = sum(r["clicks"] for r in days)
    imps = sum(r["impressions"] for r in days)
    print(f"  days with data: {len(days)}   clicks {clicks}   impressions {imps}")
    if not days:
        print("\n  No data in this window. Either the property was verified recently,\n"
              "  or the site has no search presence yet. Both are normal for a new store.")

    out = {"window": [s, e], "clicks": clicks, "impressions": imps, "days": len(days)}

    for label, dims in (("queries", ["query"]), ("pages", ["page"]), ("countries", ["country"])):
        rows = query(svc, dims, s, e, a.limit)
        out[label] = rows
        print(f"\n  === top {label} ({len(rows)}) ===")
        if not rows:
            print("     none")
            continue
        for r in rows[:a.limit]:
            k = r["keys"][0].replace(BASE, "")
            print(f"     {r['clicks']:>4}cl {r['impressions']:>7}im  p{r['position']:>5.1f}  {k[:62]}")

    # The band that is usually the biggest single lever on an established site.
    rows = out.get("queries") or []
    band = [r for r in rows if 4 <= r["position"] <= 10]
    if band:
        bc = sum(r["clicks"] for r in band); bi = sum(r["impressions"] for r in band)
        ctr = (bc / bi * 100) if bi else 0
        print(f"\n  positions 4-10: {len(band)} queries, {bi} impressions, CTR {ctr:.2f}%")
        print(f"  (3-8% is normal; below that, retitling beats new content)")

    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(out, indent=1))
        print(f"\n  wrote {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
