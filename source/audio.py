import numpy as np, wave, os
SR=22050; OUT='/mnt/user-data/outputs/assets/audio'; os.makedirs(OUT,exist_ok=True)
def t_(d): return np.arange(int(SR*d))/SR
def hz(m): return 440.0*2**((m-69)/12)
def sq(f,t,duty=.5): return np.where((f*t)%1<duty,1.0,-1.0)
def tri(f,t): return 2*np.abs(2*((f*t)%1)-1)-1
def saw(f,t): return 2*((f*t)%1)-1
def sine(f,t): return np.sin(2*np.pi*f*t)
def env(n,a=.005,r=.05,curve=1.0):
    e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,int(r*SR)); e[:na]=np.linspace(0,1,na); e[-nr:]*=np.linspace(1,0,nr)**curve; return e
def decay(n,k=6): return np.exp(-k*np.arange(n)/n)
def save(name,x,vol=.8):
    x=x/ (np.max(np.abs(x))+1e-9)*vol; d=(x*32767).astype('<i2')
    with wave.open(f'{OUT}/{name}.wav','wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
def cat(*a): return np.concatenate(a)
def gap(d): return np.zeros(int(SR*d))
def note(f,d,w=sq,v=.5,k=5,a=.003):
    t=t_(d); x=w(f,t)*v; return x*env(len(x),a,.02)*decay(len(x),k)
rnd=np.random.default_rng(1)
# SFX
save('sfx_ui_click',cat(note(1400,.03,sq,.6,3),note(900,.04,sq,.5,4)))
t=t_(.09); f=np.linspace(400,760,len(t)); save('sfx_card_pickup',np.sin(2*np.pi*np.cumsum(f)/SR)*env(len(t),.004,.03)*.7+tri(500,t)*.1)
t=t_(.12); f=np.linspace(180,70,len(t)); thud=np.sin(2*np.pi*np.cumsum(f)/SR)*decay(len(t),5); nz=rnd.uniform(-1,1,len(t))*decay(len(t),30)*.5; save('sfx_card_place',thud+nz)
t=t_(.28); save('sfx_invalid_buzz',sq(110,t)*(0.6+0.4*sq(22,t))*env(len(t),.004,.04)*.8)
save('sfx_warning_beep',cat(note(880,.11,sq,.6,1.5),gap(.06),note(880,.11,sq,.6,1.5),gap(.06),note(880,.11,sq,.6,1.5)))
d=3.0; t=t_(d); n=rnd.uniform(-1,1,len(t)); k=np.ones(48)/48; low=np.convolve(n,k,'same'); amp=np.minimum(1,t/1.2)*np.minimum(1,(d-t)/.8)
save('sfx_launch_rumble',(low*3+sine(48,t)*.6+sine(31,t)*.5)*amp)
save('sfx_event_alert',cat(note(hz(76),.13,tri,.8,3),note(hz(72),.13,tri,.8,3),note(hz(69),.2,tri,.8,4)))
mel=cat(note(hz(72),.1,sq,.5,3),note(hz(76),.1,sq,.5,3),note(hz(79),.1,sq,.5,3),note(hz(84),.45,sq,.5,2.5)); echo=np.zeros(len(mel)+3000); echo[:len(mel)]+=mel; echo[2200:2200+len(mel)]+=mel*.35; save('sfx_success_jingle',echo)
t=t_(.9); f=np.linspace(420,70,len(t)); x=(2*((np.cumsum(f)/SR)%1)-1)*decay(len(t),2.5)*.7+rnd.uniform(-1,1,len(t))*decay(len(t),6)*.25; save('sfx_fail_sound',x)
# Music (seamless: exact length)
def loop(bpm,bars,steps,name):
    spb=60/bpm; total=int(SR*spb*4*bars); out=np.zeros(total+SR); step=spb/2
    for i,fn in steps:
        s=int(SR*step*i); y=fn(); out[s:s+len(y)]+=y[:len(out)-s]
    x=out[:total]; tail=out[total:]; x[:len(tail)]+=tail[:len(x)]; save(name,x,.6)
chords=[(57,60,64),(53,57,60),(48,52,55),(55,59,62)]
def calm():
    steps=[]
    for bar in range(8):
        ch=chords[bar%4]
        for k in range(8):
            m=ch[[0,1,2,1,0,2,1,2][k]]+12
            steps.append((bar*8+k,lambda m=m: note(hz(m),.5,tri,.35,3.5,.01)))
        steps.append((bar*8,lambda c=ch: note(hz(c[0]-12),1.6,sine,.5,2.0,.05)+note(hz(c[1]),1.6,sine,.18,2.0,.08)))
        steps.append((bar*8+4,lambda c=ch: note(hz(c[0]-12),1.6,sine,.45,2.0,.05)))
    return steps
loop(90,8,calm(),'music_build_calm_loop')
def tense():
    steps=[]
    for bar in range(8):
        for k in range(8):
            steps.append((bar*8+k,lambda: note(hz(33),.22,sq,.55,5,.002)))
            if k%2==0: steps.append((bar*8+k,lambda: rnd.uniform(-1,1,int(SR*.03))*decay(int(SR*.03),12)*.5))
        if bar%2==0: steps.append((bar*8,lambda: note(hz(69),1.8,saw,.15,1.6,.1)+note(hz(70),1.8,saw,.12,1.6,.1)))
        else: steps.append((bar*8,lambda: note(hz(64),1.8,saw,.15,1.6,.1)+note(hz(65),1.8,saw,.12,1.6,.1)))
        if bar==7: steps.append((bar*8+6,lambda: note(hz(81),.2,sq,.3,4)))
    return steps
loop(130,8,tense(),'music_flight_tense_loop')
print(sorted(os.listdir(OUT)))
