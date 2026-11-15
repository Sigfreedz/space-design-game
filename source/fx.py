from lib import *
import sprites as S
import math, random
def sheet(frames): return strip(frames)
# solar flare wash (top-right origin)
fl=[]
for f in range(4):
    im=new(W,H); R_=330+f*22
    for y in range(H):
        for x in range(W):
            dx,dy=x-470,y+10; d=math.hypot(dx,dy); a=math.atan2(dy,dx)
            v=1-d/R_+0.14*math.sin(a*9+f*1.7)
            if v>0 and S.bay(x,y)<v*1.25:
                im.putpixel((x,y),P['pale'] if v>.7 else ('gold' and P['gold'] if v>.45 else (P['orange'] if v>.22 else P['salmon'])))
    fl.append(im)
fx={'fx_solar_flare_4f':sheet(fl)}
gl=[]
for f in range(4):
    r=random.Random(100+f); im=new(W,H)
    for _ in range(int(W*H*0.012)): Pt(im,r.randrange(W),r.randrange(H),r.choice(['white','cyan','magenta','lav']))
    for _ in range(7):
        y=r.randrange(H); h=r.randint(1,4); x=r.randint(0,W-120); w=r.randint(100,W-x); c=r.choice(['cyan','magenta','white','ice'])
        for yy in range(y,min(H,y+h)):
            for xx in range(x,x+w):
                if (xx+yy)%3: Pt(im,xx,yy,c)
    for y in range(0,H,4):
        for x in range(W):
            if S.bay(x,y)<.18 and im.getpixel((x,y))[3]==0: im.putpixel((x,y),P['ink'])
    gl.append(im)
fx['fx_static_glitch_4f']=sheet(gl)
sp=[]
for f in range(4):
    im=new(32,32); rr=3.5*(f+1); c=['white','pale','gold','orange'][f]
    for k in range(10):
        a=math.radians(k*36+f*9); x=16+math.cos(a)*rr*(1+0.3*(k%2)); y=16+math.sin(a)*rr*(1+0.3*(k%2))
        R(im,int(x),int(y),2 if f<3 else 1,2 if f<3 else 1,c if k%3 else 'white')
    sp.append(im)
fx['fx_sparks_4f']=sheet(sp)
mt=[]; ux,uy=0.912,0.41
for f in range(6):
    im=new(96,48)
    if f<5:
        hx_,hy_=10+f*17,4+f*8
        for k in range(1,22):
            if S.bay(int(hx_-ux*k),int(hy_-uy*k))<(1-k/22)*1.1:
                c='pale' if k<5 else ('gold' if k<10 else ('orange' if k<15 else 'salmon'))
                R(im,int(hx_-ux*k),int(hy_-uy*k),2 if k<12 else 1,2 if k<12 else 1,c)
        R(im,hx_-1,hy_-1,4,4,'white'); R(im,hx_-2,hy_,6,2,'pale') 
    else:
        cx,cy=90,44
        for k in range(8):
            a=math.radians(k*45)
            L(im,[(cx,cy),(cx+math.cos(a)*10,cy+math.sin(a)*10)],'orange' if k%2 else 'pale')
        ell(im,[cx-3,cy-3,cx+3,cy+3],'white')
    mt.append(im)
fx['fx_meteor_streak_6f']=sheet(mt)
hs=[]
for f in range(4):
    im=new(48,48)
    for y in range(0,48):
        yy=(y+f*3)%12
        if yy<2:
            for x in range(4,44):
                off=int(math.sin((x+f*5)/4.0+y/6.0)*2)
                if S.bay(x,y)<1-abs(x-24)/24*0.9: Pt(im,x,y+off,['orange','salmon','pale'][((x//4)+f)%3])
    hs.append(im)
fx['fx_heat_shimmer_4f']=sheet(hs)
dh=[]
for f in range(4):
    im=new(W,H)
    for y in range(H):
        for x in range(W):
            v=S.fbm((x+f*6)/50,y/30,77)
            if v>.52 and S.bay(x,y)<(v-.5)*3.2: im.putpixel((x,y),P['rust'] if v>.62 else P['salmon'])
    dh.append(im)
fx['fx_dust_haze_4f']=sheet(dh)
tf=[]
for f,ln in enumerate([10,16,22,12]):
    im=new(24,32); S.flame(im,12,2,ln)
    if f in(1,2): 
        r=random.Random(f); [Pt(im,12+r.randint(-7,7),2+r.randint(4,ln+4),'pale') for _ in range(5)]
    tf.append(im)
fx['fx_thruster_flash_4f']=sheet(tf)
cf=[]
r0=random.Random(9); pieces=[(r0.randrange(W),r0.randrange(H),r0.choice(['gold','red','cyan','green_l','magenta','white']),r0.random()*6) for _ in range(70)]
for f in range(6):
    im=new(W,H)
    for x,y0,c,ph in pieces:
        y=(y0+f*45)%H; xx=int(x+math.sin(ph+f)*6) % W
        R(im,xx,y,2 if (f+int(ph))%2 else 3,3 if (f+int(ph))%2 else 2,c)
    cf.append(im)
fx['fx_confetti_6f']=sheet(cf)
fs=[]
for f in range(4):
    r=random.Random(300+f); im=new(W,H)
    for _ in range(int(W*H*0.1)): Pt(im,r.randrange(W),r.randrange(H),r.choice(['g1','g2','g3','g0']))
    for _ in range(9):
        y=r.randrange(H); h=r.randint(2,9)
        R(im,0,y,W,h,r.choice(['g0','ink']))
        for x in range(0,W,2): Pt(im,x,y,'g3')
    fs.append(im)
fx['fx_fail_static_4f']=sheet(fs)
if __name__=='__main__':
    for k,v in fx.items(): save(v,f'fx/{k}.png')
    small=[fx['fx_sparks_4f'],fx['fx_meteor_streak_6f'],fx['fx_heat_shimmer_4f'],fx['fx_thruster_flash_4f']]
    big=new(480,270,'navy1'); paste(big,fl[1],0,0); paste(big,gl[0],0,0) if False else None
    preview(small+[big],1,3,'fx')
    big2=new(480,270,'ink'); paste(big2,dh[1],0,0); preview([big2,fl[2].crop((0,0,480,270)) if False else big],1,1,'fx2')
