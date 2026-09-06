(() => {
  const BASE='/agentic-eng';
  const key='organized-ai-agentic-eng-progress-v2';
  const legacyKey='organized-ai-agentic-eng-progress-v1';
  const milestoneIds=['read','tests','challenge','reflect'];
  const valid=new Set([...document.querySelectorAll('.chapter-link[data-chapter]')].map(el=>el.dataset.chapter));
  let progress={};
  try{
    const stored=JSON.parse(localStorage.getItem(key)||'{}');
    if(stored&&stored.version===2&&stored.milestones)progress=stored.milestones;
    else {
      const legacy=JSON.parse(localStorage.getItem(legacyKey)||'[]');
      if(Array.isArray(legacy))for(const slug of legacy)if(valid.has(slug))progress[slug]=[...milestoneIds];
    }
  }catch{}
  const cleanProgress=value=>{
    const clean={};
    if(!value||typeof value!=='object')return clean;
    for(const [slug,items] of Object.entries(value))if(valid.has(slug)&&Array.isArray(items))clean[slug]=[...new Set(items.filter(item=>milestoneIds.includes(item)))];
    return clean;
  };
  progress=cleanProgress(progress);
  let toastTimer;
  const toast=message=>{const el=document.querySelector('.toast');el.textContent=message;el.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.hidden=true,3200);};
  const saveProgress=()=>{try{localStorage.setItem(key,JSON.stringify({version:2,milestones:progress,updatedAt:new Date().toISOString()}));return true;}catch{return false;}};
  const milestoneDone=(slug,id)=>progress[slug]?.includes(id)??false;
  const projectCount=slug=>progress[slug]?.length||0;
  const totalCount=()=>[...valid].reduce((total,slug)=>total+projectCount(slug),0);
  const updateProgress=()=>{
    const total=totalCount();
    document.querySelectorAll('[data-chapter]').forEach(el=>el.classList.toggle('completed',projectCount(el.dataset.chapter)===4));
    document.querySelectorAll('progress').forEach(el=>{el.max=48;el.value=total;});
    document.querySelectorAll('[data-progress-label]').forEach(el=>el.textContent=`${total} / 48`);
    document.querySelectorAll('[data-progress-total]').forEach(el=>el.textContent=String(total));
    document.querySelectorAll('[data-project-count]').forEach(el=>el.textContent=`${projectCount(el.dataset.projectCount)} / 4`);
    document.querySelectorAll('[data-milestone]').forEach(input=>{input.checked=milestoneDone(input.dataset.project,input.dataset.milestone);});
    document.querySelectorAll('[data-complete]').forEach(el=>{const done=projectCount(el.dataset.complete)===4;el.setAttribute('aria-pressed',String(done));el.textContent=done?'✓ All milestones complete':'Complete all milestones';});
  };
  updateProgress();
  document.querySelectorAll('[data-milestone]').forEach(input=>input.addEventListener('change',()=>{
    const {project,milestone}=input.dataset;const items=new Set(progress[project]||[]);
    input.checked?items.add(milestone):items.delete(milestone);progress[project]=[...items];
    updateProgress();toast(saveProgress()?'Progress saved in this browser.':'Updated for this visit. Browser storage is unavailable.');
  }));
  document.querySelectorAll('[data-complete]').forEach(button=>button.addEventListener('click',()=>{
    const slug=button.dataset.complete;progress[slug]=projectCount(slug)===4?[]:[...milestoneIds];
    updateProgress();toast(saveProgress()?projectCount(slug)===4?'All four milestones completed.':'Milestones reset.':'Updated for this visit. Browser storage is unavailable.');
  }));
  document.querySelector('[data-export-progress]')?.addEventListener('click',()=>{
    const blob=new Blob([JSON.stringify({version:2,exportedAt:new Date().toISOString(),milestones:progress},null,2)],{type:'application/json'});
    const href=URL.createObjectURL(blob),link=document.createElement('a');link.href=href;link.download='agentic-engineering-progress.json';link.click();setTimeout(()=>URL.revokeObjectURL(href),0);toast('Progress exported.');
  });
  const fileInput=document.querySelector('[data-progress-file]');
  document.querySelector('[data-import-progress]')?.addEventListener('click',()=>fileInput?.click());
  fileInput?.addEventListener('change',async()=>{
    try{const parsed=JSON.parse(await fileInput.files[0].text());if(parsed.version!==2)throw new Error('version');progress=cleanProgress(parsed.milestones);updateProgress();saveProgress();toast('Progress imported.');}
    catch{toast('That progress file is not valid.');}
    finally{fileInput.value='';}
  });
  const menu=document.querySelector('.menu-trigger'),chapterMenu=document.querySelector('.chapter-menu');
  const closeMenu=()=>{if(chapterMenu.open)chapterMenu.close();menu.setAttribute('aria-expanded','false');};
  menu.addEventListener('click',()=>{chapterMenu.showModal();menu.setAttribute('aria-expanded','true');});
  chapterMenu.querySelector('.menu-close').addEventListener('click',closeMenu);
  chapterMenu.addEventListener('close',()=>menu.setAttribute('aria-expanded','false'));
  chapterMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
  const dialog=document.querySelector('.search-dialog'),input=document.querySelector('#guide-search'),results=document.querySelector('#search-results'),status=document.querySelector('#search-status');
  let indexPromise;
  const loadIndex=()=>{if(!indexPromise)indexPromise=fetch(`${BASE}/assets/search-index.json`).then(r=>{if(!r.ok)throw new Error('Search unavailable');return r.json();}).catch(e=>{indexPromise=undefined;throw e;});return indexPromise;};
  let searchVersion=0;
  const search=async()=>{
    const version=++searchVersion;const q=input.value.trim().toLowerCase();results.replaceChildren();
    if(!q){status.textContent='Search across all 12 chapters.';return;}
    status.textContent='Searching…';
    try{
      const index=await loadIndex();if(version!==searchVersion)return;
      const terms=q.split(/\s+/).filter(Boolean);
      const matches=index.map(c=>{const text=`${c.title} ${c.summary} ${c.text}`.toLowerCase();return {...c,match:terms.every(t=>text.includes(t)),score:terms.reduce((n,t)=>n+(c.title.toLowerCase().includes(t)?8:0)+(c.summary.toLowerCase().includes(t)?3:0),0)};}).filter(c=>c.match).sort((a,b)=>b.score-a.score);
      status.textContent=matches.length?`${matches.length} matching chapter${matches.length===1?'':'s'}.`:'No chapters found. Try a shorter term, such as “cache” or “policy”.';
      for(const c of matches){const link=document.createElement('a');link.className='search-result';link.href=c.href;const title=document.createElement('strong');title.textContent=`${c.number} · ${c.title}`;const snippet=document.createElement('span');const offset=c.text.toLowerCase().indexOf(terms[0]);const start=Math.max(0,offset-55);snippet.textContent=(start?'…':'')+c.text.slice(start,start+190)+'…';link.append(title,snippet);results.append(link);}
    }catch{if(version===searchVersion)status.textContent='Search is unavailable. All chapters remain accessible in the chapter menu.';}
  };
  document.querySelector('.search-trigger').addEventListener('click',()=>{closeMenu();dialog.showModal();input.focus();search();});
  document.querySelector('[data-close-search]').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog){const rect=dialog.getBoundingClientRect();if(e.clientX<rect.left||e.clientX>rect.right||e.clientY<rect.top||e.clientY>rect.bottom)dialog.close();}});
  input.addEventListener('input',search);
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu();if(e.key==='/'&&!dialog.open&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName)&&!document.activeElement?.isContentEditable){e.preventDefault();document.querySelector('.search-trigger').click();}});
  document.querySelectorAll('.prose pre').forEach(pre=>{const button=document.createElement('button');button.type='button';button.className='copy-code';button.textContent='Copy';button.setAttribute('aria-label','Copy code block');button.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(pre.querySelector('code').textContent);button.textContent='Copied';setTimeout(()=>button.textContent='Copy',1800);}catch{toast('Clipboard access is unavailable. Select and copy the code manually.');}});pre.append(button);});
  const headings=[...document.querySelectorAll('.prose h2[id]')];
  if('IntersectionObserver' in window&&document.querySelector('.page-toc')){
    const observer=new IntersectionObserver(entries=>{const visible=entries.filter(e=>e.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top)[0];if(!visible)return;document.querySelectorAll('.page-toc nav a').forEach(a=>{if(a.hash===`#${visible.target.id}`)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});},{rootMargin:'-90px 0px -65% 0px'});headings.forEach(h=>observer.observe(h));
  }
})();
