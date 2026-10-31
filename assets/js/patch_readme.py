# -*- coding: utf-8 -*-
import io

p = r"C:\Users\86152\Desktop\net\dhu-xuefu\data\README.md"
t = io.open(p, encoding="utf-8").read()

old_start = t.find("- `exceptions`")
old_end = t.find("\n> 约定：值班/空班变更")
assert old_start != -1 and old_end != -1 and old_end > old_start, (old_start, old_end)

new = """- `exceptions`：**临时变更（空班、暂停）都在这里加**，格式：
```json
{
  "date": "2026-11-05",
  "type": "空班",
  "shift": "14:40-17:00",
  "counters": ["c2", "c3"],
  "note": "柜台二、柜台三因内部培训下午暂停服务"
}
```

| 字段 | 含义 |
|---|---|
| `date` | 变更日期，格式 `2026-11-05` |
| `type` | `"空班"`（部分柜台不值班）或 `"暂停"`（全体暂停） |
| `shift` | 空班发生在哪个班次（填班次时间，如 `"14:40-17:00"`）；**不填或填 `"全天"` 表示该柜台当天空班一整天** |
| `counters` | 空班的柜台 id（`c1`~`c5`）；`type` 为 `暂停` 时可不填或留空数组 |
| `note` | 给同学看的说明，如"内部培训""临时会议" |

值班安排页把本周（周一至周五）的空班情况按班次整理成一张表：左侧是四个班次时间（10:00-12:20 / 12:20-14:40 / 14:40-17:00 / 17:00-19:00），上侧是周一至周五，**有空的格子标出空班柜台，空白即该时段正常值班**；`exceptions` 的历史记录同步显示在下方时间线上，首页状态横幅同步高亮。"""

t2 = t[:old_start] + new + t[old_end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(t2)
print("replaced ok", len(t), "->", len(t2))
