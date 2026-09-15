from PIL import Image, ImageEnhance, ImageOps
from pathlib import Path
import html

R=Path(".")
im=Image.open(R/"source-photo.jpg").convert("RGB")
w,h=im.size
im=im.crop((int(w*.12),int(h*.02),int(w*.88),int(h*.98)))
tw,th=900,1125
im.thumbnail((tw,th),Image.Resampling.LANCZOS)
canvas=Image.new("RGB",(tw,th),(10,14,22))
canvas.paste(im,((tw-im.width)//2,(th-im.height)//2))
im=ImageEnhance.Contrast(canvas).enhance(1.12)
im=ImageEnhance.Sharpness(im).enhance(1.25)
im.save(R/"source-prepped.png")

COLS,ROWS=88,56
CELL_W,CELL_H=9,15
PAD,TITLE,STATUS=22,34,34
ART_W,ART_H=COLS*CELL_W,ROWS*CELL_H
W,H=ART_W+PAD*2,TITLE+ART_H+STATUS+PAD
g=ImageOps.grayscale(im).resize((COLS,ROWS),Image.Resampling.LANCZOS)
g=ImageEnhance.Contrast(g).enhance(1.18)
px=g.load()
ramp=" .,:;irsXA253hMHGS#9B&@"
rows=[]
for yy in range(ROWS):
    line=""
    for xx in range(COLS):
        lum=(px[xx,yy]/255.0)**1.08
        idx=int((1-lum)*(len(ramp)-1)+.5)
        line+=ramp[max(0,min(len(ramp)-1,idx))]
    rows.append(line)
esc=lambda x:html.escape(x)

p=[]
p.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Aurangzaib Brohi colorful animated ASCII portrait" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'%(W,H,W,H))
p.append('<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#101827"/><stop offset="1" stop-color="#05070b"/></linearGradient>')
p.append('<linearGradient id="rainbow" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="%d" y2="0">'%W)
p.append('<stop stop-color="#00E5FF"/><stop offset=".2" stop-color="#2979FF"/><stop offset=".4" stop-color="#7C4DFF"/><stop offset=".6" stop-color="#E040FB"/><stop offset=".8" stop-color="#FF4081"/><stop offset="1" stop-color="#FFD740"/>')
p.append('<animate attributeName="x1" values="0;%d;0" dur="8s" repeatCount="indefinite"/><animate attributeName="x2" values="%d;%d;%d" dur="8s" repeatCount="indefinite"/></linearGradient>'%(W,W,W*2,W))
p.append('<linearGradient id="accent" x1="0" x2="1"><stop offset="0" stop-color="#00E5FF"/><stop offset=".5" stop-color="#7C4DFF"/><stop offset="1" stop-color="#FF4081"/></linearGradient>')
p.append('<filter id="glow"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
p.append('<rect width="100%%" height="100%%" rx="14" fill="url(#bg)"/><rect x=".5" y=".5" width="%d" height="%d" rx="14" fill="none" stroke="#26334a"/>'%(W-1,H-1))
for i,c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]):
    p.append('<circle cx="%d" cy="%g" r="5" fill="%s"/>'%(PAD+i*17,TITLE/2,c))
p.append('<text x="%g" y="%g" fill="#9FB3C8" font-size="12" text-anchor="middle">aurangzaib@github: ~$ ./portrait.sh</text>'%(W/2,TITLE/2+4))
art_top=TITLE+PAD*.35
fs=CELL_H*.84
for ry,line in enumerate(rows):
    y=art_top+ry*CELL_H+CELL_H*.74
    row_y=art_top+ry*CELL_H
    delay=ry*.065
    p.append('<clipPath id="r%d"><rect x="%d" y="%.1f" height="%d" width="0"><animate attributeName="width" from="0" to="%d" begin="%.3fs" dur=".09s" fill="freeze"/></rect></clipPath>'%(ry,PAD,row_y,CELL_H,ART_W,delay))
    p.append('<g clip-path="url(#r%d)"><text xml:space="preserve" x="%d" y="%.1f" fill="url(#rainbow)" filter="url(#glow)" font-size="%.1f" textLength="%d" lengthAdjust="spacing">%s</text></g>'%(ry,PAD,y,fs,ART_W,esc(line)))
    p.append('<rect y="%.1f" width="%d" height="%d" fill="#fff" opacity="0"><animate attributeName="x" from="%d" to="%d" begin="%.3fs" dur=".09s" fill="freeze"/><set attributeName="opacity" to=".9" begin="%.3fs"/><set attributeName="opacity" to="0" begin="%.3fs"/></rect>'%(row_y+1,CELL_W,CELL_H-2,PAD,PAD+ART_W,delay,delay,delay+.09))
sl=TITLE+ART_H+PAD*.35
sy=sl+20
p.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="#26334a"/>'%(sl,W,sl))
p.append('<text x="%d" y="%.1f" fill="#9FB3C8" font-size="13">aurangzaib@github:~$ whoami <tspan fill="url(#rainbow)" font-weight="700">Aurangzaib Brohi</tspan></text>'%(PAD,sy))
p.append('<rect x="%d" y="%.1f" width="8" height="14" fill="#00E5FF"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.51;1" dur="1s" repeatCount="indefinite"/></rect>'%(PAD+238,sy-12))
p.append('<rect x="%d" y="%.1f" width="%d" height="2" fill="url(#accent)" opacity=".22"><animate attributeName="y" from="%.1f" to="%.1f" dur="4.5s" repeatCount="indefinite"/></rect>'%(PAD,art_top,ART_W,art_top,art_top+ART_H))
p.append('</svg>')
(R/"avi-ascii.svg").write_text("".join(p),encoding="utf-8")

info=[("user","Aurangzaib Brohi"),("role","Data Scientist / ML Engineer"),("stack","Python • Pandas • NumPy • Scikit-Learn"),("web","HTML • CSS • JavaScript • REST APIs"),("automation","n8n Workflow Automation"),("database","SQL • SQLite"),("education","BS Computer Science • Sukkur IBA University"),("focus","Data Science • Machine Learning • Automation"),("status","Open to projects & collaborations")]
CW,CH=1100,455
c=['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" aria-label="Aurangzaib Brohi developer information card">'%(CW,CH,CW,CH)]
c.append('<defs><linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0b1220"/><stop offset=".55" stop-color="#111827"/><stop offset="1" stop-color="#090d16"/></linearGradient><linearGradient id="line" x1="0" x2="1"><stop stop-color="#00E5FF"/><stop offset=".5" stop-color="#7C4DFF"/><stop offset="1" stop-color="#FF4081"/></linearGradient></defs>')
c.append('<rect width="%d" height="%d" rx="16" fill="url(#cbg)"/><rect x=".5" y=".5" width="%d" height="%d" rx="16" fill="none" stroke="#26334a"/>'%(CW,CH,CW-1,CH-1))
for i,col in enumerate(["#ff5f56","#ffbd2e","#27c93f"]): c.append('<circle cx="%d" cy="26" r="5" fill="%s"/>'%(26+i*18,col))
c.append('<text x="86" y="32" fill="#E8F1FF" font-size="22" font-weight="800">aurangzaib@github — neofetch</text>')
c.append('<rect x="22" y="50" width="856" height="2" fill="url(#line)"><animate attributeName="x" values="22;200;22" dur="3s" repeatCount="indefinite"/></rect>')
y=100
colors=["#00E5FF","#64B5F6","#7C4DFF","#BA68C8","#FF4081","#FF7043","#FFD54F","#69F0AE","#40C4FF"]
for i,(k,v) in enumerate(info):
    c.append('<text x="28" y="%d" fill="%s" font-size="17" font-weight="800">%s</text>'%(y,colors[i],esc(k)))
    c.append('<text x="175" y="%d" fill="#D7E3F4" font-size="17">%s</text>'%(y,esc(v)))
    y+=38
c.append('<text x="28" y="432" fill="#7F93AA" font-size="13">Generated by Aurangzaib • animated SVG • self-hosted on GitHub</text></svg>')
(R/"info-card.svg").write_text("".join(c),encoding="utf-8")
print("Generated colorful animated SVG assets.")
