# -*- coding: utf-8 -*-
"""Generate 后台更新操作手册.docx (Word) per word skill general format."""
import docx
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\86152\Desktop\net\dhu-xuefu\后台更新操作手册.docx"

doc = Document()

# 页面：A4，上下左右 2.5cm
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin = sec.bottom_margin = sec.left_margin = sec.right_margin = Cm(2.5)

def set_font(run, cn="宋体", en="Times New Roman", size=12, bold=False, color=RGBColor(0, 0, 0)):
    run.font.name = en
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    r = run._element.rPr.rFonts
    r.set(qn("w:eastAsia"), cn)

def title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(18)
    set_font(p.add_run(text), cn="黑体", size=18, bold=True)
    return p

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    set_font(p.add_run(text), cn="黑体", size=16, bold=True)
    return p

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    set_font(p.add_run(text), cn="黑体", size=14, bold=True)
    return p

def body(text, indent=True):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        pf.first_line_indent = Pt(24)  # 2 字符（12pt 字号）
    set_font(p.add_run(text), size=12)
    return p

def bullet(text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    p.paragraph_format.left_indent = Pt(18)
    set_font(p.add_run("· " + text), size=12)
    return p

def code_block(lines):
    for ln in lines:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.left_indent = Pt(18)
        set_font(p.add_run(ln), cn="宋体", en="Courier New", size=10.5)
    return

def add_table(headers, rows):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, htxt in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(p.add_run(htxt), cn="黑体", size=10.5, bold=True)
        # 表头浅灰底纹
        tcPr = hdr[i]._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:fill"), "D9D9D9")
        tcPr.append(shd)
    for r in rows:
        cells = t.add_row().cells
        for i, val in enumerate(r):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            set_font(p.add_run(val), size=10.5)
    # 垂直居中 + cantSplit + tblHeader
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit")
        trPr.append(cant)
        if row is t.rows[0]:
            th = OxmlElement("w:tblHeader")
            trPr.append(th)
        for c in row.cells:
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    return t

# ===== 标题 =====
title("学服站后台更新操作手册")

body("适用对象：东华大学一站式学生服务大厅各柜台、各部门负责日常更新的同学。", indent=False)
body("更新时间：2026 年 10 月。", indent=False)

# ===== 一、总则 =====
h1("一、总则：网站是怎么“更新”的")
body("本网站的所有内容都由 data/ 文件夹下的数据文件（JSON 格式）驱动。改一个 JSON 文件，全站对应位置自动更新，不需要会编程，也不需要改网页代码。")
bullet("值班空班 / 暂停记录 → data/schedule.json")
bullet("首页轮播图 → data/settings.json")
bullet("通知公告 → data/notices.json")
bullet("柜台业务介绍 → data/counters.json")

h2("通用修改流程（以 schedule.json 为例）")
body("第一步：打开 GitHub 仓库 https://github.com/Bullet016/dhu-xuefu ；")
body("第二步：进入 data 文件夹，点击要修改的 JSON 文件；")
body("第三步：点击文件右上角的铅笔图标（编辑按钮）；")
body("第四步：按本手册后面的格式修改内容；")
body("第五步：点击绿色按钮 Commit changes，在输入框写一句修改说明（如“更新 11 月 3 日空班安排”）；")
body("第六步：等待约 1 分钟，刷新网页即可看到效果（如果没变，按 Ctrl + F5 强制刷新）。")
body("上传图片（轮播图、宣传图等）：在仓库页面点 Add file → Upload files，把图片拖进去，提交后即可用。图片统一放在 assets/img/ 文件夹。")

# ===== 二、轮播图 =====
h1("二、首页轮播图（settings.json → banners）")
body("首页上半部分会自动滚动播放照片，每张照片可设置跳转链接（公众号推文、活动页面等）。")
body("第一步：先把图片上传到仓库的 assets/img/ 文件夹（建议横向大图，比例 16:9 左右）；")
body("第二步：编辑 data/settings.json，找到 “banners”，按下面的格式填写：")
code_block([
    '"banners": [',
    '  { "img": "assets/img/banner-1.png", "title": "2026 秋季招新推文", "link": "https://mp.weixin.qq.com/s/xxxx" },',
    '  { "img": "assets/img/banner-2.png", "title": "迎新活动回顾", "link": "" },',
    '  { "img": "assets/img/banner-3.png", "title": "值班安排一览", "link": "" }',
    ']',
])
add_table(["字段", "作用", "怎么填"], [
    ["img", "图片在仓库里的路径", "上传后填 assets/img/图片文件名（含后缀）"],
    ["title", "图片下方的标题文字", "可留空 “”，也可写一句话"],
    ["link", "点击图片跳转的网址", "填公众号文章、活动页完整网址；不需要跳转就留 “”"],
])
body("想加几张就加几条，想删就删掉对应一条；注意每条之间用英文逗号 , 分隔，最后一组后面不要逗号。")

# ===== 三、空班/暂停 =====
h1("三、空班 / 暂停记录（schedule.json → exceptions）")
body("值班安排页的表格：绿色 = 该时段正常值班；红色 = 空班或暂停。要标记空班、暂停，只改 data/schedule.json 里的 “exceptions”。")

h2("3.1 某个柜台某天空班")
code_block([
    '{',
    '  "date": "2026-11-05",',
    '  "type": "空班",',
    '  "shift": "全天",',
    '  "counters": ["c2", "c3"],',
    '  "note": "柜台二、柜台三因内部培训暂停服务"',
    '}',
])

h2("3.2 只空某一个班次")
code_block([
    '{',
    '  "date": "2026-11-06",',
    '  "type": "空班",',
    '  "shift": "14:40-17:00",',
    '  "counters": ["c4"],',
    '  "note": "柜台四下午第三班因会议空班"',
    '}',
])
body("shift 填班次时间（10:00-12:20 / 12:20-14:40 / 14:40-17:00 / 17:00-19:00）；shift 不填或填 “全天”，表示当天该柜台整天空班。")

h2("3.3 全体暂停一天")
code_block([
    '{',
    '  "date": "2026-11-10",',
    '  "type": "暂停",',
    '  "counters": [],',
    '  "note": "全体大会暂停值班一天"',
    '}',
])

h2("柜台编号对照表（counters 填什么）")
add_table(["编号", "柜台", "业务指导部门"], [
    ["c1", "柜台一", "学生处"],
    ["c2", "柜台二", "学生处"],
    ["c3", "柜台三", "保卫处、信息办"],
    ["c4", "柜台四", "教务处"],
    ["c5", "柜台五", "教务处、研究生院"],
    ["c6", "柜台六", "信智学院"],
])
body("注意事项：")
bullet("值班/空班变更请提前至少一天更新，避免同学跑空；")
bullet("表格只显示本周（周一至周五）的空班情况，历史记录会显示在页面下方的“空班 / 暂停记录”时间线中；")
bullet("date 格式固定为 2026-11-05（年-月-日），写错格式不会生效。")

# ===== 四、值班时间与班次 =====
h1("四、值班时间与班次（schedule.json 其他字段）")
bullet("hours：值班时间文字（如“周一至周五 10:00-19:00（法定节假日除外）”），有变动时同步改；")
bullet("shifts：一天内的班次数组，一般保持默认四个班次不变；")
bullet("weekly：周一至周日常规值班/休息状态（mon~sun），一般保持默认；")
bullet("如遇节假日调休等特殊情况，用第三节的 exceptions 记录，不要改 weekly。")

# ===== 五、通知公告 =====
h1("五、通知公告（notices.json）")
body("编辑 data/notices.json，每条通知是一个 { ... }：")
code_block([
    '[',
    '  {',
    '    "title": "10 月 31 日大厅暂停值班通知",',
    '    "date": "2026-10-31",',
    '    "tag": "重要",',
    '    "body": "因全体大会，10 月 31 日大厅暂停值班一天，请同学们相互转告。",',
    '    "link": "",',
    '    "linkText": ""',
    '  }',
    ']',
])
add_table(["字段", "作用"], [
    ["title", "通知标题"],
    ["date", "发布日期"],
    ["tag", "填 “重要” 会置顶显示在首页；填其他文字只出现在通知公告页"],
    ["body", "通知正文，可留空"],
    ["link / linkText", "需要跳转公众号原文或网页时填；不需要跳转就留 “”"],
])

# ===== 六、柜台业务 =====
h1("六、柜台业务（counters.json）")
body("编辑 data/counters.json，每个柜台是一组 { ... }，内含 name（柜台名）、dept（业务指导部门）、intro（简介）、services（业务列表）。")
body("每项业务含 name（业务名）、desc（业务说明）、tips（注意事项列表，没有可写 []）。")
body("想新增业务，在对应柜台的 services 里按格式加一组；想删除直接删掉对应一组。")

# ===== 七、常见问题 =====
h1("七、常见问题")
body("1. 改了没生效？先等 1 分钟，再按 Ctrl + F5 强制刷新（GitHub 网页有时会缓存旧内容）；手机端可清除浏览器缓存。")
body("2. 日期写了但表格里没有？表格只显示本周一至周五的空班，日期需落在本周内；历史记录在页面下方时间线里查看。")
body("3. JSON 格式写错了怎么办？保存后页面会显示空白或报错，回到文件检查：花括号 { }、方括号 [ ]、英文逗号是否配对；字符串必须用英文双引号 “ ” 包裹。拿不准时对照本手册的示例逐字核对。")
body("4. 图片上传后不显示？检查 img 里填的路径和文件名是否和上传的完全一致（含大小写和后缀）。")
body("5. 自己电脑上怎么预览？在仓库页面直接刷新即可；如需本地预览，需安装 Git 和 Python，在站点文件夹执行 python -m http.server 8000，再访问 http://127.0.0.1:8000。")

doc.save(OUT)
print("saved:", OUT)
