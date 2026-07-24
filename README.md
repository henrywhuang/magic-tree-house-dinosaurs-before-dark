# Magic Tree House · 英文原著精读营

面向英语水平较好的五年级非母语学习者，包含：

- 多册 Magic Tree House 完整正文、音频、剧情插图与词汇学习。
- 每章 5 道互动阅读理解题；支持即时反馈、原文证据、成绩与进度保存。
- 依据美国五年级文学阅读标准整理的 3 个项目 Skills。
- 目录底部 `Developer Debug`，可查看 Skills 全文、全部题目标签及各册数据健康度。

本地启动：

```bash
python3 -m http.server 8080
```

然后打开 `http://localhost:8080` 。不要直接双击 `index.html`，否则浏览器会拦截章节 JSON 和离线缓存。

## 主要数据

- `assets/audio/`：各册逐章原版音频。
- `assets/audio/words/`：可点击单词的独立点读音频；使用阿里开源 `Qwen3-TTS-12Hz-0.6B-CustomVoice`、英文音色 `Aiden` 本地批量生成（24 kHz 单声道 MP3），不截取原版有声书。
- `data/`：逐词时间戳、三场景分页正文与统一题库 `questions.json`。
- `project-skills/`：标准、测评蓝图与具体命题规范。

## 扩展新读物

在 `app.js` 的 `BOOKS` 中追加一条带稳定 `id` 的配置，首页书卡、侧边目录、分册徽章和进度会自动生成。成就等级每完成 10 章提升一级，不以当前总书数作分母，因此新书上线不会让旧用户的等级倒退。完成记录使用 `book-id:chapter-index` 作为主键，并自动迁移旧版的下标式记录。

## 重新生成单词点读音频

首次准备本地模型后运行：

```bash
.venv-tts/bin/python scripts/generate_qwen3_word_audio.py --batch-size 16
```

脚本会读取 `data/words.js`，只补齐缺失的单词 MP3；使用 `--overwrite` 可全部重做。模型权重与虚拟环境保存在被 Git 忽略的 `.models/`、`.venv-tts/` 中，不会上传到网页仓库。
