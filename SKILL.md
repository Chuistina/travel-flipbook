---
name: travel-flipbook
description: 把照片、目的地、旅行文案做成一本"可以翻页翻动"的旅行纪念手册 HTML（单文件、离线可开、手机可翻）。手绘水彩插画 + 浅米白纸感 + 纪念票卡/登机牌/明信片/拍立得/盖章页等旅行纪念元素；每页可单独另存为 PNG 图片，也可一键打包下载全部页面。当用户要求生成可翻页旅行手册/旅行纪念册/旅行手账风小册子，或提供多张旅行照片希望排版成纪念册（含票根、登机牌、明信片等元素）时使用；也用于在既有手册上增加页面、换元素、改文案后重新生成。
---

# Travel Flipbook（旅行翻页手册）

把素材做成一本可翻动的电子旅行手册：CSS 3D 翻页、纸感米白底、每页一种互不重复的旅行纪念元素，页页可存图。

## 交付流程

1. **盘点输入**：确认照片清单、目的地/主题、可用文案（日期、地名、纪念语）。缺失且影响成品的事实（如活动名、日期）先用 `interaction.ask` 补齐；纯文案风格由 Agent 拟定（可后续修改）。
2. **生成水彩插画**：每张照片按 `doubao-creative-design` 串行流程做图生图（I2I），产出 1 张水彩风插画；生成一张立即单独 `present_files` 交付一张。插画用于各页"票面主视觉"，压缩到长边 ≤ 1400px 存 `assets/`。
3. **准备素材**：原图另存压缩版（长边 ≤ 900px）供胶片条/拍立得使用；全部素材放进 config 同级的 `assets/` 目录。
4. **写 config JSON**：参照 `examples/config.example.json`，按 `references/elements.md` 选元素类型与字段，页面总数（封面+中间页+封底）必须为偶数（默认 8 面）。
5. **构建**：`python scripts/build_handbook.py <config.json>` → 产出单文件 HTML（图片全内嵌 base64，双击即可离线打开）。默认输出到 config 同目录。
6. **自检**：用 html skill 的 `scripts/shot.py <输出.html>` 截图+lint；有中间展开面要核验时，可复制成品、把 JS 初始 `nFlipped` 改为 1/2/3 并去掉翻页过渡，再截图，核验后删除临时副本。
7. **交付**：`present_files` 交付 HTML 文件；若用户要可点开的链接，按 html skill 的 `references/lark-apps-publish.md` 发布为 doubao-html 链接。

## 视觉基调（模板已内置，不要改）

- 纸张：`--paper:#FBF7EE` 米白 + feTurbulence 细颗粒纹理；每页奶油白卡片 + 细线框 + 柔和阴影。
- 字体：标题 Cormorant Garamond 衬线、中文 Noto Serif SC、手写体 Caveat；均走 `https://miaoda.feishu.cn/fonts/css2?family=...` 镜像，离线自动回退系统衬线。
- 每页一个强调色 `--acc`（如玉米绿 #7C9A5A / 珊瑚 #E8927C / 黄昏金 #E0BC85 / 晴空蓝 #7E93A6），与章节内容对应。

## 元素去重规则（重要）

同一本手册里，每个内容页使用**不同**的元素类型：票卡、登机牌、明信片、拍立得、盖章页等各占一页，不重复；照片缩略图只出现在胶片条/拍立得这类"实拍展示"页。元素类型与字段见 `references/elements.md`。

## config.json 结构

```json
{
  "output": "输出文件名.html",
  "book": {
    "title": "页面标题（浏览器标签）",
    "topbar": "顶栏文字，如 SUMMER FIELD NOTES · 三下乡田野纪行",
    "download_prefix": "导出图片/压缩包的文件名前缀，如 三下乡田野纪行",
    "cover_eyebrow": "封面眉标", "title_cn": "封面中文大标题", "title_en": "封面英文标题",
    "cover_image": "@IMG:key@ 或图片路径",
    "cover_sub": "封面副文案", "cover_sub_en": "封面副文案英文（手写体）",
    "cover_foot": "封面底部小字",
    "back_eyebrow": "封底眉标", "back_title": "封底英文标题", "back_cn": "封底中文",
    "back_line": "封底一句话", "back_foot": "封底底部小字",
    "pm_t1": "邮戳上行", "pm_date": "邮戳日期", "pm_t2": "邮戳下行"
  },
  "images": { "key": "图片相对路径" },
  "faces": [ { "type": "元素类型", "face_name": "该页名称（用于导出文件名）", "...": "元素字段" } ]
}
```

- 页面顺序：封面 → `faces` 各项 → 封底。中间页数任意（可为 0），但**总页数必须为偶数**。
- 图片在 `book` / `faces` 里用 `@IMG:key@` 引用，构建时自动内嵌为 base64。
- 每个 `faces` 元素必须含 `face_name`（成为导出的 PNG / zip 内文件名的一部分）与 `type`。
- 可自定义每页底部页码：内容页写 `page_no`（如 "03"）；封面/题词/盖章/封底不写。

## 构建脚本行为

- 自动生成封面（第 1 面）与封底（最后一面）并成对分页。
- 注入 `FACE_NAMES`、文件名前缀，供"存为图片 / 下载全部图片"使用。
- 校验：剩余 `@IMG:` 占位符会报错退出；总面数非偶数会报错退出。
- 产物 HTML 是唯一交付物，`assets/` 目录无需随 HTML 分发。

## 已在产物里内置的能力（无需额外开发）

- 翻页：点书页左右区、键盘 ← →、触屏左右滑。
- 存图：每页右上角圆形按钮保存当前页 PNG；底部"存为图片"保存当前展开右页；**"下载全部图片"** 用 JSZip 把全部页面打包为 zip 下载。
- 响应式缩放：按视口自动缩放书页（下限 0.42），手机可用。
- 单页导出依赖 html2canvas + JSZip（jsDelivr CDN），导出时需联网加载；阅读翻页无需联网（字体离线回退）。
