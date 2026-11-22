import json,os,sys,urllib.request,urllib.error
E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit()
V={"p":1,"n":3,"b":3,"r":5,"q":9,"k":0}
P={"p":[0,0,0,0,0,0,0,0,5,10,10,-20,-20,10,10,5,5,-5,-10,0,0,-10,-5,5,0,0,0,20,20,0,0,0,5,5,10,25,25,10,5,5,10,10,20,30,30,20,10,10,50,50,50,50,50,50,50,50],"n":[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,5,5,0,-20,-40,-30,5,10,15,15,10,5,-30,-30,0,15,20,20,15,0,-30,-30,5,15,20,20,15,5,-30,-30,0,10,15,15,10,0,-30,-40,-20,0,0,0,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50],"b":[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-10,0,0,0,0,0,0,-10,-20,-10,-10,-10,-10,-10,-10,-20],"r":[0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0],"q":[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20],"k":[-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]}
D=3
def p(P,u,b):
    r=urllib.request.Request(E+u,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
    try:
        with urllib.request.urlopen(r) as z:return json.load(z)
    except urllib.error.HTTPError as e:sys.exit(f"{u}: {e.code}")
def B(f):
    b={}
    for i,rw in enumerate(f.split()[0].split("/")):
        f2=0
        for c in rw:
            if c.isdigit():f2+=int(c)
            else:b["abcdefgh"[f2]+str(8-i)]=c;f2+=1
    return b
def I(s):return (ord(s[0])-97,int(s[1])-1)
def J(s):
    x,y=I(s);return y*8+x
def PS(pc,sq,col):
    t=P[pc.lower()];i=J(sq);return t[i]if col=="w"else t[63-i]
def ev(f,col):
    b=B(f);s=0
    for q,pc in b.items():
        sg=1 if pc.isupper()else-1;s+=sg*(V[pc.lower()]*100+PS(pc,q,"w"if pc.isupper()else"b"))
    return s if col=="w"else -s
def FM(f,mv):
    b=B(f);ps=f.split();ts=ps[1];fs,mv2=mv[:2],mv[2:4];pc=b.get(fs,"");v=b.get(mv2)
    if v:del b[v]
    del b[fs];pr=mv[4] if len(mv)==5 else None
    if pr and pc.lower()=="p":pc=pr.upper()if pc.isupper()else pr.lower()
    b[mv2]=pc;nt="b"if ts=="w"else"w"
    rs=[]
    for r in range(8):
        ro="";em=0
        for f2 in range(8):
            c=b.get("abcdefgh"[f2]+str(8-r))
            if c:
                if em:ro+=str(em);em=0
                ro+=c
            else:em+=1
        if em:ro+=str(em)
        rs.append(ro)
    return "/".join(rs)+f" {nt} {ps[2]} {ps[3]} {ps[4]} {ps[5]}"
def S(f,col,d,a,bd):
    g=p("/game",{});lg=g.get("legal_moves",[])
    if not lg or d==0:return ev(f,col),None
    bm=None
    if col=="w":
        me=-999999
        for mv in lg:
            nf=FM(f,mv);e,_=S(nf,"b",d-1,a,bd)
            if e>me:me=e;bm=mv
            a=max(a,e)
            if bd<=a:break
        return me,bm
    else:
        mi=999999
        for mv in lg:
            nf=FM(f,mv);e,_=S(nf,"w",d-1,a,bd)
            if e<mi:mi=e;bm=mv
            bd=min(bd,e)
            if bd<=a:break
        return mi,bm
def ch(f,col,lg):
    b=None;be=-999999;a,bd=-999999,999999
    for mv in lg:
        nf=FM(f,mv);e,_=S(nf,"b"if col=="w"else"w",D-1,a,bd)
        if e>be:be=e;b=mv
        a=max(a,e)
    return b
while 1:
    g=p("/game",{})
    if g["status"]=="done":break
    while g["status"]=="your_move":
        mv=ch(g["fen"],g["colour"],g["legal_moves"])
        g=p("/move",{"game":g["game"],"move":mv})
    print(f"game {g['game']}: {g['outcome']}",file=sys.stderr)
print(f"done: {g.get('wins')}w {g.get('draws')}d {g.get('losses')}l",file=sys.stderr)
