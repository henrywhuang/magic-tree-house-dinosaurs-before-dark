const BOOKS = [
  {
    id:'book-01', number:1, title:'Dinosaurs Before Dark', cn:'勇闯恐龙谷',
    chapters:['Into the Woods','The Monster','Where Is Here?','Henry','Gold in the Grass','Dinosaur Valley','Ready, Steady, Go!','A Giant Shadow','The Amazing Ride','Home Before Dark'],
    audioStarts:[37.06,0,0,0,0,0,0,0,0,0],
    audio:i=>`assets/audio/chapter-${String(i+1).padStart(2,'0')}.mp3`,
    data:i=>`data/chapter-${String(i+1).padStart(2,'0')}.json`
  },
  {
    id:'book-02', number:2, title:'The Knight at Dawn', cn:'古堡惊魂夜',
    chapters:['The Dark Woods','Leaving Again','Across the Bridge','Into the Castle','Trapped','Ta-da!','A Secret Passage','The Knight','Under the Moon','One Mystery Solved'],
    audioStarts:[0,0,0,0,0,0,0,0,0,0],
    audio:i=>`assets/audio/book-02-chapter-${String(i+1).padStart(2,'0')}.mp3`,
    data:i=>`data/book-02-chapter-${String(i+1).padStart(2,'0')}.json`
  }
];

function readStoredJSON(key,fallback){try{return JSON.parse(localStorage.getItem(key)||'null')??fallback}catch{return fallback}}
const savedComplete=readStoredJSON('mth-complete',[]).map(x=>typeof x==='number'?`0-${x}`:String(x));
const quizStore=readStoredJSON('mth-quiz-v1',{});
const state={book:0,chapter:0,page:0,pages:[],scenes:[],words:[],view:'home',lockedWord:null,completed:new Set(savedComplete),questionBank:null,quiz:null,debugTab:'skills'};
const $=s=>document.querySelector(s); const audio=$('#audio');
const els={home:$('#homeView'),reader:$('#readerView'),exercise:$('#exerciseView'),debug:$('#debugView'),player:$('#player'),nav:$('#chapterNav'),sidebar:$('#sidebar'),scrim:$('#scrim'),story:$('#storyText'),card:$('#wordCard')};
let chapterRequestId=0;
let resumeBookAfterPronunciation=false;
const pronunciationAudio=new Audio();
pronunciationAudio.preload='auto';

function currentBook(){return BOOKS[state.book]}
function completionKey(chapter=state.chapter,book=state.book){return `${book}-${chapter}`}
function chapterRoman(n){return ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN'][n-1]}
function audioPath(i=state.chapter,bookIndex=state.book){return BOOKS[bookIndex].audio(i)}
function dataPath(i=state.chapter,bookIndex=state.book){return BOOKS[bookIndex].data(i)}
function audioStart(){return Number.isFinite(state.words[0]?.start)?state.words[0].start:(currentBook().audioStarts[state.chapter]||0)}

function pronunciationStatus(text,isError=false){const el=$('#pronunciationStatus');el.textContent=text;el.classList.toggle('error',isError)}
function finishPronunciation(message,isError=false){pronunciationAudio.pause();$('#speakWord').classList.remove('speaking');pronunciationStatus(message,isError);if(resumeBookAfterPronunciation&&audio.src&&audio.paused)audio.play().catch(()=>{});resumeBookAfterPronunciation=false}
function wordAudioPath(word){return `assets/audio/words/${encodeURIComponent(word.toLowerCase())}.mp3`}
function pronounceCurrentWord(event){
  event.preventDefault();event.stopPropagation();
  const word=$('#cardWord').textContent.trim();if(!word)return;
  resumeBookAfterPronunciation=resumeBookAfterPronunciation||!audio.paused;if(!audio.paused)audio.pause();
  pronunciationAudio.pause();pronunciationAudio.currentTime=0;
  pronunciationAudio.src=wordAudioPath(word);pronunciationStatus(`正在播放 ${word} 的 Qwen3-TTS 标准发音…`);
  $('#speakWord').classList.add('speaking');pronunciationAudio.play().catch(()=>finishPronunciation('阿里 Qwen3-TTS 发音文件加载失败，请刷新后重试',true));
}
pronunciationAudio.onended=()=>finishPronunciation('阿里 Qwen3-TTS 发音已播放 · 可再次点击');
pronunciationAudio.onerror=()=>finishPronunciation('阿里 Qwen3-TTS 发音文件加载失败，请刷新后重试',true);

function renderNav(){
  const book=currentBook();
  const tabs=`<div class="book-tabs">${BOOKS.map((item,i)=>`<button class="book-tab ${state.book===i?'active':''}" data-book="${i}"><strong>BOOK ${item.number}</strong><span>${item.cn}</span></button>`).join('')}</div><p class="book-nav-title">${book.title}<small>《${book.cn}》</small></p>`;
  const chapters=book.chapters.map((title,i)=>{const result=quizStore[`${state.book}-${i}`];const practice=result?.completed?`练习 ${result.score}/5`:'章节练习';return `<div class="chapter-block"><button class="chapter-link ${state.view==='reader'&&state.chapter===i?'active':''}" data-chapter="${i}"><strong>${i+1}</strong><span>${title}</span><small>${state.completed.has(completionKey(i))?'✓ 已完成':'Chapter '+chapterRoman(i+1)}</small></button><button class="practice-link ${result?.completed?'complete':''}" data-practice="${i}">${practice}</button></div>`}).join('');
  els.nav.innerHTML=tabs+chapters;
}
function setView(view){state.view=view;els.home.classList.toggle('hidden',view!=='home');els.reader.classList.toggle('hidden',view!=='reader');els.exercise.classList.toggle('hidden',view!=='exercise');els.debug.classList.toggle('hidden',view!=='debug');els.player.classList.toggle('hidden',view!=='reader');$('.home-link').classList.toggle('active',view==='home');closeMenu();renderNav();window.scrollTo({top:0,behavior:'smooth'})}
function showHome(){document.title='Magic Tree House · 双册原著精读营';$('#brandSubtitle').textContent='双册原著精读营';setView('home')}
function setBook(bookIndex,openFirst=false){state.book=bookIndex;state.chapter=0;state.page=0;renderNav();if(openFirst)openChapter(0,false,bookIndex)}
async function openChapter(i,keepTime=false,bookIndex=state.book){
  const requestId=++chapterRequestId;
  const changedBook=state.book!==bookIndex;state.book=bookIndex;state.chapter=i;state.page=0;
  const book=currentBook();setView('reader');
  $('#chapterNumber').textContent=i+1;$('#chapterLabel').textContent=`BOOK ${book.number} · CHAPTER ${chapterRoman(i+1)}`;$('#chapterKicker').textContent=`BOOK ${book.number} · CHAPTER ${chapterRoman(i+1)}`;$('#chapterTitle').textContent=book.chapters[i];$('#trackTitle').textContent=`Book ${book.number} · Chapter ${i+1} · ${book.chapters[i]}`;$('#currentBookLabel').textContent=`BOOK ${book.number} · 《${book.cn}》`;$('#brandSubtitle').textContent=`Book ${book.number} · ${book.title}`;document.title=`${book.chapters[i]} · ${book.cn} · Magic Tree House`;
  try{const r=await fetch(`${dataPath(i,bookIndex)}?v=20260714`,{cache:'no-store'});if(!r.ok)throw 0;const d=await r.json();if(requestId!==chapterRequestId)return;state.words=d.words||[];state.pages=d.pages||[];state.scenes=d.scenes||[];}catch{if(requestId!==chapterRequestId)return;state.words=[];state.scenes=[];state.pages=[[{text:'本章正文加载失败，请检查网络后重试。',words:[]}]]}
  renderPage();
  if(!keepTime||changedBook){audio.pause();audio.src=audioPath(i,bookIndex);audio.load()}
  updateProgress();
}
function renderPage(){
  const page=state.pages[state.page]||[],scene=state.scenes[state.page]||[];
  els.story.innerHTML=page.map(p=>`<p>${(p.words||[]).map(w=>`<span class="word ${w.key?'key-word':''}" data-index="${w.i}" data-word="${escapeHTML(w.word)}">${escapeHTML(w.before||'')}${escapeHTML(w.word)}${escapeHTML(w.after||'')}</span>`).join('')||escapeHTML(p.text||'')}</p>`).join('');
  const [sceneTitle='',sceneImage='assets/images/prehistoric-adventure.png',sceneAlt='杰克和安妮的探险场景']=$sceneTuple(scene);
  $('#sceneImage').src=sceneImage;$('#sceneImage').alt=sceneAlt;$('#sceneTitle').textContent=sceneTitle||`第 ${state.page+1} 个场景`;$('#pageLabel').textContent=`场景 ${state.page+1} / ${state.pages.length} · ${sceneTitle}`;$('#prevPage').disabled=state.page===0;$('#nextPage').disabled=state.page>=state.pages.length-1;
}
function $sceneTuple(scene){return Array.isArray(scene)?scene:[scene.title,scene.image,scene.alt]}
function escapeHTML(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function formatTime(s){s=Math.max(0,Math.floor(s||0));return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`}
function tick(){
  if(!audio.duration)return;const start=audioStart(),duration=Math.max(.1,audio.duration-start),elapsed=Math.max(0,audio.currentTime-start);
  $('#currentTime').textContent=formatTime(elapsed);$('#duration').textContent=formatTime(duration);$('#seek').value=Math.max(0,Math.min(1000,Math.round(elapsed/duration*1000)));
  const idx=findWord(audio.currentTime);if(idx<0)return;const w=state.words[idx];const changedPage=w.page!==state.page;if(changedPage){state.page=w.page;renderPage()}
  document.querySelectorAll('.word.spoken,.word.spoken-sentence').forEach(x=>x.classList.remove('spoken','spoken-sentence'));
  const active=document.querySelector(`.word[data-index="${idx}"]`);if(active){let a=idx,b=idx;while(a>0&&!/[.!?]/.test(state.words[a-1].after||''))a--;while(b<state.words.length-1&&!/[.!?]/.test(state.words[b].after||''))b++;for(let j=a;j<=b;j++)document.querySelector(`.word[data-index="${j}"]`)?.classList.add('spoken-sentence');active.classList.add('spoken');const r=active.getBoundingClientRect();if(changedPage||r.top<95||r.bottom>innerHeight-120)active.scrollIntoView({block:'center',behavior:'smooth'})}
}
function findWord(t){let lo=0,hi=state.words.length-1,best=-1;while(lo<=hi){const m=(lo+hi)>>1;if(state.words[m].start<=t){best=m;lo=m+1}else hi=m-1}return best}
function togglePlay(){if(audio.paused)audio.play();else audio.pause()}
function showWordCard(target,lock=false){const word=(target.dataset.word||'').replace(/[^A-Za-z'-]/g,'');if(!word)return;const rect=target.getBoundingClientRect();const entry=(window.WORDS||{})[word.toLowerCase()]||{};$('#cardWord').textContent=word;els.card.dataset.wordIndex=target.dataset.index;$('#cardPhonetic').textContent=entry.phonetic||phoneticFallback(word);$('#cardMeaning').textContent=entry.meaning||'专有名词或变形词，请结合上下文理解';pronunciationStatus('点击喇叭听 Qwen3-TTS 标准发音');els.card.classList.remove('hidden');const left=Math.min(innerWidth-300,Math.max(12,rect.left));const top=Math.min(innerHeight-210,rect.bottom+12);els.card.style.left=`${left}px`;els.card.style.top=`${Math.max(10,top)}px`;if(lock)state.lockedWord=target}
function phoneticFallback(word){return `/ ${word.toLowerCase()} /`}
function hideCard(){els.card.classList.add('hidden');state.lockedWord=null}
async function loadQuestionBank(){
  if(state.questionBank)return state.questionBank;
  const r=await fetch('data/questions.json?v=20260714',{cache:'no-store'});if(!r.ok)throw new Error('题库加载失败');state.questionBank=await r.json();return state.questionBank;
}
function chapterQuestions(bookIndex=state.book,chapterIndex=state.chapter){return state.questionBank?.books?.[bookIndex]?.chapters?.[chapterIndex]?.questions||[]}
function persistQuiz(){const q=state.quiz;if(!q)return;const checkedCount=Object.keys(q.checked).length;const score=q.questions.filter(item=>q.checked[item.id]&&q.answers[item.id]===item.answer).length;quizStore[q.key]={answers:q.answers,checked:q.checked,index:q.index,completed:checkedCount===q.questions.length,score};localStorage.setItem('mth-quiz-v1',JSON.stringify(quizStore))}
async function showExercise(i){
  state.chapter=i;const book=currentBook();setView('exercise');document.title=`第${i+1}章练习 · ${book.cn} · Magic Tree House`;$('#exerciseTitle').textContent=`《${book.cn}》· 第${i+1}章 ${book.chapters[i]}`;$('#exerciseContent').innerHTML='<div class="quiz-loading"><span></span><p>正在准备 5 道阅读理解题…</p></div>';
  try{await loadQuestionBank();const questions=chapterQuestions();const key=`${state.book}-${i}`,saved=quizStore[key]||{};state.quiz={key,book:state.book,chapter:i,questions,index:Math.min(saved.index||0,questions.length-1),answers:saved.answers||{},checked:saved.checked||{},summary:false};renderQuiz()}catch(error){$('#exerciseContent').innerHTML=`<div class="quiz-error"><b>题库暂时没有加载成功</b><p>${escapeHTML(error.message)}</p><button class="primary-button" data-quiz-action="retry">重新加载</button></div>`}
}
function answerClass(q,letter){const selected=state.quiz.answers[q.id]===letter,checked=state.quiz.checked[q.id];if(!checked)return selected?'selected':'';if(letter===q.answer)return'correct';if(selected)return'wrong';return'dimmed'}
function renderQuiz(){
  const qz=state.quiz;if(!qz)return;if(qz.summary){renderQuizSummary();return}const q=qz.questions[qz.index],selected=qz.answers[q.id],checked=qz.checked[q.id];const progress=Math.round((qz.index+1)/qz.questions.length*100);
  $('#exerciseContent').innerHTML=`<div class="quiz-progress"><div><span>QUESTION ${qz.index+1} / ${qz.questions.length}</span><b>${progress}%</b></div><i><b style="width:${progress}%"></b></i></div><article class="quiz-card"><div class="quiz-meta"><span>${escapeHTML(q.standard)}</span><span>${escapeHTML(q.skill)}</span><span>DOK ${q.dok} · ${escapeHTML(q.difficulty)}</span></div><h2>${escapeHTML(q.stem)}</h2><div class="quiz-options" role="radiogroup" aria-label="选择答案">${Object.entries(q.options).map(([letter,text])=>`<button class="quiz-option ${answerClass(q,letter)}" data-answer="${letter}" role="radio" aria-checked="${selected===letter}" ${checked?'disabled':''}><b>${letter}</b><span>${escapeHTML(text)}</span><i>${checked&&letter===q.answer?'✓':checked&&selected===letter?'×':''}</i></button>`).join('')}</div>${checked?`<div class="quiz-feedback ${selected===q.answer?'is-correct':'is-wrong'}"><strong>${selected===q.answer?'✓ 回答正确':'再想一步：正确答案是 '+q.answer}</strong><p>${escapeHTML(q.rationale)}</p><details><summary>查看原文证据</summary>${q.evidence.map(item=>`<blockquote>${escapeHTML(item)}</blockquote>`).join('')}</details></div>`:''}</article><div class="quiz-actions"><button class="secondary-button" data-quiz-action="previous" ${qz.index===0?'disabled':''}>← 上一题</button>${checked?`<button class="primary-button" data-quiz-action="${qz.index===qz.questions.length-1?'summary':'next'}">${qz.index===qz.questions.length-1?'查看成绩':'下一题 →'}</button>`:`<button class="primary-button" data-quiz-action="check" ${selected?'':'disabled'}>确认答案</button>`}</div>`;
}
function renderQuizSummary(){const qz=state.quiz;const score=qz.questions.filter(q=>qz.answers[q.id]===q.answer).length;persistQuiz();renderNav();const note=score===5?'太棒了，已经能准确理解本章细节与深层含义。':score>=3?'掌握得不错，建议回看错题对应的原文证据。':'先别急着重做，带着错题回原文定位关键信息。';$('#exerciseContent').innerHTML=`<div class="quiz-summary"><div class="score-ring"><strong>${score}</strong><span>/ 5</span></div><span class="eyebrow">CHAPTER COMPLETE</span><h2>${score===5?'Perfect!':'本章练习完成'}</h2><p>${note}</p><div class="summary-actions"><button class="secondary-button" data-quiz-action="review">逐题复习</button><button class="primary-button" data-quiz-action="read">返回原文</button><button class="text-button" data-quiz-action="reset">重新作答</button></div></div>`}
function handleQuizAction(action){const qz=state.quiz;if(action==='retry'){state.questionBank=null;showExercise(state.chapter);return}if(action==='read'){openChapter(qz.chapter,true,qz.book);return}if(action==='review'){qz.summary=false;qz.index=0;renderQuiz();return}if(action==='reset'){qz.answers={};qz.checked={};qz.index=0;qz.summary=false;persistQuiz();renderQuiz();return}if(action==='previous'){qz.index=Math.max(0,qz.index-1)}if(action==='next'){qz.index=Math.min(qz.questions.length-1,qz.index+1)}if(action==='check'){const q=qz.questions[qz.index];if(qz.answers[q.id])qz.checked[q.id]=true}if(action==='summary'){qz.summary=true}persistQuiz();renderQuiz()}

const DEBUG_SKILLS=[
  {title:'Grade 5 Multilingual Reading Standards',cn:'五年级非母语阅读标准',path:'project-skills/grade5-multilingual-reading-standards/SKILL.md'},
  {title:'Grade 5 Literary Assessment Blueprint',cn:'文学阅读测评蓝图',path:'project-skills/grade5-literary-assessment-blueprint/SKILL.md'},
  {title:'Grade 5 Literary Item Writer',cn:'阅读理解命题规范',path:'project-skills/grade5-literary-item-writer/SKILL.md'}
];
async function showDebug(tab=state.debugTab){state.debugTab=tab;setView('debug');document.title='Developer Debug · Magic Tree House';$('#debugPanel').innerHTML='<div class="quiz-loading"><span></span><p>正在读取项目资料…</p></div>';try{await loadQuestionBank();const chapters=state.questionBank.books.reduce((n,b)=>n+b.chapters.length,0),questions=state.questionBank.books.reduce((n,b)=>n+b.chapters.reduce((m,c)=>m+c.questions.length,0),0);$('#debugStats').innerHTML=`<div><b>${DEBUG_SKILLS.length}</b><span>Skills</span></div><div><b>${state.questionBank.books.length}</b><span>Books</span></div><div><b>${chapters}</b><span>Chapters</span></div><div><b>${questions}</b><span>Questions</span></div>`;document.querySelectorAll('[data-debug-tab]').forEach(b=>b.classList.toggle('active',b.dataset.debugTab===tab));if(tab==='skills')await renderDebugSkills();if(tab==='questions')renderDebugQuestions();if(tab==='data')await renderDebugData()}catch(error){$('#debugPanel').innerHTML=`<div class="quiz-error"><b>Debug 数据读取失败</b><p>${escapeHTML(error.message)}</p></div>`}}
async function renderDebugSkills(){const contents=await Promise.all(DEBUG_SKILLS.map(async skill=>{try{const r=await fetch(`${skill.path}?v=20260714`,{cache:'no-store'});return r.ok?await r.text():'文件未找到'}catch{return'读取失败'}}));$('#debugPanel').innerHTML=`<div class="skill-grid">${DEBUG_SKILLS.map((skill,i)=>`<details class="skill-card" ${i===0?'open':''}><summary><span>SKILL ${i+1}</span><h2>${escapeHTML(skill.cn)}</h2><p>${escapeHTML(skill.title)}</p><code>${escapeHTML(skill.path)}</code></summary><pre>${escapeHTML(contents[i])}</pre></details>`).join('')}</div>`}
function allQuestions(){return state.questionBank.books.flatMap((book,bi)=>book.chapters.flatMap((chapter,ci)=>chapter.questions.map(q=>({...q,bookIndex:bi,chapterIndex:ci,bookTitle:book.book_title_cn,chapterTitle:chapter.chapter_title}))))}
function renderDebugQuestions(){const standards=[...new Set(allQuestions().map(q=>q.standard))].sort();$('#debugPanel').innerHTML=`<div class="question-tools"><select id="debugBook"><option value="all">全部册</option>${state.questionBank.books.map((b,i)=>`<option value="${i}">Book ${b.book} · ${escapeHTML(b.book_title_cn)}</option>`).join('')}</select><select id="debugChapter"><option value="all">全部章节</option>${Array.from({length:10},(_,i)=>`<option value="${i}">Chapter ${i+1}</option>`).join('')}</select><select id="debugStandard"><option value="all">全部标准</option>${standards.map(s=>`<option>${escapeHTML(s)}</option>`).join('')}</select><input id="debugSearch" type="search" placeholder="搜索题干、技能或标签…"><span id="debugResultCount"></span></div><div class="question-inspector" id="questionInspector"></div>`;['debugBook','debugChapter','debugStandard','debugSearch'].forEach(id=>$('#'+id).addEventListener('input',filterDebugQuestions));filterDebugQuestions()}
function filterDebugQuestions(){const book=$('#debugBook').value,chapter=$('#debugChapter').value,standard=$('#debugStandard').value,query=$('#debugSearch').value.trim().toLowerCase();const list=allQuestions().filter(q=>(book==='all'||q.bookIndex===+book)&&(chapter==='all'||q.chapterIndex===+chapter)&&(standard==='all'||q.standard===standard)&&(!query||[q.id,q.stem,q.skill,q.difficulty,q.standard].join(' ').toLowerCase().includes(query)));$('#debugResultCount').textContent=`${list.length} 题`;$('#questionInspector').innerHTML=list.map(q=>`<details class="question-debug-card"><summary><div><span>${q.id}</span><b>${escapeHTML(q.stem)}</b></div><i>${escapeHTML(q.bookTitle)} · Ch.${q.chapterIndex+1}</i></summary><div class="question-debug-body"><div class="quiz-meta"><span>${escapeHTML(q.standard)}</span><span>${escapeHTML(q.skill)}</span><span>DOK ${q.dok} · ${escapeHTML(q.difficulty)}</span></div><ol type="A">${Object.entries(q.options).map(([letter,text])=>`<li class="${letter===q.answer?'answer':''}">${escapeHTML(text)} ${letter===q.answer?'<b>✓ 正确答案</b>':''}</li>`).join('')}</ol><p><b>解析：</b>${escapeHTML(q.rationale)}</p><div><b>证据：</b>${q.evidence.map(e=>`<blockquote>${escapeHTML(e)}</blockquote>`).join('')}</div></div></details>`).join('')||'<div class="empty-state">没有符合筛选条件的题目。</div>'}
async function renderDebugData(){const checks=await Promise.all(BOOKS.flatMap((book,bi)=>book.chapters.map(async(title,ci)=>{try{const r=await fetch(`${dataPath(ci,bi)}?v=20260714`,{cache:'no-store'});if(!r.ok)throw new Error(String(r.status));const d=await r.json();return{ok:true,book:bi+1,chapter:ci+1,title,pages:d.pages?.length||0,scenes:d.scenes?.length||0,words:d.words?.length||0,questions:chapterQuestions(bi,ci).length}}catch(error){return{ok:false,book:bi+1,chapter:ci+1,title,error:error.message}}})));$('#debugPanel').innerHTML=`<div class="data-summary ${checks.every(x=>x.ok&&x.pages>1&&x.questions===5)?'healthy':'warning'}"><b>${checks.filter(x=>x.ok&&x.pages>1&&x.questions===5).length} / ${checks.length}</b><span>章节正文与题目检查通过</span></div><div class="data-grid">${checks.map(x=>`<article class="data-card ${x.ok&&x.pages>1&&x.questions===5?'ok':'bad'}"><span>${x.ok&&x.pages>1&&x.questions===5?'✓':'!'}</span><div><small>BOOK ${x.book} · CHAPTER ${x.chapter}</small><h3>${escapeHTML(x.title)}</h3>${x.ok?`<p>${x.pages} 页 · ${x.scenes} 场景 · ${x.words} 词 · ${x.questions} 题</p>`:`<p>加载失败：${escapeHTML(x.error)}</p>`}</div></article>`).join('')}</div>`}
function updateProgress(){const total=BOOKS.reduce((sum,book)=>sum+book.chapters.length,0);const pct=Math.round(state.completed.size/total*100);$('#progressLabel').textContent=`双册进度 ${state.completed.size}/${total}`;$('#progressBar').style.width=pct+'%'}
function openMenu(){els.sidebar.classList.add('open');els.scrim.classList.add('show')} function closeMenu(){els.sidebar.classList.remove('open');els.scrim.classList.remove('show')}

$('#startButton').onclick=()=>openChapter(0,false,0);$('#brandButton').onclick=showHome;$('#backHome').onclick=showHome;$('#menuButton').onclick=openMenu;$('#closeMenu').onclick=closeMenu;els.scrim.onclick=closeMenu;$('.home-link').onclick=showHome;
document.querySelector('.book-library').onclick=e=>{const button=e.target.closest('[data-book-start]');if(button)openChapter(0,false,+button.dataset.bookStart)};
els.nav.onclick=e=>{const b=e.target.closest('[data-book]'),c=e.target.closest('[data-chapter]'),p=e.target.closest('[data-practice]');if(b){const index=+b.dataset.book;if(state.view==='home')setBook(index,false);else openChapter(0,false,index);return}if(c)openChapter(+c.dataset.chapter);if(p)showExercise(+p.dataset.practice)};
$('#exerciseButton').onclick=()=>showExercise(state.chapter);$('#backToReading').onclick=()=>openChapter(state.chapter,true);$('#playButton').onclick=()=>{hideCard();togglePlay()};
$('#exerciseContent').onclick=e=>{const answer=e.target.closest('[data-answer]'),action=e.target.closest('[data-quiz-action]');if(answer&&state.quiz){const q=state.quiz.questions[state.quiz.index];if(!state.quiz.checked[q.id]){state.quiz.answers[q.id]=answer.dataset.answer;persistQuiz();renderQuiz()}}if(action)handleQuizAction(action.dataset.quizAction)};
$('#debugLink').onclick=()=>showDebug('skills');$('#debugBack').onclick=showHome;document.querySelector('.debug-tabs').onclick=e=>{const tab=e.target.closest('[data-debug-tab]');if(tab)showDebug(tab.dataset.debugTab)};
audio.defaultPlaybackRate=audio.playbackRate=.9;audio.onplay=()=>$('#playButton').textContent='❚❚';audio.onpause=()=>$('#playButton').textContent='▶';audio.ontimeupdate=tick;
audio.onended=()=>{state.completed.add(completionKey());localStorage.setItem('mth-complete',JSON.stringify([...state.completed]));updateProgress();renderNav()};
audio.onloadedmetadata=()=>{const start=audioStart();if(audio.currentTime<start)audio.currentTime=start;audio.playbackRate=+document.querySelector('.speed-group button.active').dataset.speed;$('#duration').textContent=formatTime(audio.duration-start)};
$('#seek').oninput=e=>{if(audio.duration){const start=audioStart();audio.currentTime=start+e.target.value/1000*(audio.duration-start)}};
document.querySelector('.speed-group').onclick=e=>{const b=e.target.closest('[data-speed]');if(!b)return;audio.playbackRate=+b.dataset.speed;document.querySelectorAll('.speed-group button').forEach(x=>x.classList.toggle('active',x===b))};
$('#prevPage').onclick=()=>{if(state.page>0){state.page--;renderPage()}};$('#nextPage').onclick=()=>{if(state.page<state.pages.length-1){state.page++;renderPage()}};
els.story.addEventListener('mouseover',e=>{const w=e.target.closest('.word');if(w&&!state.lockedWord)showWordCard(w)});els.story.addEventListener('mouseout',()=>{if(!state.lockedWord)els.card.classList.add('hidden')});els.story.addEventListener('click',e=>{const w=e.target.closest('.word');if(w){e.stopPropagation();showWordCard(w,true)}});$('#wordClose').onclick=hideCard;document.addEventListener('click',e=>{if(!e.target.closest('.word-card')&&!e.target.closest('.word'))hideCard()});$('#speakWord').addEventListener('click',pronounceCurrentWord);
renderNav();updateProgress();
