import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {homeMarkup} from '../src/home.mjs';
import {renderShell} from '../src/shell.mjs';
import MarkdownIt from 'markdown-it';
import {base,origin,updated,chapters,sources} from '../src/catalog.mjs';
import {projects,milestones,repo} from '../src/projects.mjs';
import {feedToken,feedTitle} from '../src/audio.mjs';

const root = path.resolve(import.meta.dirname,'..');
const out = path.join(root,'public');
const assetHash=createHash('sha256');
for(const asset of ['style.css','editorial.css','app.js','editorial.js','player.js'])assetHash.update(await fs.readFile(path.join(root,'src/assets',asset)));
const assetVersion=assetHash.digest('hex').slice(0,12);
const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const md = new MarkdownIt({html:false,linkify:true,typographer:true});
// Markdown's alignment normally emits inline styles; use classes so the
// published site's strict Content Security Policy remains effective.
for (const kind of ['th_open','td_open']) md.renderer.rules[kind]=(tokens,idx,options,env,self)=>{
  const alignment=tokens[idx].attrGet('style');
  if(alignment){
    tokens[idx].attrs=tokens[idx].attrs.filter(([name])=>name!=='style');
    const value=alignment.replace('text-align:','');
    if(['left','right','center'].includes(value))tokens[idx].attrSet('class',`align-${value}`);
  }
  return self.renderToken(tokens,idx,options);
};
const slugify = s => s.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
let headingIds = new Map();
md.renderer.rules.heading_open = (tokens,idx,options,env,self) => {
  const text=tokens[idx+1].content;
  const stem=slugify(text), count=(headingIds.get(stem)||0)+1;
  headingIds.set(stem,count);
  tokens[idx].attrSet('id',count===1?stem:`${stem}-${count}`);
  return self.renderToken(tokens,idx,options);
};
const render = s => {headingIds=new Map();return md.render(s);};
const audioDir=path.join(out,'assets','audio');
let audioFiles=new Map();
try{for(const f of await fs.readdir(audioDir)){if(f.endsWith('.mp3')){const stat=await fs.stat(path.join(audioDir,f));audioFiles.set(f.replace(/\.mp3$/,''),stat.size);}}}catch{}
const playerMarkup=(slug,title)=>audioFiles.has(slug)?`<section class="audio-player" data-audio-player data-src="${base}/assets/audio/${slug}.mp3" aria-label="Listen to this chapter"><button type="button" class="audio-play" data-audio-play aria-label="Play chapter audio">\u25b6</button><div class="audio-track"><input type="range" data-audio-seek min="0" max="1000" value="0" step="1" aria-label="Seek chapter audio"><div class="audio-times"><span data-audio-current>0:00</span><span data-audio-duration>--:--</span></div></div><button type="button" class="audio-speed" data-audio-speed aria-label="Change playback speed">1\u00d7</button><a class="audio-download" href="${base}/assets/audio/${slug}.mp3" download aria-label="Download chapter audio">\u2193</a></section>`:'';

const wordCount = s => (s.match(/\b[\w'-]+\b/g)||[]).length;
const chapterData = await Promise.all(chapters.map(async c=>{
  const markdown=await fs.readFile(path.join(root,'content',c.file),'utf8');
  return {...c,markdown,words:wordCount(markdown),minutes:Math.max(1,Math.ceil(wordCount(markdown)/200))};
}));
const totalWords=chapterData.reduce((n,c)=>n+c.words,0);
const projectMap=new Map(projects.map(project=>[project.slug,project]));
const milestoneMarkup=slug=>milestones.map(item=>`<label class="milestone"><input type="checkbox" data-project="${slug}" data-milestone="${item.id}"><span><strong>${esc(item.label)}</strong>${esc(item.description)}</span></label>`).join('');
const projectMarkup=(chapter,project)=>`<section class="companion-project" id="companion-project"><div class="project-heading"><div><p class="eyebrow">HANDS-ON PROJECT ${chapter.number}</p><h2>${esc(project.title)}</h2><p>${esc(project.outcome)}</p></div><span class="test-count">${project.tests} TESTS</span></div><div class="project-grid"><div><h3>Run the checkpoint</h3><pre><code>${esc(project.command)}</code></pre><div class="project-links"><a href="${project.url}" target="_blank" rel="noopener noreferrer">Open project ↗</a><a href="${project.starter}" target="_blank" rel="noopener noreferrer">Starter</a><a href="${project.solution}" target="_blank" rel="noopener noreferrer">Solution</a><a href="${project.testFile}" target="_blank" rel="noopener noreferrer">Tests</a></div></div><div><h3>Worked code</h3><pre><code>${esc(project.code)}</code></pre></div></div><div class="milestone-panel"><div><p class="eyebrow">PROJECT PROGRESS</p><p>Complete all four milestones to finish this chapter.</p></div><div class="milestone-grid">${milestoneMarkup(chapter.slug)}</div></div></section>`;
const nav = active => {
  let group='';
  return chapterData.map(c=>{
    const label=c.group!==group?`<p class="nav-group">${esc(c.group)}</p>`:'';group=c.group;
    return `${label}<a class="chapter-link${active===c.slug?' active':''}" href="${c.href}" ${active===c.slug?'aria-current="page"':''} data-chapter="${c.slug}"><span class="chapter-number">${c.number}</span><span>${esc(c.title)}</span><span class="completion-mark" aria-hidden="true"></span></a>`;
  }).join('');
};
function shell(options){return renderShell({...options,navHTML:nav(options.active||''),assetVersion,base,origin,updated});}
const write = async (relative,contents)=>{
  const dest=path.join(out,relative);await fs.mkdir(path.dirname(dest),{recursive:true});await fs.writeFile(dest,contents);
};
await fs.mkdir(out,{recursive:true});
await fs.cp(path.join(root,'src/assets'),path.join(out,'assets'),{recursive:true});
const home=homeMarkup(chapterData);
await write('index.html',shell({title:'Agentic Engineering — The Field Guide',description:'Twenty-three deep dives into reliable AI systems, from experiments and agents to inference, ontologies, and cost per accepted outcome.',body:home,className:'home'}));
for (const [i,c] of chapterData.entries()){
  const project=projectMap.get(c.slug);
  if(!project) throw new Error(`Missing companion project for ${c.slug}`);
  const heads=[...c.markdown.matchAll(/^## (.+)$/gm)].map(m=>m[1]);
  const toc=heads.map(h=>`<a href="#${slugify(h)}">${esc(h)}</a>`).join('');
  const prev=chapterData[i-1],next=chapterData[i+1];
  const body=`<header class="chapter-header"><div class="eyebrow">${esc(c.group)} <span class="slash">/</span> CHAPTER ${c.number}</div><h1>${esc(c.title)}</h1><p class="chapter-subtitle">${esc(c.subtitle)}</p><div class="chapter-meta"><span>${c.minutes} MIN READ</span><span>${esc(c.level.toUpperCase())}</span><span>${project.tests} RUNNABLE TESTS</span></div></header>${playerMarkup(c.slug,c.title)}<article class="prose">${render(c.markdown)}</article>${projectMarkup(c,project)}<section class="chapter-finish"><div><span class="eyebrow">MAKE IT STICK</span><h2>Can you pass the ship gate?</h2><p>Complete the reading, tests, challenge, and reflection.</p></div><button class="button primary" type="button" data-complete="${c.slug}" aria-pressed="false">Complete all milestones</button></section><nav class="chapter-pagination" aria-label="Adjacent chapters">${prev?`<a href="${prev.href}"><span>← PREVIOUS</span><strong>${esc(prev.title)}</strong></a>`:`<a href="${base}/"><span>← OVERVIEW</span><strong>The field guide</strong></a>`}${next?`<a href="${next.href}"><span>NEXT →</span><strong>${esc(next.title)}</strong></a>`:`<a href="${base}/capstone/"><span>NEXT →</span><strong>Build the capstone</strong></a>`}</nav>`;
  await write(`chapters/${c.slug}/index.html`,shell({title:`${c.number}. ${c.title}`,description:c.summary,body,active:c.slug,toc,url:c.href,className:'chapter-page'}));
}
const progressRows=chapterData.map(c=>{const p=projectMap.get(c.slug);return `<article class="progress-project" data-progress-project="${c.slug}"><div class="progress-project-head"><span>${c.number}</span><div><h2><a href="${c.href}">${esc(c.title)}</a></h2><p><a href="${p.url}" target="_blank" rel="noopener noreferrer">${esc(p.title)} ↗</a> · ${p.tests} tests</p></div><strong data-project-count="${c.slug}">0 / 4</strong></div><div class="milestone-grid">${milestoneMarkup(c.slug)}</div></article>`}).join('');
const progressBody=`<header class="chapter-header"><div class="eyebrow">FIELD GUIDE / PROGRESS</div><h1>Track the work.</h1><p class="chapter-subtitle">Reading is one milestone. Running, changing, and reflecting make the knowledge durable.</p></header><section class="progress-summary"><div><span data-progress-total>0</span><p>of 124 milestones complete</p></div><progress max="124" value="0" aria-label="Overall hands-on progress"></progress><div class="progress-actions"><button class="button secondary" type="button" data-export-progress>Export progress</button><button class="button secondary" type="button" data-import-progress>Import progress</button><input type="file" accept="application/json" data-progress-file hidden></div><p class="progress-note">Saved in this browser. Export JSON to move progress between devices.</p></section><section class="progress-list">${progressRows}</section><section class="repo-callout"><div><p class="eyebrow">COMPANION REPOSITORY</p><h2>Clone once. Work all thirty-one projects.</h2><pre><code>git clone ${repo}.git\ncd agentic-engineering-labs\npython3 scripts/test_all.py</code></pre></div><a class="button primary" href="${repo}" target="_blank" rel="noopener noreferrer">Open the repository ↗</a></section>`;
await write('progress/index.html',shell({title:'Hands-on progress',description:'Track four practical milestones across all thirty-one Agentic Engineering projects.',body:progressBody,active:'progress',url:`${base}/progress/`,className:'progress-page'}));
for (const [slug,title,description] of [['capstone','Build the capstone','Bring the chapters together in a safe event-operations assistant.'],['glossary','A shared vocabulary','Plain-language definitions for the concepts in this guide.']]){
  const source=await fs.readFile(path.join(root,'content',`${slug}.md`),'utf8');
  const body=`<header class="chapter-header"><div class="eyebrow">FIELD GUIDE / REFERENCE</div><h1>${title}</h1><p class="chapter-subtitle">${description}</p></header><article class="prose">${render(source)}</article>`;
  await write(`${slug}/index.html`,shell({title,description,body,active:slug,url:`${base}/${slug}/`}));
}
{
  const source=await fs.readFile(path.join(root,'content','deep-research.md'),'utf8');
  const heads=[...source.matchAll(/^## (.+)$/gm)].map(m=>m[1]);
  const toc=heads.map(h=>`<a href="#${slugify(h)}">${esc(h)}</a>`).join('');
  const body=`<header class="chapter-header"><div class="eyebrow">FIELD GUIDE / DEEP RESEARCH</div><h1>Deep research expansion</h1><p class="chapter-subtitle">The next layer down for all 12 chapters, plus the connected topics the guide does not cover yet.</p><div class="chapter-meta"><span>${Math.max(1,Math.ceil(wordCount(source)/200))} MIN READ</span><span>RESEARCH</span><span>SOURCED</span></div></header><article class="prose">${render(source)}</article>`;
  await write('deep-research/index.html',shell({title:'Deep research expansion',description:'Per-chapter deep dives, 2026 frontier notes, and a sourced gap analysis for the Agentic Engineering field guide.',body,active:'deep-research',toc,url:`${base}/deep-research/`}));
}
const sourceBody=`<header class="chapter-header"><div class="eyebrow">FIELD GUIDE / EVIDENCE</div><h1>Sources & editorial notes</h1><p class="chapter-subtitle">Know what is documented, what is proposed, and what remains to be tested.</p></header><article class="prose"><h2>Scope and attribution</h2><p>This is an independently authored educational guide inspired by Shep Bryan’s LinkedIn post. His customer deployments, experiment counts, productivity claims, and eight-B200 GLM 5.1 load test are self-reported, not independently reproduced here. The post does not identify what kind of kernels he wrote.</p><p>The walkthroughs, system designs, numbers, code, labs, and acceptance gates are instructional proposals. All cost examples are synthetic, not prices or forecasts. Pseudocode is labeled. The downloadable starter is an offline simulation with tested invariants; it does not implement an LLM, distributed queue, production gateway, or a certified privacy boundary.</p><h2>Reading the evidence</h2><p>References support specific mechanisms, not a blanket endorsement of every design choice. Provider behavior, documentation routes, and model capabilities change. Documentation was reviewed on ${updated}; confirm the exact feature, version, region, license, and agreement before using a design in production.</p><p>A ZDR arrangement is not automatically a regulatory compliance determination. Likewise, an ontology does not enforce authorization, and a passing test suite does not prove that an agent is safe in every environment.</p><h2>Primary references</h2><div class="source-list">${sources.map((s,i)=>`<section id="${s.id}" class="source-entry"><span class="source-number">${String(i+1).padStart(2,'0')}</span><div><p class="eyebrow">${esc(s.organization)}</p><h3><a href="${s.url}" target="_blank" rel="noopener noreferrer">${esc(s.title)} →</a></h3><p>${esc(s.note)}</p></div></section>`).join('')}</div></article>`;
await write('sources/index.html',shell({title:'Sources & editorial notes',description:'Primary references, attribution, implementation boundaries, and evidence notes.',body:sourceBody,active:'sources',url:`${base}/sources/`}));
const combined=`# Agentic Engineering — An Organized AI Field Guide\n\nReviewed ${updated}.\n\nIndependent instructional expansion of the topics in Shep Bryan’s LinkedIn post. Examples and labs are proposed designs, not claims about his implementation.\n\n${chapterData.map(c=>{const p=projectMap.get(c.slug);return `# ${c.number}. ${c.title}\n\n${c.markdown}\n\n## Companion project: ${p.title}\n\n${p.outcome}\n\nProject: ${p.url}\n\nStarter: ${p.starter}\n\nTests: ${p.testFile}\n\n\`\`\`sh\n${p.command}\n\`\`\`\n\n\`\`\`python\n${p.code}\n\`\`\`\n\nMilestones: read and explain; run the tests; complete the challenge; write a reflection.`}).join('\n\n---\n\n')}\n\n# Capstone\n\n${await fs.readFile(path.join(root,'content/capstone.md'),'utf8')}\n\n# Glossary\n\n${await fs.readFile(path.join(root,'content/glossary.md'),'utf8')}\n\n# Deep research expansion\n\n${await fs.readFile(path.join(root,'content/deep-research.md'),'utf8')}\n\n# Sources\n\n${sources.map(s=>`- ${s.title} — ${s.organization}: ${s.url}`).join('\n')}\n`;
await write('downloads/agentic-engineering.md',combined.replaceAll(`${base}/`,`${origin}${base}/`));
const bookBody=`<header class="chapter-header"><div class="eyebrow">FIELD GUIDE / READING EDITION</div><h1>Agentic Engineering</h1><p class="chapter-subtitle">All 31 chapters in one place. Use your browser’s print command to save a PDF.</p><p><a href="${base}/downloads/agentic-engineering.md" download>Download Markdown ↓</a></p></header><article class="prose book-prose">${render(combined)}</article>`;
await write('book/index.html',shell({title:'Agentic Engineering — Complete Reading Edition',description:'The full guide, capstone, and glossary in a printable reading edition.',body:bookBody,url:`${base}/book/`,className:'book-page'}));
await write('assets/search-index.json',JSON.stringify(chapterData.map(c=>{const p=projectMap.get(c.slug);return {title:c.title,number:c.number,href:c.href,summary:c.summary,text:`${c.markdown} ${p.title} ${p.outcome} ${p.code}`.replace(/\[[^\]]+\]\([^)]*\)/g,m=>m.slice(1,m.indexOf(']'))).replace(/[`#*|]/g,'').replace(/\s+/g,' ')}})));
for (const name of ['pipeline.py','test_pipeline.py','README.md']) await write(`downloads/lab/${name}`,await fs.readFile(path.join(root,'labs',name)));
await write('404.html',shell({title:'Page not found',description:'This guide page does not exist.',body:`<header class="chapter-header"><div class="eyebrow">404 / UNKNOWN PATH</div><h1>This page isn’t in the guide.</h1><p><a class="button primary" href="${base}/">Back to the curriculum →</a></p></header>`}));
{
  const feedPath=`assets/audio/feed-${feedToken}.xml`;
  const rows=chapterData.map(c=>{
    const has=audioFiles.has(c.slug);
    return `<div class="audio-chapter" data-audio-chapter><h2>${c.number} · ${esc(c.title)}</h2><p class="audio-summary">${esc(c.summary)}</p>${has?playerMarkup(c.slug,c.title):'<span class="audio-pending">Narration in production</span>'}</div>`;
  }).join('');
  const feedPanel=audioFiles.size?`<section class="audio-feed"><p class="eyebrow">PRIVATE PODCAST FEED</p><h2>Listen in your podcast app</h2><p>Add this URL in Apple Podcasts, Overcast, or Pocket Casts. It is unlisted - anyone with the link can subscribe, so treat it like a password.</p><code>${origin}${base}/${feedPath}</code></section>`:`<section class="audio-feed"><p class="eyebrow">PRIVATE PODCAST FEED</p><h2>Listen in your podcast app</h2><p>The feed goes live when the first narration lands.</p></section>`;
  const body=`<header class="chapter-header"><div class="eyebrow">FIELD GUIDE / AUDIO EDITION</div><h1>Listen to the guide.</h1><p class="chapter-subtitle">Every chapter, narrated. Chapters light up as their audio lands; the playlist plays straight through.</p></header>${feedPanel}<section>${rows}</section>`;
  await write('audio/index.html',shell({title:'Audio edition',description:'Listen to every chapter of the Agentic Engineering field guide, plus a private podcast feed.',body,active:'audio',url:`${base}/audio/`}));
  if(audioFiles.size){
    const items=chapterData.filter(c=>audioFiles.has(c.slug)).map(c=>`<item><title>${c.number} · ${esc(c.title)}</title><description>${esc(c.summary)}</description><link>${origin}${c.href}</link><guid>${origin}${c.href}</guid><enclosure url="${origin}${base}/assets/audio/${c.slug}.mp3" length="${audioFiles.get(c.slug)}" type="audio/mpeg"/><pubDate>${new Date().toUTCString()}</pubDate></item>`).join('');
    await write(feedPath,`<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>${feedTitle}</title><link>${origin}${base}/audio/</link><description>Narrated chapters of the Agentic Engineering field guide. Unlisted feed - keep the URL private.</description><language>en-us</language>${items}</channel></rss>`);
  }
}
await write('sitemap.xml',`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${[`${base}/`,...chapters.map(c=>c.href),`${base}/progress/`,`${base}/capstone/`,`${base}/glossary/`,`${base}/audio/`,`${base}/deep-research/`,`${base}/sources/`].map(u=>`<url><loc>${origin}${u}</loc></url>`).join('')}</urlset>`);
console.log(`Built ${chapterData.length} chapters (${totalWords.toLocaleString()} words), capstone, glossary, sources, and full reading edition.`);
