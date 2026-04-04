import re
import os

file_path = '/home/aqtobe-hub/ProtoQol/index.html'
with open(file_path, 'r') as f:
    content = f.read()

# Pattern to capture the existing kinetic card elements
# 1: card classes, 2: MOD badge content, 3: h3 title, 4: p text
pattern = re.compile(r'<div class="pipe-card ([^"]+)"><div class="border-beam"[^>]*></div><div class="card-stage-badge">([^<]+)</div><div class="card-content"><h3 class="card-title">([^<]+)</h3><p class="card-text">([^<]+)</p></div></div>', re.DOTALL)

def bi_panel_replacer(match):
    classes = match.group(1)
    mod_badge = match.group(2)
    title = match.group(3)
    text = match.group(4)
    
    return f'''<div class="pipe-card {classes}">
                            <div class="border-beam" style="opacity:0;"></div>
                            <div class="card-upper">
                                <div class="card-stage-badge">{mod_badge}</div>
                                <h3 class="card-title">{title}</h3>
                            </div>
                            <div class="card-lower">
                                <p class="card-text">{text}</p>
                            </div>
                        </div>'''

new_content = pattern.sub(bi_panel_replacer, content)

with open(file_path, 'w') as f:
    f.write(new_content)
