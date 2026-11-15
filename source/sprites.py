from lib import *
import math
BAY=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
def bay(x,y): return (BAY[y%4][x%4]+0.5)/16
def _h(ix,iy,s):
    n=(ix*374761393+iy*668265263+s*982451653)&0xffffffff
    n=((n^(n>>13))*1274126177)&0xffffffff
    return ((n^(n>>16))&0xffff)/65535
def vn(x,y,s):
    xi,yi=math.floor(x),math.floor(y); fx,fy=x-xi,y-yi
    fx=fx*fx*(3-2*fx); fy=fy*fy*(3-2*fy)
    a=_h(xi,yi,s);b=_h(xi+1,yi,s);c=_h(xi,yi+1,s);d=_h(xi+1,yi+1,s)
    return (a*(1-fx)+b*fx)*(1-fy)+(c*(1-fx)+d*fx)*fy
def fbm(x,y,s): return vn(x,y,s)*.55+vn(x*2,y*2,s+1)*.3+vn(x*4,y*4,s+2)*.15
def body(kind,r):
    n=2*r+8; im=new(n,n); c=r+4
    for y in range(n):
        for x in range(n):
            nx,ny=(x-c)/r,(y-c)/r; d2=nx*nx+ny*ny
            if d2<=1:
                z=math.sqrt(1-d2); Lg=-.55*nx-.6*ny+.75*z; t=Lg+(bay(x,y)-.5)*.3
                lv=0 if t<.28 else (1 if t<.6 else 2)
                if kind=='earth':
                    nz=fbm(x/22,y/22,5); cl=fbm(x/14+40,y/9,9)
                    if cl>.7: col_=['mist','ice','ice'][lv]
                    elif nz>.52: col_=['green_d','green','green_l'][lv]
                    else: col_=['blue_d','blue','blue_l'][lv]
                elif kind=='mars':
                    nz=fbm(x/18,y/18,12); col_=(['maroon','salmon','orange'] if nz>.5 else ['rust','salmon','orange'])[lv] if nz>.5 else ['maroon','rust','salmon'][lv]
                elif kind=='asteroid': col_=['g1','g2','g3'][lv]
                else: col_=['g2','g3','g4'][lv]
                im.putpixel((x,y),P[col_])
            elif kind=='earth' and d2<=((r+3)/r)**2:
                a=1-(math.sqrt(d2)*r-r)/3
                if a+(bay(x,y)-.5)*.6>.45: im.putpixel((x,y),P['cyan'] if a>.7 else P['blue_l'])
    if kind=='moon':
        rnd=random.Random(7)
        for _ in range(int(r/5)):
            a=rnd.random()*6.28; rr=rnd.random()**.5*r*.8; x=int(c+math.cos(a)*rr); y=int(c+math.sin(a)*rr); s=rnd.choice([2,3,4])
            ell(im,[x-s,y-s//2,x+s,y+s//2],'g1')
    if kind=='asteroid':
        # lumpy mask
        for y in range(n):
            for x in range(n):
                ang=math.atan2(y-c,x-c); rr=r*(0.82+0.3*vn(math.cos(ang)*2+5,math.sin(ang)*2+5,3))
                if math.hypot(x-c,y-c)>rr: im.putpixel((x,y),T)
        rnd=random.Random(3)
        for _ in range(7):
            x=c+rnd.randint(-r//2,r//2); y=c+rnd.randint(-r//2,r//2); s=rnd.choice([2,3,4])
            if im.getpixel((x,y))[3]: ell(im,[x-s,y-s//2,x+s,y+s//2],'g0')
    return im
def _booster(im,x,w,top,h,cap):
    R(im,x,top+w,w,h,'ice'); R(im,x+w-max(1,w//3),top+w,max(1,w//3),h,'g4'); R(im,x,top+w,1,h,'white')
    poly(im,[(x,top+w),(x+w-1,top+w),(x+w//2,top)],cap); R(im,x,top+w+3,w,2,'red'); R(im,x+1,top+w+h,max(1,w-2),2,'g2')
def rocket(cw,ch,nh,per_side=0,bw=5,bh=0):
    side=per_side*(bw+1); w=cw+2*side+6; h=nh+ch+4
    im=new(w,h); x0=3+side; top=0
    for k in range(per_side):
        bx=x0-(k+1)*(bw+1); ex=x0+cw+k*(bw+1)+1
        _booster(im,bx,bw,nh+8+k*4,bh-k*4,'red'); _booster(im,ex,bw,nh+8+k*4,bh-k*4,'red')
    R(im,x0,top+nh,cw,ch,'ice'); R(im,x0+cw-max(2,cw//3),top+nh,max(2,cw//3),ch,'g4'); R(im,x0,top+nh,1,ch,'white')
    poly(im,[(x0,top+nh),(x0+cw-1,top+nh),(x0+cw//2,top)],'red'); poly(im,[(x0+cw//2,top),(x0+cw-1,top+nh),(x0+cw//2,top+nh)],'maroon')
    R(im,x0,top+nh+2,cw,2,'red'); R(im,x0,top+nh+ch-5,cw,1,'g2')
    ell(im,[x0+cw//2-2,top+nh+7,x0+cw//2+1,top+nh+10],'blue'); Pt(im,x0+cw//2-1,top+nh+8,'white')
    R(im,x0+cw//4,top+nh+ch,cw-2*(cw//4),3,'g2'); R(im,x0+cw//4,top+nh+ch+3,cw-2*(cw//4),1,'g1')
    fx=3 if per_side==0 else 0
    poly(im,[(x0,top+nh+ch-9),(x0-3,top+nh+ch),(x0,top+nh+ch)],'red'); poly(im,[(x0+cw-1,top+nh+ch-9),(x0+cw+2,top+nh+ch),(x0+cw-1,top+nh+ch)],'maroon')
    return im
ROCKETS={'light':lambda:rocket(8,34,10),'medium':lambda:rocket(12,44,12),'heavy':lambda:rocket(12,50,12,1,6,34),'super_heavy':lambda:rocket(14,64,14,2,6,44)}
def flame(img,cx,y,ln,k=0):
    w=max(2,ln//3)
    poly(img,[(cx-w-1,y),(cx+w+1,y),(cx,y+ln)],'orange'); poly(img,[(cx-w+1,y),(cx+w-1,y),(cx,y+ln-3)],'gold'); poly(img,[(cx-1,y),(cx+1,y),(cx,y+max(2,ln//2))],'white')
def smoke(img,cx,y,r,lv):
    rnd=random.Random(5)
    for k in range(r):
        a=rnd.random()*6.28; d=rnd.random()*r*2
        x=int(cx+math.cos(a)*d*1.6); yy=int(y+abs(math.sin(a))*d*.5)
        s=rnd.choice([2,3,4]); ell(img,[x-s,yy-s,x+s,yy+s],'g5' if k%2 else 'g4')
def launch_sheet(kind):
    r=ROCKETS[kind](); FW=max(64,r.width+30); FH=r.height+110; base=FH-24
    frames=[]
    # idle x2, ignition x2, ascent x3, fade x1
    spec=[(0,0,0,0,16),(0,0,0,0,16),(0,5,6,0,16),(0,10,14,0,16),(14,18,0,0,16),(36,24,0,0,16),(62,26,0,0,12),(84,26,0,0,5)]
    for n,(rise,fl,sm,_,keep) in enumerate(spec):
        fr=new(FW,FH); y=base-r.height-rise
        if sm: smoke(fr,FW//2,base-2,sm//2,n)
        if fl: flame(fr,FW//2,y+r.height-1,fl,n)
        paste(fr,r,(FW-r.width)//2,y)
        if n==1: Pt(fr,FW//2,y+4,'red')
        if keep<16: fr=dither_mask(fr,keep)
        frames.append(fr)
    return strip(frames)
def craft(frame=0,k=1):
    im=new(48,48)
    R(im,10,23,3,2,'g3'); R(im,35,23,3,2,'g3')
    for x in (1,32):
        R(im,x,19,15,9,'blue_d'); R(im,x+1,20,13,7,'blue')
        for q in range(3,14,4): L(im,[(x+q,20),(x+q,26)],'blue_d')
        L(im,[(x+1,23),(x+13,23)],'blue_d'); R(im,x+1,20,13,1,'blue_l')
    R(im,17,15,14,17,'g4'); R(im,27,15,4,17,'g3'); R(im,17,15,14,2,'white'); R(im,17,22,14,3,'gold'); R(im,17,25,14,1,'rust')
    R(im,19,28,4,2,'ink'); Pt(im,20,28,'cyan')
    L(im,[(24,15),(24,11)],'g3'); poly(im,[(19,10),(29,10),(24,13)],'g5','g3'); Pt(im,24,9,'red')
    poly(im,[(20,32),(28,32),(26,36),(22,36)],'g2'); R(im,22,36,4,1,'g1')
    ln=[3,5,7,5][frame%4]
    poly(im,[(21,37),(27,37),(24,37+ln+2)],'blue_l'); poly(im,[(22,37),(26,37),(24,37+ln)],'cyan'); poly(im,[(23,37),(25,37),(24,37+max(2,ln-2))],'white')
    return im if k==1 else scale(im,k)
if __name__=='__main__':
    items=[body('earth',48),body('moon',40),ROCKETS['light'](),ROCKETS['medium'](),ROCKETS['heavy'](),ROCKETS['super_heavy'](),craft(0),craft(1)]
    preview(items,8,3,'sprites')
    preview([launch_sheet('medium')],1,2,'launch')
