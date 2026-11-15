from lib import *
from icons import I
import sprites as S
import math, random
def starfield(img,seed,n,ymax=H,big=0):
    r=random.Random(seed)
    for _ in range(n):
        x,y=r.randrange(img.width),r.randrange(ymax); c=r.choice(['white','lav','lav','pale','lav'])
        Pt(img,x,y,c)
        if big and r.random()<big and 1<x<img.width-2 and 1<y<img.height-2:
            for dx,dy in((1,0),(-1,0),(0,1),(0,-1)): Pt(img,x+dx,y+dy,'lav')
def space_bg(w=W,h=H):
    im=new(w,h)
    for y in range(h):
        for x in range(w):
            t=y/h+(S.bay(x,y)-.5)*.35; im.putpixel((x,y),P['ink'] if t<.45 else (P['navy1'] if t<.8 else P['navy2']))
    return im
def dashed(im,x,y,w,h,c,on=3,off=2):
    pts=[(x+i,y) for i in range(w)]+[(x+w-1,y+j) for j in range(1,h)]+[(x+w-2-i,y+h-1) for i in range(w-1)]+[(x,y+h-2-j) for j in range(h-2)]
    for n,(a,b) in enumerate(pts):
        if n%(on+off)<on: Pt(im,a,b,c)
def outline_chamfer(im,c):
    for x,y in((0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)): im.putpixel((x,y),T)
ALL={}   # relpath -> image
def out(rel,im): ALL[rel]=im; save(im,rel)
# =================== BUILD SCREEN ===================
bg=new(W,H,'navy1')
for x in range(0,W,16): L(bg,[(x,0),(x,H)],'navy2' if x%64 else 'navy3')
for y in range(0,H,16): L(bg,[(0,y),(W,y)],'navy2' if y%64 else 'navy3')
for y in range(0,H):
    for x in range(0,W):
        if (x%64==0 and y%64==0): R(bg,x-1,y-1,3,3,'peri')
R(bg,0,0,W,20,'navy2'); L(bg,[(0,20),(W,20)],'lav'); L(bg,[(0,21),(W,21)],'ink'); L(bg,[(0,0),(W,0)],'navy3')
R(bg,0,H-4,W,4,'navy2'); L(bg,[(0,H-5),(W,H-5)],'lav')
text(bg,8,7,'MISSION BUILDER','lav'); 
out('build/build_board_bg.png',bg)
SLOTS=[('mission','MISSION','mission'),('orbit','ORBIT','orbit'),('rocket','ROCKET','rocket'),('bus','BUS','spacecraft'),('power','POWER','spacecraft'),
       ('comms','COMMS','spacecraft'),('propulsion','PROP','spacecraft'),('instrument','INSTR.','instrument'),('support','SUPPORT','spacecraft')]
def slot(label,t,state):
    lt,bs,dk=TYPES[t]; im=new(64,96); R(im,0,0,64,96,'navy1'); outline_chamfer(im,None)
    if state=='empty':
        dashed(im,0,0,64,96,bs); dashed(im,1,1,62,94,dk)
        R(im,28,44,8,2,'navy3'); R(im,31,41,2,8,'navy3')
    elif state=='valid':
        for y in range(96):
            for x in range(64):
                if (x+y)%2==0 and 2<=x<62 and 2<=y<94: im.putpixel((x,y),P['green_d'])
        O(im,0,0,64,96,'green_l',2)
        poly(im,[(32,60),(24,50),(29,50),(29,40),(35,40),(35,50),(40,50)],'green_l','white')
        for x,y in((0,0),(63,0),(0,95),(63,95)): im.putpixel((x,y),T)
    else:
        for y in range(96):
            for x in range(64):
                if (x+y)%4==0 and 2<=x<62 and 2<=y<94: im.putpixel((x,y),P['maroon'])
        dashed(im,0,0,64,96,'red',2,2); dashed(im,1,1,62,94,'red',2,2)
        L(im,[(24,40),(40,56)],'red',3); L(im,[(40,40),(24,56)],'red',3)
    R(im,2,3,60,10,'navy2' if state=='empty' else ('green_d' if state=='valid' else 'maroon')); text_c(im,32,5,label,lt if state=='empty' else 'white')
    return im
slots_prev=[]
for name,label,t in SLOTS:
    sh=strip([slot(label,t,s) for s in ('empty','valid','invalid')],2); out(f'build/slot_{name}_3states.png',sh); slots_prev.append(sh)
# catalog panel + tabs
TAB=[('mission','M'),('orbit','O'),('rocket','R'),('spacecraft','S'),('instrument','I'),('event','E')]
def tab(t,letter,active):
    lt,bs,dk=TYPES[t]; im=new(23,14)
    if active:
        R(im,0,0,23,14,bs); R(im,1,1,21,13,bs); L(im,[(1,1),(21,1)],lt); text_c(im,11,4,letter,'ink')
    else:
        R(im,0,2,23,12,dk); R(im,1,3,21,11,'navy2'); L(im,[(1,3),(21,3)],'navy3'); R(im,1,3,21,2,bs); text_c(im,11,6,letter,lt)
    for x,y in((0,0 if active else 2),(22,0 if active else 2)): im.putpixel((x,y),T)
    return im
tabs_a=strip([tab(t,l,True) for t,l in TAB],0); tabs_i=strip([tab(t,l,False) for t,l in TAB],0)
out('build/catalog_tabs_active.png',tabs_a); out('build/catalog_tabs_inactive.png',tabs_i)
cat=panel(140,230); R(cat,2,17,136,211,'navy2'); L(cat,[(2,16),(137,16)],'lav')
paste(cat,tabs_a.crop((0,0,23,14)),2,2)
for k in range(1,6): paste(cat,tabs_i.crop((k*23,0,k*23+23,14)),2+k*23,2)
# list rows placeholders
for k in range(5): 
    y=21+k*40; R(cat,5,y,120,36,'navy1'); O(cat,5,y,120,36,'navy3'); R(cat,8,y+4,28,28,'ink')
R(cat,130,18,7,209,'navy1'); R(cat,131,20,5,40,'lav')   # scrollbar
out('build/catalog_panel.png',cat)
# gauges
def gauge_frame(icon):
    im=new(120,14); R(im,0,0,120,14,'g1'); R(im,1,1,118,12,'navy2'); R(im,1,1,14,12,'navy1'); paste(im,icon,4,3)
    for k in range(17): R(im,16+k*6,3,5,8,'navy1')
    x=16+int(.8*101); R(im,x,0,1,14,'white'); poly(im,[(x-2,0),(x+2,0),(x,2)],'white')
    return im
def seg(state):
    t=new(5,8)
    if state=='empty': R(t,0,0,5,8,'navy1'); L(t,[(0,0),(4,0)],'navy3')
    elif state=='green': R(t,0,0,5,8,'green'); R(t,0,0,5,1,'green_l'); R(t,0,7,5,1,'green_d')
    elif state=='yellow':
        R(t,0,0,5,8,'gold'); R(t,0,0,5,1,'pale'); R(t,0,7,5,1,'rust'); R(t,1,3,3,2,'rust')
    elif state=='red':
        R(t,0,0,5,8,'red'); R(t,0,7,5,1,'maroon')
        for k in range(-3,5): Pt(t,k+3,k+3,'maroon'); Pt(t,k+4,k+3,'maroon') if False else None
        for k in range(0,8,3): L(t,[(0,k),(4,k-4)],'maroon') if False else None
        L(t,[(0,5),(4,1)],'maroon'); L(t,[(0,2),(2,0)],'maroon'); L(t,[(2,7),(4,5)],'maroon')
    else: R(t,0,0,5,8,'white')
    return t
segs=strip([seg(s) for s in('empty','green','yellow','red','flash')],1); out('build/gauge_segment_tiles.png',segs)
demo=[]
for name,icon,cnt,state in (('cost','mini_cost',8,'green'),('mass','mini_mass',15,'yellow'),('power','mini_power',17,'red'),('data','mini_data',5,'green')):
    g=gauge_frame(I[icon]); out(f'build/gauge_frame_{name}.png',g)
    d=g.copy()
    for k in range(cnt): paste(d,seg(state),16+k*6,3)
    demo.append(d)
out('build/gauge_examples.png',vstrip(demo,2))
fl=[]
for ph in (0,1):
    g=gauge_frame(I['mini_power']); 
    if ph==0: O(g,0,0,120,14,'red'); [paste(g,seg('red'),16+k*6,3) for k in range(17)]
    else: O(g,0,0,120,14,'maroon'); [paste(g,seg('flash'),16+k*6,3) for k in range(17)]
    fl.append(g)
out('build/gauge_overlimit_flash_2f.png',vstrip(fl,2))
# briefing panel
br=panel(200,80); header(br,'MISSION BRIEF','gold','ink')
for k,l in enumerate(('OBJECTIVE','BUDGET CAP','SCI. TARGET','PRIORITY TAGS')):
    y=17+k*14; text(br,7,y+2,l,'lav'); R(br,88,y,105,11,'navy2'); O(br,88,y,105,11,'navy3')
for k in range(3): O(br,90+k*18,y+2,16,8,'g1') if False else None
out('build/mission_briefing_panel.png',br)
# launch check
lc=panel(140,100); header(lc,'LAUNCH CHECK','teal','white')
for k,(l,ic) in enumerate((('COST','mini_cost'),('MASS','mini_mass'),('POWER','mini_power'),('DATA','mini_data'),('COMPAT.',None))):
    y=17+k*16; R(lc,3,y,134,14,'navy2'); L(lc,[(3,y+14),(136,y+14)],'navy1')
    if ic: paste(lc,I[ic],6,y+3)
    else: R(lc,7,y+4,6,6,'peri'); O(lc,7,y+4,6,6,'lav')
    text(lc,19,y+4,l,'ice'); R(lc,118,y+1,16,12,'ink'); O(lc,118,y+1,16,12,'g1')
out('build/launch_check_panel.png',lc)
lb=strip([button(80,24,s,('LAUNCH',),'go') for s in ('disabled','default','hover','pressed')],2); out('build/launch_button_4states.png',lb)
cs=S.craft(0,2); out('build/spacecraft_preview_static_96.png',cs)
# =================== FLIGHT SCREEN ===================
out('flight/body_earth_128.png',S.body('earth',60)); out('flight/body_moon_96.png',S.body('moon',44))
out('flight/body_mars_96.png',S.body('mars',44)); out('flight/body_asteroid_64.png',S.body('asteroid',28))
for k in S.ROCKETS: out(f'flight/sprite_rocket_{k}.png',S.ROCKETS[k]())
for k in S.ROCKETS: out(f'flight/launch_anim_{k}_8f.png',S.launch_sheet(k))
out('flight/craft_flight_idle_4f.png',strip([S.craft(f) for f in range(4)]))
def tracker(lit):
    im=new(300,20); L(im,[(10,9),(290,9)],'g1',2); 
    names=['stage_launch','stage_cruise','stage_orbit_insertion','stage_science_ops_1','stage_science_ops_2','stage_science_ops_3']
    for k,n in enumerate(names):
        ic=I[n] if lit else dim(I[n]); x=2+k*56
        if lit: L(im,[(10,9),(x+8,9)],'cyan',2)
        paste(im,ic,x,2)
    return im
out('flight/stage_tracker_pending.png',tracker(False)); out('flight/stage_tracker_lit.png',tracker(True))
m=new(8,8); poly(m,[(0,0),(7,0),(3,5)],'gold','rust'); R(m,3,6,2,2,'gold'); out('flight/stage_marker_8.png',m)
out('flight/stage_icons_lit_6f.png',strip([I[n] for n in ['stage_launch','stage_cruise','stage_orbit_insertion','stage_science_ops_1','stage_science_ops_2','stage_science_ops_3']],0))
ev=panel(200,140); header(ev,'EVENT','magenta','white'); dashed(ev,8,20,64,96,'magenta')
text(ev,80,22,'DIFFICULTY','lav'); R(ev,80,32,32,14,'navy2'); O(ev,80,32,32,14,'navy3')
text(ev,80,52,'COUNTER TAG','lav'); R(ev,80,62,18,10,'navy2'); O(ev,80,62,18,10,'navy3'); R(ev,100,62,18,10,'navy2'); O(ev,100,62,18,10,'navy3')
R(ev,80,80,114,52,'navy2'); O(ev,80,80,114,52,'navy3'); text(ev,8,122,'EVENT CARD','peri')
out('flight/event_reveal_panel.png',ev)
od=panel(140,60); header(od,'ROLL ODDS','navy3','white',9)
R(od,6,16,50,38,'ink'); O(od,6,16,50,38,'navy3'); text_c(od,31,28,'--%','gold',2)
for k,l in enumerate(('MARGIN','TAG +','RESPONSE')):
    y=16+k*13; text(od,62,y+2,l,'lav'); R(od,112,y,22,10,'navy2'); O(od,112,y,22,10,'navy3')
out('flight/odds_panel.png',od)
RESP=[('safe_mode',('SAFE','MODE'),'primary'),('spend_contingency',('SPEND','CONTINGENCY'),'gold'),('throttle_data',('THROTTLE','DATA'),'teal')]
for n,lines,st in RESP: out(f'flight/response_button_{n}_4states.png',strip([button(80,24,s,lines,st) for s in ('default','hover','disabled','pressed')],2))
ins=['instr_wide_camera','instr_hires_imager','instr_thermal_ir','instr_spectrometer','instr_radar_sounder','instr_neutron_detector','instr_laser_altimeter','instr_magnetometer']
def status(n,state):
    g=I[n].copy()
    if state=='online': R(g,13,13,3,3,'green_l'); O(g,13,13,3,3,'green_d')
    elif state=='offline':
        g=dim(g); L(g,[(1,1),(14,14)],'g4'); L(g,[(14,1),(1,14)],'g4')
    else:
        g=dither_mask(dim(g),7)
        for x,y in((7,0),(6,3),(8,6),(6,9),(9,12),(8,15)): R(g,x,y,2,1,'red')
        R(g,13,13,3,3,'red')
    return g
out('flight/instrument_status_sheet_8x3.png',vstrip([strip([status(n,s) for s in ('online','offline','lost')]) for n in ins]))
out('flight/instrument_glyphs_8.png',strip([I[n] for n in ins]))
lm=panel(220,60); R(lm,5,6,50,48,'ink'); O(lm,5,6,50,48,'g1'); R(lm,7,8,46,44,'navy2')
text(lm,62,7,'DID YOU KNOW?','cyan'); R(lm,62,18,152,36,'navy2'); O(lm,62,18,152,36,'navy3')
out('flight/learning_moment_box.png',lm)
sc=panel(100,20); paste(sc,I['mini_science'],4,6); R(sc,15,6,60,8,'ink'); O(sc,15,6,60,8,'g1'); R(sc,78,5,19,10,'ink'); O(sc,78,5,19,10,'navy3')
out('flight/science_counter_frame.png',sc)
scd=sc.copy(); 
for k in range(5): R(scd,16+k*10,7,9,6,'green'); R(scd,16+k*10,7,9,1,'green_l')
out('flight/science_counter_demo.png',scd)
def portrait(mood):
    im=new(48,48); R(im,8,38,32,10,'blue'); R(im,8,38,32,2,'blue_l'); R(im,20,32,8,7,'salmon')
    ell(im,[12,5,35,22],'g0'); ell(im,[13,10,34,36],'orange','rust'); R(im,13,10,22,6,'g0'); ell(im,[13,6,34,18],'g0')
    ell(im,[14,12,33,35],'orange'); R(im,14,12,20,5,'g0'); L(im,[(15,18),(32,18)],'orange')
    arc(im,[10,3,37,30],200,340,'lav',2); R(im,8,20,4,9,'lav'); R(im,9,21,2,7,'peri'); L(im,[(11,28),(18,33)],'lav'); R(im,18,33,3,2,'gold')
    R(im,19,22,2,3,'ink'); R(im,28,22,2,3,'ink')
    if mood=='neutral': L(im,[(18,19),(21,19)],'g0',1); L(im,[(27,19),(30,19)],'g0'); R(im,22,30,5,1,'rust')
    elif mood=='worried':
        L(im,[(18,20),(21,18)],'g0'); L(im,[(30,20),(27,18)],'g0'); arc(im,[21,29,28,34],200,340,'rust'); R(im,34,14,2,3,'cyan'); Pt(im,35,13,'cyan')
    else:
        L(im,[(18,19),(21,18)],'g0'); L(im,[(27,18),(30,19)],'g0'); arc(im,[20,25,29,33],20,160,'rust',2); R(im,16,26,2,1,'salmon'); R(im,31,26,2,1,'salmon')
    return im
out('flight/mission_control_portrait_3f.png',strip([portrait(m) for m in ('neutral','worried','happy')]))
# =================== REPORT SCREEN ===================
rp=new(W,H,'navy1')
for y in range(0,H,2):
    for x in range(0,W,2):
        if (x//2+y//2)%2==0: Pt(rp,x,y,'navy2')
R(rp,0,0,W,20,'navy3'); L(rp,[(0,20),(W,20)],'lav'); text(rp,8,6,'MISSION REPORT','white')
sp=panel(150,80); header(sp,'TOTAL SCORE','gold','ink'); R(sp,6,17,90,58,'ink'); O(sp,6,17,90,58,'navy3'); R(sp,102,22,34,34,'navy2'); O(sp,102,22,34,34,'peri'); text_c(sp,119,60,'RANK','lav')
paste(rp,sp,8,26)
bp=panel(306,80); header(bp,'BREAKDOWN','navy3','white')
for k,l in enumerate(('SCIENCE','RESILIENCE','BUDGET','MARGIN')):
    y=17+k*15; text(bp,8,y+2,l,'ice'); R(bp,86,y,180,10,'ink'); O(bp,86,y,180,10,'g1'); R(bp,272,y,28,10,'navy2'); O(bp,272,y,28,10,'navy3')
paste(rp,bp,166,26)
for k,(t,c,ic) in enumerate((('HELPED','green','report_helped'),('HURT','red','report_hurt'),('WHAT-IF','blue','report_whatif'))):
    p=panel(152,118); header(p,'',c,'white',14); text(p,22,6,t,'white'); R(p,4,19,144,95,'navy2'); O(p,4,19,144,95,'navy1')
    for q in range(5): L(p,[(8,32+q*18),(144,32+q*18)],'navy3')
    paste(rp,p,8+k*156,112)
out('report/report_panel_layout.png',rp)
def ric(kind):
    i=mk=new(16,16)
    if kind=='helped': ell(i,[0,0,15,15],'green_d','green_l'); ell(i,[1,1,14,14],'green'); poly(i,[(8,3),(13,9),(10,9),(10,13),(6,13),(6,9),(3,9)],'white')
    elif kind=='hurt': ell(i,[0,0,15,15],'maroon','salmon'); ell(i,[1,1,14,14],'red'); poly(i,[(8,13),(13,7),(10,7),(10,3),(6,3),(6,7),(3,7)],'white')
    else: ell(i,[0,0,15,15],'blue_d','cyan'); ell(i,[1,1,14,14],'blue'); text(i,5,4,'?','white')
    return i
RI={k:ric(k) for k in('helped','hurt','whatif')}
for k,v in RI.items(): out(f'report/report_icon_{k}.png',v); I['report_'+k]=v
for k,(t,c,ic) in enumerate((('HELPED','green','report_helped'),('HURT','red','report_hurt'),('WHAT-IF','blue','report_whatif'))): paste(rp,RI[ic.split('_')[1]],8+k*156+3,112+3)
out('report/report_panel_layout.png',rp)
def star(cx,cy,ro,ri): return S.__dict__.get('x') or None
def star_pts(cx,cy,ro,ri,n=5,rot=-90):
    pts=[]
    for k in range(n*2):
        r=ro if k%2==0 else ri; a=math.radians(rot+k*180/n); pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return pts
def emblem(n):
    i=new(32,32)
    if n==0:
        ell(i,[1,1,30,30],'g1','g3'); ell(i,[4,4,27,27],'g0'); L(i,[(10,10),(21,21)],'red',3); L(i,[(21,10),(10,21)],'red',3)
        for a in(40,150,260): ImageDraw.Draw(i).arc([1,1,30,30],a,a+25,fill=P['ink'],width=2)
    elif n==1:
        poly(i,[(9,1),(22,1),(30,16),(22,30),(9,30),(1,16)],'maroon','salmon'); poly(i,[(10,4),(21,4),(27,16),(21,27),(10,27),(4,16)],'red'); poly(i,[(16,24),(24,13),(19,13),(19,7),(13,7),(13,13),(8,13)],'white')
    elif n==2:
        poly(i,[(16,1),(30,16),(16,31),(2,16)],'rust','gold'); poly(i,[(16,5),(26,16),(16,27),(6,16)],'gold')
        poly(i,[(16,5),(16,27),(6,16)],'orange'); text_c(i,16,12,'1/2','ink')
    elif n==3:
        poly(i,[(3,3),(16,0),(29,3),(29,17),(16,31),(3,17)],'green_d','green_l'); poly(i,[(6,6),(16,3),(26,6),(26,16),(16,27),(6,16)],'green'); L(i,[(10,14),(14,19),(23,9)],'white',3)
    else:
        for k in range(8):
            a=math.radians(k*45); L(i,[(16+math.cos(a)*12,16+math.sin(a)*12),(16+math.cos(a)*15.5,16+math.sin(a)*15.5)],'pale',2)
        poly(i,star_pts(16,16,13,6),'rust'); poly(i,star_pts(16,16,11,5),'gold'); poly(i,star_pts(16,15,6,3),'pale')
        for x,y in((2,3),(29,5),(3,28),(28,27)): R(i,x,y,2,2,'white')
    return i
EM=[emblem(n) for n in range(5)]
for n,e in zip(('mission_lost','failed','partial_success','success','outstanding'),EM): out(f'report/rank_{n}.png',e)
def badge(kind):
    i=new(24,24); ring={'frugal':('rust','gold'),'minimal':('navy3','teal'),'closecall':('green_d','green'),'odds':('maroon','purple')}[kind]
    ell(i,[0,0,23,23],ring[0],'ink'); ell(i,[2,2,21,21],ring[1])
    if kind=='frugal': ell(i,[6,6,17,17],'gold','rust'); text(i,9,8,'$','rust')
    elif kind=='minimal': ell(i,[9,9,14,14],'white','ice'); ell(i,[4,4,19,19],None,'teal') if False else None
    elif kind=='closecall': L(i,[(7,12),(11,16),(17,8)],'white',2); ell(i,[4,4,19,19],None,'green_l')
    else: R(i,7,7,10,10,'white'); O(i,7,7,10,10,'ice'); R(i,9,9,2,2,'ink'); R(i,13,13,2,2,'ink'); R(i,13,9,2,2,'ink') if False else None; poly(i,star_pts(18,6,4,2),'gold') 
    return i
BD=[badge(k) for k in('frugal','minimal','closecall','odds')]
for n,b in zip(('frugal_explorer','minimalist','no_close_calls','against_the_odds'),BD): out(f'report/badge_{n}.png',b)
out('report/report_buttons_replay_menu.png',vstrip([strip([button(96,24,s,('REPLAY','MISSION') if False else ('REPLAY MISSION',),'primary') for s in('default','hover','pressed','disabled')],2),strip([button(96,24,s,('MAIN MENU',),'secondary') for s in('default','hover','pressed','disabled')],2)],2))
# =================== GENERAL UI ===================
logo=new(200,60)
def logo_text(img,s,y,k,c1,c2):
    x=(200-tw(s,k))//2
    for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1),(0,2),(1,2),(-1,2)): text(img,x+dx,y+dy,s,'ink',k)
    text(img,x,y,s,c1,k)
    ImageDraw.Draw(img)
    for yy in range(y+k*4,y+k*7):
        for xx in range(x,x+tw(s,k)):
            if 0<=xx<200 and 0<=yy<60 and img.getpixel((xx,yy))==P[c1]: img.putpixel((xx,yy),P[c2])
logo_text(logo,'MISSION',4,4,'pale','gold'); logo_text(logo,'ARCHITECT',36,2,'cyan','blue_l')
for x,y in((6,10),(190,8),(8,44),(188,46)): R(logo,x,y,2,2,'white'); R(logo,x-1,y,4,2,'white') if False else None
out('general/logo_placeholder_200x60.png',logo)
tb=space_bg(); starfield(tb,11,240,H,0.04); pl=S.body('earth',150); paste(tb,pl,-60,150)
rk=S.ROCKETS['medium']()
for y in range(150,H):
    t=(y-150)/(H-150); w=int(3+t*12)
    for xx in range(-w,w+1):
        if S.bay(xx+370,y)<(1-t)*0.95: Pt(tb,370+xx,y,'orange' if (abs(xx)<w//3+1 and t<.45) else ('salmon' if t<.7 else 'g2'))
S.flame(tb,370,142,22); paste(tb,scale(rk,2),370-rk.width,142-rk.height*2)
out('general/title_screen_bg.png',tb)
f=new(W,H); starfield(f,21,80,H); out('general/title_stars_far.png',f)
n=new(W,H); r_=random.Random(22)
for _ in range(30):
    x,y=r_.randrange(W),r_.randrange(H); R(n,x,y,2,2,'white' if r_.random()<.5 else 'pale')
out('general/title_stars_near.png',n)
MODES=[('LEARNING','green',1,'book'),('STANDARD','blue',2,'rocket'),('CHALLENGE','red',3,'flame')]
mc=[]
for name,c,pips,ic in MODES:
    p=panel(96,128); header(p,'',c,'white',14); text_c(p,48,6,name,'white')
    big=new(32,32)
    if ic=='book': poly(big,[(2,8),(15,10),(15,28),(2,26)],'ice','lav'); poly(big,[(29,8),(16,10),(16,28),(29,26)],'mist','lav'); L(big,[(5,13),(12,15)],'blue'); L(big,[(5,18),(12,20)],'blue'); L(big,[(26,13),(19,15)],'blue'); L(big,[(26,18),(19,20)],'blue'); R(big,15,9,2,19,'rust')
    elif ic=='rocket': big=scale(I['stage_launch'],2)
    else: poly(big,[(16,2),(24,12),(28,20),(24,29),(16,31),(8,29),(4,20),(9,12),(12,17)],'red','maroon'); poly(big,[(16,10),(22,20),(20,28),(16,30),(12,28),(10,20)],'orange'); poly(big,[(16,18),(19,24),(16,29),(13,24)],'gold')
    paste(p,big,32,20)
    for q in range(3): 
        poly(p,[(float(x),float(y)) for x,y in star_pts(30+q*18,66,6,3)],'gold' if q<pips else 'navy3','rust' if q<pips else 'g1')
    R(p,6,76,84,46,'navy2'); O(p,6,76,84,46,'navy3'); out(f'general/mode_card_{name.lower()}.png',p); mc.append(p)
btn=[]
for st,lab in (('primary','BUTTON'),('secondary','BUTTON')):
    s=strip([button(80,24,x,(lab,),st) for x in ('default','hover','pressed','disabled')],2); out(f'general/button_{st}_4states.png',s); btn.append(s)
out('general/panel_9slice_72x72_corner24.png',panel(72,72))
w9=panel(96,72); R(w9,2,2,92,14,'navy3'); L(w9,[(2,2),(93,2)],'peri'); L(w9,[(2,16),(93,16)],'ink'); 
for k in range(3): R(w9,84-k*7,6,5,5,'lav'); R(w9,85-k*7,7,3,3,'navy2')
out('general/window_9slice_96x72_corner24.png',w9)
out('general/tooltip_9slice_48x48_corner8.png',panel(48,48,'ink','lav','navy2','ink'))
mo=panel(96,96); O(mo,0,0,96,96,'lav'); R(mo,1,1,94,94,'navy3'); R(mo,2,2,92,92,'navy1'); R(mo,3,3,90,90,'navy2'); L(mo,[(3,3),(92,3)],'navy3'); 
for x,y in((0,0),(95,0),(0,95),(95,95)): mo.putpixel((x,y),T)
out('general/modal_9slice_96x96_corner16.png',mo)
ar=[]
for dy in (0,2):
    a=new(16,16); poly(a,[(8,12+dy),(2,5+dy),(6,5+dy),(6,1+dy),(10,1+dy),(10,5+dy),(14,5+dy)],'gold','rust'); ar.append(a)
out('general/tutorial_arrow_2f.png',strip(ar))
hl=[]
for c1,c2 in (('gold','white'),('rust','gold')):
    h_=new(16,16); O(h_,0,0,16,16,c1,2); O(h_,2,2,12,12,c2) if c2=='white' else None; hl.append(h_)
out('general/tutorial_highlight_2f_9slice.png',strip(hl))
cur=[]
for name,rows in (('arrow',["k...............","kk..............","kwk.............","kwwk............","kwwwk...........","kwwwwk..........","kwwwwwk.........","kwwwwwwk........","kwwwwwwwk.......","kwwwwwkkkk......","kwwkwwk.........","kwk.kwwk........","kk..kwwk........","k....kwwk.......",".....kwwk.......","......kk........"]),
 ('hand',[".....kk.........","....kwwk........","....kwwk........","....kwwk........","....kwwkkk......","....kwwkwwkkk...",".kk.kwwkwwkwwk..","kwwkkwwwwwwwwwk.","kwwwkwwwwwwwwwk.",".kwwwwwwwwwwwwk.","..kwwwwwwwwwwwk.","..kwwwwwwwwwwk..","...kwwwwwwwwwk..","...kwwwwwwwwk...","....kwwwwwwwk...","....kkkkkkkkk..."]),
 ('grab',["................","................","....kk.kk.kk....","...kwwkwwkwwk...","...kwwkwwkwwkk..","..kkwwwwwwwwwwk.",".kwwkwwwwwwwwwk.",".kwwwwwwwwwwwwk.","..kwwwwwwwwwwwk.","..kwwwwwwwwwwwk.","...kwwwwwwwwwk..","...kwwwwwwwwwk..","....kwwwwwwwk...","....kkkkkkkkk...","................","................"])):
    c=ascii_img(rows,dict(k='ink',w='white')); out(f'general/cursor_{name}.png',c); cur.append(c)
tog=[]
for on in (False,True):
    t=new(24,12); R(t,0,0,24,12,'g3' if not on else 'green_l'); R(t,1,1,22,10,'g1' if not on else 'green_d')
    kx=2 if not on else 13; R(t,kx,2,9,8,'g4' if not on else 'white')
    if on: L(t,[(4,6),(5,7)],'green_d') if False else None; L(t,[(15,6),(16,8),(19,4)],'green_d')
    else: Pt(t,5,5,'g2'); Pt(t,6,6,'g2'); Pt(t,5,6,'g2')
    for x,y in((0,0),(23,0),(0,11),(23,11)): t.putpixel((x,y),T)
    out(f'general/toggle_{"on" if on else "off"}.png',t); tog.append(t)
sb=new(8,32); R(sb,0,0,8,32,'g1'); R(sb,1,1,6,30,'navy1'); out('general/scrollbar_track_8x32_vertical.png',sb)
th=new(8,16); R(th,0,0,8,16,'peri'); R(th,1,1,6,14,'lav'); R(th,1,1,6,1,'white'); R(th,3,6,2,1,'peri'); R(th,3,8,2,1,'peri'); R(th,3,10,2,1,'peri'); out('general/scrollbar_thumb_8x16.png',th)
pf=new(100,8); R(pf,0,0,100,8,'g1'); R(pf,1,1,98,6,'ink'); out('general/progress_bar_frame_100x8.png',pf)
pt=new(4,6); R(pt,0,0,4,6,'green'); R(pt,0,0,4,1,'green_l'); Pt(pt,1,3,'green_d'); Pt(pt,3,4,'green_d'); out('general/progress_bar_fill_tile_4x6.png',pt)
spin=[]
for f_ in range(8):
    s=new(16,16)
    for k in range(8):
        a=math.radians(k*45-90); x=int(round(7+math.cos(a)*5.5)); y=int(round(7+math.sin(a)*5.5)); d=(f_-k)%8
        c=['white','cyan','lav','peri','navy3','navy3','navy3','navy3'][d]; R(s,x,y,2,2,c)
    spin.append(s)
out('general/spinner_8f.png',strip(spin))
if __name__=='__main__':
    preview(slots_prev[:3]+[cat,br,lc,lb,segs,vstrip(demo,2),vstrip(fl,2)],3,2,'build')
    preview([tracker(False),tracker(True),ev,od,lm,sc,scd,strip([portrait(m) for m in('neutral','worried','happy')]),strip([status(n,s) for n in ins[:4] for s in('online','offline','lost')])]+[strip([button(80,24,s,l,st) for s in('default','hover','disabled','pressed')],2) for _,l,st in RESP],3,2,'flight')
    preview([rp]+EM+BD+list(RI.values())+mc+[logo,tb]+btn+cur+tog+[mo,w9]+ar+hl+[spin[0],spin[3]],4,2,'general')
    print(len(ALL))
