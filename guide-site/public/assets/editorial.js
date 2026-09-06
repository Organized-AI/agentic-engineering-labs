/* Procedural field adapted from the user's local Concept B reference.
   No reference-site content, third-party assets, or animation dependency. */
(() => {
  const hero=document.querySelector('#home');
  const canvas=document.querySelector('#signal-canvas');
  const header=document.querySelector('.topbar');
  const motionButton=document.querySelector('[data-motion-toggle]');
  if(!hero||!canvas)return;
  const ctx=canvas.getContext('2d');
  const preference=matchMedia('(prefers-reduced-motion: reduce)');
  let paused=false,visible=true,frame=0,width=1,height=1,lastPaint=-Infinity;
  const points=[];
  for(let ring=0;ring<28;ring++)for(let point=0;point<78;point++){
    const u=point/78*Math.PI*2,v=ring/28*Math.PI*2,r=.78+.29*Math.cos(v);
    points.push({x:r*Math.cos(u),y:.29*Math.sin(v),z:r*Math.sin(u),ring,point});
  }
  const reduced=()=>preference.matches||paused;
  const paint=(time=0)=>{
    if(!ctx)return;
    ctx.clearRect(0,0,width,height);
    const mobile=width<760,cx=width*(mobile?.68:.74),cy=height*(mobile?.30:.37);
    const unit=Math.min(width*(mobile?.73:.37),height*.56);
    const glow=ctx.createRadialGradient(cx,cy,0,cx,cy,unit*1.3);
    glow.addColorStop(0,'rgba(164,124,21,.15)');glow.addColorStop(.55,'rgba(118,88,9,.055)');glow.addColorStop(1,'rgba(9,11,6,0)');
    ctx.fillStyle=glow;ctx.fillRect(0,0,width,height);
    const a=time*.045+.15,b=.9;
    const rotated=points.map(p=>{
      const x=p.x*Math.cos(a)+p.z*Math.sin(a),z=-p.x*Math.sin(a)+p.z*Math.cos(a);
      const y=p.y*Math.cos(b)-z*Math.sin(b),depth=p.y*Math.sin(b)+z*Math.cos(b),perspective=3.5/(3.5-depth);
      return {x:cx+(x*.91+y*.2)*unit*perspective,y:cy+(y*.94-x*.13)*unit*perspective,z:depth,r:.45+(depth+1.1)*.5};
    });
    ctx.lineWidth=.5;
    for(let ring=0;ring<28;ring+=2){ctx.beginPath();for(let p=0;p<=78;p++){const q=rotated[ring*78+p%78];p?ctx.lineTo(q.x,q.y):ctx.moveTo(q.x,q.y);}ctx.strokeStyle='rgba(194,166,72,.05)';ctx.stroke();}
    rotated.sort((p,q)=>p.z-q.z).forEach(p=>{ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle=`rgba(239,207,102,${Math.max(.07,Math.min(.75,(p.z+1.2)*.3))})`;ctx.fill();});
    for(let i=0;i<70;i++){const seed=Math.sin(i*78.233)*43758.5453,f=seed-Math.floor(seed);ctx.fillStyle=`rgba(220,199,130,${.07+f*.12})`;ctx.fillRect((i*137.3)%width,(f*height+time*(i%3)*.4)%height,1,1);}
  };
  const tick=now=>{
    frame=0;if(reduced()||!visible||document.hidden)return;
    if(now-lastPaint>=1000/24){paint(now/1000);lastPaint=now;}
    frame=requestAnimationFrame(tick);
  };
  const sync=()=>{
    if(frame)cancelAnimationFrame(frame);frame=0;
    const active=!!ctx&&!reduced()&&visible&&!document.hidden;
    canvas.dataset.motion=active?'running':reduced()?'static':'paused';
    if(motionButton){motionButton.textContent=preference.matches?'Reduced motion enabled':paused?'Resume motion':'Pause motion';motionButton.setAttribute('aria-pressed',String(reduced()));motionButton.disabled=preference.matches;}
    if(active)frame=requestAnimationFrame(tick);else paint();
  };
  const resize=()=>{const rect=hero.getBoundingClientRect();width=rect.width;height=rect.height;const scale=Math.min(devicePixelRatio||1,1.75);canvas.width=Math.round(width*scale);canvas.height=Math.round(height*scale);ctx?.setTransform(scale,0,0,scale,0,0);paint();};
  if('ResizeObserver'in window)new ResizeObserver(resize).observe(hero);else{resize();addEventListener('resize',resize);}
  if('IntersectionObserver'in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync();},{threshold:0}).observe(hero);
  preference.addEventListener('change',sync);document.addEventListener('visibilitychange',sync);
  motionButton?.addEventListener('click',()=>{paused=!paused;sync();});
  addEventListener('pagehide',()=>{if(frame)cancelAnimationFrame(frame);frame=0;});
  addEventListener('pageshow',sync);
  const sections=[...document.querySelectorAll('section[data-surface]')];
  let scheduled=false;
  const updateHeader=()=>{scheduled=false;let active=sections[0];for(const section of sections){if(section.getBoundingClientRect().top<=90)active=section;else break;}header.classList.toggle('on-light',active?.dataset.surface==='light');header.classList.toggle('scrolled',scrollY>24);};
  addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(updateHeader);}},{passive:true});
  updateHeader();resize();sync();
})();
