import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import worker from '../src/worker.mjs';
const root=path.resolve(import.meta.dirname,'../public');
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.md':'text/markdown; charset=utf-8','.py':'text/plain; charset=utf-8','.xml':'application/xml','.woff2':'font/woff2','.txt':'text/plain; charset=utf-8'};
const env = {
  ASSETS: {
    async fetch(req) {
      const file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url).pathname));
      if (!file.startsWith(root + path.sep)) return new Response('Not found', {status:404});
      try {
        const content = await fs.readFile(file);
        return new Response(req.method === 'HEAD' ? null : content, {
          headers: {'Content-Type': types[path.extname(file)] || 'application/octet-stream'}
        });
      } catch {
        return new Response('Not found', {status:404});
      }
    }
  }
};
const server=http.createServer(async(req,res)=>{try{const url=new URL(req.url,'http://127.0.0.1:4186');if(url.pathname==='/'){res.writeHead(302,{Location:'/agentic-eng/'});res.end();return;}if(url.pathname!=='/agentic-eng'&&!url.pathname.startsWith('/agentic-eng/')){res.writeHead(404);res.end('Not found');return;}const result=await worker.fetch(new Request(url,{method:req.method,headers:req.headers}),env);res.writeHead(result.status,Object.fromEntries(result.headers));res.end(req.method==='HEAD'?undefined:Buffer.from(await result.arrayBuffer()));}catch(e){console.error(e);res.writeHead(500);res.end('Preview error');}});
server.listen(4186,'127.0.0.1',()=>console.log('Agentic Engineering preview: http://127.0.0.1:4186/agentic-eng/'));
