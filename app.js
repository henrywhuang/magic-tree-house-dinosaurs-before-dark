const BOOKS = [
  {
    id:'book-01', number:1, title:'Dinosaurs Before Dark', cn:'勇闯恐龙谷',
    chapters:['Into the Woods','The Monster','Where Is Here?','Henry','Gold in the Grass','Dinosaur Valley','Ready, Set, Go!','A Giant Shadow','The Amazing Ride','Home Before Dark'],
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
  },
  {
    id:'book-03', number:3, title:'Mummies in the Morning', cn:'木乃伊之谜',
    chapters:['Meow!','Oh, Man. Mummies!',"It's Alive!",'Back from the Dead','The Ghost-Queen','The Writing on the Wall','The Scroll','The Mummy','Follow the Leader','Another Clue'],
    audioStarts:[0,0,0,0,0,0,0,0,0,0],
    audio:i=>`assets/audio/book-03-chapter-${String(i+1).padStart(2,'0')}.mp3`,
    data:i=>`data/book-03-chapter-${String(i+1).padStart(2,'0')}.json`
  },
  {
    id:'book-04', number:4, title:'Pirates Past Noon', cn:'加勒比海盗',
    chapters:['Too Late!','The Bright Blue Sea','Three Men in a Boat','Vile Booty',"The Kid's Treasure","The Whale's Eye","Gale's a-Blowin'",'Dig, Dogs, Dig','The Mysterious M','Treasure Again'],
    audioStarts:[0,0,0,0,0,0,0,0,0,0],
    audio:i=>`assets/audio/book-04-chapter-${String(i+1).padStart(2,'0')}.mp3`,
    data:i=>`data/book-04-chapter-${String(i+1).padStart(2,'0')}.json`
  },
  {
    id:'book-05', number:5, title:'Night of the Ninjas', cn:'忍者的秘密',
    chapters:['Back into the Woods','The Open Book','E-hy!','Captured','Flames in the Mist','Shadow Warrior','To the East','Dragon Water','Mouse-walk',"'Night, Peanut"],
    audioStarts:[0,0,0,0,0,0,0,0,0,0],
    audio:i=>`assets/audio/book-05-chapter-${String(i+1).padStart(2,'0')}.mp3`,
    data:i=>`data/book-05-chapter-${String(i+1).padStart(2,'0')}.json`
  },
  {
    id:'book-06', number:6, title:'Afternoon on the Amazon', cn:'亚马孙探险',
    chapters:["Where's Peanut?",'Big Bugs','Yikes!','Millions of Them!','Pretty Fish','Monkey Trouble','Freeze!','Vampire Bats?','The Thing','Halfway There'],
    audioStarts:[0,0,0,0,0,0,0,0,0,0],
    audio:i=>`assets/audio/book-06-chapter-${String(i+1).padStart(2,'0')}.mp3`,
    data:i=>`data/book-06-chapter-${String(i+1).padStart(2,'0')}.json`
  }
];

function readStoredJSON(key,fallback){try{return JSON.parse(localStorage.getItem(key)||'null')??fallback}catch{return fallback}}
const savedComplete=readStoredJSON('mth-complete',[]).map(x=>typeof x==='number'?`0-${x}`:String(x));
const quizStore=readStoredJSON('mth-quiz-v1',{});
const addedStore=readStoredJSON('mth-added-vocab-v1',{});
const state={book:0,chapter:0,page:0,pages:[],scenes:[],words:[],view:'home',lockedWord:null,completed:new Set(savedComplete),questionBank:null,quiz:null,debugTab:'skills',vocabulary:null,vocabLesson:null};
const $=s=>document.querySelector(s); const audio=$('#audio');
const els={home:$('#homeView'),reader:$('#readerView'),exercise:$('#exerciseView'),vocabulary:$('#vocabularyView'),debug:$('#debugView'),player:$('#player'),nav:$('#chapterNav'),sidebar:$('#sidebar'),scrim:$('#scrim'),story:$('#storyText'),card:$('#wordCard')};
let chapterRequestId=0;
const pronunciationAudio=new Audio();
pronunciationAudio.preload='auto';
let activeTTS=null;

function currentBook(){return BOOKS[state.book]}
function completionKey(chapter=state.chapter,book=state.book){return `${book}-${chapter}`}
function chapterRoman(n){return ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN'][n-1]}
function audioPath(i=state.chapter,bookIndex=state.book){return BOOKS[bookIndex].audio(i)}
function dataPath(i=state.chapter,bookIndex=state.book){return BOOKS[bookIndex].data(i)}
function vocabularyPath(i=state.chapter,bookIndex=state.book){return `data/vocabulary-book-${String(bookIndex+1).padStart(2,'0')}-chapter-${String(i+1).padStart(2,'0')}.json`}
function audioStart(){return Number.isFinite(state.words[0]?.start)?state.words[0].start:(currentBook().audioStarts[state.chapter]||0)}
function hasVocabulary(bookIndex=state.book,chapterIndex=state.chapter){return bookIndex>=0&&bookIndex<BOOKS.length&&chapterIndex>=0&&chapterIndex<BOOKS[bookIndex].chapters.length}

function pronunciationStatus(text,isError=false){const el=$('#pronunciationStatus');el.textContent=text;el.classList.toggle('error',isError)}
function wordAudioPath(word){const key=String(word||'').toLowerCase().replace(/[^a-z'-]/g,'');return key?`assets/audio/words/${encodeURIComponent(key)}.mp3`:''}
function clearTTS(){pronunciationAudio.pause();pronunciationAudio.currentTime=0;activeTTS?.button?.classList.remove('speaking');activeTTS=null}
function finishTTS(isError=false){const current=activeTTS;if(!current)return;pronunciationAudio.pause();current.button?.classList.remove('speaking');if(current.showStatus)pronunciationStatus(isError?'音频加载失败，请刷新后重试':current.endMessage,isError);activeTTS=null}
function playTTS(path,button,{startMessage='正在播放…',endMessage='播放完毕 · 可再次点击',showStatus=false}={}){
  if(!path)return;if(!audio.paused)audio.pause();clearTTS();
  activeTTS={button,endMessage,showStatus};button?.classList.add('speaking');if(showStatus)pronunciationStatus(startMessage);
  pronunciationAudio.src=path;pronunciationAudio.load();pronunciationAudio.play().catch(()=>finishTTS(true));
}
function pronounceCurrentWord(event){
  event.preventDefault();event.stopPropagation();
  const word=els.card.dataset.audioWord||$('#cardWord').textContent.trim();if(!word)return;
  playTTS(wordAudioPath(word),$('#speakWord'),{startMessage:`正在播放 ${word} 的美式标准发音…`,endMessage:'单词发音已播放 · 可再次点击',showStatus:true});
}
function pronounceCurrentSentence(event){event.preventDefault();event.stopPropagation();playTTS(els.card.dataset.sentenceAudio,$('#speakSentence'),{startMessage:'正在播放原文例句…',endMessage:'原文例句已播放 · 可再次点击',showStatus:true})}
pronunciationAudio.onended=()=>finishTTS(false);
pronunciationAudio.onerror=()=>finishTTS(true);

function renderNav(){
  const book=currentBook();
  const tabs=`<div class="book-tabs">${BOOKS.map((item,i)=>`<button class="book-tab ${state.book===i?'active':''}" data-book="${i}"><strong>BOOK ${item.number}</strong><span>${item.cn}</span></button>`).join('')}</div><p class="book-nav-title">${book.title}<small>《${book.cn}》</small></p>`;
  const chapters=book.chapters.map((title,i)=>{const result=quizStore[`${state.book}-${i}`];const practice=result?.completed?`练习 ${result.score}/5`:'章节练习';return `<div class="chapter-block"><button class="chapter-link ${state.view==='reader'&&state.chapter===i?'active':''}" data-chapter="${i}"><strong>${i+1}</strong><span>${title}</span><small>${state.completed.has(completionKey(i))?'✓ 已完成':'Chapter '+chapterRoman(i+1)}</small></button><div class="chapter-actions"><button class="practice-link ${result?.completed?'complete':''} ${state.view==='exercise'&&state.chapter===i?'active':''}" data-practice="${i}">${practice}</button><button class="vocabulary-link ${state.view==='vocabulary'&&state.chapter===i?'active':''}" data-vocabulary="${i}">词汇学习</button></div></div>`}).join('');
  els.nav.innerHTML=tabs+chapters;
}
function setView(view){state.view=view;els.home.classList.toggle('hidden',view!=='home');els.reader.classList.toggle('hidden',view!=='reader');els.exercise.classList.toggle('hidden',view!=='exercise');els.vocabulary.classList.toggle('hidden',view!=='vocabulary');els.debug.classList.toggle('hidden',view!=='debug');els.player.classList.toggle('hidden',view!=='reader');$('.home-link').classList.toggle('active',view==='home');closeMenu();renderNav();window.scrollTo({top:0,behavior:'smooth'})}
function showHome(){document.title='Magic Tree House · 六册原著精读营';$('#brandSubtitle').textContent='六册原著精读营';setView('home')}
function setBook(bookIndex,openFirst=false){state.book=bookIndex;state.chapter=0;state.page=0;renderNav();if(openFirst)openChapter(0,false,bookIndex)}
async function openChapter(i,keepTime=false,bookIndex=state.book){
  const requestId=++chapterRequestId;
  const changedBook=state.book!==bookIndex;state.book=bookIndex;state.chapter=i;state.page=0;
  const book=currentBook();setView('reader');
  $('#chapterNumber').textContent=i+1;$('#chapterLabel').textContent=`BOOK ${book.number} · CHAPTER ${chapterRoman(i+1)}`;$('#chapterKicker').textContent=`BOOK ${book.number} · CHAPTER ${chapterRoman(i+1)}`;$('#chapterTitle').textContent=book.chapters[i];$('#trackTitle').textContent=`Book ${book.number} · Chapter ${i+1} · ${book.chapters[i]}`;$('#currentBookLabel').textContent=`BOOK ${book.number} · 《${book.cn}》`;$('#brandSubtitle').textContent=`Book ${book.number} · ${book.title}`;document.title=`${book.chapters[i]} · ${book.cn} · Magic Tree House`;
  try{const r=await fetch(`${dataPath(i,bookIndex)}?v=20260719-book6`,{cache:'no-store'});if(!r.ok)throw 0;const d=await r.json();if(requestId!==chapterRequestId)return;state.words=d.words||[];state.pages=d.pages||[];state.scenes=d.scenes||[];}catch{if(requestId!==chapterRequestId)return;state.words=[];state.scenes=[];state.pages=[[{text:'本章内容正在制作中，敬请期待～（若为已上线章节请检查网络后重试）',words:[]}]]}
  state.vocabulary=null;state.vocabLesson=null;
  if(hasVocabulary(bookIndex,i)){try{const r=await fetch(`${vocabularyPath(i,bookIndex)}?v=20260719-vocab-book6`,{cache:'no-store'});if(!r.ok)throw 0;const vocabulary=await r.json();if(requestId!==chapterRequestId)return;state.vocabulary=vocabulary}catch{state.vocabulary={words:[]}}}
  mergeAddedVocabulary(bookIndex,i);
  $('#vocabularyButton').classList.toggle('hidden',!state.vocabulary?.words?.length);
  renderPage();
  if(!keepTime||changedBook){audio.pause();audio.src=audioPath(i,bookIndex);audio.load()}
  updateProgress();
}
function renderPage(){
  const page=state.pages[state.page]||[],scene=state.scenes[state.page]||[];
  els.story.innerHTML=page.map(p=>`<p>${(p.words||[]).map(w=>{const vocab=findVocabByForm(w.word);return `<span class="word ${w.key?'key-word':''} ${vocab?'vocab-'+vocab.tier:''}" data-index="${w.i}" data-word="${escapeHTML(w.word)}" ${vocab?`data-vocab-id="${vocab.id}"`:''}>${escapeHTML(w.before||'')}${escapeHTML(w.word)}${escapeHTML(w.after||'')}</span>`}).join('')||escapeHTML(p.text||'')}</p>`).join('');
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
function normalizeWord(word){return String(word||'').toLowerCase().replace(/[^a-z'-]/g,'')}
function findVocabByForm(word){const normalized=normalizeWord(word);return state.vocabulary?.words?.find(item=>item.forms.some(form=>normalizeWord(form)===normalized))||null}
function vocabById(id){return state.vocabulary?.words?.find(item=>item.id===id)||null}
function showWordCard(target,lock=false){
  const sourceWord=(target.dataset.word||'').replace(/[^A-Za-z’'-]/g,'');if(!sourceWord)return;const normalized=normalizeWord(sourceWord),vocab=vocabById(target.dataset.vocabId)||findVocabByForm(sourceWord),dictionary=(window.WORDS||{})[normalized]||{};const displayWord=vocab?.word||sourceWord;
  const meaningText=vocab?.meaning||dictionary.meaning||'专有名词或变形词，请结合上下文理解';
  $('#cardWord').textContent=displayWord;els.card.dataset.wordIndex=target.dataset.index;els.card.dataset.audioWord=displayWord;els.card.dataset.sentenceAudio=vocab?.sentenceAudio||'';$('#cardPhonetic').textContent=vocab?.phonetic||dictionary.phonetic||phoneticFallback(displayWord);$('#cardMeaning').textContent=meaningText;
  $('#cardTier').textContent=vocab?(vocab.added?'MY WORD · 我的生词':vocab.tier==='core'?'CORE WORD · 核心掌握':'READING WORD · 阅读认识'):'WORD CARD';$('#cardPartOfSpeech').textContent=vocab?.partOfSpeech||'';$('#cardSourceForm').textContent=vocab&&normalizeWord(displayWord)!==normalized?`原文：${sourceWord}`:'';
  $('#cardForms').textContent=vocab?.wordForms||'';$('#cardFormsRow').classList.toggle('hidden',!vocab?.wordForms);$('#cardSentence').textContent=vocab?.sentence||'';$('#speakSentence').classList.toggle('hidden',!vocab?.sentenceAudio);$('#cardDetails').classList.toggle('hidden',!(vocab&&(vocab.wordForms||vocab.sentence)));
  const canAdd=!vocab&&!!dictionary.meaning,already=!!(vocab&&vocab.added);els.card.dataset.addWord=displayWord;els.card.dataset.addSource=sourceWord;els.card.dataset.addMeaning=meaningText;els.card.dataset.addPhonetic=$('#cardPhonetic').textContent;els.card.dataset.addSentence=readingSentence(target.dataset.index);
  $('#wordAddButton').classList.toggle('hidden',!(canAdd||already));if(canAdd||already)updateAddButton(already);
  pronunciationStatus(vocab?'单词和原文例句均可点击播放':canAdd?'可加入本章生词本 · 点击喇叭听发音':'点击喇叭听美式标准发音');
  els.card.classList.remove('hidden');const rect=target.getBoundingClientRect();if(innerWidth>650){const left=Math.min(innerWidth-310,Math.max(12,rect.left));const desiredTop=rect.bottom+12;const top=desiredTop+els.card.offsetHeight<innerHeight-12?desiredTop:rect.top-els.card.offsetHeight-12;els.card.style.left=`${left}px`;els.card.style.top=`${Math.max(78,top)}px`}if(lock)state.lockedWord=target;
}
function phoneticFallback(word){return `/ ${word.toLowerCase()} /`}
function hideCard(){if(activeTTS?.button?.closest('.word-card'))clearTTS();els.card.classList.add('hidden');state.lockedWord=null}
async function loadQuestionBank(){
  if(state.questionBank)return state.questionBank;
  const r=await fetch('data/questions.json?v=20260719-book6',{cache:'no-store'});if(!r.ok)throw new Error('题库加载失败');state.questionBank=await r.json();return state.questionBank;
}
function chapterQuestions(bookIndex=state.book,chapterIndex=state.chapter){return state.questionBank?.books?.[bookIndex]?.chapters?.[chapterIndex]?.questions||[]}
function persistQuiz(){const q=state.quiz;if(!q)return;const checkedCount=Object.keys(q.checked).length;const score=q.questions.filter(item=>q.checked[item.id]&&q.answers[item.id]===item.answer).length;quizStore[q.key]={answers:q.answers,checked:q.checked,index:q.index,completed:checkedCount===q.questions.length,score};localStorage.setItem('mth-quiz-v1',JSON.stringify(quizStore))}
async function showExercise(i){
  state.chapter=i;const book=currentBook();setView('exercise');document.title=`第${i+1}章练习 · ${book.cn} · Magic Tree House`;$('#exerciseTitle').textContent=`《${book.cn}》· 第${i+1}章 ${book.chapters[i]}`;$('#exerciseContent').innerHTML='<div class="quiz-loading"><span></span><p>正在准备 5 道阅读理解题…</p></div>';
  try{await loadQuestionBank();const questions=chapterQuestions();if(!questions.length){$('#exerciseContent').innerHTML=`<div class="pending-box"><span>📝</span><p>《${book.cn}》的章节练习正在制作中，敬请期待。</p></div>`;return}const key=`${state.book}-${i}`,saved=quizStore[key]||{};state.quiz={key,book:state.book,chapter:i,questions,index:Math.min(saved.index||0,questions.length-1),answers:saved.answers||{},checked:saved.checked||{},summary:false};renderQuiz()}catch(error){$('#exerciseContent').innerHTML=`<div class="quiz-error"><b>题库暂时没有加载成功</b><p>${escapeHTML(error.message)}</p><button class="primary-button" data-quiz-action="retry">重新加载</button></div>`}
}
function answerClass(q,letter){const selected=state.quiz.answers[q.id]===letter,checked=state.quiz.checked[q.id];if(!checked)return selected?'selected':'';if(letter===q.answer)return'correct';if(selected)return'wrong';return'dimmed'}
function renderQuiz(){
  const qz=state.quiz;if(!qz)return;if(qz.summary){renderQuizSummary();return}const q=qz.questions[qz.index],selected=qz.answers[q.id],checked=qz.checked[q.id];const progress=Math.round((qz.index+1)/qz.questions.length*100);
  $('#exerciseContent').innerHTML=`<div class="quiz-progress"><div><span>QUESTION ${qz.index+1} / ${qz.questions.length}</span><b>${progress}%</b></div><i><b style="width:${progress}%"></b></i></div><article class="quiz-card"><div class="quiz-meta"><span>${escapeHTML(q.standard)}</span><span>${escapeHTML(q.skill)}</span><span>DOK ${q.dok} · ${escapeHTML(q.difficulty)}</span></div><h2>${escapeHTML(q.stem)}</h2><div class="quiz-options" role="radiogroup" aria-label="选择答案">${Object.entries(q.options).map(([letter,text])=>`<button class="quiz-option ${answerClass(q,letter)}" data-answer="${letter}" role="radio" aria-checked="${selected===letter}" ${checked?'disabled':''}><b>${letter}</b><span>${escapeHTML(text)}</span><i>${checked&&letter===q.answer?'✓':checked&&selected===letter?'×':''}</i></button>`).join('')}</div>${checked?`<div class="quiz-feedback ${selected===q.answer?'is-correct':'is-wrong'}"><strong>${selected===q.answer?'✓ 回答正确':'再想一步：正确答案是 '+q.answer}</strong><p>${escapeHTML(q.rationale)}</p><details><summary>查看原文证据</summary>${q.evidence.map(item=>`<blockquote>${escapeHTML(item)}</blockquote>`).join('')}</details></div>`:''}</article><div class="quiz-actions"><button class="secondary-button" data-quiz-action="previous" ${qz.index===0?'disabled':''}>← 上一题</button>${checked?`<button class="primary-button" data-quiz-action="${qz.index===qz.questions.length-1?'summary':'next'}">${qz.index===qz.questions.length-1?'查看成绩':'下一题 →'}</button>`:`<button class="primary-button" data-quiz-action="check" ${selected?'':'disabled'}>确认答案</button>`}</div>`;
}
function renderQuizSummary(){const qz=state.quiz;const score=qz.questions.filter(q=>qz.answers[q.id]===q.answer).length;persistQuiz();renderNav();const note=score===5?'太棒了，已经能准确理解本章细节与深层含义。':score>=3?'掌握得不错，建议回看错题对应的原文证据。':'先别急着重做，带着错题回原文定位关键信息。';$('#exerciseContent').innerHTML=`<div class="quiz-summary"><div class="score-ring"><strong>${score}</strong><span>/ 5</span></div><span class="eyebrow">CHAPTER COMPLETE</span><h2>${score===5?'Perfect!':'本章练习完成'}</h2><p>${note}</p><div class="summary-actions"><button class="secondary-button" data-quiz-action="review">逐题复习</button><button class="primary-button" data-quiz-action="read">返回原文</button><button class="text-button" data-quiz-action="reset">重新作答</button></div></div>`}
function handleQuizAction(action){const qz=state.quiz;if(action==='retry'){state.questionBank=null;showExercise(state.chapter);return}if(action==='read'){openChapter(qz.chapter,true,qz.book);return}if(action==='review'){qz.summary=false;qz.index=0;renderQuiz();return}if(action==='reset'){qz.answers={};qz.checked={};qz.index=0;qz.summary=false;persistQuiz();renderQuiz();return}if(action==='previous'){qz.index=Math.max(0,qz.index-1)}if(action==='next'){qz.index=Math.min(qz.questions.length-1,qz.index+1)}if(action==='check'){const q=qz.questions[qz.index];if(qz.answers[q.id])qz.checked[q.id]=true}if(action==='summary'){qz.summary=true}persistQuiz();renderQuiz()}

function coreVocabulary(){return state.vocabulary?.words?.filter(item=>item.tier==='core')||[]}
function recognitionVocabulary(){return state.vocabulary?.words?.filter(item=>item.tier==='recognition')||[]}
function addedVocabulary(){return state.vocabulary?.words?.filter(item=>item.added)||[]}
function addedKey(b=state.book,c=state.chapter){return `${b}-${c}`}
function addedListFor(b=state.book,c=state.chapter){return addedStore[addedKey(b,c)]||[]}
function addedWordId(word){return 'u-'+normalizeWord(word)}
function persistAdded(){localStorage.setItem('mth-added-vocab-v1',JSON.stringify(addedStore))}
function mergeAddedVocabulary(b=state.book,c=state.chapter){if(!state.vocabulary)state.vocabulary={words:[]};if(!Array.isArray(state.vocabulary.words))state.vocabulary.words=[];state.vocabulary.words=state.vocabulary.words.filter(w=>!w.added);const have=new Set(state.vocabulary.words.map(w=>w.id));addedListFor(b,c).forEach(w=>{if(!have.has(w.id))state.vocabulary.words.push({...w,tier:'added',added:true})})}
function readingSentence(index){index=Number(index);if(!Number.isInteger(index)||!state.words[index])return '';let a=index,b=index;while(a>0&&!/[.!?]/.test(state.words[a-1].after||''))a--;while(b<state.words.length-1&&!/[.!?]/.test(state.words[b].after||''))b++;let s='';for(let j=a;j<=b;j++){const w=state.words[j];s+=(w.before||'')+w.word+(w.after||'')}return s.trim()}
function previewList(){const t=state.vocabLesson?.previewTier;return t==='recognition'?recognitionVocabulary():t==='added'?addedVocabulary():coreVocabulary()}
function toggleAddCurrentWord(){
  const word=els.card.dataset.addWord;if(!word)return;
  const key=addedKey(),id=addedWordId(word),list=addedStore[key]||(addedStore[key]=[]);
  const idx=list.findIndex(w=>w.id===id);let addedNow;
  if(idx>=0){list.splice(idx,1);if(!list.length)delete addedStore[key];addedNow=false}
  else{list.push({id,word,forms:[word,els.card.dataset.addSource].filter((v,i,a)=>v&&a.indexOf(v)===i),tier:'added',added:true,phonetic:els.card.dataset.addPhonetic||'',partOfSpeech:els.card.dataset.addPos||'',meaning:els.card.dataset.addMeaning||'',wordForms:'',sentence:els.card.dataset.addSentence||'',sentenceAudio:''});addedNow=true}
  persistAdded();mergeAddedVocabulary();updateAddButton(addedNow);
  pronunciationStatus(addedNow?'已加入本章生词本，可在「词汇学习 · 我的生词」复习':'已从本章生词本移除');
  $('#vocabularyButton').classList.toggle('hidden',!state.vocabulary?.words?.length);
  const span=document.querySelector(`.word[data-index="${els.card.dataset.wordIndex}"]`);if(span)span.classList.toggle('vocab-added',addedNow);
}
function updateAddButton(isAdded){const btn=$('#wordAddButton');if(!btn)return;btn.classList.toggle('is-added',!!isAdded);btn.textContent=isAdded?'✓ 已加入生词本 · 点此移除':'＋ 加入本章生词本'}
function freshVocabLesson(){return{screen:'preview',index:0,stage:'read',previewTier:'core',previewIndex:0,readResults:{},meaningResults:{},spellingResults:{},meaningChoice:null,meaningChecked:false,blendSlots:[],blendAttempted:false,blendSolved:false,spellingValue:'',spellingAttempts:0,spellingSolved:false}}
function showVocabulary(reset=false){
  const book=currentBook();audio.pause();clearTTS();hideCard();$('#vocabularyChapterMeta').textContent=`Book ${book.number} · Chapter ${state.chapter+1} · ${book.chapters[state.chapter]}`;setView('vocabulary');document.title=`第${state.chapter+1}章词汇学习 · ${book.cn}`;
  if(!state.vocabulary?.words?.length){state.vocabLesson=null;$('#vocabularyContent').innerHTML=`<div class="pending-box"><span>📚</span><p>《${book.cn}》第 ${state.chapter+1} 章的词汇学习内容正在准备中。</p></div>`;return}
  if(reset||!state.vocabLesson)state.vocabLesson=freshVocabLesson();renderVocabulary();
}
async function showChapterVocabulary(i,bookIndex=state.book){await openChapter(i,false,bookIndex);if(state.book===bookIndex&&state.chapter===i)showVocabulary(true)}
function vocabAudioButton(item,type='word',className='vocab-audio'){const label=type==='sentence'?`播放 ${item.word} 的原文例句`:`播放单词 ${item.word}`;return `<button class="${className}" type="button" data-vocab-audio="${type}" data-vocab-id="${item.id}" aria-label="${escapeHTML(label)}">${type==='sentence'?'▸':'🔊'}</button>`}
function focusAudioButton(item,type,label,icon){return `<button class="focus-audio-button" type="button" data-vocab-audio="${type}" data-vocab-id="${item.id}" aria-label="${escapeHTML(label+' '+item.word)}"><span>${icon}</span><b>${label}</b></button>`}
function renderVocabulary(){
  const lesson=state.vocabLesson;if(!lesson)return;clearTTS();
  if(lesson.screen==='preview'){renderVocabPreview();return}if(lesson.screen==='summary'){renderVocabSummary();return}renderVocabLesson();
}
function renderVocabPreview(){
  const lesson=state.vocabLesson,core=coreVocabulary(),recognition=recognitionVocabulary(),added=addedVocabulary();
  const tier=lesson.previewTier==='recognition'||lesson.previewTier==='added'?lesson.previewTier:'core';
  const list=tier==='recognition'?recognition:tier==='added'?added:core;
  lesson.previewIndex=Math.max(0,Math.min(lesson.previewIndex||0,Math.max(0,list.length-1)));const item=list[lesson.previewIndex];
  const tabs=`<div class="vocab-preview-tabs" role="tablist" aria-label="词汇分类"><button class="${tier==='core'?'active':''}" data-vocab-action="preview-core" role="tab" aria-selected="${tier==='core'}">核心掌握词 <b>${core.length}</b><small>会读 · 知意 · 会写</small></button><button class="${tier==='recognition'?'active':''}" data-vocab-action="preview-recognition" role="tab" aria-selected="${tier==='recognition'}">阅读认识词 <b>${recognition.length}</b><small>听懂 · 认得即可</small></button><button class="${tier==='added'?'active':''}" data-vocab-action="preview-added" role="tab" aria-selected="${tier==='added'}">我的生词 <b>${added.length}</b><small>阅读中收藏</small></button></div>`;
  let card;
  if(!item){card=tier==='added'?`<div class="vocab-empty"><span>📌</span><p>还没有收藏生词。<br>阅读时点开任意单词卡片，点「＋ 加入本章生词本」，生词就会出现在这里供复习。</p></div>`:`<div class="vocab-empty"><span>📚</span><p>本章暂无该类词汇。</p></div>`;}
  else{const label=tier==='core'?'CORE WORD · 核心词':tier==='added'?'MY WORD · 我的生词':'READING WORD · 认识词';
    card=`<article class="vocab-focus-card ${item.tier}"><header><span>${label}</span><b>${lesson.previewIndex+1} / ${list.length}</b></header><div class="focus-word-line"><div><h2>${escapeHTML(item.word)}</h2><p>${escapeHTML(item.phonetic||'')}</p></div><span>${escapeHTML(item.partOfSpeech||'')}</span></div><p class="focus-meaning">${escapeHTML(item.meaning||'')}</p>${item.wordForms?`<p class="focus-forms"><b>常见词形</b>${escapeHTML(item.wordForms)}</p>`:''}${item.sentence?`<blockquote>${escapeHTML(item.sentence)}</blockquote>`:''}<div class="focus-audio-actions">${focusAudioButton(item,'word','听单词','🔊')}${item.sentenceAudio?focusAudioButton(item,'sentence','听原句','▶'):''}${item.added?`<button class="focus-remove-button" type="button" data-vocab-action="remove-added"><span>✕</span><b>移除生词</b></button>`:''}</div><footer><button class="focus-nav-button" data-vocab-action="preview-prev" ${lesson.previewIndex===0?'disabled':''}>← 上一个</button><div class="focus-dots">${list.map((_,index)=>`<i class="${index===lesson.previewIndex?'active':''}"></i>`).join('')}</div><button class="focus-nav-button" data-vocab-action="preview-next" ${lesson.previewIndex>=list.length-1?'disabled':''}>下一个 →</button></footer></article>`;}
  $('#vocabularyContent').innerHTML=`<div class="vocab-preview-stage">${tabs}${card}<div class="vocab-start"><p>核心词进入五步练习；认识词与我的生词可点开听读复习。</p><button class="primary-button" data-vocab-action="start" ${core.length?'':'disabled'}>开始五步练习 <span>→</span></button></div></div>`;
}
function phonicsFor(item){return item.phonics?.length?item.phonics:[{letters:item.word,sound:item.phonetic,rule:'完整单词'}]}
function vocabProgress(lesson){const stages={read:0,meaning:1,split:2,blend:3,spell:4};return Math.round((lesson.index*5+stages[lesson.stage]+1)/(coreVocabulary().length*5)*100)}
function lessonHeader(item,lesson){const labels={read:'读一读',meaning:'懂词义',split:'拼读拆分',blend:'拼读组合',spell:'键盘拼写'};const pct=vocabProgress(lesson);return `<div class="vocab-lesson-progress"><div><span>核心词 ${lesson.index+1} / ${coreVocabulary().length} · ${labels[lesson.stage]}</span><b>${pct}%</b></div><i><b style="width:${pct}%"></b></i></div><div class="lesson-stepper five-steps"><span class="${lesson.stage==='read'?'active':''}">1 · 读一读</span><span class="${lesson.stage==='meaning'?'active':''}">2 · 懂词义</span><span class="${lesson.stage==='split'?'active':''}">3 · 拼读拆分</span><span class="${lesson.stage==='blend'?'active':''}">4 · 拼读组合</span><span class="${lesson.stage==='spell'?'active':''}">5 · 键盘拼写</span></div>`}
function phonicsMap(item){return `<div class="phonics-whole-word">${phonicsFor(item).map(part=>`<span>${escapeHTML(part.letters)}</span>`).join('')}</div><div class="phonics-map">${phonicsFor(item).map((part,index)=>`${index?'<i>+</i>':''}<div><strong>${escapeHTML(part.letters)}</strong><b>${escapeHTML(part.sound)}</b><small>${escapeHTML(part.rule)}</small></div>`).join('')}</div>`}
function shuffledPhonicsIndexes(item,index){const parts=phonicsFor(item),order=parts.map((_,i)=>i);if(order.length<2)return order;const shift=index%(order.length-1)+1;return order.slice(shift).concat(order.slice(0,shift))}
function ensureBlendSlots(item,lesson){const count=phonicsFor(item).length;if(!Array.isArray(lesson.blendSlots)||lesson.blendSlots.length!==count)lesson.blendSlots=Array(count).fill(null);return lesson.blendSlots}
function renderPhonicsPiece(part,index,source){return `<button class="phonics-piece" type="button" draggable="true" data-phonics-piece="${index}" data-phonics-source="${source}"><strong>${escapeHTML(part.letters)}</strong><small>${escapeHTML(part.sound)}</small></button>`}
function renderBlend(item,lesson){const parts=phonicsFor(item),slots=ensureBlendSlots(item,lesson),placed=new Set(slots.filter(value=>value!==null)),bank=shuffledPhonicsIndexes(item,lesson.index).filter(index=>!placed.has(index));return `<div class="blend-target" aria-label="单词拼组区">${slots.map((pieceIndex,slotIndex)=>`<div class="phonics-slot ${pieceIndex===null?'':'filled'}" data-phonics-slot="${slotIndex}">${pieceIndex===null?'<span>拖到这里</span>':renderPhonicsPiece(parts[pieceIndex],pieceIndex,'slot')}</div>`).join('')}</div><div class="phonics-bank" aria-label="待拼组的拼读块">${bank.map(index=>renderPhonicsPiece(parts[index],index,'bank')).join('')||'<span>拼读块已全部放入</span>'}</div><p class="blend-tip">拖到上方空格；触屏上也可依次点击拼读块。</p>${lesson.blendAttempted&&!lesson.blendSolved?'<div class="lesson-feedback try">顺序还不对，读一读每个拼读块再调整。</div>':''}${lesson.blendSolved?`<div class="lesson-feedback good">✓ ${escapeHTML(item.word)} 拼组正确，连起来读一遍。</div>`:''}`}
function spellingSlots(item,lesson){return `<div class="keyboard-spelling" aria-live="polite">${[...item.word].map((_,index)=>`<span class="${lesson.spellingValue[index]?'filled':''}">${lesson.spellingValue[index]?escapeHTML(lesson.spellingValue[index]):'&nbsp;'}</span>`).join('')}</div>`}
function spellingKeyboard(item){const active=new Set(item.word.toLowerCase()),rows=['qwertyuiop','asdfghjkl','zxcvbnm'];return `<div class="spelling-keyboard" aria-label="拼写键盘">${rows.map(row=>`<div>${[...row].map(letter=>`<button type="button" data-spelling-key="${letter}" class="${active.has(letter)?'needed':'muted'}" ${active.has(letter)?'':'disabled'}>${letter}</button>`).join('')}</div>`).join('')}<div class="keyboard-tools"><button type="button" data-vocab-action="keyboard-clear">清空</button><button type="button" data-vocab-action="keyboard-backspace">⌫ 删除</button></div></div>`}
function renderVocabLesson(){
  const lesson=state.vocabLesson,item=coreVocabulary()[lesson.index];if(!item){lesson.screen='summary';renderVocabSummary();return}const header=lessonHeader(item,lesson);let body='';
  if(lesson.stage==='read')body=`<article class="lesson-card"><small>STEP 1 · LISTEN & READ</small><h2>先听，再跟读</h2><p>听清重音和每个音节，可以重复播放。</p><div class="lesson-focus-word"><strong>${escapeHTML(item.word)}</strong><span>${escapeHTML(item.phonetic)} · ${escapeHTML(item.partOfSpeech)}</span></div><div class="lesson-audio-row">${vocabAudioButton(item,'word','lesson-audio-button')}${vocabAudioButton(item,'sentence','lesson-audio-button secondary')}</div><blockquote class="lesson-context">${escapeHTML(item.sentence)}</blockquote><div class="lesson-actions"><button class="text-button" data-vocab-action="preview">返回词表</button><button class="primary-button" data-vocab-action="read-done">我听清楚了 →</button></div></article>`;
  if(lesson.stage==='meaning'){const options=orderedMeaningOptions(item,lesson.index);body=`<article class="lesson-card"><small>STEP 2 · MEANING IN CONTEXT</small><h2>原句中的意思是什么？</h2><blockquote class="lesson-context">${escapeHTML(item.sentence)}</blockquote><div class="lesson-options">${options.map(option=>`<button class="lesson-option ${meaningOptionClass(option,item,lesson)}" data-vocab-meaning="${escapeHTML(option)}" ${lesson.meaningChecked?'disabled':''}>${escapeHTML(option)}</button>`).join('')}</div>${lesson.meaningChecked?`<div class="lesson-feedback ${lesson.meaningChoice===item.meaning?'good':'try'}">${lesson.meaningChoice===item.meaning?'✓ 理解正确。':'再看原句中的线索。正确意思是：'+escapeHTML(item.meaning)}</div>`:''}<div class="lesson-actions">${vocabAudioButton(item,'sentence','lesson-audio-button secondary')}${lesson.meaningChecked?'<button class="primary-button" data-vocab-action="meaning-next">看拼读拆分 →</button>':`<button class="primary-button" data-vocab-action="meaning-check" ${lesson.meaningChoice?'':'disabled'}>确认答案</button>`}</div></article>`}
  if(lesson.stage==='split')body=`<article class="lesson-card phonics-card"><small>STEP 3 · PHONICS BREAKDOWN</small><h2>按自然拼读拆开</h2><p>先看字母组合，再连起来读整个单词。</p>${phonicsMap(item)}<div class="lesson-audio-row">${vocabAudioButton(item,'word','lesson-audio-button')}</div><div class="lesson-actions"><button class="text-button" data-vocab-action="preview">返回词表</button><button class="primary-button" data-vocab-action="split-done">我会拆分了 →</button></div></article>`;
  if(lesson.stage==='blend')body=`<article class="lesson-card phonics-card"><small>STEP 4 · DRAG & BLEND</small><h2>拖拽拼成完整单词</h2><p>边读边排，把拼读块放到正确的位置。</p>${renderBlend(item,lesson)}<div class="lesson-actions"><button class="text-button" data-vocab-action="blend-reset">重新拼组</button><button class="primary-button" data-vocab-action="blend-next" ${lesson.blendSolved?'':'disabled'}>进入键盘拼写 →</button></div></article>`;
  if(lesson.stage==='spell'){const hasAttempt=lesson.spellingAttempts>0,complete=lesson.spellingValue.length===item.word.length;body=`<article class="lesson-card keyboard-card"><small>STEP 5 · KEYBOARD SPELLING</small><h2>点击键盘拼出单词</h2><p>单词需要的字母为深色，其他字母为灰色。按顺序点击，字母会浮入上方空格。</p><div class="keyboard-word-meta"><span>${escapeHTML(item.meaning)}</span>${vocabAudioButton(item,'word','lesson-audio-button')}</div>${spellingSlots(item,lesson)}${spellingKeyboard(item)}${hasAttempt&&!lesson.spellingSolved?`<div class="lesson-feedback try">顺序还需要调整。${spellingDiff(item.word,lesson.spellingValue)}</div>`:''}${lesson.spellingSolved?'<div class="lesson-feedback good">✓ 拼写正确，读音、词义和词形已经连在一起了。</div>':''}<div class="lesson-actions"><button class="text-button" data-vocab-action="preview">返回词表</button>${lesson.spellingSolved?`<button class="primary-button" data-vocab-action="word-next">${lesson.index===coreVocabulary().length-1?'查看本次结果':'学习下一个词 →'}</button>`:`<button class="primary-button" data-vocab-action="spelling-check" ${complete?'':'disabled'}>检查拼写</button>`}</div></article>`}
  $('#vocabularyContent').innerHTML=header+body;
}
function orderedMeaningOptions(item,index){const options=[...item.options],shift=(index*2+1)%options.length;return options.slice(shift).concat(options.slice(0,shift))}
function meaningOptionClass(option,item,lesson){if(!lesson.meaningChecked)return lesson.meaningChoice===option?'selected':'';if(option===item.meaning)return'correct';if(option===lesson.meaningChoice)return'wrong';return''}
function spellingDiff(answer,value){const typed=value.trim().toLowerCase();return `<div class="spelling-diff">${[...answer].map((letter,index)=>`<span class="${typed[index]===letter?'':'wrong'}">${escapeHTML(letter)}</span>`).join('')}</div>`}
function updateBlendResult(item,lesson){const slots=ensureBlendSlots(item,lesson);lesson.blendAttempted=slots.every(value=>value!==null);lesson.blendSolved=lesson.blendAttempted&&slots.every((value,index)=>value===index)}
function placePhonicsPiece(pieceIndex,slotIndex){const lesson=state.vocabLesson,item=coreVocabulary()[lesson?.index];if(!lesson||lesson.stage!=='blend'||!item)return;const slots=ensureBlendSlots(item,lesson),oldSlot=slots.indexOf(pieceIndex);if(oldSlot>=0)slots[oldSlot]=null;if(slotIndex>=0&&slotIndex<slots.length)slots[slotIndex]=pieceIndex;updateBlendResult(item,lesson);renderVocabulary()}
function clickPhonicsPiece(pieceIndex,source){const lesson=state.vocabLesson,item=coreVocabulary()[lesson?.index];if(!lesson||lesson.stage!=='blend'||!item)return;const slots=ensureBlendSlots(item,lesson);if(source==='slot'){const slot=slots.indexOf(pieceIndex);if(slot>=0)slots[slot]=null;updateBlendResult(item,lesson);renderVocabulary();return}const empty=slots.indexOf(null);if(empty>=0)placePhonicsPiece(pieceIndex,empty)}
function renderVocabSummary(){
  const lesson=state.vocabLesson,core=coreVocabulary(),meaning=Object.values(lesson.meaningResults).filter(Boolean).length,spelling=Object.values(lesson.spellingResults).filter(Boolean).length,read=Object.keys(lesson.readResults).length;
  $('#vocabularyContent').innerHTML=`<div class="vocab-summary"><span>🌱</span><h2>本次五步练习完成</h2><p>从听读、词义到拼读组合和键盘拼写，完成了一次完整记忆。</p><div class="vocab-result-grid"><div><b>${read}/${core.length}</b><span>完成听读</span></div><div><b>${meaning}/${core.length}</b><span>首次辨义正确</span></div><div><b>${spelling}/${core.length}</b><span>首次拼写正确</span></div></div><div class="review-schedule"><span>今天 · 已练习</span><span>第1天 · 看义拼写</span><span>第3天 · 听写</span><span>第7天 · 混合复习</span></div><div class="vocab-summary-actions"><button class="secondary-button" data-vocab-action="restart">重新体验</button><button class="primary-button" data-vocab-action="return-reading">回到原文找这些词</button></div></div>`;
}
function handleVocabularyAction(action){
  const lesson=state.vocabLesson,item=coreVocabulary()[lesson.index];clearTTS();
  if(action==='preview'){lesson.screen='preview';renderVocabulary();return}if(action==='preview-core'||action==='preview-recognition'||action==='preview-added'){lesson.previewTier=action==='preview-recognition'?'recognition':action==='preview-added'?'added':'core';lesson.previewIndex=0;renderVocabulary();return}if(action==='preview-prev'||action==='preview-next'){const list=previewList(),delta=action==='preview-next'?1:-1;lesson.previewIndex=Math.max(0,Math.min(list.length-1,(lesson.previewIndex||0)+delta));renderVocabulary();return}if(action==='remove-added'){const list=addedVocabulary(),target=list[lesson.previewIndex];if(target){const arr=addedStore[addedKey()]||[],i=arr.findIndex(w=>w.id===target.id);if(i>=0){arr.splice(i,1);if(!arr.length)delete addedStore[addedKey()];persistAdded();mergeAddedVocabulary()}lesson.previewIndex=Math.max(0,lesson.previewIndex-1);renderNav()}renderVocabulary();return}if(action==='start'||action==='restart'){state.vocabLesson=freshVocabLesson();state.vocabLesson.screen='lesson';renderVocabulary();return}if(action==='return-reading'){openChapter(state.chapter,true,state.book);return}
  if(action==='read-done'){lesson.readResults[item.id]=true;lesson.stage='meaning';lesson.meaningChoice=null;lesson.meaningChecked=false;renderVocabulary();return}
  if(action==='meaning-check'&&lesson.meaningChoice){lesson.meaningChecked=true;if(!(item.id in lesson.meaningResults))lesson.meaningResults[item.id]=lesson.meaningChoice===item.meaning;renderVocabulary();return}
  if(action==='meaning-next'){lesson.stage='split';renderVocabulary();return}
  if(action==='split-done'){lesson.stage='blend';lesson.blendSlots=Array(phonicsFor(item).length).fill(null);lesson.blendAttempted=false;lesson.blendSolved=false;renderVocabulary();return}
  if(action==='blend-reset'){lesson.blendSlots=Array(phonicsFor(item).length).fill(null);lesson.blendAttempted=false;lesson.blendSolved=false;renderVocabulary();return}
  if(action==='blend-next'&&lesson.blendSolved){lesson.stage='spell';lesson.spellingValue='';lesson.spellingAttempts=0;lesson.spellingSolved=false;renderVocabulary();return}
  if(action==='keyboard-clear'){lesson.spellingValue='';lesson.spellingSolved=false;renderVocabulary();return}
  if(action==='keyboard-backspace'){lesson.spellingValue=lesson.spellingValue.slice(0,-1);lesson.spellingSolved=false;renderVocabulary();return}
  if(action==='spelling-check'){lesson.spellingAttempts++;const correct=lesson.spellingValue===item.word.toLowerCase();if(!(item.id in lesson.spellingResults))lesson.spellingResults[item.id]=correct;lesson.spellingSolved=correct;renderVocabulary();return}
  if(action==='word-next'){if(lesson.index===coreVocabulary().length-1){lesson.screen='summary'}else{lesson.index++;lesson.stage='read';lesson.meaningChoice=null;lesson.meaningChecked=false;lesson.blendSlots=[];lesson.blendAttempted=false;lesson.blendSolved=false;lesson.spellingValue='';lesson.spellingAttempts=0;lesson.spellingSolved=false}renderVocabulary()}
}

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
function updateProgress(){const total=BOOKS.reduce((sum,book)=>sum+book.chapters.length,0);const pct=Math.round(state.completed.size/total*100);$('#progressLabel').textContent=`六册进度 ${state.completed.size}/${total}`;$('#progressBar').style.width=pct+'%'}
function openMenu(){els.sidebar.classList.add('open');els.scrim.classList.add('show')} function closeMenu(){els.sidebar.classList.remove('open');els.scrim.classList.remove('show')}

$('#startButton').onclick=()=>openChapter(0,false,0);$('#brandButton').onclick=showHome;$('#backHome').onclick=showHome;$('#menuButton').onclick=openMenu;$('#closeMenu').onclick=closeMenu;els.scrim.onclick=closeMenu;$('.home-link').onclick=showHome;
document.querySelector('.book-library').onclick=e=>{const button=e.target.closest('[data-book-start]');if(button)openChapter(0,false,+button.dataset.bookStart)};
els.nav.onclick=e=>{const b=e.target.closest('[data-book]'),c=e.target.closest('[data-chapter]'),p=e.target.closest('[data-practice]'),v=e.target.closest('[data-vocabulary]');if(b){const index=+b.dataset.book;if(state.view==='home')setBook(index,false);else openChapter(0,false,index);return}if(c){openChapter(+c.dataset.chapter);return}if(p){showExercise(+p.dataset.practice);return}if(v)showChapterVocabulary(+v.dataset.vocabulary)};
$('#exerciseButton').onclick=()=>showExercise(state.chapter);$('#backToReading').onclick=()=>openChapter(state.chapter,true);$('#vocabularyButton').onclick=()=>showVocabulary();$('#backFromVocabulary').onclick=()=>openChapter(state.chapter,true,state.book);$('#playButton').onclick=()=>{hideCard();togglePlay()};
$('#exerciseContent').onclick=e=>{const answer=e.target.closest('[data-answer]'),action=e.target.closest('[data-quiz-action]');if(answer&&state.quiz){const q=state.quiz.questions[state.quiz.index];if(!state.quiz.checked[q.id]){state.quiz.answers[q.id]=answer.dataset.answer;persistQuiz();renderQuiz()}}if(action)handleQuizAction(action.dataset.quizAction)};
const vocabularyContent=$('#vocabularyContent');let suppressPhonicsClick=false,phonicsPointerDrag=null;
vocabularyContent.onclick=e=>{const audioButton=e.target.closest('[data-vocab-audio]'),meaning=e.target.closest('[data-vocab-meaning]'),phonicsPiece=e.target.closest('[data-phonics-piece]'),spellingKey=e.target.closest('[data-spelling-key]'),action=e.target.closest('[data-vocab-action]');if(audioButton){const item=vocabById(audioButton.dataset.vocabId);if(item){const sentence=audioButton.dataset.vocabAudio==='sentence';playTTS(sentence?item.sentenceAudio:wordAudioPath(item.word),audioButton)}return}if(phonicsPiece){if(!suppressPhonicsClick)clickPhonicsPiece(+phonicsPiece.dataset.phonicsPiece,phonicsPiece.dataset.phonicsSource);return}if(spellingKey&&state.vocabLesson?.stage==='spell'&&!state.vocabLesson.spellingSolved){const item=coreVocabulary()[state.vocabLesson.index];if(state.vocabLesson.spellingValue.length<item.word.length){state.vocabLesson.spellingValue+=spellingKey.dataset.spellingKey;renderVocabulary()}return}if(meaning&&state.vocabLesson&&!state.vocabLesson.meaningChecked){state.vocabLesson.meaningChoice=meaning.dataset.vocabMeaning;renderVocabulary();return}if(action)handleVocabularyAction(action.dataset.vocabAction)};
vocabularyContent.addEventListener('dragstart',e=>{const piece=e.target.closest('[data-phonics-piece]');if(!piece)return;e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',piece.dataset.phonicsPiece);piece.classList.add('dragging')});
vocabularyContent.addEventListener('dragend',e=>e.target.closest('[data-phonics-piece]')?.classList.remove('dragging'));
vocabularyContent.addEventListener('dragover',e=>{const slot=e.target.closest('[data-phonics-slot]');if(slot){e.preventDefault();e.dataTransfer.dropEffect='move'}});
vocabularyContent.addEventListener('drop',e=>{const slot=e.target.closest('[data-phonics-slot]');if(!slot)return;e.preventDefault();placePhonicsPiece(+e.dataTransfer.getData('text/plain'),+slot.dataset.phonicsSlot)});
vocabularyContent.addEventListener('pointerdown',e=>{const piece=e.target.closest('[data-phonics-piece]');if(!piece||e.pointerType==='mouse')return;phonicsPointerDrag={piece,index:+piece.dataset.phonicsPiece,source:piece.dataset.phonicsSource,startX:e.clientX,startY:e.clientY,moved:false,pointerId:e.pointerId};piece.setPointerCapture?.(e.pointerId)});
vocabularyContent.addEventListener('pointermove',e=>{if(!phonicsPointerDrag||phonicsPointerDrag.pointerId!==e.pointerId)return;if(Math.hypot(e.clientX-phonicsPointerDrag.startX,e.clientY-phonicsPointerDrag.startY)>8){phonicsPointerDrag.moved=true;phonicsPointerDrag.piece.classList.add('dragging')}});
vocabularyContent.addEventListener('pointerup',e=>{if(!phonicsPointerDrag||phonicsPointerDrag.pointerId!==e.pointerId)return;const drag=phonicsPointerDrag;phonicsPointerDrag=null;drag.piece.classList.remove('dragging');if(!drag.moved)return;suppressPhonicsClick=true;const slot=document.elementFromPoint(e.clientX,e.clientY)?.closest('[data-phonics-slot]');if(slot)placePhonicsPiece(drag.index,+slot.dataset.phonicsSlot);else if(drag.source==='slot')clickPhonicsPiece(drag.index,'slot');setTimeout(()=>suppressPhonicsClick=false,0)});
$('#debugLink').onclick=()=>showDebug('skills');$('#debugBack').onclick=showHome;document.querySelector('.debug-tabs').onclick=e=>{const tab=e.target.closest('[data-debug-tab]');if(tab)showDebug(tab.dataset.debugTab)};
audio.defaultPlaybackRate=audio.playbackRate=.9;audio.onplay=()=>$('#playButton').textContent='❚❚';audio.onpause=()=>$('#playButton').textContent='▶';audio.ontimeupdate=tick;
audio.onended=()=>{state.completed.add(completionKey());localStorage.setItem('mth-complete',JSON.stringify([...state.completed]));updateProgress();renderNav()};
audio.onloadedmetadata=()=>{const start=audioStart();if(audio.currentTime<start)audio.currentTime=start;audio.playbackRate=+document.querySelector('.speed-group button.active').dataset.speed;$('#duration').textContent=formatTime(audio.duration-start)};
$('#seek').oninput=e=>{if(audio.duration){const start=audioStart();audio.currentTime=start+e.target.value/1000*(audio.duration-start)}};
document.querySelector('.speed-group').onclick=e=>{const b=e.target.closest('[data-speed]');if(!b)return;audio.playbackRate=+b.dataset.speed;document.querySelectorAll('.speed-group button').forEach(x=>x.classList.toggle('active',x===b))};
$('#prevPage').onclick=()=>{if(state.page>0){state.page--;renderPage()}};$('#nextPage').onclick=()=>{if(state.page<state.pages.length-1){state.page++;renderPage()}};
els.story.addEventListener('mouseover',e=>{const w=e.target.closest('.word');if(w&&!state.lockedWord)showWordCard(w)});els.story.addEventListener('mouseout',()=>{if(!state.lockedWord)els.card.classList.add('hidden')});els.story.addEventListener('click',e=>{const w=e.target.closest('.word');if(w){e.stopPropagation();showWordCard(w,true)}});$('#wordClose').onclick=hideCard;document.addEventListener('click',e=>{if(!e.target.closest('.word-card')&&!e.target.closest('.word'))hideCard()});$('#speakWord').addEventListener('click',pronounceCurrentWord);$('#speakSentence').addEventListener('click',pronounceCurrentSentence);$('#wordAddButton').addEventListener('click',e=>{e.preventDefault();e.stopPropagation();toggleAddCurrentWord()});
renderNav();updateProgress();
