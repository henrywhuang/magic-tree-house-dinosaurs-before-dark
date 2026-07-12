# Magic Tree House · Book 1 精读 H5

本地启动：

```bash
python3 -m http.server 8080
```

然后打开 `http://localhost:8080` 。不要直接双击 `index.html`，否则浏览器会拦截章节 JSON 和离线缓存。

## 素材说明

- `assets/audio/`：用户提供的第 1–10 轨原版音频，对应第一册 10 章。
- `assets/images/cover.jpg`：从原版音频元数据中提取的封面。
- `assets/images/prehistoric-adventure.png`：为 H5 原创生成的章节氛围插图，不是原书内页插图。
- `data/`：逐词时间戳、分页与文本数据。

练习区已实现入口与结构，但当前目录未提供《勇闯恐龙谷》正文 Word/PDF 及练习题原稿，因此页面会如实显示“待导入”。
