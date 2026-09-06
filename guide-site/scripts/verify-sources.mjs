import fs from 'node:fs/promises';
import {sources} from '../src/catalog.mjs';
const results=[];
const pending=sources.filter(s=>s.id!=='post');
async function run(){while(pending.length){const s=pending.shift();try{const r=await fetch(s.url,{signal:AbortSignal.timeout(25000),headers:{'User-Agent':'OrganizedAI-Guide-SourceCheck/1.0'}});const html=await r.text();const title=html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]||'';const clean=html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,'');const main=clean.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1]||clean.match(/<article\b[^>]*>([\s\S]*?)<\/article>/i)?.[1]||clean;const text=main.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();results.push({id:s.id,url:s.url,resolvedURL:r.url,status:r.status,title,checkedAt:new Date().toISOString()});console.log(JSON.stringify({id:s.id,status:r.status,url:r.url,title,excerpt:text.slice(0,1000)}));}catch(e){results.push({id:s.id,url:s.url,error:e.message});console.log(JSON.stringify({id:s.id,error:e.message}));}}}
await Promise.all(Array.from({length:4},run));
await fs.mkdir(new URL('../research/',import.meta.url),{recursive:true});
await fs.writeFile(new URL('../research/source-audit.json',import.meta.url),JSON.stringify(results,null,2)+'\n');
if(results.some(r=>r.status>=400||r.error))process.exitCode=1;
