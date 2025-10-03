#!/usr/bin/env python3
import re
from pathlib import Path

file_path = Path('/var/www/html/github/brijeshwork.github.io/tools/index.html')
if not file_path.exists():
    print('File not found:', file_path)
    raise SystemExit(1)

text = file_path.read_text(encoding='utf-8')
original = text

# This regex finds <a ...> tags containing target=_blank
pattern = re.compile(r"(<a\b[^>]*?target\s*=\s*['\"]_blank['\"][^>]*?>)", re.IGNORECASE | re.DOTALL)

def add_noopener(match):
    tag = match.group(1)
    # If rel exists
    rel_search = re.search(r"rel\s*=\s*([\'\"])(.*?)\1", tag, flags=re.IGNORECASE | re.DOTALL)
    if rel_search:
        rel_val = rel_search.group(2)
        tokens = rel_val.split()
        if 'noopener' in tokens:
            return tag
        # keep existing order, prepend noopener
        new_rel = 'rel="noopener ' + rel_val + '"'
        new_tag = tag[:rel_search.start()] + new_rel + tag[rel_search.end():]
        return new_tag
    else:
        # insert rel="noopener" before the end of the opening tag
        # but keep attributes intact
        insert_pos = tag.rfind('>')
        if insert_pos == -1:
            return tag
        # remove the ending '>' then add rel and close
        new_tag = tag[:-1] + ' rel="noopener">'
        return new_tag

new_text = pattern.sub(add_noopener, text)

if new_text == original:
    print('No changes made')
else:
    backup = file_path.with_suffix('.html.bak2')
    file_path.replace(backup)
    file_path.write_text(new_text, encoding='utf-8')
    print('Updated file and backed up original to', backup)
