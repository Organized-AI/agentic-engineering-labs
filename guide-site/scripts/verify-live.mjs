import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {base,origin,chapters} from '../src/catalog.mjs';
const root=path.resolve(import.meta.dirname,'..');
const checks=[];
const routes=[['/', 'index.html'],...chapters.map(c=>[`/chapters/${c.slug}/`,`chapters/${c.slug}/index.html`]),['/progress/','progress/index.html'],['/capstone/','capstone/index.html'],['/glossary/','glossary/index.html'],['/sources/','sources/index.html'],['/book/','book/index.html'],['/assets/style.css','assets/style.css'],['/assets/app.js','assets/app.js'],['/assets/search-index.json','assets/search-index.json'],['/downloads/agentic-engineering.md','downloads/agentic-engineering.md'],['/downloads/lab/pipeline.py','downloads/lab/pipeline.py'],['/downloads/lab/test_pipeline.py','downloads/lab/test_pipeline.py']];
routes.push(
  ['/assets/favicon.svg','assets/favicon.svg'],
  ['/assets/editorial.css','assets/editorial.css'],
  ['/assets/editorial.js','assets/editorial.js'],
  ['/assets/fonts/inter-latin-variable.woff2','assets/fonts/inter-latin-variable.woff2'],
  ['/assets/fonts/jetbrains-mono-latin-variable.woff2','assets/fonts/jetbrains-mono-latin-variable.woff2']
);
const pending=[...routes];
const hash=b=>createHash('sha256').update(b).digest('hex');
async function worker(){while(pending.length){const [route,file]=pending.shift();const r=await fetch(`${origin}${base}${route}`,{signal:AbortSignal.timeout(30000)});const body=Buffer.from(await r.arrayBuffer());const local=await fs.readFile(path.join(root,'public',file));const record={path:`${base}${route}`,status:r.status,bytes:body.length,matchesBuild:hash(body)===hash(local),contentType:r.headers.get('content-type'),csp:r.headers.has('content-security-policy')};checks.push(record);console.log(JSON.stringify(record));}}
await Promise.all(Array.from({length:4},worker));
for(const suffix of ['', '?source=verification']){const r=await fetch(`${origin}${base}${suffix}`,{redirect:'manual'});checks.push({path:base+suffix,status:r.status,redirect:r.headers.get('location'),pass:r.status===308&&r.headers.get('location')?.includes(`${base}/`)});}
const missing=await fetch(`${origin}${base}/not-a-chapter/`);checks.push({path:base+'/not-a-chapter/',status:missing.status,pass:missing.status===404&&(await missing.text()).includes('This page isn’t in the guide.')});
const existing=await fetch(`${origin}/harness`);checks.push({path:'/harness',status:existing.status,pass:existing.ok&&(await existing.text()).includes('Organized Harness')});
const sibling=await fetch(`${origin}/agentic-engineering-other`);checks.push({path:'/agentic-engineering-other',status:sibling.status,pass:(await sibling.text()).includes('No route for')});
await fs.mkdir(path.join(root,'research'),{recursive:true});
await fs.writeFile(path.join(root,'research/live-verification.json'),JSON.stringify({checkedAt:new Date().toISOString(),checks},null,2)+'\n');
const fail=checks.filter(c=>c.pass===false||c.matchesBuild===false||('matchesBuild'in c&&c.status!==200));
console.log(`${checks.length} live checks; ${fail.length} failures.`);
if(fail.length){console.error(fail);process.exitCode=1;}
