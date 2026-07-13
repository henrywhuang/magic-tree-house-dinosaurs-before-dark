const CHAPTERS = [
  'Into the Woods','The Monster','Where Is Here?','Henry','Gold in the Grass',
  'Dinosaur Valley','Ready, Steady, Go!','A Giant Shadow','The Amazing Ride','Home Before Dark'
];
const AUDIO_STARTS=[37.06,0,0,0,0,0,0,0,0,0];
const state={chapter:0,page:0,pages:[],scenes:[],words:[],view:'home',lockedWord:null,completed:new Set(JSON.parse(localStorage.getItem('mth-complete')||'[]'))};
const $=s=>document.querySelector(s); const audio=$('#audio');
const els={home:$('#homeView'),reader:$('#readerView'),exercise:$('#exerciseView'),player:$('#player'),nav:$('#chapterNav'),sidebar:$('#sidebar'),scrim:$('#scrim'),story:$('#storyText'),card:$('#wordCard')};
let currentUtterance=null,resumeBookAfterSpeech=false,englishVoices=[];
const pronunciationAudio=new Audio();
pronunciationAudio.preload='auto';
let pronunciationEndTime=0;
let pronunciationMode='idle',pronunciationFallbackItem=null;

function loadEnglishVoices(){if(!('speechSynthesis' in window))return;englishVoices=speechSynthesis.getVoices().filter(v=>/^en([-_]|$)/i.test(v.lang));}
function pronunciationStatus(text,isError=false){const el=$('#pronunciationStatus');el.textContent=text;el.classList.toggle('error',isError)}
function finishPronunciation(message,isError=false){pronunciationAudio.pause();pronunciationMode='idle';$('#speakWord').classList.remove('speaking');currentUtterance=null;pronunciationStatus(message,isError);if(resumeBookAfterSpeech&&audio.src&&audio.paused)audio.play().catch(()=>{});resumeBookAfterSpeech=false}
function speakWithSystemVoice(word){
  if(!('speechSynthesis' in window)||!('SpeechSynthesisUtterance' in window)){finishPronunciation('当前浏览器无法播放发音',true);return}
  speechSynthesis.cancel();loadEnglishVoices();
  const utterance=new SpeechSynthesisUtterance(word);currentUtterance=utterance;
  utterance.lang='en-US';utterance.rate=.78;utterance.pitch=1;utterance.volume=1;
  utterance.voice=englishVoices.find(v=>/samantha|ava|serena|daniel|google us english/i.test(v.name))||englishVoices.find(v=>/^en-US/i.test(v.lang))||englishVoices[0]||null;
  utterance.onstart=()=>{$('#speakWord').classList.add('speaking');pronunciationStatus(`正在朗读 ${word}…`)};
  utterance.onend=()=>finishPronunciation('发音已播放 · 可再次点击');
  utterance.onerror=e=>{if(e.error!=='canceled'&&e.error!=='interrupted')finishPronunciation('系统发音启动失败，请检查设备静音设置',true)};
  pronunciationStatus(`正在启动 ${word} 的备用发音…`);
  setTimeout(()=>speechSynthesis.speak(utterance),60);
}
function wordAudioPath(word){return `assets/audio/words/${encodeURIComponent(word.toLowerCase())}.mp3`}
function playBookWordFallback(word,item){
  if(!item||!Number.isFinite(item.start)||!Number.isFinite(item.end)){speakWithSystemVoice(word);return}
  pronunciationMode='book';pronunciationFallbackItem=item;
  const start=Math.max(0,item.start-.08);pronunciationEndTime=Math.max(item.end+.14,start+.32);
  pronunciationAudio.src=audioPath(state.chapter);
  const seekAndPlay=()=>{pronunciationAudio.currentTime=start;pronunciationAudio.play().catch(()=>speakWithSystemVoice(word))};
  if(pronunciationAudio.readyState>=1)seekAndPlay();else pronunciationAudio.addEventListener('loadedmetadata',seekAndPlay,{once:true});
  pronunciationStatus(`AI 发音加载失败，正在播放 ${word} 的原版发音…`);
}
function pronounceCurrentWord(event){
  event.preventDefault();event.stopPropagation();
  const word=$('#cardWord').textContent.trim();
  if(!word)return;
  resumeBookAfterSpeech=resumeBookAfterSpeech||!audio.paused;if(!audio.paused)audio.pause();
  pronunciationAudio.pause();
  if('speechSynthesis' in window)speechSynthesis.cancel();
  const item=state.words[Number(els.card.dataset.wordIndex)];
  pronunciationMode='qwen';pronunciationFallbackItem=item;pronunciationEndTime=0;
  pronunciationAudio.src=wordAudioPath(word);
  pronunciationStatus(`正在播放 ${word} 的 Qwen3-TTS 标准发音…`);
  $('#speakWord').classList.add('speaking');
  pronunciationAudio.play().catch(()=>playBookWordFallback(word,item));
}
pronunciationAudio.ontimeupdate=()=>{if(pronunciationMode==='book'&&pronunciationEndTime&&pronunciationAudio.currentTime>=pronunciationEndTime)finishPronunciation('原版发音已播放 · 可再次点击')};
pronunciationAudio.onended=()=>finishPronunciation(pronunciationMode==='qwen'?'Qwen3-TTS 发音已播放 · 可再次点击':'原版发音已播放 · 可再次点击');
pronunciationAudio.onerror=()=>{const word=$('#cardWord').textContent.trim();if(!word)return;if(pronunciationMode==='qwen')playBookWordFallback(word,pronunciationFallbackItem);else speakWithSystemVoice(word)};
loadEnglishVoices();if('speechSynthesis' in window)speechSynthesis.addEventListener?.('voiceschanged',loadEnglishVoices);

function chapterRoman(n){return ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN'][n-1]}
function audioPath(i){return `assets/audio/chapter-${String(i+1).padStart(2,'0')}.mp3`}
function renderNav(){els.nav.innerHTML=CHAPTERS.map((title,i)=>`<div class="chapter-block"><button class="chapter-link ${state.view==='reader'&&state.chapter===i?'active':''}" data-chapter="${i}"><strong>${i+1}</strong><span>${title}</span><small>${state.completed.has(i)?'✓ 已完成':'Chapter '+chapterRoman(i+1)}</small></button><button class="practice-link" data-practice="${i}">章节练习</button></div>`).join('')}
function setView(view){state.view=view;els.home.classList.toggle('hidden',view!=='home');els.reader.classList.toggle('hidden',view!=='reader');els.exercise.classList.toggle('hidden',view!=='exercise');els.player.classList.toggle('hidden',view!=='reader');$('.home-link').classList.toggle('active',view==='home');closeMenu();renderNav();window.scrollTo({top:0,behavior:'smooth'})}
async function openChapter(i,keepTime=false){state.chapter=i;state.page=0;setView('reader');$('#chapterNumber').textContent=i+1;$('#chapterLabel').textContent=`CHAPTER ${chapterRoman(i+1)}`;$('#chapterKicker').textContent=`CHAPTER ${chapterRoman(i+1)}`;$('#chapterTitle').textContent=CHAPTERS[i];$('#trackTitle').textContent=`Chapter ${i+1} · ${CHAPTERS[i]}`;try{const r=await fetch(`data/chapter-${String(i+1).padStart(2,'0')}.json`);if(!r.ok)throw 0;const d=await r.json();state.words=d.words||[];state.pages=d.pages||[];state.scenes=d.scenes||[];}catch{state.words=[];state.scenes=[];state.pages=[[{text:'正文与逐词时间戳正在生成，请稍后刷新页面。',words:[]}]]}renderPage();if(!keepTime){audio.src=audioPath(i);audio.load()}updateProgress()}
function renderPage(){const page=state.pages[state.page]||[],scene=state.scenes[state.page]||[];els.story.innerHTML=page.map(p=>`<p>${(p.words||[]).map(w=>`<span class="word ${w.key?'key-word':''}" data-index="${w.i}" data-word="${escapeHTML(w.word)}">${escapeHTML(w.before||'')}${escapeHTML(w.word)}${escapeHTML(w.after||'')}</span>`).join('')||escapeHTML(p.text||'')}</p>`).join('');const [sceneTitle='',sceneImage='assets/images/prehistoric-adventure.png',sceneAlt='杰克和安妮的史前探险场景']=$sceneTuple(scene);$('#sceneImage').src=sceneImage;$('#sceneImage').alt=sceneAlt;$('#sceneTitle').textContent=sceneTitle||`第 ${state.page+1} 个场景`;$('#pageLabel').textContent=`场景 ${state.page+1} / ${state.pages.length} · ${sceneTitle}`;$('#prevPage').disabled=state.page===0;$('#nextPage').disabled=state.page>=state.pages.length-1}
function $sceneTuple(scene){return Array.isArray(scene)?scene:[scene.title,scene.image,scene.alt]}
function escapeHTML(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function formatTime(s){s=Math.max(0,Math.floor(s||0));return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`}
function tick(){if(!audio.duration)return;const start=AUDIO_STARTS[state.chapter];$('#currentTime').textContent=formatTime(audio.currentTime-start);$('#duration').textContent=formatTime(audio.duration-start);$('#seek').value=Math.round((audio.currentTime-start)/(audio.duration-start)*1000);const idx=findWord(audio.currentTime);if(idx<0)return;const w=state.words[idx];const changedPage=w.page!==state.page;if(changedPage){state.page=w.page;renderPage()}document.querySelectorAll('.word.spoken,.word.spoken-sentence').forEach(x=>x.classList.remove('spoken','spoken-sentence'));const active=document.querySelector(`.word[data-index="${idx}"]`);if(active){let a=idx,b=idx;while(a>0&&!/[.!?]/.test(state.words[a-1].after||''))a--;while(b<state.words.length-1&&!/[.!?]/.test(state.words[b].after||''))b++;for(let j=a;j<=b;j++)document.querySelector(`.word[data-index="${j}"]`)?.classList.add('spoken-sentence');active.classList.add('spoken');const r=active.getBoundingClientRect();if(changedPage||r.top<95||r.bottom>innerHeight-120)active.scrollIntoView({block:'center',behavior:'smooth'})}}
function findWord(t){let lo=0,hi=state.words.length-1,best=-1;while(lo<=hi){const m=(lo+hi)>>1;if(state.words[m].start<=t){best=m;lo=m+1}else hi=m-1}return best}
function togglePlay(){if(audio.paused)audio.play();else audio.pause()}
function showWordCard(target,lock=false){const word=(target.dataset.word||'').replace(/[^A-Za-z'-]/g,'');if(!word)return;const rect=target.getBoundingClientRect();const entry=(window.WORDS||{})[word.toLowerCase()]||{};$('#cardWord').textContent=word;els.card.dataset.wordIndex=target.dataset.index;$('#cardPhonetic').textContent=entry.phonetic||phoneticFallback(word);$('#cardMeaning').textContent=entry.meaning||'专有名词或变形词，请结合上下文理解';pronunciationStatus('点击喇叭听 Qwen3-TTS 标准发音');els.card.classList.remove('hidden');const left=Math.min(innerWidth-300,Math.max(12,rect.left));const top=Math.min(innerHeight-210,rect.bottom+12);els.card.style.left=`${left}px`;els.card.style.top=`${Math.max(10,top)}px`;if(lock)state.lockedWord=target}
function phoneticFallback(word){return `/ ${word.toLowerCase()} /`}
function hideCard(){els.card.classList.add('hidden');state.lockedWord=null}
function showExercise(i){state.chapter=i;setView('exercise');$('#exerciseTitle').textContent=`第${i+1}章 · ${CHAPTERS[i]} · 章节练习`;$('#exerciseContent').innerHTML=`<div class="pending-box"><span>📝</span><h3>练习题原稿待导入</h3><p>当前项目目录中未发现《勇闯恐龙谷》的 Word / PDF 练习文件。<br>提供文件后，这里将按原稿生成可作答、可判对错、可返回原文的互动题。</p><button class="primary-button" id="exerciseBackInline">返回原文找答案</button></div>`;$('#exerciseBackInline').onclick=()=>openChapter(i,true)}
function updateProgress(){const pct=Math.round(state.completed.size/CHAPTERS.length*100);$('#progressLabel').textContent=`学习进度 ${pct}%`;$('#progressBar').style.width=pct+'%'}
function openMenu(){els.sidebar.classList.add('open');els.scrim.classList.add('show')} function closeMenu(){els.sidebar.classList.remove('open');els.scrim.classList.remove('show')}

$('#startButton').onclick=()=>openChapter(0);$('#brandButton').onclick=()=>setView('home');$('#backHome').onclick=()=>setView('home');$('#menuButton').onclick=openMenu;$('#closeMenu').onclick=closeMenu;els.scrim.onclick=closeMenu;$('.home-link').onclick=()=>setView('home');
els.nav.onclick=e=>{const c=e.target.closest('[data-chapter]'),p=e.target.closest('[data-practice]');if(c)openChapter(+c.dataset.chapter);if(p)showExercise(+p.dataset.practice)};$('#exerciseButton').onclick=()=>showExercise(state.chapter);$('#backToReading').onclick=()=>openChapter(state.chapter,true);$('#playButton').onclick=()=>{hideCard();togglePlay()};audio.defaultPlaybackRate=audio.playbackRate=.9;audio.onplay=()=>$('#playButton').textContent='❚❚';audio.onpause=()=>$('#playButton').textContent='▶';audio.ontimeupdate=tick;audio.onended=()=>{state.completed.add(state.chapter);localStorage.setItem('mth-complete',JSON.stringify([...state.completed]));updateProgress();renderNav()};audio.onloadedmetadata=()=>{const start=AUDIO_STARTS[state.chapter];if(audio.currentTime<start)audio.currentTime=start;audio.playbackRate=+document.querySelector('.speed-group button.active').dataset.speed;$('#duration').textContent=formatTime(audio.duration-start)};$('#seek').oninput=e=>{if(audio.duration){const start=AUDIO_STARTS[state.chapter];audio.currentTime=start+e.target.value/1000*(audio.duration-start)}};
document.querySelector('.speed-group').onclick=e=>{const b=e.target.closest('[data-speed]');if(!b)return;audio.playbackRate=+b.dataset.speed;document.querySelectorAll('.speed-group button').forEach(x=>x.classList.toggle('active',x===b))};
$('#prevPage').onclick=()=>{if(state.page>0){state.page--;renderPage()}};$('#nextPage').onclick=()=>{if(state.page<state.pages.length-1){state.page++;renderPage()}};
els.story.addEventListener('mouseover',e=>{const w=e.target.closest('.word');if(w&&!state.lockedWord)showWordCard(w)});els.story.addEventListener('mouseout',()=>{if(!state.lockedWord)els.card.classList.add('hidden')});els.story.addEventListener('click',e=>{const w=e.target.closest('.word');if(w){e.stopPropagation();showWordCard(w,true)}});$('#wordClose').onclick=hideCard;document.addEventListener('click',e=>{if(!e.target.closest('.word-card')&&!e.target.closest('.word'))hideCard()});$('#speakWord').addEventListener('click',pronounceCurrentWord);
renderNav();updateProgress();
