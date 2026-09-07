const BASE = '/agentic-eng';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // Cloudflare route matching includes query strings. The wildcard captures
    // the bare URL with queries; a strict boundary preserves all other paths.
    if (url.pathname !== BASE && !url.pathname.startsWith(`${BASE}/`)) {
      if (url.hostname.endsWith('.workers.dev') && url.pathname === '/') {
        url.pathname = `${BASE}/`;
        return Response.redirect(url, 308);
      }
      // The guide's existing origin is itself a routed Worker. A same-zone
      // global fetch bypasses that route, so use its explicit service binding.
      if (env.GUIDE_ROUTER) return env.GUIDE_ROUTER.fetch(request);
      return new Response('Not found', {status:404});
    }
    if (!['GET', 'HEAD'].includes(request.method)) {
      return new Response('Method not allowed', { status: 405, headers: { Allow: 'GET, HEAD' } });
    }
    if (url.pathname === BASE) {
      url.pathname += '/';
      return Response.redirect(url, 308);
    }
    const assetURL = new URL(request.url);
    let path = url.pathname.slice(BASE.length);
    if (path.endsWith('/')) path += 'index.html';
    else if (!path.split('/').at(-1).includes('.')) {
      url.pathname += '/';
      return Response.redirect(url, 308);
    }
    assetURL.pathname = path;
    const asset = await env.ASSETS.fetch(new Request(assetURL, request));
    let response = new Response(asset.body, asset);
    // Media files need Content-Length and Range support: browsers' media
    // pipeline stalls on streaming responses without them. Buffer these and
    // answer byte-range requests directly (files are a few MB at most).
    if (response.status === 200 && /\.(mp3|m4a|ogg|wav|mp4|webm)$/.test(path)) {
      const buf = await asset.arrayBuffer();
      const mediaHeaders = new Headers(asset.headers);
      mediaHeaders.set('Accept-Ranges', 'bytes');
      const range = request.headers.get('Range');
      const match = range && range.match(/^bytes=(\d*)-(\d*)$/);
      if (match && (match[1] !== '' || match[2] !== '')) {
        let start = match[1] === '' ? Math.max(0, buf.byteLength - parseInt(match[2], 10)) : parseInt(match[1], 10);
        let end = match[2] === '' || match[1] === '' ? buf.byteLength - 1 : Math.min(parseInt(match[2], 10), buf.byteLength - 1);
        if (start > end || start >= buf.byteLength) {
          return new Response(null, { status: 416, headers: { 'Content-Range': `bytes */${buf.byteLength}` } });
        }
        mediaHeaders.set('Content-Range', `bytes ${start}-${end}/${buf.byteLength}`);
        mediaHeaders.set('Content-Length', String(end - start + 1));
        response = new Response(buf.slice(start, end + 1), { status: 206, headers: mediaHeaders });
      } else {
        mediaHeaders.set('Content-Length', String(buf.byteLength));
        response = request.method === 'HEAD'
          ? new Response(null, { status: 200, headers: mediaHeaders })
          : new Response(buf, { status: 200, headers: mediaHeaders });
      }
    }
    if (response.status === 404) {
      assetURL.pathname = '/404.html';
      const missing = await env.ASSETS.fetch(new Request(assetURL, request));
      response = new Response(missing.body, { status: 404, headers: missing.headers });
    }
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    response.headers.set('X-Frame-Options', 'SAMEORIGIN');
    response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
    response.headers.set('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; font-src 'self'; base-uri 'self'; frame-ancestors 'self'; form-action 'none'");
    response.headers.set('Cache-Control', path.endsWith('.html') ? 'no-cache' : 'public, max-age=300');
    if (response.status === 200 && path.startsWith('/downloads/')) {
      const filename = path.split('/').at(-1).replace(/[^a-zA-Z0-9._-]/g, '_');
      response.headers.set('Content-Disposition', `attachment; filename="${filename}"`);
      response.headers.set('Content-Type', filename.endsWith('.md')
        ? 'text/markdown; charset=utf-8' : 'text/plain; charset=utf-8');
    }
    return response;
  }
};
