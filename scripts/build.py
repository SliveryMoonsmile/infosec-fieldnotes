#!/usr/bin/env python3
"""Build a complete static publication using only the Python standard library.

content/*.html is trusted, reviewed editorial HTML, never a raw Notion export.
Metadata is escaped; articles are rendered at build time, not in the browser.
"""
import argparse
import html
import json
import math
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
REVIEWED = "30 October 2026"


def esc(value):
    return html.escape(str(value), quote=True)


def load_articles():
    articles = json.loads((ROOT / "content/articles.json").read_text())
    for article in articles:
        slug = article["slug"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"Invalid article slug: {slug}")
        article["body"] = (ROOT / f"content/{slug}.html").read_text()
        words = re.sub(r"<[^>]+>", " ", article["body"]).split()
        article["minutes"] = max(2, math.ceil(len(words) / 190))
    return articles


def sidebar(articles, prefix, current):
    links = "".join(
        f'<a class="series-link {"is-active" if current == a["slug"] else ""}" '
        f'href="{prefix}articles/{a["slug"]}.html"'
        f'{" aria-current=\"page\"" if current == a["slug"] else ""}>'
        f'<span class="series-number">{a["id"]}</span><span>{esc(a["label"])}</span></a>'
        for a in articles
    )
    return f'''<aside class="sidebar" id="sidebar">
      <a class="brand" href="{prefix}index.html" aria-label="Fieldnotes home">
        <span class="brand-symbol" aria-hidden="true">F<span>↗</span></span>
        <span>FIELDNOTES<span class="brand-sub">INFORMATION SECURITY</span></span>
      </a>
      <div class="sidebar-inner">
        <p class="nav-label">THE PUBLICATION</p>
        <nav class="main-nav" aria-label="Main navigation">
          <a {"aria-current='page'" if current == 'home' else ''} href="{prefix}index.html">Overview <span>↗</span></a>
          <a {"aria-current='page'" if current == 'library' else ''} href="{prefix}library.html">Article index <span>08</span></a>
          <a {"aria-current='page'" if current == 'labs' else ''} href="{prefix}labs.html">Lab resources <span>↓</span></a>
          <a {"aria-current='page'" if current == 'sources' else ''} href="{prefix}sources.html">Sources & method <span>↗</span></a>
        </nav>
        <p class="nav-label series-heading">READ THE SERIES</p>
        <nav class="series-nav" aria-label="Article series">{links}</nav>
        <div class="sidebar-bottom"><span class="status-dot"></span> A working security notebook
          <p>Observe carefully.<br>Document what holds up.</p>
          <a href="{prefix}about.html">About this publication ↗</a>
        </div>
      </div>
    </aside>'''


def page(title, body, articles, current, prefix="", description="Practical information security fieldnotes: networks, applications, systems, identity, and cloud delivery."):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{esc(description)}"><meta name="color-scheme" content="dark light">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)} · Fieldnotes</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
{sidebar(articles, prefix, current)}
<div class="page-shell"><header class="topbar"><button class="menu-toggle" aria-label="Open navigation" aria-controls="sidebar" aria-expanded="false">☰</button>
<div class="breadcrumbs"><a href="{prefix}index.html">Fieldnotes</a><span>/</span><span>{esc('Series' if prefix else title)}</span></div>
<div class="topbar-actions"><a class="index-shortcut" href="{prefix}library.html">Browse the index <span>↗</span></a><button class="theme-toggle" aria-label="Switch to light theme" title="Toggle color theme">◐</button></div></header>
<main id="main" tabindex="-1">{body}</main>
<footer class="footer"><span>FIELDNOTES <span class="muted">/ Security, understood in layers.</span></span><span>Edited {REVIEWED} <span class="footer-sep">·</span> <a href="{prefix}sources.html">Sources & method ↗</a></span></footer></div>
<p class="sr-only" id="copy-status" role="status"></p></body></html>'''


def card(a, prefix="", featured=False):
    return f'''<a class="article-card {'featured-card' if featured else ''}" href="{prefix}articles/{a['slug']}.html" data-category="{esc(a['category'])}">
    <div class="card-top"><span class="mono">NOTE {a['id']}</span><span class="tag">{esc(a['category'])}</span></div>
    <h3>{esc(a['title'])}</h3><p>{esc(a['summary'])}</p><div class="card-bottom"><span>{a['minutes']} min read</span><span aria-hidden="true">↗</span></div></a>'''


def home(articles):
    rows = "".join(f'''<a class="series-row" href="articles/{a['slug']}.html"><span class="row-number">{a['id']}</span><div><span class="eyebrow">{esc(a['category'])}</span><h3>{esc(a['label'])}</h3></div><span class="row-description">{esc(a['summary'])}</span><span class="row-arrow">↗</span></a>''' for a in articles)
    return f'''<div class="home-content">
      <section class="hero"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> NOTES FROM THE TECHNICAL FRONTIER</p>
      <h1>Security,<br>from the<br><em>packet up.</em></h1>
      <p class="hero-description">A field guide to the systems we trust.<br>Networks, applications, identity, and the work<br class="desktop-break"> of understanding what can go wrong.</p>
      <div class="hero-actions"><a class="button primary" href="articles/{articles[0]['slug']}.html">Start the series <span>↗</span></a><a class="text-link" href="library.html">Explore all notes →</a></div>
      <div class="hero-caption"><span class="mono">08 NOTES</span><span class="caption-rule"></span> From a persistent notebook to a practical publication.</div></div>
      <figure class="hero-figure"><svg viewBox="0 0 480 410" role="img" aria-labelledby="network-title network-desc"><title id="network-title">A connection through layers</title><desc id="network-desc">An illustrative network path through link, network, transport, and application layers.</desc>
      <defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="currentColor" stroke-width=".5" opacity=".18"/></pattern></defs>
      <rect width="480" height="410" fill="url(#grid)"/><g fill="none" stroke="currentColor" stroke-width="1.2">
      <path d="M48 294L240 390L432 294L240 198Z" opacity=".15"/><path d="M48 246L240 342L432 246L240 150Z" opacity=".28"/><path d="M48 198L240 294L432 198L240 102Z" opacity=".42"/><path d="M48 150L240 246L432 150L240 54Z" opacity=".7"/>
      <path d="M48 150V294M240 246V390M432 150V294M240 54V198" stroke-dasharray="4 7" opacity=".35"/>
      <path d="M112 182L176 150L240 182L304 150L368 182" stroke="var(--accent)" stroke-width="2"/>
      </g><g fill="var(--surface)" stroke="var(--accent)" stroke-width="2"><circle cx="112" cy="182" r="7"/><circle cx="176" cy="150" r="7"/><circle cx="240" cy="182" r="9"/><circle cx="304" cy="150" r="7"/><circle cx="368" cy="182" r="7"/></g>
      <g fill="currentColor" font-size="10" font-family="monospace" letter-spacing="2"><text x="20" y="34">FIG. 01 / LAYERS OF TRUST</text><text x="332" y="355">OBSERVE</text><text x="332" y="372">VERIFY</text><text x="332" y="389">DOCUMENT</text></g><path d="M20 51H83" stroke="var(--accent)"/></svg><figcaption><span>01 / NETWORK → APPLICATION</span><span>A model, not live telemetry</span></figcaption></figure></section>
      <section class="featured-section"><div class="section-heading"><div><p class="eyebrow">PICK A THREAD</p><h2>Start with a question.</h2></div><a href="library.html" class="text-link">All eight notes ↗</a></div><div class="featured-grid">{card(articles[2],featured=True)}{card(articles[1],featured=True)}{card(articles[6],featured=True)}</div></section>
      <section class="series-section"><div class="section-heading"><div><p class="eyebrow">THE READING PATH</p><h2>One system. Several layers.</h2></div><span class="mono muted">01 — 08</span></div><div class="series-rows">{rows}</div></section>
      <section class="method-strip"><div class="method-mark" aria-hidden="true">↳</div><div><p class="eyebrow">A NOTE ON THE NOTES</p><h2>From collected links to tested thinking.</h2><p>Adapted from a technical Notion journal. Rewritten for clarity, checked against primary references, and paired with proposed exercises.</p></div><a class="button secondary" href="sources.html">Read the method ↗</a></section>
    </div>'''


def library(articles):
    categories = list(dict.fromkeys(a['category'] for a in articles))
    filters = '<button class="filter is-active" data-filter="All" aria-pressed="true">All notes <span>08</span></button>'
    filters += ''.join(f'<button class="filter" data-filter="{esc(c)}" aria-pressed="false">{esc(c)}</button>' for c in categories)
    return f'''<div class="standard-content"><div class="page-intro"><p class="eyebrow">THE ARTICLE INDEX</p><h1>Follow your curiosity.</h1><p>Eight connected notes. Read in order, or find the layer you’re working on.</p></div>
      <section aria-label="Find an article"><label class="search-label" for="article-search">Search the fieldnotes</label><div class="search-box"><span aria-hidden="true">⌕</span><input id="article-search" type="search" placeholder="Try ‘Kerberos’, ‘SQL’, or ‘cloud’" autocomplete="off"><kbd>/</kbd></div>
      <div class="filters" aria-label="Filter by subject">{filters}</div><p class="result-count" id="result-count" role="status">8 notes</p>
      <div class="article-grid" id="article-grid">{''.join(card(a) for a in articles)}</div><p class="empty-state" id="empty-state" hidden>No matching notes. Try another subject or clear the search.</p><noscript><p>Search and filters need JavaScript. All articles remain available above.</p></noscript></section></div>'''


def article_page(a, articles):
    index=articles.index(a)
    headings = re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>', a['body'])
    toc = ''.join(f'<a href="#{key}">{esc(label)}</a>' for key,label in headings)
    refs = ''.join(f'<li id="reference-{i}"><a href="{esc(url)}">{esc(label)} ↗</a></li>' for i,(label,url) in enumerate(a['references'],1))
    source_titles = {e['url'].split('/')[-1]:e['title'] for e in json.loads((ROOT/'content/source-map.json').read_text())['entries'] if e['url']}
    sources = ''.join(f'<li><a href="https://app.notion.com/p/{key}">{esc(source_titles[key])} ↗</a></li>' for key in a['notion'])
    prev = articles[index-1] if index else None
    nxt = articles[index+1] if index+1<len(articles) else None
    prev_link=f'<a href="{prev["slug"]}.html"><span>← PREVIOUS NOTE</span>{esc(prev["label"])}</a>' if prev else '<a href="../library.html"><span>← THE INDEX</span>All fieldnotes</a>'
    next_link=f'<a href="{nxt["slug"]}.html"><span>NEXT NOTE →</span>{esc(nxt["label"])}</a>' if nxt else '<a href="../labs.html"><span>CONTINUE WITH A LAB →</span>Put the notes to work</a>'
    return f'''<div class="article-layout"><article class="article-content"><header class="article-header"><p class="eyebrow">NOTE {a['id']} <span>/</span> {esc(a['category'])}</p><h1>{esc(a['title'])}</h1><div class="article-meta"><span>{a['minutes']} MIN READ</span><span>EDITED 30 OCT 2026</span><button class="print-button">Print note ↗</button></div></header><div class="prose">{a['body']}
      <section class="references" id="references"><h2>Primary references</h2><ol>{refs}</ol></section>
      <details class="notebook-sources"><summary>Notebook sources & editorial context</summary><p>Adapted from technical themes in the following entries. Private Notion sources may require access. Explanations and exercises were added for this series; this is not a verbatim export.</p><ul>{sources}</ul><p><a href="../sources.html">Full source map and coverage limits →</a></p></details>
      </div><nav class="article-pagination" aria-label="Series pagination">{prev_link}{next_link}</nav></article><aside class="toc"><p class="nav-label">IN THIS NOTE</p><nav aria-label="On this page">{toc}<a href="#references">Primary references</a></nav><div class="toc-note"><span class="status-dot"></span> Read. Reproduce. Reconsider.<p>Proposed exercises use owned applications and local sample data.</p><a href="../labs.html">Open the lab resources ↗</a></div></aside></div>'''


def labs():
    items=[('01','A query that stays a query','An in-memory SQLite example with assertions for a quoted title and an injection-shaped value.','labs/sqlite_binding.py','Python · local example'),('02','An access decision matrix','A starting CSV for recording positive and denied authorization decisions.','labs/access-matrix.csv','CSV · fictional policy'),('03','An incident reasoning record','A compact timeline and competing-hypotheses template.','labs/incident-record.md','Markdown · exercise template'),('04','A reproducible finding','Scope, observed behavior, inferred impact, correction, and retest evidence.','labs/finding-template.md','Markdown · review template')]
    cards=''.join(f'<article class="download-card"><span class="row-number">{i}</span><div><p class="eyebrow">{esc(kind)}</p><h2>{esc(title)}</h2><p>{esc(desc)}</p><a class="text-link" href="{path}" download>Download {esc(Path(path).name)} ↓</a></div></article>' for i,title,desc,path,kind in items)
    return f'''<div class="standard-content"><div class="page-intro"><p class="eyebrow">FROM READING TO DOING</p><h1>Keep a better lab notebook.</h1><p>Small, inspectable resources to accompany the series. The templates contain fictional examples and proposed work.</p></div><div class="downloads">{cards}</div><div class="prose"><h2>Run the local example</h2><pre><code class="language-bash">python3 sqlite_binding.py</code></pre><p>Expected result: <code>PASS: values stayed data; table intact.</code> Python 3 with its standard sqlite3 module is sufficient. No network service, API key, or external dependency is required.</p></div></div>'''


def sources():
    entries=json.loads((ROOT/'content/source-map.json').read_text())['entries']
    rows=''.join(f'<tr><td>{esc(e["title"])}</td><td>{esc(e["status"].replace("-"," "))}</td><td>{esc(", ".join(e["articles"]) or "—")}</td></tr>' for e in entries)
    return f'''<div class="standard-content"><div class="page-intro"><p class="eyebrow">PROVENANCE & EDITORIAL METHOD</p><h1>Show the working.</h1><p>A public technical series adapted from the Infosec view of a persistent Notion journal.</p></div><div class="prose"><h2>What supplied the material</h2><p>Twenty-three security-related records were inspected from a view containing thirty-two entries. The original technical notes and resource lists supplied the themes. Coding and game entries outside this series were not reviewed for publication.</p><h2>What changed in editing</h2><p>The articles group related notes by topic, replace informal shorthand with explanations, and link primary references beside factual claims. Exercises and templates are new editorial additions. The material does not claim professional engagement results, completed labs, or security certification.</p><p>Blank records contribute no claims. Image-only material was not transcribed; the Application Hacking entry supplies only its topic. Original screenshots, private comments, exam scores, and credential material are not included. Source dates describe the notebook history, not proof of technical currency.</p><h2>Technical corrections</h2><ul><li>SQL values should be parameterized; “sanitize the query bar” is too vague.</li><li>XSS and CSRF cross different boundaries and require different controls.</li><li>DNSSEC validates signed DNS data; it does not encrypt queries.</li><li>Kerberos V5 does not require public-key cryptography for every session.</li><li>The Heartbleed advisory supplied a fix in April 2014; old uncertainty about a patch was not carried forward.</li></ul><p>Each article links the relevant primary documentation. Sources were checked during preparation on 30 October 2026. This series is a curated snapshot; it has no live connection to the private notebook.</p><h2>Source map</h2><p>“Adapted” means the entry supplied themes or study method, not that its full text was copied. Original source links are available in each article’s context panel.</p><div class="table-wrap source-table"><table><thead><tr><th>Notebook entry</th><th>Treatment</th><th>Notes</th></tr></thead><tbody>{rows}</tbody></table></div></div></div>'''


def about():
    return '''<div class="standard-content"><div class="page-intro"><p class="eyebrow">ABOUT FIELDNOTES</p><h1>Understand the boundary.<br>Then test it.</h1><p>A compact information security publication by Syed Hussain.</p></div><div class="prose"><p>Fieldnotes connects networking, application behavior, systems, identity, and cloud delivery. Its starting point is a technical notebook; its purpose is to make the ideas easier to inspect and use.</p><h2>A publication with a working method</h2><p>Every note moves from a question to an explanation and a bounded exercise. References support technical claims. Notebook links show where the topic began. Examples are educational or fictional unless explicitly described otherwise.</p><h2>Built to stay understandable</h2><p>The site uses static HTML, local CSS and JavaScript, and a Python standard-library builder. Article text remains readable without JavaScript. Search, subject filters, navigation controls, and code copying are progressive enhancements.</p><p>No analytics, third-party embeds, API keys, or browser requests to Notion are included. The full repository includes the articles, build script, validation, and a GitHub Pages deployment workflow.</p><p><a class="text-link" href="library.html">Browse the series →</a></p></div></div>'''


def build():
    articles=load_articles()
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT/'articles').mkdir(parents=True)
    shutil.copytree(ROOT/'assets', OUT/'assets')
    shutil.copytree(ROOT/'labs', OUT/'labs', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for filename,body,current,title in [('index.html',home(articles),'home','Overview'),('library.html',library(articles),'library','Article index'),('labs.html',labs(),'labs','Lab resources'),('sources.html',sources(),'sources','Sources & method'),('about.html',about(),'about','About')]:
        (OUT/filename).write_text(page(title,body,articles,current))
    for a in articles:
        (OUT/f'articles/{a["slug"]}.html').write_text(page(a['title'],article_page(a,articles),articles,a['slug'],prefix='../',description=a['summary']))
    search=[{k:a[k] for k in ('id','slug','title','category','summary')} | {'text':html.unescape(re.sub(r'<[^>]+>',' ',a['body']))} for a in articles]
    (OUT/'assets/search.json').write_text(json.dumps(search,ensure_ascii=False))
    # Search data is an external JS file so opening index pages from disk also works.
    # Escape script delimiters for defense if this file is ever embedded by another tool.
    (OUT/'assets/search-data.js').write_text('window.FIELDNOTES_SEARCH = '+json.dumps(search,ensure_ascii=True).replace('<','\\u003c')+';\n')
    # Prepend the index data before the deferred behavior script on the library page.
    lib=(OUT/'library.html').read_text().replace('<script src="assets/site.js" defer>', '<script src="assets/search-data.js" defer></script><script src="assets/site.js" defer>')
    (OUT/'library.html').write_text(lib)
    (OUT/'.nojekyll').touch()
    print(f'Built {len(articles)} articles and 5 index/resource pages in {OUT}')


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    build()
