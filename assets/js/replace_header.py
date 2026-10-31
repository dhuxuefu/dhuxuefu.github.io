# -*- coding: utf-8 -*-
"""Unify the topbar header across all pages."""
import io, os, re

BASE = r"C:\Users\86152\Desktop\net\dhu-xuefu"

HEADER = """<header class="topbar">
  <div class="nav-inner">
    <a class="nav-logo" href="index.html">
      <img src="assets/img/logo.jpg" alt="东华大学一站式学生服务大厅 logo">
      <span class="nav-title">东华大学一站式学生服务大厅</span>
    </a>
    <button class="nav-toggle" aria-label="展开菜单" aria-expanded="false">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav-links" aria-label="主导航">
      <a data-nav="home" href="index.html">首页</a>
      <a data-nav="counters" href="counters.html">柜台业务</a>
      <a data-nav="schedule" href="schedule.html">值班安排</a>
      <a data-nav="notices" href="notices.html">通知公告</a>
      <a data-nav="about" href="about.html">关于我们</a>
    </nav>
  </div>
</header>"""

pages = ["index.html", "counters.html", "schedule.html", "notices.html", "about.html"] + \
        ["counter%d.html" % i for i in range(1, 6)]

pat = re.compile(r"<header class=\"topbar\">.*?</header>", re.S)

for name in pages:
    path = os.path.join(BASE, name)
    with io.open(path, "r", encoding="utf-8") as f:
        html = f.read()
    new, n = pat.subn(HEADER, html)
    if n != 1:
        print("WARN", name, "replacements=", n)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    print("ok", name, "n=", n)
