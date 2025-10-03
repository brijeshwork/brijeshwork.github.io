#!/usr/bin/env python3
import re
from pathlib import Path

root = Path('/var/www/html/github/brijeshwork.github.io')
files = list(root.rglob('*.html'))
changed = []

anchor_re = re.compile(r"<a\b([^>]*?)>", re.IGNORECASE | re.DOTALL)

for fp in files:
    text = fp.read_text(encoding='utf-8')
    def repl(m):
        attrs = m.group(1)
        if 'target="_blank"' not in attrs.lower() and "target='_blank'" not in attrs.lower():
            return m.group(0)
        # find rel attribute
        rel_match = re.search(r"rel\s*=\s*([\"'])(.*?)\1", attrs, flags=re.IGNORECASE | re.DOTALL)
        if rel_match:
            quote = rel_match.group(1)
            rel_value = rel_match.group(2)
            tokens = [t for t in re.split(r"\s+", rel_value.strip()) if t]
            if 'noopener' in [t.lower() for t in tokens]:
                return m.group(0)
            # insert noopener at start
            tokens.insert(0, 'noopener')
            new_rel = 'rel=' + quote + ' '.join(tokens) + quote
            new_attrs = attrs[:rel_match.start()] + new_rel + attrs[rel_match.end():]
            return '<a ' + new_attrs + '>'
        else:
            # add rel="noopener" preserving spacing
            new_attrs = attrs + ' rel="noopener"'
            return '<a ' + new_attrs + '>'
    new_text = anchor_re.sub(repl, text)
    if new_text != text:
        bak = fp.with_suffix('.html.noopener.bak')
        fp.replace(bak)
        fp.write_text(new_text, encoding='utf-8')
        changed.append(str(fp))

print('Processed', len(files), 'files. Updated', len(changed), 'files.')
for c in changed:
    print(c)
