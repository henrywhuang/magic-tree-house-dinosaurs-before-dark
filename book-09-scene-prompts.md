# Book 9 · Dolphins at Daybreak · Scene Image Prompts

## Generation mode

- Built-in image generation tool, one generated composition per requested scene.
- New-image generation with existing Book 8 artwork supplied only as recurring-character and painterly-style reference.
- Reference 1: `assets/images/book-08-scenes/chapter-10-scene-02.webp`
- Reference 2: `assets/images/book-08-scenes/chapter-09-scene-01.webp`
- Final delivery: 30 WebP files at 1600×900, quality 88, in `assets/images/book-09-scenes/`.

## Shared prompt

> Use case: illustration-story. Asset type: 16:9 H5 children's chapter-reader scene, no text. Create a completely new scene and composition; do not edit or copy the reference compositions. Preserve the recurring identities: Jack is an 8-year-old boy with short tousled dark-brown hair, round black glasses, forest-green hoodie and tan pants; Annie is a 7-year-old girl with a warm brown ponytail, rust-orange hoodie and green shorts. Morgan, when requested, is a graceful older woman with long wavy white hair and a red velvet medieval robe. Use cinematic hand-painted gouache and watercolor children's-book illustration, rich layered brush texture, soft painterly edges, the same established series proportions, wide landscape 16:9, clear story action, readable faces and body language. No text, letters, captions, logo, border or watermark; no extra people; age-appropriate; anatomically correct hands.

## Scene-specific requests

The exact 30 scene requests, titles, chapter order and Chinese accessibility descriptions are maintained in `scripts/book9_content.py` under `SCENES`. Each item is combined with the shared prompt above. The sequence is:

1. 共同的清晨梦境；树屋与摩根归来；图书馆大师的第一道谜题
2. 粉红珊瑚礁上的谜语；发现白色迷你潜艇；潜艇意外潜入深海
3. 研究潜艇控制面板；安妮学会转向；窗外的彩色海底星球
4. 珊瑚礁鱼城；巨型蛤蜊与黄貂鱼；苏琪和山姆来访
5. 电脑日志中的危险警告；破损潜艇开始上浮；巨型章鱼露出两只眼睛
6. 章鱼抱住迷你潜艇；翻书了解温和的章鱼；裂缝开始漏水
7. 漏水潜艇冲出海面；控制屏熄灭；保持冷静下水
8. 鲨鱼鳍悄悄逼近；筋疲力尽漂浮休息；海豚及时救援
9. 拥抱海豚告别；他们都在保护对方；灰色牡蛎解开谜题
10. 晨光中整理第一道答案；穿过金色树林回家；真正的珍珠

All image-generation calls also include the full matching Chinese description from `SCENES`, translated into a concrete visual action, setting, lighting and composition while preserving the shared character/style constraints.
