# 2026-11 宏村 · 黄山 · 唐模亲子五日行
2026-11-25 至 11-29，厦门北 ⇄ 黄山北动车往返；宏村住 2 晚，黄山雲麓北海宾馆住 1 晚，唐模住 1 晚，11/29 坐 G1611 回厦门。

- [`index.html`](./index.html)：长页面版，可以直接部署到 GitHub Pages。包含行程总览、每日安排、天气、穿衣建议、上黄山路线、唐模鳌鱼灯和吃什么。
- [`book.html`](./book.html)：翻页书版，由 `index.html` 自动生成，**不要直接改**。
- 天气：页面内写入 2026-11-23 查到的预报；打开页面时会从 Open-Meteo 拉取最新预报，拉取失败时显示内置数据。
- [`docs/travel/`](./docs/travel/)：调研记录与来源。

## 修改流程
1. 只改 `index.html`。
2. 重新生成书版：`python3 scripts/book/build_book.py`
3. 提交并推送，GitHub Pages 会自动更新。

`scripts/book/` 里的文件：
- `build_book.py`：从 `index.html` 取内容，按书页分页，生成 `book.html`。分页顺序在 `PAGES` 里调整。
- `book.css` / `book.js`：书版专用的样式和翻页脚本。
- `vignettes.py`：景点线描插画（SVG）。`index.html` 里的插画也是用它生成的；改了插画后，要同时更新 `index.html` 里对应的 `<figure class="vignette">`。

页面里的时间、价格只用于规划，出发时请以景区官方公告、12306 和实时导航为准。
