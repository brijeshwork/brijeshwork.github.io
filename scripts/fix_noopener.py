#!/usr/bin/env python3
import re
from pathlib import Path

file_path = Path('/var/www/html/github/brijeshwork.github.io/tools/index.html')
if not file_path.exists():
    print('File not found:', file_path)
    raise SystemExit(1)

text = file_path.read_text(encoding='utf-8')

# Pattern to find anchor tags with target="_blank"
anchor_re = re.compile(r"<a\s+([^>]*?)>", re.IGNORECASE | re.DOTALL)

def ensure_noopener(match):
    attrs = match.group(1)
    if 'target="_blank"' not in attrs and "target='_blank'" not in attrs:
        return match.group(0)
    # find rel attribute
    rel_match = re.search(r"rel\s*=\s*([\"'])(.*?)\1", attrs, flags=re.IGNORECASE | re.DOTALL)
    if rel_match:
        quote = rel_match.group(1)
        rel_value = rel_match.group(2)
        tokens = {t for t in re.split(r"\s+", rel_value.strip()) if t}
        if 'noopener' in tokens:
            return match.group(0)
        # add noopener
        tokens_list = list(tokens)
        # Prefer to keep order: add noopener at the start
        tokens_list.insert(0, 'noopener')
        new_rel = 'rel=' + quote + ' '.join(tokens_list) + quote
        # replace old rel in attrs
        new_attrs = attrs[:rel_match.start()] + new_rel + attrs[rel_match.end():]
        return '<a ' + new_attrs + '>'
    else:
        # insert rel="noopener" before the closing '>' of the tag attributes
        new_attrs = attrs + ' rel="noopener"'
        return '<a ' + new_attrs + '>'

new_text = anchor_re.sub(ensure_noopener, text)

if new_text == text:
    print('No changes needed')
else:
    backup = file_path.with_suffix('.html.bak')
    file_path.replace(backup)
    file_path.write_text(new_text, encoding='utf-8')
    print('Updated file and backed up original to', backup)
