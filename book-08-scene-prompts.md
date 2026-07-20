# Book 8 场景图生成提示词

## 生成模式

- 模式：以 Book 1 / Book 7 现有成品作为人物与风格参考，生成 Book 8 新场景。
- 参考图：`assets/images/scenes/chapter-01-scene-03.webp`
- 参考图：`assets/images/book-07-scenes/chapter-10-scene-02.webp`
- 成品目录：`assets/images/book-08-scenes/`
- 成品规格：1600 × 900 WebP，质量 88，每章 3 张，共 30 张。

## 人物与风格锁定

```text
Use the attached images only as strict recurring-character and visual-style references.
Jack is an 8-year-old boy with tousled dark-brown short hair, round glasses, blue/green practical clothes and a small brown backpack when appropriate.
Annie is a 7-year-old girl with warm-brown hair in a high ponytail, an orange-red top or hoodie, and khaki or denim bottoms.
Preserve their faces, ages, child proportions, and warm sibling chemistry.
When a scene explicitly mentions Peanut, include exactly one tiny brown-and-white mouse; otherwise include no mouse.
On the Moon, both children wear believable bulky white spacesuits with clear visors only after the story says they change clothes; keep Jack's glasses visible.
The moon man is one tall mysterious adult astronaut with a reflective metal visor and a very large rectangular white jet pack; never show his face.
Morgan le Fay is one kind mysterious adult woman with long luminous white hair and elegant teal-and-violet medieval robes.
Cinematic children's storybook illustration, richly hand-painted gouache and watercolor texture, warm expressive anime-inspired faces, softly realistic dramatic lighting, emotionally clear and age-appropriate, high detail.
No readable text, labels, logos, watermark, extra children, or duplicate characters.
```

## 单场景提示词模板

```text
Create a completely new wide 16:9 landscape story illustration for Magic Tree House Book 8.
Scene title: {SCENE_TITLE}.
Story action: {SCENE_DESCRIPTION}.
{CHARACTER_AND_STYLE_LOCK}
```

## 同章分镜提示词模板

```text
Create one exact edge-to-edge 2-by-2 storyboard sheet for Magic Tree House Book 8 Chapter {CHAPTER}, with four equal panels, no gutters, borders, labels, or text.
TOP LEFT: {SCENE_1_TITLE}. {SCENE_1_DESCRIPTION}
TOP RIGHT: {SCENE_2_TITLE}. {SCENE_2_DESCRIPTION}
BOTTOM LEFT: {SCENE_3_TITLE}. {SCENE_3_DESCRIPTION}
BOTTOM RIGHT: a quiet scenic establishing view of the same chapter environment, no people.
{CHARACTER_AND_STYLE_LOCK}
```

每章标题、场景标题和中文剧情描述的唯一数据源为 `scripts/book8_content.py` 中的 `SCENES`，修改剧情分页时应同步更新该文件。
