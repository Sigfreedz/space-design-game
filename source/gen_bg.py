from PIL import Image, ImageDraw
import random, math
W,H=480,270
def hx(s): return tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
C=[hx(c) for c in """#0b0d1f #141a3a #1f2a5c #2f3f8a #ffffff #8ea0d0 #ffe9a8 #1b4f9c #2d79d1 #5aa5e8
#2f7a3a #4fa84a #86cf5a #e8f0ff #b9c8e6 #7fc8ff #4a4d58 #6b6f7a #8d919c #b4b8c2 #d6d9e0 #5a5fa8
#e07a5f #f2a65a #ffd27a #2a2a3a #3d3d52 #5a5a70 #c0c4d0 #d94a4a #1a1f4a #2c3a7a""".split()]
BAY=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
def bay(x,y): return (BAY[y%4][x%4]+0.5)/16
def h(ix,iy,s):
    n=(ix*374761393+iy*668265263+s*982451653)&0xffffffff
    n=((n^(n>>13))*1274126177)&0xffffffff
    return ((n^(n>>16))&0xffff)/65535
def vn(x,y,s):
    xi,yi=math.floor(x),math.floor(y); fx,fy=x-xi,y-yi
    fx=fx*fx*(3-2*fx); fy=fy*fy*(3-2*fy)
    a=h(xi,yi,s);b=h(xi+1,yi,s);c=h(xi,yi+1,s);d=h(xi+1,yi+1,s)
    return (a*(1-fx)+b*fx)*(1-fy)+(c*(1-fx)+d*fx)*fy
def fbm(x,y,s):
    return vn(x,y,s)*.55+vn(x*2,y*2,s+1)*.3+vn(x*4,y*4,s+2)*.15
def stars(img,seed,n,ymax=H):
    r=random.Random(seed); px=img.load()
    for _ in range(n):
        x,y=r.randrange(W),r.randrange(ymax)
        c=r.choice([4,5,5,5,6,5])
        px[x,y]=C[c]
        if r.random()<0.04 and 1<x<W-2 and 1<y<H-2:
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)): px[x+dx,y+dy]=C[6]
def space_bg(img):
    px=img.load()
    for y in range(H):
        for x in range(W):
            t=y/H+ (bay(x,y)-.5)*.35
            px[x,y]=C[0] if t<.45 else (C[1] if t<.8 else C[2])
def planet(img,cx,cy,r,shade,rim=True,seed=3):
    px=img.load()
    for y in range(max(0,cy-r-4),min(H,cy+r+4)):
        for x in range(max(0,cx-r-4),min(W,cx+r+4)):
            nx,ny=(x-cx)/r,(y-cy)/r; d2=nx*nx+ny*ny
            if d2<=1:
                z=math.sqrt(1-d2); L=-.55*nx-.6*ny+.75*z
                t=L+(bay(x,y)-.5)*.3
                lv=0 if t<.28 else (1 if t<.6 else 2)
                px[x,y]=shade(x,y,lv)
            elif rim and d2<=((r+3)/r)**2:
                a=1-(math.sqrt(d2)*r-r)/3
                if a+(bay(x,y)-.5)*.6>.45: px[x,y]=C[15] if a>.7 else C[7]
def earth(x,y,lv):
    n=fbm(x/22,y/22,5); cl=fbm(x/14+40,y/9,9)
    if cl>.7: return [C[14],C[13],C[13]][lv]
    if n>.52: return [C[10],C[11],C[12]][lv]
    return [C[7],C[8],C[9]][lv]
def moon(x,y,lv): return [C[17],C[18],C[19]][lv]
def craters(img,cx,cy,r,seed,n):
    d=ImageDraw.Draw(img); rnd=random.Random(seed); px=img.load()
    for _ in range(n):
        a=rnd.random()*6.28; rr=rnd.random()**.5*r*.88
        x=int(cx+math.cos(a)*rr); y=int(cy+math.sin(a)*rr)
        if not(0<x<W and 0<y<H): continue
        s=rnd.choice([3,4,5,7,9])
        d.ellipse([x-s,y-s//2,x+s,y+s//2],fill=C[16])
        d.arc([x-s,y-s//2,x+s,y+s//2],190,350,fill=C[20])
# 1 cruise
im=Image.new("RGBA",(W,H));space_bg(im);stars(im,1,260)
px=im.load()
for y in range(H):
    for x in range(W):
        n=fbm(x/60,y/26+3,21)
        if n>.55 and bay(x,y)<(n-.5)*3: px[x,y]=C[3]
        elif n>.62: px[x,y]=C[2]
for y in range(40,110):
    for x in range(380,470):
        d=math.hypot(x-425,y-75)
        if d<5: px[x,y]=C[4]
        elif d<9: px[x,y]=C[6]
        elif d<9+ (bay(x,y)*14) and d<20: px[x,y]=C[5]
im.save("bg_deep_space_cruise.png")
# 2 earth orbit
im=Image.new("RGBA",(W,H));space_bg(im);stars(im,2,200,170)
planet(im,300,400,250,earth);im.save("bg_earth_orbit.png")
# 3 moon orbit
im=Image.new("RGBA",(W,H));space_bg(im);stars(im,3,220,200)
planet(im,150,410,235,moon,rim=False);craters(im,150,410,235,7,40)
# small earth in sky
planet(im,400,60,26,earth,rim=True);im.save("bg_moon_orbit.png")
# 4 launch pad
im=Image.new("RGBA",(W,H));px=im.load()
sky=[1,30,31,21,22,23,24,25]
hz=200
for y in range(hz):
    t=y/hz*(len(sky)-1); i=int(t); f=t-i
    for x in range(W):
        px[x,y]=C[sky[min(i+(1 if f+(bay(x,y)-.5)*.9>.5 else 0),len(sky)-1)]]
stars(im,4,70,80)
d=ImageDraw.Draw(im)
# far hills
for x in range(W):
    y=hz-8-int(10*fbm(x/40,2,31)+5*fbm(x/12,9,32))
    d.line([x,y,x,hz],fill=C[3])
d.rectangle([0,hz,W,H],fill=C[26])
for y in range(hz,H):
    for x in range(W):
        if bay(x,y)<(y-hz)/(H-hz)*.8: px[x,y]=C[25]
        elif fbm(x/8,y/4,41)>.7: px[x,y]=C[27]
# pad
d.rectangle([170,hz+30,310,hz+44],fill=C[28]);d.rectangle([170,hz+30,310,hz+32],fill=C[29])
d.rectangle([225,hz+44,255,H],fill=C[27])
# tower
tx=330
d.rectangle([tx,70,tx+8,hz+30],fill=C[28])
for y in range(76,hz+30,12):
    d.line([tx,y,tx+8,y+12],fill=C[29]); d.line([tx+8,y,tx,y+12],fill=C[27])
d.rectangle([tx-2,70,tx+10,72],fill=C[29])
d.rectangle([tx-40,100,tx,104],fill=C[29]);d.rectangle([tx-40,100,tx-38,112],fill=C[28])
for y in (80,150): d.rectangle([tx+3,y,tx+5,y+2],fill=C[30])
d.rectangle([tx+3,60,tx+5,70],fill=C[29]);px[tx+4,58]=C[30]
# lights on pad
for x in range(176,310,22): d.rectangle([x,hz+27,x+2,hz+29],fill=C[24])
im.save("bg_launch_pad.png")
# preview sheet x2
names=["bg_launch_pad","bg_deep_space_cruise","bg_earth_orbit","bg_moon_orbit"]
sheet=Image.new("RGBA",(W*2,H*2))
for i,n in enumerate(names):
    sheet.paste(Image.open(n+".png"),((i%2)*W,(i//2)*H))
sheet.save("bg_preview_sheet.png")
cols=set()
for n in names: cols|=set(c for _,c in Image.open(n+".png").getcolors(10**6))
print(len(cols))
