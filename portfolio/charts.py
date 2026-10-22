from html import escape
from pathlib import Path

def bars(values,path,title):
    width=860;height=100+len(values)*46;maxval=max([abs(v) for v in values.values()]+[1])
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',f'<rect width="100%" height="100%" fill="#f5f8fb"/><text x="24" y="32" font-family="sans-serif" font-size="18">{escape(title)}</text>']
    for i,(label,value) in enumerate(values.items()):
        y=65+i*46
        svg.append(f'<text x="24" y="{y+16}" font-family="sans-serif" font-size="12">{escape(str(label))}</text><rect x="260" y="{y}" width="{abs(value)/maxval*470}" height="24" fill="{"#087f8c" if value>=0 else "#b54a4a"}"/><text x="750" y="{y+16}" font-family="sans-serif" font-size="12">{value:.3f}</text>')
    svg.append('</svg>');Path(path).write_text(''.join(svg))
