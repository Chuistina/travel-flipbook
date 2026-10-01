# 旅行纪念元素库（Element Catalog）

每本手册的内容页从下列元素中挑，**同一本内不重复**。所有元素共用同一种"票面语法"：奶油白底 + 细线框 + 柔和阴影 → 水彩主视觉 → 衬线英文大标题 + 手写体短语 → 票据/实物特征（齿边、虚线、邮戳）→ 左侧或局部小字注释 → 左下角取色圆点（票卡类）。

通用规则：

- 每个元素必须有 `type` 与 `face_name`；内容页可加 `page_no` 显示底部页码。
- 图片一律用 `@IMG:key@` 引用；`acc` 为该页强调色（`--acc`），与照片主色调呼应。
- 英文标题/短语走 Cormorant Garamond / Caveat，中文走 Noto Serif SC；英文短语避免全大写堆叠，用短句。

## 已实现元素（build_handbook.py 直接支持）

### 1. ticket · 纪念票卡（用户点名的核心元素）
票根横向大卡，左侧水彩画 + 英文大标题 + 取色圆点，右侧可撕票根（齿边 + 手写短语 + 日期）。
```json
{"type":"ticket","face_name":"玉米票卡","stop":"STOP 01 · FIELD 田野",
 "image":"@IMG:corn@","no":"001","title":"Green Gold","sub":"玉米地里的夏天",
 "dots":["#7C9A5A","#B7C68B","#D9C07A","#4E6B3A"],
 "note":"苞叶里的夏天，是绿色的。","phrase":"Grow with<br>the sun.",
 "date":"2024 · 07 · 31","page_no":"03","acc":"#7C9A5A"}
```
字段：`stop`(页眉章节) `image` `no`(票号) `title`(英文标题) `sub`(中文副题) `dots`(2–5 个取色圆点，来自原图) `note`(手写体小注) `phrase`(撕票区英文短语，可含 `<br>`) `date`(票面日期) `acc`。

### 2. boarding_pass · 登机牌
航司名 + 出发/到达 + 航班/座位/登机口/日期 四联信息 + 右侧撕票区嵌水彩小图与短语。
```json
{"type":"boarding_pass","face_name":"摩天轮登机牌","stop":"STOP 02 · ROAD 旅途",
 "image":"@IMG:wheel@","acc":"#E8927C","airline":"Field Air","bp_kind":"BOARDING PASS · 登机牌",
 "from":"CITY","to":"FIELD","flight":"SXX · 2024","seat":"07 A","gate":"C-01","date":"26 JUL",
 "note":"从城市出发，去田野里过夏天。","phrase":"Rolling to somewhere.","page_no":"04"}
```

### 3. postcard · 明信片
左侧书写区（留言 + 收件地址 + 右上角邮票 + 圆形邮戳），右侧整幅水彩画，中间虚线分界。
```json
{"type":"postcard","face_name":"黄昏明信片","stop":"STOP 03 · DUSK 黄昏",
 "image":"@IMG:sunset@","acc":"#E0BC85",
 "msg_cn":"此刻晚霞正好，风也温柔。","msg_en":"Slow down, sunset is here.",
 "addr":"TO：未来的自己<br>三下乡 · 2024 夏",
 "stamp":"CN<br>2024","postmark":"SANXIAXIANG<br>07 · 26","page_no":"05"}
```
字段：`msg_cn`(中文留言) `msg_en`(手写体英文留言) `addr`(收件地址，可含 `<br>`) `stamp`(邮票文字) `postmark`(邮戳文字)。

### 4. polaroid · 拍立得大卡
手写体标注、胶带贴纸的拍立得照片（唯一"实拍照片"展示页），配右侧衬线大标题区。
```json
{"type":"polaroid","face_name":"蓝天拍立得","stop":"STOP 04 · SKY 晴空",
 "image":"@IMG:roof@","acc":"#7E93A6","title":"Blue Roof",
 "sub":"RAISE HIGH THE BLUE · 晴空纪念",
 "cap":"Blue Roof","cap_sub":"2024 · 07 · 29 晴",
 "note":"蓝屋顶与白云，是夏天的晴空。","page_no":"06"}
```
字段：`title` `sub`(大标题区) `cap`(相纸下方手写标注) `cap_sub`(标注小字) `note`(手写体说明)。

### 5. foreword · 题词页（胶片条）
居中大引语 + 手写体英文 + 分隔线 + 四格"胶片条"（原图缩略 + 编号 + 中英文小标）。**全册唯一放多张原图缩略的页面**。
```json
{"type":"foreword","face_name":"题词","quote_cn":"去田野里，收集一整个夏天。",
 "quote_en":"Collect a whole summer in the fields.",
 "note":"这本小册子收录了四张照片与四种旅途纪念。",
 "photos":[{"file":"@IMG:p_corn@","num":"01","cn":"田野","en":"Green Gold"},
           {"file":"@IMG:p_wheel@","num":"02","cn":"旅途","en":"Wheel of Sky"},
           {"file":"@IMG:p_sunset@","num":"03","cn":"黄昏","en":"Golden Hour"},
           {"file":"@IMG:p_roof@","num":"04","cn":"晴空","en":"Blue Roof"}]}
```
`photos` 数量不限（1–6 张皆可），胶片条自动等分。

### 6. stamps · 盖章页
圆形印章（SVG 图标 + 英文 + 中文），每枚对应一站。
```json
{"type":"stamps","face_name":"印章页","title_cn":"沿途盖章",
 "title_en":"STAMP PAGE · COLLECT THE MOMENTS","note":"One stamp, one memory.",
 "stamps":[{"color":"#7C9A5A","icon":"corn","en":"FIELD","cn":"田野 · 玉米地"},
           {"color":"#E8927C","icon":"wheel","en":"ROAD","cn":"旅途 · 摩天轮"},
           {"color":"#E0BC85","icon":"sun","en":"DUSK","cn":"黄昏 · 晚霞"},
           {"color":"#7E93A6","icon":"roof","en":"SKY","cn":"晴空 · 蓝屋顶"}]}
```
`icon` 可选内置：`corn`(玉米) `wheel`(摩天轮) `sun`(太阳) `roof`(屋顶)。需要新图标时在 `build_handbook.py` 的 `ICONS` 字典里加 SVG 路径。

## 扩展新元素的方法

在 `build_handbook.py` 里加一个渲染函数（返回 `<section class="page">...</section>`），注册进 `RENDERERS`，并在本文件补字段说明。渲染函数只输出页面 HTML（CSS 与 JS 全部在 `assets/template.html`），新元素需要新样式时把 CSS 加进 template.html 的 `:root` 之后。

可扩展的元素灵感（与已实现 6 种风格同族，均围绕"票据/实物 + 水彩"）：

- **复古火车票**：窄长条票、中间大圆孔、车站名+车次+硬座号，中文大标题。
- **景点门票**：副券 + 存根双联，主票面水彩全景图，副券盖日期章。
- **邮票整版**：4–8 枚同系列邮票，每枚一枚小景 + 面值 + 齿孔，右下角英文地名。
- **行李牌**：圆角硬纸牌 + 打孔绳圈，目的地+姓名+日期，手写体地址。
- **天气卡**：当日天气图标（晴/雨/风）+ 温度 + 一句话心情，水彩天空作底。
- **美食卡**：一道当地小吃的迷你水彩 + 口味打分圆点 + "值得再吃一次"手写注。
- **语言卡**：两句当地方言/外语及音译，配小插图。
- **手绘小地图**：一站到一站的水彩路线简图（SVG 路径 + 站点圆点），配合页码连线。
- **信封 + 信纸**：左侧信封（收件人 + 邮票），右侧展开信纸上的手写体长信。
- **口袋页**：半页插袋造型，露出一张"拍立得"的边角，模拟抽出实物的动作。

原则：一个新元素 = 一个明确的实物隐喻 + 水彩插画位 + 至少一个手写体英文短语 + 票据特征（齿边/虚线/邮戳/编号至少取一）+ 与页面强调色呼应。**扩展时保持元素间不重复**。

## 文案风格速查

- 英文标题：2–3 词、首字母大写，如 "Green Gold" "Blue Roof"。
- 撕票/标注短语：手写体短句，如 "Grow with the sun." "Rolling to somewhere." "Slow down, sunset is here."
- 中文小注：一句话，克制、写景不写情绪，如 "苞叶里的夏天，是绿色的。"
- 章节眉标：`STOP 0X · <EN> <中文>` 或 `FOREWORD · 题词` 等。
