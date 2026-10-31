# -*- coding: utf-8 -*-
"""Add counter c6 (信智学院) to counters.json, schedule.json counterNames, and create counter6.html."""
import io, json, os

base = r"C:\Users\86152\Desktop\net\dhu-xuefu"

# 1) counters.json: append c6
cp = os.path.join(base, "data", "counters.json")
d = json.load(io.open(cp, encoding="utf-8"))
ids = [c["id"] for c in d["counters"]]
if "c6" not in ids:
    d["counters"].append({
        "id": "c6",
        "name": "柜台六",
        "dept": "业务指导部门：信智学院",
        "intro": "柜台六主要对接信智学院，提供电脑系统重装、硬件除尘及校园正版软件下载等信息化技术服务。",
        "services": [
            {"name": "系统重装", "desc": "针对电脑出现的系统崩溃、运行缓慢等问题，提供 Windows 操作系统重装服务。", "tips": []},
            {"name": "硬件除尘", "desc": "为电脑进行硬件除尘，延长设备使用寿命。", "tips": []},
            {"name": "正版软件下载", "desc": "提供学校平台正版软件的下载服务，包括微软操作系统、办公软件、数据库软件，正版 MATLAB 和正版 Adobe 产品等。", "tips": []}
        ]
    })
    io.open(cp, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
    print("counters.json: c6 appended")
else:
    print("counters.json: c6 exists")

# 2) schedule.json counterNames: add c6
sp = os.path.join(base, "data", "schedule.json")
s = json.load(io.open(sp, encoding="utf-8"))
if "c6" not in (s.get("counterNames") or {}):
    s.setdefault("counterNames", {})["c6"] = "柜台六（信智学院）"
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(s, ensure_ascii=False, indent=2))
    print("schedule.json: counterNames.c6 added")
else:
    print("schedule.json: c6 exists")

# 3) counter6.html from counter5.html template
tpl = io.open(os.path.join(base, "counter5.html"), encoding="utf-8").read()
out = tpl.replace('data-counter="c5"', 'data-counter="c6"').replace("柜台业务 · 东华大学一站式学生服务大厅", "柜台业务 · 东华大学一站式学生服务大厅")
tgt = os.path.join(base, "counter6.html")
if not os.path.exists(tgt) or io.open(tgt, encoding="utf-8").read() != out:
    io.open(tgt, "w", encoding="utf-8", newline="\n").write(out)
    print("counter6.html created")
else:
    print("counter6.html unchanged")
