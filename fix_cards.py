import re
import os

file_path = '/home/aqtobe-hub/ProtoQol/index.html'
with open(file_path, 'r') as f:
    content = f.read()

# Pattern for unified cards
# Captures: 1: Prefix (card dive with badge), 2: Title (h3), 3: Text (p), 4: Closing div
pattern = re.compile(r'(<div class="pipe-card [^"]+">.*?<div class="card-stage-badge">MOD \d+</div>)(<h3 class="card-title">.*?</h3>)(<p class="card-text">.*?</p>)(</div>)', re.DOTALL)

def replacer(match):
    header = match.group(1)
    title = match.group(2)
    text = match.group(3)
    footer = match.group(4)
    # Check if already wrapped
    if 'class="card-content"' in match.group(0):
        return match.group(0)
    return f'{header}<div class="card-content">{title}{text}</div>{footer}'

new_content = pattern.sub(replacer, content)

# Specific legacy cleanup
new_content = new_content.replace('<div class="card-upper"><div class="card-stage-badge">MOD 18</div><h3 class="card-title">Real-Time CCTV</h3></div><div class="card-lower"><p class="card-text">Visual evidence layers for physical verification.</p></div>', '<div class="card-stage-badge">MOD 18</div><div class="card-content"><h3 class="card-title">Real-Time CCTV</h3><p class="card-text">Visual evidence layers for physical verification.</p></div>')

with open(file_path, 'w') as f:
    f.write(new_content)
