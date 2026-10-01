# travel-flipbook · 旅行翻页手册 Skill

把照片、目的地、旅行文案做成一本**可以翻页翻动**的旅行纪念手册 HTML：

- 单文件、图片全内嵌 base64、离线可开、手机可翻
- 手绘水彩插画 + 浅米白纸感 + 纪念票卡 / 登机牌 / 明信片 / 拍立得 / 盖章页等旅行纪念元素
- 每页可单独另存为 PNG，也可一键打包下载全部页面（zip）
- 配置驱动：改一份 `config.json` 即可重新生成不同内容的手册

## 目录结构

```
travel-flipbook/
├── SKILL.md                     # Skill 使用说明（触发与流程）
├── assets/template.html         # 手册模板（CSS + 翻页交互 + 存图逻辑）
├── scripts/build_handbook.py    # 配置驱动生成器（内嵌图片、自动分页）
├── examples/config.example.json # 配置示例
└── references/elements.md       # 旅行纪念元素库（6 种已实现 + 扩展灵感）
```

## 快速用法

```bash
# 1. 准备素材：水彩插画（长边 ≤1400px）+ 原图缩略（长边 ≤900px）放进 assets/
# 2. 按 examples/config.example.json 写一份 config.json
# 3. 构建单文件手册
python scripts/build_handbook.py config.json
# 产物：config 同目录下的 .html，双击即可翻阅
```

## 内置能力

- 翻页：点书页左右区 / 键盘 ← → / 触屏滑动
- 存图：每页右上角按钮保存单页 PNG；底部"下载全部图片"打包 zip
- 响应式：按视口自动缩放，手机可用
- 导出图片需联网加载 html2canvas + JSZip；阅读翻页无需联网

## 元素去重规则

同一本手册里每个内容页使用**不同**的元素类型（票卡、登机牌、明信片、拍立得、盖章页等各占一页）；扩展新元素只需在 `build_handbook.py` 的 `RENDERERS` 注册渲染函数、在 `assets/template.html` 补 CSS。

## License

MIT
