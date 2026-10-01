# -*- coding: utf-8 -*-
"""
build_handbook.py —— 旅行翻页手册生成器
用法: python build_handbook.py <config.json> [--template template.html] [--out out.html]
读取配置 JSON（书信息 + 图片映射 + 页面清单），按元素类型渲染每面页面，
将图片内嵌为 base64，组装 template.html 生成最终单文件 HTML。
"""
import argparse
import base64
import json
import os
import re
import sys

# ---- 常量 ---------------------------------------------------------------
DL_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0l-4-4m4 4l4-4"/>'
          '<path d="M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"/></svg>')

PLANE_SVG = ('<svg class="bp-plane" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
             '<path d="M2 16l9-2V6.5A1.5 1.5 0 0 1 12.5 5h1A1.5 1.5 0 0 1 15 6.5V14l7 2v2l-7-1.5V20'
             'l2 1.5v1.5l-3.5-1-3.5 1v-1.5L12 20v-5.5L2 18v-2z"/></svg>')

ICONS = {
    "corn": ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.5v4.5"/>'
             '<path d="M8.6 5.4c.5-1.8 2-2.8 3.4-2.8s2.9 1 3.4 2.8"/>'
             '<path d="M12 7.5c-3 0-5 2-5 5s2 6 5 6 5-3 5-6-2-5-5-5z"/>'
             '<path d="M9.4 10c.8.8.8 2 .4 3M14.6 10c-.8.8-.8 2-.4 3M10.2 13.6c.5.6 1.3.6 1.8.5'
             'M12 15.6c.7.1 1.5.1 2.1-.5"/></svg>'),
    "wheel": ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">'
              '<circle cx="12" cy="12" r="8"/><path d="M12 4v16M4 12h16M6.3 6.3l11.4 11.4M17.7 6.3L6.3 17.7"/>'
              '<circle cx="12" cy="12" r="1.6" fill="currentColor"/></svg>'),
    "sun": ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round">'
            '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5'
            'M5.2 5.2l1.8 1.8M17 17l1.8 1.8M18.8 5.2L17 7M7 17l-1.8 1.8"/></svg>'),
    "roof": ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M3 12.5L12 4.5l9 8"/>'
             '<path d="M5.5 10.6V20h13v-9.4"/><path d="M10 20v-5h4v5"/>'
             '<path d="M8.5 14h3M13 14h2.5"/></svg>'),
}

FACE_NAMES = ["封面"]


# ---- 工具 ---------------------------------------------------------------
def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")


def save_btn(prefix, n, face_name):
    return ('<button class="save-btn" data-name="%s-第%d面-%s.png" title="保存本页为图片">%s</button>'
            % (prefix, n, face_name, DL_SVG))


# ---- 各页面渲染 ---------------------------------------------------------
def face_cover(b, prefix):
    return '''<section class="page cover">
  %(btn)s
  <div class="c-top">%(eyebrow)s</div>
  <div class="c-title">%(cn)s</div>
  <div class="c-en">%(en)s</div>
  <div class="c-art"><img src="%(img)s" alt="%(cn)s封面插画"><span class="tape t1"></span><span class="tape t2"></span></div>
  <div class="c-sub">%(sub)s<span class="c-sub-en">%(sub_en)s</span></div>
  <div class="c-foot">%(foot)s</div>
</section>''' % {
        "btn": save_btn(prefix, 1, "封面"),
        "eyebrow": b["cover_eyebrow"], "cn": b["title_cn"], "en": b["title_en"],
        "img": b["cover_image"], "sub": b["cover_sub"], "sub_en": b["cover_sub_en"],
        "foot": b["cover_foot"],
    }


def face_foreword(p, prefix, n):
    frs = "".join(
        '<div class="fr"><img src="%s" alt="%s"><div class="fl">%s · %s<br><b>%s</b></div></div>'
        % (ph["file"], ph.get("alt", ""), ph["num"], ph["cn"], ph["en"])
        for ph in p["photos"]
    )
    return '''<section class="page inscript">
  %(btn)s
  <div class="ins-top">FOREWORD · 题词</div>
  <div class="q">%(q)s</div>
  <div class="q-en">%(qe)s</div>
  <div class="divider"></div>
  <div class="film">%(frs)s</div>
  <div class="note">%(note)s</div>
</section>''' % {"btn": save_btn(prefix, n, p["face_name"]), "q": p["quote_cn"],
                 "qe": p["quote_en"], "frs": frs, "note": p["note"]}


def face_ticket(p, prefix, n):
    dots = "".join('<i style="--d:%s"></i>' % c for c in p["dots"])
    return '''<section class="page">
  %(btn)s
  <div class="t-head"><span class="line"></span>%(stop)s<span class="line"></span></div>
  <div class="ticket" style="--acc:%(acc)s">
    <div class="ticket-body">
      <div class="ticket-art"><img src="%(img)s" alt="%(alt)s"></div>
      <div class="ticket-meta">
        <div class="ticket-stop">NO. %(no)s · ADMIT ONE</div>
        <div class="ticket-title">%(title)s</div>
        <div class="ticket-sub">%(sub)s</div>
        <div class="ticket-dots">%(dots)s</div>
        <div class="ticket-note">%(note)s</div>
      </div>
    </div>
    <div class="ticket-stub">
      <div class="tear">TEAR HERE</div>
      <div class="ticket-phrase">%(phrase)s</div>
      <div class="ticket-date">%(date)s</div>
    </div>
  </div>
  <div class="page-num">%(page_no)s</div>
</section>''' % {"btn": save_btn(prefix, n, p["face_name"]), "stop": p["stop"], "acc": p["acc"],
                 "img": p["image"], "alt": p.get("alt", ""), "no": p["no"], "title": p["title"],
                 "sub": p["sub"], "dots": dots, "note": p["note"], "phrase": p["phrase"],
                 "date": p["date"], "page_no": p["page_no"]}


def face_boarding(p, prefix, n):
    return '''<section class="page">
  %(btn)s
  <div class="t-head"><span class="line"></span>%(stop)s<span class="line"></span></div>
  <div class="bp" style="--acc:%(acc)s">
    <div class="bp-info">
      <div class="bp-head"><span class="bp-logo">%(airline)s</span><span class="bp-line">%(kind)s</span></div>
      <div class="bp-route"><div class="bp-airport">%(from)s</div>%(plane)s<div class="bp-airport">%(to)s</div></div>
      <div class="bp-rows">
        <div>FLIGHT<b>%(flight)s</b></div>
        <div>SEAT<b>%(seat)s</b></div>
        <div>GATE<b>%(gate)s</b></div>
        <div>DATE<b>%(date)s</b></div>
      </div>
      <div class="bp-note">%(note)s</div>
    </div>
    <div class="bp-stub">
      <div class="tear">TEAR HERE</div>
      <div class="bp-art"><img src="%(img)s" alt="%(alt)s"></div>
      <div class="bp-phrase">%(phrase)s</div>
    </div>
  </div>
  <div class="page-num">%(page_no)s</div>
</section>''' % {"btn": save_btn(prefix, n, p["face_name"]), "stop": p["stop"], "acc": p["acc"],
                 "airline": p["airline"], "kind": p["bp_kind"], "from": p["from"], "to": p["to"],
                 "plane": PLANE_SVG, "flight": p["flight"], "seat": p["seat"], "gate": p["gate"],
                 "date": p["date"], "note": p["note"], "img": p["image"], "alt": p.get("alt", ""),
                 "phrase": p["phrase"], "page_no": p["page_no"]}


def face_postcard(p, prefix, n):
    return '''<section class="page">
  %(btn)s
  <div class="t-head"><span class="line"></span>%(stop)s<span class="line"></span></div>
  <div class="pc" style="--acc:%(acc)s">
    <div class="pc-write">
      <div class="pc-head"><span class="pc-k">POSTCARD · 明信片</span></div>
      <div class="pc-msg">%(msg_cn)s<span class="e">%(msg_en)s</span></div>
      <div class="pc-addr">%(addr)s</div>
      <div class="pc-stamp">%(stamp)s</div>
      <div class="pc-postmark">%(postmark)s</div>
    </div>
    <div class="pc-art"><img src="%(img)s" alt="%(alt)s"></div>
  </div>
  <div class="page-num">%(page_no)s</div>
</section>''' % {"btn": save_btn(prefix, n, p["face_name"]), "stop": p["stop"], "acc": p["acc"],
                 "msg_cn": p["msg_cn"], "msg_en": p["msg_en"], "addr": p["addr"],
                 "stamp": p["stamp"], "postmark": p["postmark"], "img": p["image"],
                 "alt": p.get("alt", ""), "page_no": p["page_no"]}


def face_polaroid(p, prefix, n):
    return '''<section class="page">
  %(btn)s
  <div class="t-head"><span class="line"></span>%(stop)s<span class="line"></span></div>
  <div class="pl-wrap">
    <div class="pl">
      <span class="tape"></span>
      <img src="%(img)s" alt="%(alt)s">
      <div class="cap">%(cap)s<small>%(cap_sub)s</small></div>
    </div>
    <div class="pl-meta">
      <div class="pl-title">%(title)s</div>
      <div class="pl-sub">%(sub)s</div>
      <div class="pl-note">%(note)s</div>
    </div>
  </div>
  <div class="page-num">%(page_no)s</div>
</section>''' % {"btn": save_btn(prefix, n, p["face_name"]), "stop": p["stop"], "img": p["image"],
                 "alt": p.get("alt", ""), "cap": p["cap"], "cap_sub": p["cap_sub"],
                 "title": p["title"], "sub": p["sub"], "note": p["note"], "page_no": p["page_no"]}


def face_stamps(p, prefix, n):
    rows = "".join(
        '<div class="stamp" style="--sc:%(c)s"><div class="ring">%(ic)s</div><div class="sw">%(en)s</div>'
        '<div class="scn">%(cn)s</div></div>'
        % {"c": s["color"], "ic": ICONS[s["icon"]], "en": s["en"], "cn": s["cn"]}
        for s in p["stamps"]
    )
    return '''<section class="page stamps">
  %(btn)s
  <div class="st-title">%(cn)s</div>
  <div class="st-en">%(en)s</div>
  <div class="st-row">%(rows)s</div>
  <div class="st-note">%(note)s</div>
</section>''' % {"btn": save_btn(prefix, n, p["face_name"]), "cn": p["title_cn"],
                 "en": p["title_en"], "rows": rows, "note": p["note"]}


def face_back(b, prefix, n):
    return '''<section class="page backc">
  %(btn)s
  <div class="bc-top">%(eyebrow)s</div>
  <div class="bc-mid">
    <div class="postmark">
      <div class="pm-txt">%(pm1)s</div>
      <div class="pm-date">%(pmd)s</div>
      <div class="pm-txt">%(pm2)s</div>
    </div>
    <div class="bc-title">%(title)s</div>
    <div class="bc-cn">%(cn)s</div>
  </div>
  <div class="bc-line">%(line)s</div>
  <div class="bc-foot">%(foot)s</div>
</section>''' % {"btn": save_btn(prefix, n, "封底"), "eyebrow": b["back_eyebrow"],
                 "pm1": b["pm_t1"], "pmd": b["pm_date"], "pm2": b["pm_t2"],
                 "title": b["back_title"], "cn": b["back_cn"], "line": b["back_line"],
                 "foot": b["back_foot"]}


RENDERERS = {
    "foreword": face_foreword,
    "ticket": face_ticket,
    "boarding_pass": face_boarding,
    "postcard": face_postcard,
    "polaroid": face_polaroid,
    "stamps": face_stamps,
}


# ---- 主流程 -------------------------------------------------------------
def find_template(override):
    if override:
        return override
    base = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(base, "template.html"),
                 os.path.join(base, "..", "assets", "template.html")):
        if os.path.exists(cand):
            return cand
    return os.path.join(base, "template.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--template", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    args.template = find_template(args.template)

    base_dir = os.path.dirname(os.path.abspath(args.config))
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    book = cfg["book"]
    out = args.out or os.path.join(base_dir, cfg["output"])

    faces_html = [face_cover(book, book["download_prefix"])]
    for i, p in enumerate(cfg["faces"]):
        faces_html.append(RENDERERS[p["type"]](p, book["download_prefix"], i + 2))
        FACE_NAMES.append(p["face_name"])
    faces_html.append(face_back(book, book["download_prefix"], len(faces_html) + 1))
    FACE_NAMES.append("封底")

    total = len(faces_html)
    if total % 2 != 0:
        sys.exit("页面总数必须为偶数（封面+中间页+封底），当前 %d 面" % total)

    leaves = []
    for i in range(0, total, 2):
        leaves.append(
            '<div class="leaf" data-leaf="%d"><div class="face front"><div class="gutter"></div>%s</div>'
            '<div class="face back"><div class="gutter"></div>%s</div></div>'
            % (i // 2, faces_html[i], faces_html[i + 1])
        )

    with open(args.template, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("{{TITLE}}", book["title"])
    html = html.replace("{{TOPBAR}}", book["topbar"])
    html = html.replace("{{PAGES}}", "\n".join(leaves))
    html = html.replace("{{FACE_NAMES}}", json.dumps(FACE_NAMES, ensure_ascii=False))
    html = html.replace("{{FILE_PREFIX}}", book["download_prefix"])
    html = html.replace("{{TOTAL_FACES}}", str(total))

    # 图片内嵌 base64
    for key, path in cfg["images"].items():
        full = path if os.path.isabs(path) else os.path.join(base_dir, path)
        html = html.replace("@IMG:%s@" % key, data_uri(full))

    left = re.findall(r"@IMG:[^@]+@", html)
    if left:
        sys.exit("存在未替换的图片占位符: %s" % set(left))

    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK ->", out, os.path.getsize(out) // 1024, "KB,", total, "面")


if __name__ == "__main__":
    main()
