#!/usr/bin/env python3
"""Validate release files, local links/fragments, metadata, and recognizable secrets.

This is a bounded pattern check, not a complete secret detector or security audit.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.title_count = 0
        self.main_count = 0
        self.errors = []
        self.svg_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs['id'] in self.ids: self.errors.append(f"Duplicate id {attrs['id']}")
            self.ids.add(attrs['id'])
        if tag == 'svg': self.svg_depth += 1
        if tag == 'title' and not self.svg_depth: self.title_count += 1
        if tag == 'main': self.main_count += 1
        for key in ('href','src'):
            if key in attrs: self.links.append(attrs[key])
        if tag == 'script' and not attrs.get('src'): self.errors.append('Inline script is blocked by CSP')
        if any(key.startswith('on') for key in attrs): self.errors.append('Inline event handler is blocked by CSP')

    def handle_endtag(self, tag):
        if tag == 'svg': self.svg_depth = max(0, self.svg_depth - 1)


def secret_findings(text):
    patterns = {
        'AWS access key': r'(?:AK' + r'IA|AS' + r'IA)[A-Z0-9]{16}',
        'private key': r'-----BEGIN (?:RSA |EC |OPENSSH )?' + r'PRIVATE KEY-----',
        'GitHub token': r'(?:gh' + r'p_|github_' + r'pat_)[A-Za-z0-9_]{30,}',
        'assigned secret': r'(?i)(?:aws_secret_access_key|secret_access_key|api_key|api_token)\s*[=:]\s*[\x22\x27]?[A-Za-z0-9/+_=-]{24,}',
    }
    return [label for label,pattern in patterns.items() if re.search(pattern,text)]


def check():
    errors=[]
    articles=json.loads((ROOT/'content/articles.json').read_text())
    slugs=[a['slug'] for a in articles]
    if len(slugs)!=len(set(slugs)): errors.append('Duplicate article slug')
    entries=json.loads((ROOT/'content/source-map.json').read_text())['entries']
    source_ids={entry['url'].split('/')[-1] for entry in entries if entry.get('url')}
    for article in articles:
        if not set(article['notion']).issubset(source_ids): errors.append(f"Missing provenance: {article['slug']}")
        if not article['references']: errors.append(f"No references: {article['slug']}")
    documents={}
    for path in OUT.rglob('*.html'):
        document=Document(); document.feed(path.read_text()); documents[path.resolve()]=document
        errors.extend(f'{path.relative_to(ROOT)}: {e}' for e in document.errors)
        if document.title_count!=1 or document.main_count!=1: errors.append(f'Invalid document landmarks: {path}')
    if len(documents)!=len(articles)+5: errors.append('Missing generated pages; run scripts/build.py first')
    for path,document in documents.items():
        for link in document.links:
            url=urlsplit(link)
            if url.scheme in ('https','http','mailto','data'): continue
            if url.scheme or link.startswith('//'):
                errors.append(f'Unsupported link scheme in {path.name}'); continue
            if url.path.startswith('/'):
                errors.append(f'Root-relative link breaks project Pages: {path.name}: {link}'); continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            if not target.is_relative_to(OUT.resolve()): errors.append(f'Link leaves published directory: {path.name}: {link}'); continue
            if target.is_dir(): target=target/'index.html'
            if not target.exists(): errors.append(f'Broken local link: {path.name}: {link}')
            elif url.fragment and target.suffix=='.html' and unquote(url.fragment) not in documents.get(target,Document()).ids:
                errors.append(f'Broken fragment: {path.name}: {link}')
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(part in ('.git','__pycache__','.openai') for part in path.relative_to(ROOT).parts): continue
        if path.suffix in ('.pyc','.zip','.bundle'): continue
        try: text=path.read_text()
        except UnicodeError: continue
        for label in secret_findings(text): errors.append(f'{label} pattern found in {path.relative_to(ROOT)} (value omitted)')
    if errors:
        print('\n'.join(errors),file=sys.stderr); return 1
    print(f'PASS: {len(documents)} HTML pages, internal links/fragments, source mappings, and secret-pattern checks.')
    return 0


if __name__=='__main__':
    sys.exit(check())
