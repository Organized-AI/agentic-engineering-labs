import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {base,chapters,sources} from '../src/catalog.mjs';
import {projects,milestones,repo} from '../src/projects.mjs';
const root=path.resolve(import.meta.dirname,'..');
const pub=path.join(root,'public');
const files=[];
async function walk(dir){for(const e of await fs.readdir(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())await walk(p);else files.push(p);}}
await walk(pub);
const htmls=new Map();
for(const file of files.filter(f=>f.endsWith('.html')))htmls.set(file,await fs.readFile(file,'utf8'));
let links=0;
for(const [file,html] of htmls){
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(ids.length,new Set(ids).size,`Duplicate HTML ID: ${file}`);
  assert.ok(html.includes('name="viewport"'),`Missing viewport: ${file}`);
  assert.ok(html.includes('<main id="main"'),`Missing main landmark: ${file}`);
  assert.ok(!/\sstyle="/.test(html),`Inline styles violate the CSP: ${file}`);
  assert.ok(html.includes('class="brand-yellow">AI</span>'),`Missing supplied wordmark: ${file}`);
  assert.ok(html.includes('/assets/editorial.css?v='),`Missing versioned editorial styling: ${file}`);
  assert.ok(html.includes('id="chapter-menu"'),`Missing chapter navigation dialog: ${file}`);
  for(const m of html.matchAll(/\b(?:href|src)="([^"]+)"/g)){
    const href=m[1].replaceAll('&amp;','&');
    if(!href.startsWith(base+'/')&&!href.startsWith('#'))continue;
    links++;
    const url=new URL(href,`https://guide.organizedai.vip${base}/${path.relative(pub,file)}`);
    let relative=url.pathname.slice(base.length+1);
    if(!relative||relative.endsWith('/'))relative+='index.html';
    const target=path.join(pub,relative);
    await fs.access(target).catch(()=>{throw new Error(`Broken internal URL ${href} in ${file}`);});
    if(url.hash&&target.endsWith('.html'))assert.ok(htmls.get(target)?.includes(`id="${decodeURIComponent(url.hash.slice(1))}"`),`Missing anchor ${href} in ${file}`);
  }
}
assert.equal(chapters.length,31);
assert.equal(projects.length,31);
assert.equal(milestones.length,4);
assert.ok(repo.includes('Organized-AI/agentic-engineering-labs'));
for(const c of chapters){
  const text=await fs.readFile(path.join(root,'content',c.file),'utf8');
  assert.ok(text.split(/\s+/).length>=650,`Chapter too short: ${c.slug}`);
  assert.ok(/^## Lab:/m.test(text),`Missing lab: ${c.slug}`);
  assert.ok(text.includes('## Failure drills'),`Missing drills: ${c.slug}`);
  assert.ok(text.includes('## Ship gate'),`Missing ship gate: ${c.slug}`);
  assert.equal((text.match(/^```/gm)||[]).length%2,0,`Unbalanced code block: ${c.slug}`);
}
const index=JSON.parse(await fs.readFile(path.join(pub,'assets/search-index.json'),'utf8'));
assert.equal(index.length,31);
assert.ok(index.every(c=>c.text.length>2000&&c.href.startsWith(base)));
for(const name of ['pipeline.py','test_pipeline.py','README.md'])assert.equal(await fs.readFile(path.join(root,'labs',name),'utf8'),await fs.readFile(path.join(pub,'downloads/lab',name),'utf8'));
assert.equal(new Set(sources.map(s=>s.id)).size,sources.length);
for(const project of projects){
  const chapter=htmls.get(path.join(pub,'chapters',project.slug,'index.html'));
  assert.ok(chapter?.includes(project.url),`Missing project URL for ${project.slug}`);
  assert.ok(chapter?.includes(`data-project="${project.slug}"`),`Missing milestones for ${project.slug}`);
  assert.ok(chapter?.includes('Worked code')&&chapter.includes(project.title),`Missing worked code panel for ${project.slug}`);
}
const progressPage=htmls.get(path.join(pub,'progress','index.html'));
assert.ok(progressPage?.includes('data-export-progress')&&progressPage.includes('data-import-progress'),'Missing progress portability controls');
const css=await fs.readFile(path.join(pub,'assets/style.css'),'utf8');
for(const [token,value] of Object.entries({'bg':'#0c0b09','bg-2':'#100f0c','surface':'#1a1814','surface-2':'#211e19','line':'#2a2520','muted':'#605848','text-2':'#a09888','text-1':'#cfc7b6','text-hi':'#f0ece4','accent':'#f5d623','accent-dim':'#c4943d','accent-deep':'#8b7a12'}))assert.ok(css.includes(`--${token}:${value}`),`Design token mismatch: ${token}`);
for(const font of ['inter-latin-variable.woff2','jetbrains-mono-latin-variable.woff2']){
  const bytes=await fs.readFile(path.join(pub,'assets/fonts',font));
  assert.equal(bytes.subarray(0,4).toString(),'wOF2',`Invalid font file: ${font}`);
}
// Audio edition: page exists, referenced audio resolves, files stay under the asset limit.
const audioPage=htmls.get(path.join(pub,'audio','index.html'));
assert.ok(audioPage,'Missing audio edition page');
const audioDir=path.join(pub,'assets','audio');
let audioCount=0;
try{
  for(const f of await fs.readdir(audioDir)){
    if(!f.endsWith('.mp3'))continue;
    audioCount++;
    const stat=await fs.stat(path.join(audioDir,f));
    assert.ok(stat.size<25*1024*1024,`Audio file over the 25MiB asset limit: ${f}`);
  }
}catch{}
for(const [file,html] of htmls){
  for(const m of html.matchAll(/data-src="([^"]+\.mp3)"/g)){
    const rel=m[1].replace(base+'/','');
    await fs.access(path.join(pub,rel)).catch(()=>{throw new Error(`Missing audio file ${m[1]} referenced in ${file}`);});
  }
}
if(audioCount>0){
  const feeds=(await fs.readdir(audioDir)).filter(f=>/^feed-.+\.xml$/.test(f));
  assert.equal(feeds.length,1,'Expected exactly one tokenized feed file');
  const feed=await fs.readFile(path.join(audioDir,feeds[0]),'utf8');
  for(const m of feed.matchAll(/url="[^"]+\/([^/"]+\.mp3)"/g)){
    await fs.access(path.join(audioDir,m[1])).catch(()=>{throw new Error(`Feed references missing audio ${m[1]}`);});
  }
  assert.ok(feed.includes('<item>'),'Feed has no episodes despite audio files present');
}
console.log(`PASS: ${htmls.size} pages, ${links} internal links/assets/anchors, ${chapters.length} substantive chapters, search index, and matching lab downloads.`);
const editorial=await fs.readFile(path.join(pub,'assets/editorial.css'),'utf8');
assert.ok(editorial.includes('--cream:#fffcf4')&&editorial.includes('--dark:#10100b'),'Missing reference light/dark palette');
assert.ok(htmls.get(path.join(pub,'index.html')).includes('id="signal-canvas"'),'Missing procedural hero');
console.log('PASS: brand tokens, editorial light/dark theme, chapter menu, hero, and local fonts.');
