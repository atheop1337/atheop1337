import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone

API = "https://api.github.com/graphql"
HI, MID, DIM, BG = "#f2f2f2", "#8a8a8a", "#5a5a5a", "#0b0b0b"
HEAT = ["#161616", "#3a3a3a", "#6a6a6a", "#a8a8a8", "#f2f2f2"]


def gql(query, **variables):
    req = urllib.request.Request(
        API,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"bearer {os.environ['GH_TOKEN']}",
            "Content-Type": "application/json",
            "User-Agent": "readme-stats-script",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]


def fetch(login):
    base = gql(
        """query($login: String!) {
          user(login: $login) {
            createdAt
            followers { totalCount }
            pullRequests { totalCount }
            issues { totalCount }
            contributionsCollection { totalCommitContributions restrictedContributionsCount }
            repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
              totalCount
              nodes {
                stargazerCount
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                  edges { size node { name } }
                }
              }
            }
          }
        }""",
        login=login,
    )["user"]

    start_year = int(base["createdAt"][:4])
    this_year = datetime.now(timezone.utc).year
    parts = []
    for y in range(start_year, this_year + 1):
        parts.append(
            f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") '
            "{ contributionCalendar { weeks { contributionDays { date contributionCount } } } }"
        )
    cal = gql(f'query($login: String!) {{ user(login: $login) {{ {" ".join(parts)} }} }}', login=login)["user"]
    days = {}
    for block in cal.values():
        for w in block["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
    return base, days


def streaks(days):
    today = datetime.now(timezone.utc).date()
    ordered = sorted(days.items())
    longest = run = 0
    for _, c in ordered:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    cur, d = 0, today
    if days.get(d.isoformat(), 0) == 0:
        d -= timedelta(days=1)
    while days.get(d.isoformat(), 0) > 0:
        cur += 1
        d -= timedelta(days=1)
    return cur, longest


def fmt(n):
    return f"{n/1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(login, base, days):
    total = sum(days.values())
    cur, longest = streaks(days)
    stars = sum(r["stargazerCount"] for r in base["repositories"]["nodes"])
    cc = base["contributionsCollection"]
    langs = Counter()
    for r in base["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] += e["size"]
    lang_total = sum(langs.values()) or 1
    top = langs.most_common(5)

    W, H = 860, 264
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
      f'aria-label="{login}: {total} contributions, current streak {cur} days, longest {longest} days">')
    a("""  <defs>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1" fill="#ffffff" opacity="0.025"/>
    </pattern>
    <style>
      text { font-family: 'JetBrains Mono', 'Fira Code', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace; }
      .lbl { fill: #5a5a5a; font-size: 11px; letter-spacing: 2px; }
      .big { fill: #f2f2f2; font-size: 34px; font-weight: 800; }
      .sub { fill: #8a8a8a; font-size: 12px; }
      .row { fill: #5a5a5a; font-size: 12px; }
      .row tspan { fill: #f2f2f2; }
      .in  { opacity: 0; animation: in .6s ease-out forwards; }
      .c   { opacity: 0; animation: on .25s ease-out forwards; }
      .bar { transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: grow .9s ease-out .4s forwards; }
      .dot { animation: blink 1.2s steps(1) infinite; }
      @keyframes in    { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: none; } }
      @keyframes on    { to { opacity: 1; } }
      @keyframes grow  { to { transform: scaleX(1); } }
      @keyframes blink { 50% { opacity: 0; } }
    </style>
  </defs>""")
    a(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{BG}" stroke="#2a2a2a"/>')
    a(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="url(#scan)"/>')
    a(f'  <line x1="32" y1="126" x2="{W-32}" y2="126" stroke="#1f1f1f"/>')

    blocks = [
        ("CONTRIBUTIONS", fmt(total), "all time, public"),
        ("CURRENT STREAK", str(cur), "day" if cur == 1 else "days"),
        ("LONGEST STREAK", str(longest), "day" if longest == 1 else "days"),
    ]
    for i, (lbl, big, sub) in enumerate(blocks):
        x = 32 + i * 185
        a(f'  <g class="in" style="animation-delay:{i*0.12:.2f}s">')
        if i == 1:
            a(f'    <circle cx="{x+4}" cy="36" r="3.5" fill="{HI}" class="dot"/>')
            a(f'    <text x="{x+16}" y="40" class="lbl">{lbl}</text>')
        else:
            a(f'    <text x="{x}" y="40" class="lbl">{lbl}</text>')
        a(f'    <text x="{x}" y="84" class="big">{big}</text>')
        a(f'    <text x="{x}" y="104" class="sub">{sub}</text>')
        a("  </g>")

    rows = [
        ("stars", stars),
        ("commits " + str(datetime.now(timezone.utc).year), cc["totalCommitContributions"]),
        ("pull requests", base["pullRequests"]["totalCount"]),
        ("issues", base["issues"]["totalCount"]),
        ("repositories", base["repositories"]["totalCount"]),
        ("followers", base["followers"]["totalCount"]),
    ]
    a('  <g class="in" style="animation-delay:.4s">')
    for i, (k, v) in enumerate(rows):
        dots = "." * max(2, 22 - len(k) - len(fmt(v)))
        a(f'    <text x="{W-32}" y="{38 + i*16}" text-anchor="end" class="row">{esc(k)} {dots} <tspan>{fmt(v)}</tspan></text>')
    a("  </g>")

    a('  <text x="32" y="150" class="lbl">LAST 12 MONTHS</text>')
    today = datetime.now(timezone.utc).date()
    end = today + timedelta(days=(5 - today.weekday()) % 7)
    first = end - timedelta(days=53 * 7 - 1)
    nonzero = sorted(c for c in days.values() if c > 0) or [1]
    q = [nonzero[int(len(nonzero) * p)] for p in (0.25, 0.5, 0.75)]

    def level(c):
        if c <= 0:
            return 0
        return 1 + sum(c > t for t in q)

    cell, gap = 8, 2
    for wk in range(53):
        for dow in range(7):
            d = first + timedelta(days=wk * 7 + dow)
            if d > today:
                continue
            c = days.get(d.isoformat(), 0)
            x, y = 32 + wk * (cell + gap), 160 + dow * (cell + gap)
            a(f'  <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="1.5" fill="{HEAT[level(c)]}" '
              f'class="c" style="animation-delay:{0.3 + wk*0.015:.3f}s"><title>{d.isoformat()}: {c}</title></rect>')

    lx = 600
    a(f'  <text x="{lx}" y="150" class="lbl">LANGUAGES</text>')
    for i, (name, size) in enumerate(top):
        y = 172 + i * 15
        pct = size / lang_total * 100
        a(f'  <text x="{lx}" y="{y}" class="sub">{esc(name[:12])}</text>')
        a(f'  <rect x="{lx+100}" y="{y-5}" width="90" height="3" rx="1.5" fill="#1f1f1f"/>')
        a(f'  <rect x="{lx+100}" y="{y-5}" width="{max(2, 90*pct/100):.1f}" height="3" rx="1.5" fill="{HI}" class="bar"/>')
        a(f'  <text x="{W-32}" y="{y}" text-anchor="end" class="row">{pct:.0f}%</text>')
    if not top:
        a(f'  <text x="{lx}" y="172" class="sub">no public code yet</text>')

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    a(f'  <text x="{W-32}" y="{H-12}" text-anchor="end" font-size="9" fill="#333">updated {stamp}</text>')
    a("</svg>")
    return "\n".join(o) + "\n"


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: stats.py <login> <out.svg>")
    login, out = sys.argv[1], sys.argv[2]
    base, days = fetch(login)
    svg = render(login, base, days)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
