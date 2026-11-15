from PIL import Image, ImageDraw
import math, random, os
HEX = dict(ink='#0b0d1f', navy1='#141a3a', navy2='#1f2a5c', navy3='#2f3f8a', peri='#5a5fa8', lav='#8ea0d0',
 white='#ffffff', ice='#e8f0ff', mist='#b9c8e6', cyan='#7fc8ff', blue_d='#1b4f9c', blue='#2d79d1', blue_l='#5aa5e8',
 green_d='#2f7a3a', green='#4fa84a', green_l='#86cf5a', g0='#2a2a3a', g1='#4a4d58', g2='#6b6f7a', g3='#8d919c',
 g4='#b4b8c2', g5='#d6d9e0', red='#d94a4a', salmon='#e07a5f', orange='#f2a65a', gold='#ffd27a', pale='#ffe9a8',
 teal='#2aa7a0', purple='#8a5fd0', magenta='#d24fa8', maroon='#7a2a3a', rust='#9a4a1e')
def hx(s): return tuple(int(s[i:i+2],16) for i in (1,3,5))+(255,)
P = {k: hx(v) for k,v in HEX.items()}
T = (0,0,0,0)
OUT = '/mnt/user-data/outputs/assets'
W,H = 480,270
# card type colors: light, base, dark
TYPES = {'mission':('pale','gold','rust'),'orbit':('blue_l','blue','blue_d'),'rocket':('salmon','orange','maroon'),
         'spacecraft':('cyan','teal','green_d'),'instrument':('lav','purple','navy3'),'event':('lav','magenta','maroon')}
def col(c): return P[c] if isinstance(c,str) else c
def new(w,h,fill=None): return Image.new('RGBA',(w,h),T if fill is None else col(fill))
def save(img,rel):
    p=os.path.join(OUT,rel); os.makedirs(os.path.dirname(p),exist_ok=True); img.save(p); return p
def R(img,x,y,w,h,c):
    if w<=0 or h<=0: return
    ImageDraw.Draw(img).rectangle([x,y,x+w-1,y+h-1],fill=col(c))
def O(img,x,y,w,h,c,t=1):
    for i in range(t):
        if w-2*i<=0 or h-2*i<=0: break
        ImageDraw.Draw(img).rectangle([x+i,y+i,x+w-1-i,y+h-1-i],outline=col(c))
def L(img,pts,c,wd=1): ImageDraw.Draw(img).line(pts,fill=col(c),width=wd)
def Pt(img,x,y,c):
    if 0<=x<img.width and 0<=y<img.height: img.putpixel((int(x),int(y)),col(c))
def poly(img,pts,c,outline=None):
    ImageDraw.Draw(img).polygon(pts,fill=None if c is None else col(c),outline=None if outline is None else col(outline))
def ell(img,box,c,outline=None):
    ImageDraw.Draw(img).ellipse(box,fill=None if c is None else col(c),outline=None if outline is None else col(outline))
def arc(img,box,a0,a1,c,wd=1): ImageDraw.Draw(img).arc(box,a0,a1,fill=col(c),width=wd)
def clear(img,x,y,w,h): ImageDraw.Draw(img).rectangle([x,y,x+w-1,y+h-1],fill=T)
def paste(dst,src,x,y): dst.paste(src,(int(x),int(y)),src)
def scale(img,k): return img.resize((img.width*k,img.height*k),Image.NEAREST)
def ascii_img(rows,legend):
    im=new(len(rows[0]),len(rows))
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            if ch in legend: im.putpixel((x,y),col(legend[ch]))
    return im
def strip(imgs,gap=0):
    w=sum(i.width for i in imgs)+gap*(len(imgs)-1); h=max(i.height for i in imgs)
    s=new(w,h); x=0
    for i in imgs: paste(s,i,x,0); x+=i.width+gap
    return s
def vstrip(imgs,gap=0):
    h=sum(i.height for i in imgs)+gap*(len(imgs)-1); w=max(i.width for i in imgs)
    s=new(w,h); y=0
    for i in imgs: paste(s,i,0,y); y+=i.height+gap
    return s
def preview(items,cols,k,name,bg='g0',pad=4):
    cw=max(i.width for i in items); ch=max(i.height for i in items)
    rows=(len(items)+cols-1)//cols
    Wd=cols*(cw+pad)+pad; Ht=rows*(ch+pad)+pad
    im=new(Wd,Ht,bg)
    for n,i in enumerate(items): paste(im,i,pad+(n%cols)*(cw+pad),pad+(n//cols)*(ch+pad))
    scale(im,k).save(f'/home/claude/prev/{name}.png')
# ---- bitmap font 5x7 (placeholder UI font, uppercase only)
GL = {
'A':'.###./#...#/#...#/#####/#...#/#...#/#...#','B':'####./#...#/#...#/####./#...#/#...#/####.',
'C':'.###./#...#/#..../#..../#..../#...#/.###.','D':'####./#...#/#...#/#...#/#...#/#...#/####.',
'E':'#####/#..../#..../####./#..../#..../#####','F':'#####/#..../#..../####./#..../#..../#....',
'G':'.###./#...#/#..../#.###/#...#/#...#/.####','H':'#...#/#...#/#...#/#####/#...#/#...#/#...#',
'I':'.###./..#../..#../..#../..#../..#../.###.','J':'..###/...#./...#./...#./...#./#..#./.##..',
'K':'#...#/#..#./#.#../##.../#.#../#..#./#...#','L':'#..../#..../#..../#..../#..../#..../#####',
'M':'#...#/##.##/#.#.#/#.#.#/#...#/#...#/#...#','N':'#...#/##..#/#.#.#/#..##/#...#/#...#/#...#',
'O':'.###./#...#/#...#/#...#/#...#/#...#/.###.','P':'####./#...#/#...#/####./#..../#..../#....',
'Q':'.###./#...#/#...#/#...#/#.#.#/#..#./.##.#','R':'####./#...#/#...#/####./#.#../#..#./#...#',
'S':'.####/#..../#..../.###./....#/....#/####.','T':'#####/..#../..#../..#../..#../..#../..#..',
'U':'#...#/#...#/#...#/#...#/#...#/#...#/.###.','V':'#...#/#...#/#...#/#...#/#...#/.#.#./..#..',
'W':'#...#/#...#/#...#/#.#.#/#.#.#/##.##/#...#','X':'#...#/#...#/.#.#./..#../.#.#./#...#/#...#',
'Y':'#...#/#...#/.#.#./..#../..#../..#../..#..','Z':'#####/....#/...#./..#../.#.../#..../#####',
'0':'.###./#...#/#..##/#.#.#/##..#/#...#/.###.','1':'..#../.##../..#../..#../..#../..#../.###.',
'2':'.###./#...#/....#/...#./..#../.#.../#####','3':'####./....#/....#/.###./....#/....#/####.',
'4':'...#./..##./.#.#./#..#./#####/...#./...#.','5':'#####/#..../####./....#/....#/#...#/.###.',
'6':'.###./#..../#..../####./#...#/#...#/.###.','7':'#####/....#/...#./..#../.#.../.#.../.#...',
'8':'.###./#...#/#...#/.###./#...#/#...#/.###.','9':'.###./#...#/#...#/.####/....#/....#/.###.',
' ':'...../...../...../...../...../...../.....','.':'...../...../...../...../...../...../..#..',
':':'...../..#../...../...../..#../...../.....','/':'....#/....#/...#./..#../.#.../#..../#....',
'-':'...../...../...../.###./...../...../.....','+':'...../..#../..#../#####/..#../..#../.....',
'%':'##..#/##..#/...#./..#../.#.../#..##/#..##','!':'..#../..#../..#../..#../..#../...../..#..',
'?':'.###./#...#/....#/...#./..#../...../..#..','$':'..#../.####/#.#../.###./..#.#/####./..#..',
'>':'#..../.#.../..#../...#./..#../.#.../#....','<':'...#./..#../.#.../#..../.#.../..#../...#.',
'x':'...../...../#...#/.#.#./..#../.#.#./#...#',"'":'..#../..#../...../...../...../...../.....',
}
def tw(s,k=1): return max(0,len(s)*6*k-k)
def text(img,x,y,s,c,k=1):
    cx=x
    for ch in s.upper():
        g=GL.get(ch)
        if g:
            for r,row in enumerate(g.split('/')):
                for q,v in enumerate(row):
                    if v=='#':
                        if k==1: Pt(img,cx+q,y+r,c)
                        else: R(img,cx+q*k,y+r*k,k,k,c)
        cx+=6*k
def text_c(img,cx,y,s,c,k=1): text(img,cx-tw(s,k)//2,y,s,c,k)
def text_o(img,x,y,s,c,oc='ink',k=1):
    for dx,dy in ((-k,0),(k,0),(0,-k),(0,k),(-k,-k),(k,k),(-k,k),(k,-k)): text(img,x+dx,y+dy,s,oc,k)
    text(img,x,y,s,c,k)
D3 = {'1':'.#./##./.#./.#./###','2':'##./..#/.#./#../###','3':'##./..#/.#./..#/##.'}
def digit3(img,x,y,d,c):
    for r,row in enumerate(D3[d].split('/')):
        for q,v in enumerate(row):
            if v=='#': Pt(img,x+q,y+r,c)
# ---- panels and buttons
def panel(w,h,fill='navy1',border='lav',hi='navy3',sh='ink'):
    im=new(w,h)
    R(im,0,0,w,h,border); R(im,1,1,w-2,h-2,fill)
    L(im,[(1,1),(w-2,1)],hi); L(im,[(1,1),(1,h-2)],hi)
    L(im,[(1,h-2),(w-2,h-2)],sh); L(im,[(w-2,1),(w-2,h-2)],sh)
    for x,y in ((0,0),(w-1,0),(0,h-1),(w-1,h-1)): im.putpixel((x,y),T)
    return im
def header(im,title,c='navy3',tc='white',h=11,x=2,y=2):
    R(im,x,y,im.width-2*x,h,c); L(im,[(x,y),(im.width-x-1,y)],'peri') if c=='navy3' else None
    text(im,x+4,y+(h-7)//2+0,title,tc)
STY = {'primary':dict(fill='blue',hi='blue_l',lo='blue_d',edge='ink',tc='white'),
 'secondary':dict(fill='navy2',hi='navy3',lo='navy1',edge='lav',tc='ice'),
 'go':dict(fill='green',hi='green_l',lo='green_d',edge='ink',tc='white'),
 'gold':dict(fill='gold',hi='pale',lo='rust',edge='ink',tc='ink'),
 'teal':dict(fill='teal',hi='cyan',lo='green_d',edge='ink',tc='white'),
 'danger':dict(fill='red',hi='salmon',lo='maroon',edge='ink',tc='white')}
def button(w,h,state='default',lines=('',),style='primary'):
    s=STY[style]
    if state=='disabled': f,hi,lo,tc,edge='g1','g2','g0','g2','g0'
    elif state=='pressed': f,hi,lo,tc,edge=s['lo'],s['lo'],s['hi'],s['tc'],s['edge']
    elif state=='hover': f,hi,lo,tc,edge=s['hi'],'white',s['fill'],s['tc'] if style!='secondary' else 'white','white'
    else: f,hi,lo,tc,edge=s['fill'],s['hi'],s['lo'],s['tc'],s['edge']
    if style=='gold' and state=='hover': tc='ink'
    im=new(w,h); R(im,0,0,w,h,edge); R(im,1,1,w-2,h-2,f)
    L(im,[(1,1),(w-2,1)],hi); L(im,[(1,1),(1,h-2)],hi); L(im,[(1,h-2),(w-2,h-2)],lo); L(im,[(w-2,1),(w-2,h-2)],lo)
    for x,y in ((0,0),(w-1,0),(0,h-1),(w-1,h-1)): im.putpixel((x,y),T)
    off=1 if state=='pressed' else 0
    n=len(lines); th=n*7+(n-1)*1; y0=(h-th)//2+off
    for i,t in enumerate(lines): text_c(im,w//2+off,y0+i*8,t,tc)
    return im
def dither_mask(img,level):
    # level 0..16: keep pixels where bayer < level
    B=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
    o=img.copy()
    for y in range(o.height):
        for x in range(o.width):
            if B[y%4][x%4]>=level: o.putpixel((x,y),T)
    return o
def dim(img):
    o=img.copy(); ramp=['g0','g1','g2','g3']
    for y in range(o.height):
        for x in range(o.width):
            r,g,b,a=o.getpixel((x,y))
            if a: o.putpixel((x,y),col(ramp[min(3,int((0.3*r+0.59*g+0.11*b)/64))]))
    return o
