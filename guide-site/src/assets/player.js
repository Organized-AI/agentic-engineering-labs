// Chapter audio player. Self-contained, CSP-safe, no dependencies.
(function(){
  const players=[...document.querySelectorAll('[data-audio-player]')];
  if(!players.length)return;
  const fmt=s=>{if(!isFinite(s))return'--:--';s=Math.round(s);return Math.floor(s/60)+':'+String(s%60).padStart(2,'0');};
  const speeds=[1,1.25,1.5,2];
  players.forEach(el=>{
    const audio=new Audio(el.dataset.src);audio.preload='metadata';
    const play=el.querySelector('[data-audio-play]');
    const seek=el.querySelector('[data-audio-seek]');
    const cur=el.querySelector('[data-audio-current]');
    const dur=el.querySelector('[data-audio-duration]');
    const speed=el.querySelector('[data-audio-speed]');
    let speedIdx=0;
    audio.addEventListener('loadedmetadata',()=>{dur.textContent=fmt(audio.duration);});
    audio.addEventListener('timeupdate',()=>{cur.textContent=fmt(audio.currentTime);if(isFinite(audio.duration)&&audio.duration>0)seek.value=Math.round(audio.currentTime/audio.duration*1000);});
    audio.addEventListener('play',()=>{players.forEach(o=>{if(o!==el&&o._audio)o._audio.pause();});play.textContent='❚❚';play.setAttribute('aria-label','Pause');});
    audio.addEventListener('pause',()=>{play.textContent='▶';play.setAttribute('aria-label','Play');});
    audio.addEventListener('ended',()=>{
      const next=el.closest('[data-audio-chapter]')?.nextElementSibling?.querySelector('[data-audio-player]');
      if(next){next.scrollIntoView({behavior:'smooth',block:'center'});next._audio.play();}
    });
    el._audio=audio;
    play.addEventListener('click',()=>{audio.paused?audio.play():audio.pause();});
    seek.addEventListener('input',()=>{if(isFinite(audio.duration))audio.currentTime=seek.value/1000*audio.duration;});
    speed.addEventListener('click',()=>{speedIdx=(speedIdx+1)%speeds.length;audio.playbackRate=speeds[speedIdx];speed.textContent=speeds[speedIdx]+'×';});
  });
})();
