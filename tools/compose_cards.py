"""Put your 56x48 illustrations under the card frames.
usage: python compose_cards.py <illustrations_dir> <output_dir> [scale]
file name = card id, e.g. instr_radar_sounder.png  (prefix decides the frame)
"""
import sys, os
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__)); FR=os.path.join(HERE,'..','cards')
PREFIX=[('mission_','mission'),('orbit_','orbit'),('rocket_','rocket'),('bus_','spacecraft'),('power_','spacecraft'),('comms_','spacecraft'),
        ('prop_','spacecraft'),('support_','spacecraft'),('instr_','instrument'),('event_','event')]
src,dst=sys.argv[1],sys.argv[2]; k=int(sys.argv[3]) if len(sys.argv)>3 else 1
os.makedirs(dst,exist_ok=True)
for fn in sorted(os.listdir(src)):
    if not fn.endswith('.png'): continue
    t=next((t for p,t in PREFIX if fn.startswith(p)),None)
    if not t: print('skip',fn); continue
    art=Image.open(os.path.join(src,fn)).convert('RGBA')
    if art.size!=(56,48): print('WARNING',fn,'is',art.size,'(expected 56x48)')
    card=Image.new('RGBA',(64,96),(0,0,0,0)); card.paste(art,(4,13),art)
    frame=Image.open(os.path.join(FR,f'card_frame_{t}.png')).convert('RGBA'); card.alpha_composite(frame)
    if k>1: card=card.resize((64*k,96*k),Image.NEAREST)
    card.save(os.path.join(dst,fn.replace('.png','_card.png'))); print('ok',fn)
