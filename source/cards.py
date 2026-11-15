from lib import *
from icons import I
ART=(4,13,56,48)
def card_frame(t):
    lt,bs,dk=TYPES[t]
    im=new(64,96); R(im,0,0,64,96,dk); R(im,1,1,62,94,bs); R(im,2,2,60,92,'navy1')
    for x,y in((0,0),(63,0),(0,95),(63,95)): im.putpixel((x,y),T)
    L(im,[(1,1),(62,1)],lt); L(im,[(1,1),(1,94)],lt)
    R(im,2,2,60,10,bs); L(im,[(2,2),(61,2)],lt); R(im,2,11,60,1,dk)            # name bar
    R(im,3,12,58,50,'ink'); clear(im,*ART)                                       # art window (transparent hole)
    R(im,2,63,60,12,'navy2'); L(im,[(2,63),(61,63)],'navy3')                     # stat row
    for k in range(1,5): L(im,[(2+k*12,64),(2+k*12,74)],'navy1')
    R(im,2,76,60,8,'navy1'); 
    for x in range(3,61,2): Pt(im,x,76,'navy3')                                  # chip area guide
    R(im,2,85,60,9,'navy2'); L(im,[(2,85),(61,85)],'navy3')                      # flavor text area
    return im
def card_back():
    im=new(64,96); R(im,0,0,64,96,'maroon'); R(im,1,1,62,94,'magenta'); R(im,3,3,58,90,'navy1')
    for x,y in((0,0),(63,0),(0,95),(63,95)): im.putpixel((x,y),T)
    for y in range(4,92):
        for x in range(4,60):
            if (x+y)%8==0 or (x-y)%8==0: Pt(im,x,y,'navy2')
    ell(im,[20,32,43,63],'maroon'); ell(im,[21,33,42,62],'magenta'); ell(im,[23,35,40,60],'navy1')
    text_c(im,32,42,'?','white',3)
    for x,y in((6,6),(55,6),(6,87),(55,87)): R(im,x,y,3,3,'lav')
    return im
def st_hover():
    im=new(64,96); O(im,0,0,64,96,'cyan'); O(im,1,1,62,94,'white')
    for x,y in((0,0),(63,0),(0,95),(63,95)): im.putpixel((x,y),T)
    for k in (4,5,6): Pt(im,k,3,'white'); Pt(im,3,k,'white')
    return im
def st_selected():
    im=new(64,96); O(im,0,0,64,96,'gold',2); O(im,2,2,60,92,'white')
    for x,y in((0,0),(63,0),(0,95),(63,95),(1,0),(0,1),(62,0),(63,1),(0,94),(1,95),(63,94),(62,95)): im.putpixel((x,y),T)
    return im
def lock_icon():
    i=new(16,16); arc(i,[4,1,11,9],180,360,'g5',2); R(i,3,7,10,8,'g4'); R(i,3,7,10,1,'white'); R(i,3,14,10,1,'g2'); R(i,7,9,2,3,'ink'); R(i,7,12,2,1,'ink'); return i
def st_locked():
    im=new(64,96)
    for y in range(96):
        for x in range(64):
            if (x+y)%2==0: im.putpixel((x,y),P['ink'])
    R(im,22,36,20,24,'ink'); O(im,22,36,20,24,'g2'); paste(im,lock_icon(),24,40)
    return im
def st_over(frame):
    c1,c2=('red','white') if frame==0 else ('maroon','red')
    im=new(64,96); O(im,0,0,64,96,c1,2); O(im,2,2,60,92,c2) if frame==0 else None
    for x,y in((0,0),(63,0),(0,95),(63,95)): im.putpixel((x,y),T)
    return im
def st_over_sheet():
    a=st_over(0); b=st_over(1)
    for im,c in ((a,'red'),(b,'maroon')):
        poly(im,[(32,4),(36,12),(28,12)],c) if False else None
    # warning triangle with ! in corner for non-color cue
    for im,c in ((a,'red'),(b,'maroon')):
        R(im,48,4,12,11,'ink'); poly(im,[(54,5),(59,14),(49,14)],c); R(im,54,8,1,3,'white'); Pt(im,54,12,'white')
    return strip([a,b])
def st_placed():
    im=new(64,96)
    for y in range(96):
        for x in range(64):
            e=min(x,y,63-x,95-y)
            if e==0 and (x+y)%2==0: im.putpixel((x,y),P['ink'])
            elif e==1: im.putpixel((x,y),P['g0'])
    for x,y in((3,3),(58,3),(3,90),(58,90)): R(im,x,y,3,3,'lav'); Pt(im,x,y,'white')
    return im
def chip(hl=False):
    im=new(16,8); R(im,0,0,16,8,'gold' if hl else 'lav'); R(im,1,1,14,6,'navy3' if not hl else 'rust')
    for x,y in((0,0),(15,0),(0,7),(15,7)): im.putpixel((x,y),T)
    return im
def stat_row():
    im=new(64,12); R(im,0,0,64,12,'navy2'); L(im,[(0,0),(63,0)],'navy3')
    for k,n in enumerate(('cost','mass','power','data','science')):
        x=k*12 +1
        paste(im,I['mini_'+n],x,2)
        if k<4: L(im,[(k*12+11,1),(k*12+11,10)],'navy1')
    # number slots: icon (8) + 3px digit? row is 12 wide per stat: icon 8 + 3x5 digit fits at x+9? -> numbers drawn by engine below icon
    return im
if __name__=='__main__':
    out=[]
    for t in TYPES:
        f=card_frame(t); save(f,f'cards/card_frame_{t}.png'); out.append(f)
    b=card_back(); save(b,'cards/card_back.png'); out.append(b)
    for n,im in (('hover',st_hover()),('selected',st_selected()),('locked',st_locked()),('placed',st_placed())):
        save(im,f'cards/card_state_{n}.png'); out.append(im)
    s=st_over_sheet(); save(s,'cards/card_state_overlimit_2f.png'); out.append(s.crop((0,0,64,96)))
    save(strip([chip(False),chip(True)]),'cards/tag_chip_2states.png'); save(stat_row(),'cards/stat_row_template.png')
    preview(out,7,3,'cards',bg='g0')
