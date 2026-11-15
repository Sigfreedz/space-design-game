from lib import *
import math
I={}   # name -> image (16x16 unless noted)
def mk(): return new(16,16)
def star_pts(cx,cy,ro,ri,n=5,rot=-90):
    pts=[]
    for k in range(n*2):
        r=ro if k%2==0 else ri; a=math.radians(rot+k*180/n)
        pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    return pts
# ---------- stat icons
i=mk(); ell(i,[1,1,14,14],'rust'); ell(i,[2,2,13,13],'gold'); ell(i,[4,4,11,11],None,'pale'); text(i,5,4,'$','rust'); I['icon_cost']=i
i=mk(); R(i,6,1,4,1,'g4'); R(i,5,2,1,3,'g4'); R(i,10,2,1,3,'g4'); R(i,6,4,4,1,'g4')
poly(i,[(4,5),(11,5),(14,14),(1,14)],'g3'); R(i,3,5,9,2,'g4'); R(i,2,13,12,2,'g2'); I['icon_mass']=i
i=mk(); poly(i,[(10,0),(3,9),(7,9),(5,15),(13,6),(8,6),(12,0)],'gold','rust'); L(i,[(9,2),(5,8)],'pale'); I['icon_power']=i
i=mk(); R(i,1,14,14,1,'lav'); R(i,2,9,3,5,'blue_l'); R(i,6,5,3,9,'blue_l'); R(i,10,2,3,12,'blue_l')
for x,y in((2,9),(6,5),(10,2)): R(i,x,y,3,1,'cyan')
I['icon_data']=i
i=mk(); R(i,5,0,6,1,'g4'); R(i,6,1,4,5,'ice'); poly(i,[(6,6),(10,6),(14,14),(2,14)],'ice'); poly(i,[(4,10),(12,10),(14,14),(2,14)],'green_l')
R(i,2,14,13,1,'green_d'); Pt(i,7,8,'white'); Pt(i,9,7,'white'); I['icon_science']=i
i=mk(); poly(i,[(8,1),(15,14),(1,14)],None,'lav'); poly(i,[(8,3),(13,13),(3,13)],None,'navy3'); L(i,[(8,7),(8,12)],'cyan'); Pt(i,7,8,'cyan'); Pt(i,9,8,'cyan'); Pt(i,6,9,'cyan'); Pt(i,10,9,'cyan'); I['icon_delta_v']=i
i=mk(); poly(i,[(2,1),(8,0),(14,1),(14,8),(8,15),(2,8)],'blue','lav'); poly(i,[(4,3),(8,2),(12,3),(12,8),(8,13),(4,8)],'blue_d'); L(i,[(5,7),(7,10),(11,4)],'white',2); I['icon_reliability']=i
i=mk(); ell(i,[0,0,15,15],'gold','rust')
for a0 in (240,0,120): ImageDraw.Draw(i).pieslice([2,2,13,13],a0+0,a0+60,fill=P['ink'])
ell(i,[5,5,10,10],'gold'); ell(i,[6,6,9,9],'ink'); I['icon_radiation']=i
i=mk(); ell(i,[4,4,11,11],'gold','pale'); ell(i,[6,6,9,9],'pale')
for k in range(8):
    a=math.radians(k*45); L(i,[(7.5+math.cos(a)*5.5,7.5+math.sin(a)*5.5),(7.5+math.cos(a)*7.5,7.5+math.sin(a)*7.5)],'gold')
I['icon_sun']=i
i=mk(); R(i,2,12,2,2,'cyan')
for r,c in((4,'cyan'),(7,'blue_l'),(10,'lav')): arc(i,[3-r,13-r,3+r,13+r],270,360,c)
R(i,1,14,4,1,'g3'); I['icon_signal']=i
# ---------- tag icons
i=mk(); R(i,1,4,14,10,'g3'); R(i,5,2,6,2,'g3'); R(i,1,12,14,2,'g2'); ell(i,[4,5,11,12],'g1'); ell(i,[5,6,10,11],'blue'); Pt(i,6,7,'white'); Pt(i,13,5,'gold'); I['tag_imaging']=i
i=mk(); R(i,6,1,4,10,'ice'); ell(i,[4,9,11,15],'red'); R(i,7,4,2,8,'red'); R(i,6,1,1,1,'T') if False else None
for y in (2,4,6): Pt(i,11,y,'lav')
I['tag_thermal']=i
i=mk(); L(i,[(4,4),(12,4)],'g3'); L(i,[(4,4),(8,12)],'g3'); L(i,[(12,4),(8,12)],'g3')
ell(i,[1,1,6,6],'cyan','blue'); ell(i,[9,1,14,6],'green_l','green'); ell(i,[5,9,11,15],'salmon','red'); I['tag_composition']=i
i=mk(); R(i,0,1,16,3,'green'); R(i,0,4,16,4,'rust'); R(i,0,8,16,4,'g2'); R(i,0,12,16,3,'g1'); L(i,[(8,3),(8,14)],'cyan')
for x,y in((7,12),(9,12),(6,11),(10,11)): Pt(i,x,y,'cyan')
I['tag_subsurface']=i
i=mk(); poly(i,[(0,14),(5,4),(9,10),(12,6),(15,14)],'green_d','green'); poly(i,[(4,6),(5,4),(6,6)],'white'); poly(i,[(11,8),(12,6),(13,8)],'white'); R(i,0,14,16,1,'g1'); I['tag_topography']=i
i=mk(); R(i,2,2,3,10,'red'); R(i,10,2,3,10,'red'); R(i,3,11,9,3,'red'); R(i,5,10,5,1,'red'); R(i,2,2,3,3,'white'); R(i,10,2,3,3,'white'); R(i,2,5,3,1,'maroon'); R(i,10,5,3,1,'maroon'); R(i,3,13,9,1,'maroon'); Pt(i,3,14,T) if False else None; I['tag_fields']=i
i=mk(); poly(i,[(2,1),(8,0),(14,1),(14,8),(8,15),(2,8)],'g2','lav'); poly(i,[(9,3),(5,8),(8,8),(7,12),(11,6),(8,6)],'gold'); I['tag_rad_hardened']=i
i=mk(); R(i,1,1,9,9,'g3'); O(i,1,1,9,9,'lav'); R(i,6,6,9,9,'g4'); O(i,6,6,9,9,'white')
for k in (3,5,7): Pt(i,k,0,'gold'); Pt(i,0,k,'gold')
for k in (8,10,12): Pt(i,k,15,'gold'); Pt(i,15,k,'gold')
R(i,8,8,5,5,'g2'); I['tag_redundant']=i
i=mk(); poly(i,[(3,1),(12,1),(14,3),(14,15),(3,15)],'blue_d','lav'); R(i,5,2,1,3,'gold'); R(i,7,2,1,3,'gold'); R(i,9,2,1,3,'gold'); R(i,5,8,8,5,'blue_l'); R(i,5,8,8,1,'cyan'); I['tag_storage']=i
# ---------- margin tier icons (distinct shapes: square+check, diamond+dash, triangle+!)
i=mk(); R(i,1,1,14,14,'green_d'); R(i,2,2,12,12,'green'); L(i,[(4,8),(7,11),(12,4)],'white',2); I['tier_green']=i
i=mk(); poly(i,[(8,0),(15,8),(8,15),(1,8)],'gold','rust'); R(i,5,7,6,2,'ink'); I['tier_yellow']=i
i=mk(); poly(i,[(8,1),(15,14),(1,14)],'red','maroon'); R(i,7,5,2,5,'white'); R(i,7,11,2,2,'white'); I['tier_red']=i
# ---------- outcome icons 32x32 (circle+check, diamond+bar, octagon+X)
i=new(32,32); ell(i,[1,1,30,30],'green_d'); ell(i,[3,3,28,28],'green'); ell(i,[3,3,28,28],None,'green_l'); L(i,[(9,16),(14,22),(23,10)],'white',4); I['outcome_success']=i
i=new(32,32); poly(i,[(16,0),(31,16),(16,31),(0,16)],'rust'); poly(i,[(16,3),(28,16),(16,28),(4,16)],'gold'); R(i,9,14,14,4,'ink'); I['outcome_partial']=i
i=new(32,32); poly(i,[(10,0),(21,0),(31,10),(31,21),(21,31),(10,31),(0,21),(0,10)],'maroon'); poly(i,[(11,3),(20,3),(28,11),(28,20),(20,28),(11,28),(3,20),(3,11)],'red'); L(i,[(10,10),(21,21)],'white',4); L(i,[(21,10),(10,21)],'white',4); I['outcome_fail']=i
# ---------- response icons
i=mk(); ell(i,[0,0,15,15],'navy3','cyan'); R(i,5,4,2,8,'cyan'); R(i,9,4,2,8,'cyan'); I['resp_safe_mode']=i
i=mk(); ell(i,[0,0,11,11],'rust'); ell(i,[1,1,10,10],'gold'); text(i,3,2,'$','rust'); L(i,[(9,9),(14,14)],'white',2); Pt(i,14,10,'white'); Pt(i,10,14,'white'); R(i,13,13,2,2,'white'); I['resp_spend_contingency']=i
i=mk(); R(i,1,9,3,6,'teal'); R(i,5,6,3,9,'teal'); R(i,9,3,3,12,'teal'); L(i,[(13,1),(13,8)],'gold'); Pt(i,12,6,'gold'); Pt(i,14,6,'gold'); Pt(i,11,5,'gold'); Pt(i,15,5,'gold'); I['resp_throttle_data']=i
i=mk(); ell(i,[1,1,14,14],'g3','lav'); ell(i,[2,2,13,13],'g4'); ell(i,[4,4,11,11],None,'g2'); L(i,[(8,5),(8,10)],'g2'); L(i,[(6,8),(10,8)],'g2'); I['icon_contingency_coin']=i
# ---------- stage icons
def rocket_ic():
    i=mk(); poly(i,[(8,0),(11,4),(11,11),(5,11),(5,4)],'ice','g4'); poly(i,[(8,0),(10,3),(6,3)],'red'); ell(i,[7,5,9,7],'blue')
    poly(i,[(5,8),(2,12),(5,11)],'red'); poly(i,[(11,8),(14,12),(11,11)],'red'); poly(i,[(6,12),(10,12),(8,15)],'orange'); return i
I['stage_launch']=rocket_ic()
i=mk(); L(i,[(1,8),(10,8)],'lav',2); poly(i,[(10,3),(15,8),(10,13)],'cyan'); R(i,1,3,2,1,'g3'); R(i,4,12,2,1,'g3'); I['stage_cruise']=i
i=mk(); ell(i,[5,5,10,10],'blue_l'); ell(i,[0,3,15,12],None,'lav'); ell(i,[1,3,14,12],None,'lav'); R(i,12,4,2,2,'white'); I['stage_orbit_insertion']=i
for n in '123':
    i=mk(); L(i,[(1,1),(5,1)],'lav'); L(i,[(1,1),(1,5)],'lav'); L(i,[(10,1),(14,1)],'lav'); L(i,[(14,1),(14,5)],'lav')
    L(i,[(1,14),(5,14)],'lav'); L(i,[(1,10),(1,14)],'lav'); L(i,[(10,14),(14,14)],'lav'); L(i,[(14,10),(14,14)],'lav')
    ell(i,[4,3,11,10],'navy3','cyan'); R(i,7,5,2,3,'cyan'); digit3(i,6,10,n,'gold') if False else None
    digit3(i,6,9+0,n,'gold'); I['stage_science_ops_'+n]=i
# redraw sci ops so digit sits clean below lens
for n in '123':
    i=mk(); 
    for (a,b,c,d) in ((1,1,5,1),(1,1,1,5),(10,1,14,1),(14,1,14,5),(1,14,5,14),(1,10,1,14),(10,14,14,14),(14,10,14,14)): L(i,[(a,b),(c,d)],'lav')
    ell(i,[5,3,10,8],'navy3','cyan'); Pt(i,7,5,'white'); digit3(i,6,9,n,'gold'); I['stage_science_ops_'+n]=i
# ---------- instrument glyphs
g={}
i=mk(); R(i,5,9,6,5,'g3'); ell(i,[6,10,9,13],'blue'); L(i,[(8,8),(1,1)],'cyan'); L(i,[(8,8),(14,1)],'cyan'); L(i,[(1,1),(14,1)],'navy3'); g['instr_wide_camera']=i
i=mk(); R(i,2,6,10,4,'g3'); R(i,12,5,2,6,'g4'); R(i,2,6,10,1,'g4'); R(i,4,10,2,4,'g2'); L(i,[(14,8),(15,8)],'cyan'); g['instr_hires_imager']=i
i=mk(); R(i,1,8,7,6,'g3'); ell(i,[2,9,5,12],'g1'); 
for k,(x,y) in enumerate(((10,2),(12,5),(10,8),(12,11))): R(i,x,y,2,2,'orange' if k%2==0 else 'salmon')
g['instr_thermal_ir']=i
i=mk(); poly(i,[(7,3),(12,13),(2,13)],'ice','lav'); L(i,[(0,8),(5,8)],'white')
for k,c in enumerate(('red','orange','gold','green_l','blue_l')): L(i,[(10,5+k*2),(15,5+k*2)],c)
g['instr_spectrometer']=i
i=mk(); R(i,7,1,2,5,'g4'); poly(i,[(4,6),(11,6),(8,3)],'g3'); 
for r,c in((3,'cyan'),(5,'blue_l'),(7,'lav')): arc(i,[8-r,7-r+3,8+r,7+r+3],20,160,c)
R(i,6,0,4,1,'red'); R(i,0,14,16,1,'rust'); g['instr_radar_sounder']=i
i=mk(); R(i,6,6,9,8,'g3'); O(i,6,6,9,8,'g4')
for x,y in((1,7),(3,10),(2,12),(4,8)): Pt(i,x,y,'cyan')
L(i,[(0,7),(6,9)],'navy3'); g['instr_neutron_detector']=i
i=mk(); R(i,5,1,6,4,'g3'); R(i,7,5,2,1,'g1'); L(i,[(8,6),(8,13)],'red'); R(i,5,14,6,1,'rust'); Pt(i,8,13,'white'); g['instr_laser_altimeter']=i
i=mk(); R(i,10,10,5,5,'g3'); L(i,[(10,11),(2,3)],'g4',2); ell(i,[0,1,4,5],'cyan')
arc(i,[-2,-1,8,9],300,60,'lav'); arc(i,[-4,-3,10,11],300,60,'navy3'); g['instr_magnetometer']=i
I.update(g)
# ---------- 8x8 mini stat icons
def mini(rows,leg): return ascii_img(rows,leg)
M={}
M['cost']=mini(['..rrrr..','.rggggr.','rggppggr','rgpggggr','rggggpgr','rggppggr','.rggggr.','..rrrr..'],dict(r='rust',g='gold',p='pale'))
M['mass']=mini(['...hh...','..h..h..','.HHHHHH.','HhhhhhhH','HhhhhhhH','HhhhhhhH','HHHHHHHH','........'],dict(h='g3',H='g4'))
M['power']=mini(['.....pp.','....pg..','...pg...','..pgggg.','....pg..','...pg...','..pg....','..g.....'],dict(p='pale',g='gold'))
M['data']=mini(['......cc','......cc','...cc.cc','...cc.cc','cc.cc.cc','cc.cc.cc','cc.cc.cc','LLLLLLLL'],dict(c='blue_l',L='lav'))
M['science']=mini(['..wwww..','...ww...','...ww...','..wllw..','.wlllw..','.wllllw.','wllllllw','wwwwwwww'],dict(w='ice',l='green_l'))
for k,v in M.items(): I['mini_'+k]=v
if __name__=='__main__':
    for k,v in I.items(): save(v,f'icons/{k}.png')
    order=[k for k in I if k.startswith('icon_')]
    preview([I[k] for k in I if not k.startswith('mini_')],12,5,'icons')
    print(len(I))
