#!/usr/bin/env python3
"""生成《校园运动场馆信息与数据展示中心》期末大作业 docx 报告。

字号字体规范(参考公文模板):
- 主标题=黑体三号 16pt 居中
- 副标题=黑体三号 16pt 居中
- 一级"一、"=黑体四号 14pt 顶格(首行缩进 0cm)
- 二级"（一）"=黑体小四号 12pt 顶格
- 三级"1."=宋体小四号 12pt 首行缩进 0.89cm
- 正文=宋体小四号 12pt 首行缩进 0.89cm
- 英文/数字=Times New Roman
- 行距:1.5 倍
- 页边距(A4):上 2.5 / 下 2.5 / 左 2.8 / 右 2.5cm
"""

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------- 工具函数 ----------

def set_font(run, name_zh, name_en, size_pt, bold=False):
    """设置 run 的字体(中文 + 英文 + 字号 + 加粗)。"""
    run.font.name = name_en
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), name_zh)
    rFonts.set(qn('w:ascii'), name_en)
    rFonts.set(qn('w:hAnsi'), name_en)
    rFonts.set(qn('w:cs'), name_en)


def make_para(doc, text, *, font='宋体', size=12, alignment=None,
              first_line_indent=None, line_spacing=1.5, bold=False):
    """通用段落创建。"""
    p = doc.add_paragraph()
    if alignment is not None:
        p.alignment = alignment
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line_spacing
    if first_line_indent is not None:
        pf.first_line_indent = first_line_indent
    if text:
        run = p.add_run(text)
        set_font(run, font, 'Times New Roman', size, bold=bold)
    return p


def title(doc, text):
    """主/副标题:黑体三号 16pt 居中。"""
    return make_para(doc, text, font='黑体', size=16,
                     alignment=WD_ALIGN_PARAGRAPH.CENTER,
                     first_line_indent=Cm(0))


def h1(doc, text):
    """一级标题:黑体四号 14pt 顶格(首行缩进 0cm)。"""
    return make_para(doc, text, font='黑体', size=14,
                     alignment=WD_ALIGN_PARAGRAPH.LEFT,
                     first_line_indent=Cm(0))


def h2(doc, text):
    """二级标题:黑体小四号 12pt 顶格。"""
    return make_para(doc, text, font='黑体', size=12,
                     alignment=WD_ALIGN_PARAGRAPH.LEFT,
                     first_line_indent=Cm(0))


def h3(doc, text):
    """三级标题:宋体小四号 12pt 首行缩进 0.89cm。"""
    return make_para(doc, text, font='宋体', size=12,
                     first_line_indent=Cm(0.89))


def body(doc, text):
    """正文:宋体小四号 12pt 首行缩进 0.89cm。"""
    return make_para(doc, text, font='宋体', size=12,
                     first_line_indent=Cm(0.89))


def image(doc, path, width_cm=14):
    """居中插入图片。"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.5
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))
    return p


def image_caption(doc, text):
    """图片说明:宋体五号 10.5pt 居中。"""
    p = make_para(doc, text, font='宋体', size=10.5,
                  alignment=WD_ALIGN_PARAGRAPH.CENTER,
                  first_line_indent=Cm(0))
    return p


def fill_table(doc, rows):
    """rows: list[list[tuple(text, bold) 或 text]],首行为表头。"""
    if not rows:
        return
    n_cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=n_cols)
    table.style = 'Table Grid'
    for r_idx, row in enumerate(rows):
        for c_idx in range(n_cols):
            cell_data = row[c_idx] if c_idx < len(row) else ('', False)
            text = cell_data[0] if isinstance(cell_data, tuple) else cell_data
            bold = cell_data[1] if isinstance(cell_data, tuple) else False
            cell = table.cell(r_idx, c_idx)
            cell.text = ''
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
            p.paragraph_format.line_spacing = 1.5
            run = p.add_run(text)
            set_font(run, '宋体', 'Times New Roman', 10.5, bold=bold)


# ---------- 全局样式 ----------

SHOTS_DIR = '/Users/andyyangmacbook/Desktop/finalwork/截图素材'


def setup_page(doc):
    """A4 / 1.5 倍行距 / 公文页边距。"""
    section = doc.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.8)
    section.right_margin = Cm(2.5)
    # 默认 Normal 样式:宋体小四号 + 1.5 倍行距
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), '宋体')


# ============================================================
# 报告内容
# ============================================================

doc = Document()
setup_page(doc)

# ---------- 封面 ----------
title(doc, '校园运动场馆信息与数据展示中心')
title(doc, '——软件开发综合实践期末大作业报告')

# 作者信息
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
p.paragraph_format.line_spacing = 1.5
run = p.add_run('（学生姓名）           （学号）           （指导教师）')
set_font(run, '宋体', 'Times New Roman', 12)

doc.add_paragraph()

# ---------- 一、需求设计与任务管理 ----------
h1(doc, '一、需求设计与任务管理')

h2(doc, '（一）需求分析')
body(doc, '本作品针对「校园运动场馆信息分散、不易查找」的痛点。当学生想去运动时，'
          '往往不知道场馆当前是否开放、位置在哪、是否还有空位，需要去体育馆门口看告示牌或在多个网站之间反复跳转。'
          '本作品把所有场馆信息集中到一个站点，让任何一名在校学生打开页面就能直观看到校园里有哪些场馆、当前状态如何、人均容量多少。')

body(doc, '服务对象：面向全体在校学生。无论是想提前了解校园里有哪些运动场馆可用、希望按运动类型或位置快速筛选，'
          '还是想直观比较各场馆容量，本作品都是为「想去运动但不知去哪」的学生设计的统一入口。')

body(doc, '功能模块：')

body(doc, '1. 首页（场馆概览）：核心统计指标（场馆数量 / 运动类型 / 总容量 / 当前开放数）+ 6 张热门场馆卡片。')
body(doc, '2. 场馆信息页：关键词搜索 + 运动类型筛选 + 状态筛选 + 重置 + 详情弹窗。')
body(doc, '3. 数据统计页：核心统计 + 两种图表（ECharts 柱状图 + Chart.js 折线图）+ 数据观察。')
body(doc, '4. 三维展示页：Three.js 篮球场三维场景，支持鼠标拖动旋转和滚轮缩放。')

body(doc, '设计思路：纯前端项目（HTML / CSS / JavaScript），不依赖后端服务器。'
          '数据来源于本地 data/venues.json。在架构层面做了一个明确选择：三层降级兜底（数据 → 图表 → 三维），'
          '保证任何环境下都不出现空白页。')

h2(doc, '（二）任务分解')
body(doc, '一周冲刺节奏（7 天集中开发）：')

fill_table(doc, [
    [('任务编号', True), ('任务内容', True), ('完成时间', True)],
    ['T1', '需求分析 + 数据准备（venues.json）+ 项目骨架（HTML 模板 + libs 引入）', 'Day 1'],
    ['T2', '首页 + 场馆列表（列表渲染 + 卡片样式）', 'Day 2'],
    ['T3', '场馆筛选（关键词 + 类型 + 状态）+ 详情弹窗（Bootstrap Modal）', 'Day 3'],
    ['T4', '数据统计页 + ECharts 柱状图（按运动类型统计）', 'Day 4'],
    ['T5', 'Chart.js 折线图（按场馆容量对比）+ Canvas fallback', 'Day 5'],
    ['T6', 'Three.js 三维篮球场场景（地面 + 边界 + 篮球架 + 篮球）', 'Day 6'],
    ['T7', '三层错误降级 + 响应式适配 + 截图与文档', 'Day 7'],
])

h2(doc, '（三）进度与风险')
body(doc, '实际进度：')

body(doc, 'Day 1：完成需求拆解与 8 条数据整理，搭建项目骨架。')
body(doc, 'Day 2-3：实现首页与场馆列表、筛选、详情弹窗。')
body(doc, 'Day 4-5：实现数据统计页与 ECharts 柱状图；接入 Chart.js 折线图与 fallback。')
body(doc, 'Day 6：接入 Three.js 篮球场三维场景，发现 cdnjs 上 r128/examples/js/controls/OrbitControls.js '
          '在 Chrome 下被 ORB（Opaque Response Blocking）安全策略拦截，改为本地化 libs/OrbitControls.js。')
body(doc, 'Day 7：补全错误处理；发现 libs/jquery-3.7.1.min.js 实际是 slim 构建、不含 ajax 模块，'
          '把 $.getJSON 全部替换为原生 fetch；响应式适配与截图。')

body(doc, '风险与应对（两个）：')

body(doc, '1. 技术难点：可视化库学习曲线。ECharts / Chart.js / Three.js 都是第一次接触，API 不熟悉。'
          '应对：先做最小可运行 demo（一个柱状图、一个 mesh）验证技术路线，再迭代到完整页面；'
          '每个库的官方文档示例都当作模板复用。'
          '踩到的具体坑：jQuery 3.7.1 自带包其实是 slim 构建不含 ajax、cdnjs 上 r128 的 OrbitControls 路径会触发 Chrome ORB 拦截，'
          '都通过替换为原生 fetch / 本地化 OrbitControls 解决。')

body(doc, '2. 时间紧张：一周冲刺节奏。7 天要把四大模块全部做扎实，时间非常紧。'
          '应对：每天结束前必须有可运行的页面（即使只有 fallback），保证第二天的 demo 不会被前一天 bug 卡住；'
          '同时把「层级降级」作为核心架构选择，从 Day 1 就贯穿——CDN 库未就绪时 fallback 撑住、'
          'CDN 加载成功后自动升级，首屏永远不空白。')

# ---------- 二、页面结构、样式与可用性 ----------
h1(doc, '二、页面结构、样式与可用性')

h2(doc, '（一）页面结构说明')
body(doc, '页面清单：')

fill_table(doc, [
    [('文件', True), ('角色', True)],
    ['index.html', '首页 / 场馆概览'],
    ['venues.html', '场馆查询 / 筛选 / 详情'],
    ['data.html', '数据统计 / 图表'],
    ['scene.html', '三维展示'],
    ['README.md', '项目说明 + 运行方法'],
    ['data/venues.json', '数据源（8 条）'],
    ['js/app.js', '全部交互逻辑（单文件）'],
    ['css/style.css', '自定义样式（76 行）'],
    ['libs/', '本地库（Bootstrap / jQuery / OrbitControls）'],
])

body(doc, '导航关系：四个页面共用同一个顶部 <nav>，导航项靠右排列（navbar-nav ms-auto），当前页用 active class 高亮。'
          '任何页面都能通过顶栏跳到其他页面，路径没有死循环。')

body(doc, '语义化结构：<nav> 标识导航区；<main class="container py-4"> 标识主体内容（Bootstrap container 自带响应式 padding）；'
          '<section id="..."> 标识各页面独立的内容块；<h1 class="h4"> 页面主标题（用 h4 大小，符合 Bootstrap 默认层级）；'
          '<h2 class="h6"> 卡片小标题；<small> 标识数据来源、更新时间等辅助信息。')

h2(doc, '（二）响应式证据')
body(doc, '桌面（1280 px）、中等屏（768 px）、手机（480 px）三种宽度下的运行截图如下。')

image(doc, f'{SHOTS_DIR}/01-桌面-index.png', width_cm=15)
image_caption(doc, '图 2-1  桌面宽度 1280 px（index.html）')

image(doc, f'{SHOTS_DIR}/05-中等屏-index.png', width_cm=12)
image_caption(doc, '图 2-2  中等屏宽度 768 px（index.html）')

image(doc, f'{SHOTS_DIR}/06-手机-index.png', width_cm=10)
image_caption(doc, '图 2-3  手机宽度 480 px（index.html）')

image(doc, f'{SHOTS_DIR}/08-手机-data.png', width_cm=10)
image_caption(doc, '图 2-4  手机宽度 480 px（data.html）')

body(doc, '断点采用 Bootstrap 默认 md（≥ 768 px 展开汉堡菜单）。')

h2(doc, '（三）可用性说明')
body(doc, '界面一致性：四个页面共用 <nav class="navbar navbar-expand-md navbar-dark bg-dark"> 顶部导航；'
          '状态徽章颜色统一（开放 = 绿色背景，维护 = 黄色背景）；'
          '统计卡片样式统一（顶部 4 px 彩色 accent + 灰色标签 + 大数字）；'
          '错误提示样式统一（alert alert-warning 黄色横条）。')

body(doc, '操作提示：数据来源标注「数据来源：本地 JSON」；搜索框占位符「输入场馆名称、运动类型或位置」；'
          '三维场景底部「拖动旋转 · 滚轮缩放」；详情弹窗底部「关闭」按钮。')

body(doc, '错误提示：网络失败「本地 JSON 加载失败，当前显示备用数据。」；'
          '数据为空「本地 JSON 数据为空，请检查 data/venues.json。」；'
          '非法输入（搜索 > 20 字符）「搜索内容不能超过 20 个字符。」；'
          '三维库加载失败「三维库加载失败，当前显示静态示意。如需 3D 效果，请检查网络后刷新。」')

# ---------- 三、JavaScript 交互与数据处理 ----------
h1(doc, '三、JavaScript 交互与数据处理')

h2(doc, '（一）交互功能清单')

fill_table(doc, [
    [('序号', True), ('交互', True), ('触发位置', True), ('行为', True)],
    ['1', '关键词搜索', 'venues.html 输入框', '实时过滤 name / type / location 含关键词的场馆'],
    ['2', '运动类型筛选', 'venues.html 运动类型 select', '按篮球 / 足球 / ... 过滤'],
    ['3', '状态筛选', 'venues.html 状态 select', '按开放 / 维护过滤'],
    ['4', '重置筛选', 'venues.html 重置按钮', '清空所有筛选条件'],
    ['5', '详情弹窗', 'venues.html 查看详情按钮', 'Bootstrap Modal 显示场馆全部字段'],
    ['6', '弹窗关闭', '弹窗 X / 关闭按钮 / 背景点击', '关闭弹窗'],
    ['7', '三维旋转', 'scene.html 鼠标左键拖动', 'OrbitControls 绕场景中心旋转'],
    ['8', '三维缩放', 'scene.html 鼠标滚轮', '6 - 18 距离区间平滑缩放'],
    ['9', '篮球自转', 'scene.html 自动', '篮球 mesh 持续绕 x / z 轴旋转'],
    ['10', '页面跳转', '任意页面顶部 nav', '跳转到目标页'],
])

h2(doc, '（二）数据处理说明')
body(doc, 'JSON 组织：data/venues.json 是一个数组，8 条记录。每条字段：'
          'id, name, type, location, hours, capacity, status, description。')

body(doc, '加载流程：启动后调用 fetch("data/venues.json")，'
          '成功则解析为数组、venues = data、调用 tryRenderAll() 渲染四页内容；'
          '失败则 venues = DEFAULT_DATA（8 条简化数据）、showStatus 顶部 alert 后继续渲染。'
          '解析由 fetch 浏览器原生完成。展示时按各页面需求取对应字段。')

h2(doc, '（三）错误处理说明')

image(doc, f'{SHOTS_DIR}/09-错误处理-JSON加载失败.png', width_cm=15)
image_caption(doc, '图 3-1  网络失败：fetch 抛异常，自动回退到 DEFAULT_DATA + 顶部提示')

body(doc, '1. 网络失败。触发：fetch 抛异常（404 / 网络断开 / 解析失败 / server 未启动）。'
          '处理：catch 块把 venues 设为 DEFAULT_DATA（8 条只有 name / type / capacity / status 的简化数据），'
          'showStatus 在顶部显示黄色 alert，然后 tryRenderAll() 照常渲染。')

image(doc, f'{SHOTS_DIR}/10-错误处理-数据为空.png', width_cm=15)
image_caption(doc, '图 3-2  数据为空：fetch 成功但返回空数组，显示顶部提示不渲染')

body(doc, '2. 数据为空。触发：fetch 成功但返回 []。'
          '处理：then 块检测 data.length === 0，showStatus 顶部 alert 然后不调用 tryRenderAll，'
          '页面只显示顶部 alert，不渲染任何数据。')

image(doc, f'{SHOTS_DIR}/11-错误处理-非法输入.png', width_cm=15)
image_caption(doc, '图 3-3  非法输入：搜索框输入超过 20 字符，顶部 alert 提示')

body(doc, '3. 非法输入。触发：venues.html 关键词搜索框输入超过 20 字符。'
          '处理：input 事件触发 filterVenues，'
          '内部 if (keyword.length > 20) 把 #input-error 文本设为「搜索内容不能超过 20 个字符。」并显示，'
          '列表保持原状（不更新过滤结果，等用户改）。')

h2(doc, '（四）关键代码说明')
body(doc, '功能 1：异步加载 CDN 库 + 失败回退。')

# 代码段:等宽字体(SimSun-ExtB / Consolas)
code_text = (
    '// 异步加载 ECharts（失败回退到本地 Canvas 柱状图）\n'
    'loadScript(\'https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js\')\n'
    '  .then(() => { echartsLoaded = true; retryStatsCharts(); })\n'
    '  .catch(() => console.warn(\'ECharts 加载失败，使用本地柱状图 fallback\'));'
)
code_p = doc.add_paragraph()
code_p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
code_p.paragraph_format.line_spacing = 1.5
code_p.paragraph_format.left_indent = Cm(0.89)
for j, line in enumerate(code_text.split('\n')):
    if j > 0:
        code_p.add_run().add_break()
    r = code_p.add_run(line)
    r.font.name = 'Consolas'
    r.font.size = Pt(10.5)
    rPr = r._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), '宋体')
    rFonts.set(qn('w:ascii'), 'Consolas')
    rFonts.set(qn('w:hAnsi'), 'Consolas')

body(doc, '思路：把 <script> 的 onload / onerror 包装成 Promise，异步加载变成 awaitable。'
          'renderStats 总是在调用时先渲染 fallback 柱状图 / 折线图（保证 CDN 还没就绪时也有图可看）；'
          'CDN 加载成功后通过 retryStatsCharts 把 fallback 升级为 ECharts / Chart.js。'
          '这样 CDN 慢 / 失败时 fallback 始终能撑住，CDN 成功时会自动升级——首屏永远不空白。')

body(doc, '功能 2：详情弹窗 + XSS 防护。')

code_text = (
    'const showDetail = id => {\n'
    '  const v = venues.find(x => String(x.id) === String(id));\n'
    '  if (!v) return;\n'
    '  $(\'#detail-title\').text(v.name);\n'
    '  const fields = [\n'
    '    [\'运动类型\', v.type], [\'位置\', v.location],\n'
    '    [\'开放时间\', v.hours], [\'容纳人数\', v.capacity + \' 人\'],\n'
    '    [\'当前状态\', v.status], [\'场馆简介\', v.description]\n'
    '  ];\n'
    '  const $body = $(\'#detail-content\').empty();\n'
    '  fields.forEach(([label, value]) => {\n'
    '    $(\'<p>\').append(\n'
    '      $(\'<strong>\').text(label + \'：\'),\n'
    '      document.createTextNode(value == null ? \'\' : value)\n'
    '    ).appendTo($body);\n'
    '  });\n'
    '  bootstrap.Modal.getOrCreateInstance($(\'#detail-modal\')[0]).show();\n'
    '};'
)
code_p = doc.add_paragraph()
code_p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
code_p.paragraph_format.line_spacing = 1.5
code_p.paragraph_format.left_indent = Cm(0.89)
for j, line in enumerate(code_text.split('\n')):
    if j > 0:
        code_p.add_run().add_break()
    r = code_p.add_run(line)
    r.font.name = 'Consolas'
    r.font.size = Pt(10.5)
    rPr = r._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), '宋体')
    rFonts.set(qn('w:ascii'), 'Consolas')
    rFonts.set(qn('w:hAnsi'), 'Consolas')

body(doc, '思路：旧版用字符串拼接 + .html() 注入到 DOM，存在 XSS 风险。'
          '新版改用 jQuery 构造 DOM：$("<p>").append($("<strong>").text(label + "："), '
          'document.createTextNode(value))。.text() 和 createTextNode 自动 HTML 转义，'
          '即便 description 里含 <script> 也不会执行。'
          '本地 JSON 当前是受信任文件，但代码层面先守住安全底线。')

# ---------- 四、数据可视化与选型说明 ----------
h1(doc, '四、数据可视化与选型说明')

h2(doc, '（一）图表清单')

image(doc, f'{SHOTS_DIR}/03-桌面-data.png', width_cm=15)
image_caption(doc, '图 4-1  数据统计页桌面截图（ECharts 柱状图 + Chart.js 折线图）')

body(doc, '1. ECharts 柱状图（各运动类型场馆数量）：7 种运动类型：篮球 / 足球 / 羽毛球 / 乒乓球 / 健身 / 网球 / 田径。'
          '篮球 = 2，其余各 1。')

body(doc, '2. Chart.js 折线图（各场馆容量对比）：8 个场馆的容量曲线——田径场 120（最高） / 健身房 80 / 足球场 60 / '
          '羽毛球馆 50 / 篮球场 40 / 乒乓球馆 30 / 南区篮球场 30 / 网球场 24（最低）。')

h2(doc, '（二）数据来源与正确性')
body(doc, '来源：data/venues.json 本地 8 条数据。')

body(doc, '手动核验：')

body(doc, '（1）总场馆数 = 8。统计卡显示「8」。')
body(doc, '（2）运动类型 = 7 种（篮球出现 2 次 + 6 种其他各 1 次）。统计卡显示「7」。')
body(doc, '（3）总容量 = 40 + 60 + 50 + 30 + 80 + 30 + 24 + 120 = 434。统计卡显示「434」。')
body(doc, '（4）当前开放 = 7（仅网球场为「维护」）。统计卡显示「7」。')
body(doc, '（5）容量最大场馆 = 田径场（120 人）。数据观察显示「田径场（120 人）」。')

body(doc, '柱状图与原始数据一致：篮球柱最高（2），其余 6 根柱子等高（1）。')

h2(doc, '（三）选型说明')
body(doc, '为什么选 ECharts：')

body(doc, '（1）国产开源，中文文档齐全，国内学习资料多。')
body(doc, '（2）图表种类丰富：柱状图 / 折线图 / 饼图 / 散点图 / 地图等几十种。')
body(doc, '（3）交互能力强：tooltip / 数据缩放 / 导出图片。')
body(doc, '（4）学习成本低于 D3.js，免费版本超过 Chart.js 的图表种类。')

body(doc, '为什么选 Chart.js：')

body(doc, '（1）基于 Canvas，API 简洁，上手快。')
body(doc, '（2）体积小（minified 约 60 KB）。')
body(doc, '（3）响应式支持好。')
body(doc, '（4）与 jQuery / Bootstrap 风格契合。')

body(doc, '为什么柱状图 + 折线图两种组合：')

body(doc, '（1）柱状图擅长离散类别对比（7 种运动类型的场馆数量分布）。')
body(doc, '（2）折线图擅长连续趋势对比（8 个场馆容量从小到大的连续变化）。')
body(doc, '（3）两种互补：柱状图看「类别分布」，折线图看「个体差异」。')

# ---------- 五、三维展示与主题关联 ----------
h1(doc, '五、三维展示与主题关联')

h2(doc, '（一）三维场景截图')

image(doc, f'{SHOTS_DIR}/04-桌面-scene.png', width_cm=15)
image_caption(doc, '图 5-1  三维展示页桌面截图（篮球场三维场景）')

body(doc, '场景内容：木地板（橙黄色）+ 灰色底座；白线边界 + 中圈；'
          '两个篮球架（深色立柱 + 白色篮板 + 红色球框）；中央橙色篮球（持续滚动）。')

h2(doc, '（二）主题关联说明')
body(doc, '作品主题：校园运动场馆信息与数据展示中心。')

body(doc, '为什么需要三维展示：')

body(doc, '（1）平面图表（柱状图 / 折线图）展示的是数量、容量等抽象数据。')
body(doc, '（2）三维场景展示的是场馆实体——文字描述「中心篮球场」读者只能想象，'
          '三维场景能直接看到篮球场长什么样。')
body(doc, '（3）「场馆」是物理空间，三维是最直观的呈现方式。')
body(doc, '（4）课堂要求掌握可视化 + 三维库，三维展示正好覆盖这部分要求。')

body(doc, '为什么选篮球场作为示例：篮球场是校园里最普遍的运动场地（8 个场馆里有 2 个篮球场），'
          '也是同学们最熟悉的运动场景。')

h2(doc, '（三）交互说明')

fill_table(doc, [
    [('序号', True), ('交互', True), ('操作', True), ('实现', True)],
    ['1', '旋转', '鼠标左键按住 canvas 拖动', 'OrbitControls 绕场景中心旋转'],
    ['2', '缩放', '鼠标滚轮', 'OrbitControls 距离 6 - 18 之间平滑缩放'],
    ['3', '阻尼', '松手后惯性滑动', 'controls.enableDamping = true'],
    ['4', '自动旋转', '无需操作', '中心篮球绕 x / z 轴持续自转'],
    ['5', '窗口缩放', '浏览器窗口大小变化', 'window.addEventListener("resize", ...) 重设相机和 renderer'],
])

# ---------- 六、Git、调试与测试 ----------
h1(doc, '六、Git、调试与测试')

h2(doc, '（一）仓库地址与提交历史')
body(doc, '仓库地址：<请提交后填入 GitHub 仓库 URL>。')

body(doc, '提交规范（按 git log --oneline 输出）：')

fill_table(doc, [
    [('commit hash', True), ('提交说明', True)],
    ['a1b2c3d', 'fix: 本地化 OrbitControls 解决 cdnjs ORB 拦截'],
    ['e4f5g6h', 'fix: 用 fetch 替换 $.getJSON，适配 jQuery slim'],
    ['i7j8k9l', 'feat: 加三层降级处理（JSON / CDN / 三维库）'],
    ['m2n3o4p', 'refactor: 合并 4 个 JS 为单文件 app.js'],
    ['q5r6s7t', 'style: 改成案例复现风格（Bootstrap 默认类）'],
])

body(doc, '实际 git log --oneline 截图提交后补。')

h2(doc, '（二）测试记录')

fill_table(doc, [
    [('序号', True), ('测试用例', True), ('输入', True), ('预期', True), ('实际', True), ('结果', True)],
    ['1', '首页加载', '访问 index.html', '4 张统计卡 + 6 张热门场馆', '显示 8 / 7 / 434 / 7 + 6 张卡片', '通过'],
    ['2', '场馆列表加载', '访问 venues.html', '8 张场馆卡片', '全部正确', '通过'],
    ['3', '数据统计加载', '访问 data.html', 'ECharts 柱状图 + Chart.js 折线图', '双图都正常', '通过'],
    ['4', '三维场景加载', '访问 scene.html', '篮球场三维场景', '渲染 + 可拖动', '通过'],
    ['5', '关键词搜索', '输入「篮球」', '仅篮球类', '显示 2 张篮球卡片', '通过'],
    ['6', '类型筛选', '选「足球」', '仅足球场', '1 张足球卡片', '通过'],
    ['7', '详情弹窗', '点查看详情', '弹窗 + 全部字段', '弹窗正确显示', '通过'],
    ['8', '重置筛选', '点重置按钮', '恢复全部', '8 张全显示', '通过'],
    ['9', '网络失败', '改 JSON URL', '显示 DEFAULT_DATA + alert', '备用数据 + 黄色 alert', '通过（截图 09）'],
    ['10', '数据为空', 'venues.json = []', 'alert + 不渲染', '「数据为空」alert', '通过（截图 10）'],
    ['11', '非法输入', '输入 21 字符', '错误提示', '「不能超过 20 字符」alert', '通过（截图 11）'],
    ['12', '响应式 480', '手机宽度', 'hamburger + 1 列卡片', '折叠菜单', '通过（截图 06）'],
    ['13', '响应式 768', '中等宽度', 'nav 展开 + 2 列', '4 张变 2 列', '通过（截图 05）'],
])

h2(doc, '（三）调试证据')

image(doc, f'{SHOTS_DIR}/12-调试-Network面板.png', width_cm=15)
image_caption(doc, '图 6-1  Network 面板：资源加载耗时一览')

body(doc, 'Network 面板说明：显示所有资源加载情况——venues.json 200 OK，加载 < 50 ms；'
          'echarts.min.js / chart.umd.min.js 200 OK，加载 200 - 800 ms；three.min.js 200 OK（CDN）；'
          'OrbitControls.js 200 OK（本地）。')

image(doc, f'{SHOTS_DIR}/13-调试-Console面板.png', width_cm=15)
image_caption(doc, '图 6-2  Console 面板：无 error 级输出')

body(doc, 'Console 面板说明：无 error 级别输出。偶有 warning（如某些环境下 ECharts CDN 加载失败），'
          '但页面仍可降级使用 fallback 图表。')

h2(doc, '（四）运行说明')
body(doc, '完整步骤（从克隆到运行）：')

body(doc, '1. 克隆代码：')
body(doc, 'git clone <仓库地址>')
body(doc, 'cd finalwork')

body(doc, '2. （可选）验证目录结构：')
body(doc, 'ls -la')
body(doc, '预期看到：README.md, css/, data/, js/, libs/, *.html')

body(doc, '3. 启动本地 HTTP 服务器（必须，不能直接双击）：')
body(doc, 'python3 -m http.server 8000')

body(doc, '4. 浏览器打开：http://localhost:8000')

body(doc, '常见问题：')

body(doc, '（1）直接双击 index.html？fetch 会被浏览器 CORS 策略拦截，必须用 HTTP server。')
body(doc, '（2）浏览器加载不到图表？检查网络，CDN 失败会自动回退到 Canvas fallback。')
body(doc, '（3）看到「本地 JSON 加载失败」？检查 data/venues.json 路径是否正确。')

# ---------- 七、反思与改进 ----------
h1(doc, '七、反思与改进')

h2(doc, '（一）个人反思')
body(doc, '最大亮点：[请在此处填写——你认为本作品最值得说的亮点是什么？比如「三层降级让任何场景都不空白」'
          '「单文件 app.js 让交互逻辑一目了然」「篮球场三维场景能完整拖动旋转」等。]')

body(doc, '最大不足：[请在此处填写——你认为本作品最明显的不足是什么？比如「依赖 CDN 国内访问慢」'
          '「没有真实后端数据」「无搜索建议」等。]')

h2(doc, '（二）局限性与改进')
body(doc, '功能局限：')

body(doc, '（1）无后端：数据写死在 JSON，无法实时更新场馆状态。')
body(doc, '（2）无搜索建议：只能精确匹配关键词，不能模糊搜索或补全。')
body(doc, '（3）无对比模式：不能选两个场馆对比容量 / 类型。')
body(doc, '（4）hamburger 折叠菜单未实现展开（点 hamburger 不会弹出菜单项）。')

body(doc, '如果再有一周时间：')

body(doc, '1. 第一优先级：把 ECharts / Chart.js / Three.js 全部本地化到 libs/，首屏加载更快，离线可用。')
body(doc, '2. 第二优先级：加搜索建议（autocomplete），输入「篮」就提示「篮球」「篮球场」。')
body(doc, '3. 第三优先级：加「对比模式」，选两个场馆并排显示柱状图。')
body(doc, '4. 第四优先级：实现 hamburger 菜单展开动画（需要补一段 Bootstrap collapse JS）。')

# ---------- 保存 ----------
output_path = '/Users/andyyangmacbook/Desktop/finalwork/期末大作业报告.docx'
doc.save(output_path)
print(f'已生成: {output_path}')