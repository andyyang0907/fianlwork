# 校园运动场馆信息与数据展示中心

软件开发综合实践期末大作业示例项目。

## 运行方法

不要直接双击 index.html。推荐在项目根目录打开终端：

```bash
python3 -m http.server 8000
```

然后浏览器访问：

```text
http://localhost:8000
```

## 页面

- `index.html`：首页与场馆概览
- `venues.html`：JSON 场馆查询、筛选、详情弹窗
- `data.html`：ECharts 柱状图 + Chart.js 折线图
- `scene.html`：Three.js 篮球场三维展示

## 技术

HTML、CSS、JavaScript、Bootstrap、jQuery、JSON、ECharts、Chart.js、Three.js。

没有使用 React、Vue、Node.js、数据库或后端。

## 关于网络依赖

Bootstrap、jQuery 和项目数据文件均为本地文件。
ECharts、Chart.js、Three.js 在有网络时动态加载，以便使用课堂要求的可视化/三维库。

## 关于降级方案

页面设计了三层降级，确保任何情况下都能看到内容：

- **数据层**：`data/venues.json` 加载失败时，使用内置的 `DEFAULT_DATA` 兜底数据（容量更小的备用版本），并在顶部显示提示。
- **图表层（数据统计页）**：CDN 加载失败时，使用纯 HTML/CSS 柱状图 fallback 和 Canvas 2D 折线图 fallback；CDN 加载成功后会覆盖 fallback。
- **三维层（场景页）**：CDN 加载失败时，使用 Canvas 2D 静态示意图，可拖动旋转、滚轮缩放，并在顶部显示提示。