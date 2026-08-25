#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-templates.

Pure geometry + templating: the six sheet designs are hand-authored below, this
only lays them out and wraps them in the page shell. No content is invented at
build time, so the printed sheet is always exactly what is reviewed here.
"""
import html as _html
import math
import pathlib

W, H = 210, 297  # A4 portrait in mm; every sheet uses the same viewBox

INK = "#111827"
MUTED = "#6B7280"
RULE = "#D4D4D8"
SOFT = "#FAFAFA"
ACC = "#6D28D9"

SANS = "Helvetica Neue, Helvetica, Arial, sans-serif"
SERIF = "Georgia, Times New Roman, serif"


def head(title, sub):
    """Shared sheet header: title, one-line instruction, hairline."""
    return (
        f'<text x="16" y="20" font-family="{SERIF}" font-size="10.5" fill="{INK}">{title}</text>'
        f'<text x="194" y="20" text-anchor="end" font-family="{SANS}" font-size="4.2" '
        f'fill="{MUTED}">visionboard.bemooore.com</text>'
        f'<text x="16" y="27.5" font-family="{SANS}" font-size="4.6" fill="{MUTED}">{sub}</text>'
        f'<line x1="16" y1="31.5" x2="194" y2="31.5" stroke="{RULE}" stroke-width="0.3"/>'
    )


def box(x, y, w, h, label, hint="", r=2.2):
    """A paste-a-picture area with its label sitting on the frame, not inside."""
    o = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{SOFT}" '
        f'stroke="{RULE}" stroke-width="0.35"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="6.6" rx="{r}" fill="#FFFFFF" stroke="none"/>'
        f'<text x="{x + 3.2}" y="{y + 4.7}" font-family="{SANS}" font-size="3.9" '
        f'letter-spacing="0.55" fill="{ACC}">{_html.escape(label.upper())}</text>'
        f'<line x1="{x}" y1="{y + 6.6}" x2="{x + w}" y2="{y + 6.6}" stroke="{RULE}" stroke-width="0.3"/>'
    )
    if hint:
        o += (
            f'<text x="{x + w / 2}" y="{y + h / 2 + 3.2}" text-anchor="middle" '
            f'font-family="{SANS}" font-size="4" fill="#C7C7CC">{hint}</text>'
        )
    return o


def wline(x, y, w, label, gap=9, n=1):
    """Write-on rules with a small caption above the first one."""
    o = ""
    if label:
        o += (
            f'<text x="{x}" y="{y - 3.4}" font-family="{SANS}" font-size="3.9" '
            f'letter-spacing="0.55" fill="{ACC}">{_html.escape(label.upper())}</text>'
        )
    for i in range(n):
        yy = y + i * gap
        o += f'<line x1="{x}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="{RULE}" stroke-width="0.35"/>'
    return o


def foot(note):
    return (
        f'<line x1="16" y1="284" x2="194" y2="284" stroke="{RULE}" stroke-width="0.3"/>'
        f'<text x="16" y="289.5" font-family="{SANS}" font-size="3.7" fill="{MUTED}">{note}</text>'
    )


# ---------------------------------------------------------------- 1. six zones
def sheet_six_zones():
    s = head("Six Life Zones", "One picture per zone. Cut, paste, or draw. Nothing has to be pretty.")
    zones = ["Health & body", "Work & craft", "Money", "People I love", "Growth", "Play & rest"]
    bw, bh, gx, gy = 86, 60, 6, 6
    for i, z in enumerate(zones):
        x = 16 + (i % 2) * (bw + gx)
        y = 38 + (i // 2) * (bh + gy)
        s += box(x, y, bw, bh, z, "paste here")
    s += wline(16, 236, 178, "I am becoming someone who", n=2, gap=9)
    s += wline(16, 260, 110, "One step I take this week")
    s += wline(134, 260, 60, "By when")
    s += foot("Six Life Zones - free printable vision board template - MIT licensed")
    return s


# ------------------------------------------------------------------ 2. one goal
def sheet_one_goal():
    s = head("One Goal, Loud", "For the goal that actually keeps you awake. One image, three reasons.")
    s += box(16, 38, 178, 112, "The thing itself", "one big picture")
    s += wline(16, 160, 178, "Say it in one sentence, present tense", n=2, gap=9)
    for i, lab in enumerate(["Because", "Because", "Because"]):
        x = 16 + i * 60.67
        s += f'<rect x="{x}" y="184" width="55.3" height="34" rx="2.2" fill="{SOFT}" stroke="{RULE}" stroke-width="0.35"/>'
        s += (
            f'<text x="{x + 3.2}" y="{190.5}" font-family="{SANS}" font-size="3.9" '
            f'letter-spacing="0.55" fill="{ACC}">{lab.upper()}</text>'
        )
        for k in range(3):
            yy = 197.5 + k * 6.5
            s += f'<line x1="{x + 3.2}" y1="{yy}" x2="{x + 52.1}" y2="{yy}" stroke="{RULE}" stroke-width="0.3"/>'
    s += wline(16, 236, 110, "The very next physical action")
    s += wline(134, 236, 60, "Before this date")
    s += wline(16, 262, 178, "How I will know it happened")
    s += foot("One Goal, Loud - free printable vision board template - MIT licensed")
    return s


# ---------------------------------------------------------------- 3. year wheel
def _sector(cx, cy, r0, r1, a0, a1):
    def p(r, a):
        rad = math.radians(a - 90)
        return f"{cx + r * math.cos(rad):.2f} {cy + r * math.sin(rad):.2f}"

    large = 1 if (a1 - a0) > 180 else 0
    return (
        f"M {p(r0, a0)} L {p(r1, a0)} A {r1} {r1} 0 {large} 1 {p(r1, a1)} "
        f"L {p(r0, a1)} A {r0} {r0} 0 {large} 0 {p(r0, a0)} Z"
    )


def sheet_year_wheel():
    s = head("The 12-Month Wheel", "One word per month. The wheel fills itself as the year goes.")
    cx, cy = 105, 148
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    for i, m in enumerate(months):
        a0, a1 = i * 30, (i + 1) * 30
        s += (
            f'<path d="{_sector(cx, cy, 34, 96, a0 + 0.6, a1 - 0.6)}" fill="{SOFT}" '
            f'stroke="{RULE}" stroke-width="0.35"/>'
        )
        mid = math.radians((a0 + a1) / 2 - 90)
        lx, ly = cx + 40 * math.cos(mid), cy + 40 * math.sin(mid)
        s += (
            f'<text x="{lx:.2f}" y="{ly:.2f}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="3.9" letter-spacing="0.55" fill="{ACC}">{m}</text>'
        )
    s += f'<circle cx="{cx}" cy="{cy}" r="33" fill="#FFFFFF" stroke="{RULE}" stroke-width="0.35"/>'
    s += (
        f'<text x="{cx}" y="{cy - 12}" text-anchor="middle" font-family="{SANS}" font-size="3.9" '
        f'letter-spacing="0.55" fill="{ACC}">THE YEAR IN ONE WORD</text>'
    )
    for k in range(3):
        yy = cy - 2 + k * 9
        s += f'<line x1="{cx - 25}" y1="{yy}" x2="{cx + 25}" y2="{yy}" stroke="{RULE}" stroke-width="0.35"/>'
    s += wline(16, 262, 110, "The month I am most likely to quit")
    s += wline(134, 262, 60, "What I do instead")
    s += foot("The 12-Month Wheel - free printable vision board template - MIT licensed")
    return s


# ----------------------------------------------------------------- 4. now/next
def sheet_now_next():
    s = head("Now / Next", "Left is honest. Right is chosen. The gap between them is the plan.")
    s += box(16, 38, 86, 96, "Where I am now", "a real photo")
    s += box(108, 38, 86, 96, "Where I am going", "the picture I want")
    s += wline(16, 148, 86, "What is true today", n=4, gap=8)
    s += wline(108, 148, 86, "What is true then", n=4, gap=8)
    s += f'<line x1="16" y1="192" x2="194" y2="192" stroke="{RULE}" stroke-width="0.3"/>'
    s += wline(16, 206, 178, "The one habit that closes the gap", n=2, gap=9)
    s += wline(16, 236, 110, "First step, small enough to do today")
    s += wline(134, 236, 60, "Today is")
    s += wline(16, 262, 178, "Who I tell about it")
    s += foot("Now / Next - free printable vision board template - MIT licensed")
    return s


# ---------------------------------------------------------------- 5. 90-day
def sheet_sprint():
    s = head("The 90-Day Sprint", "Three months, three proofs. A vision board with a deadline.")
    rows = [("FOCUS", "What gets my best hour"), ("PROOF", "What exists at the end of the month"), ("REWARD", "What I give myself")]
    cw, gx = 56.7, 4
    for c in range(3):
        x = 16 + c * (cw + gx)
        s += (
            f'<text x="{x + cw / 2}" y="42" text-anchor="middle" font-family="{SERIF}" '
            f'font-size="7" fill="{INK}">Month {c + 1}</text>'
        )
        s += box(x, 47, cw, 44, "picture", "")
        for r, (lab, hint) in enumerate(rows):
            y = 96 + r * 40
            s += f'<rect x="{x}" y="{y}" width="{cw}" height="34" rx="2.2" fill="{SOFT}" stroke="{RULE}" stroke-width="0.35"/>'
            s += (
                f'<text x="{x + 3}" y="{y + 6.2}" font-family="{SANS}" font-size="3.7" '
                f'letter-spacing="0.55" fill="{ACC}">{lab}</text>'
            )
            if c == 0:
                s += (
                    f'<text x="{x + 3}" y="{y + 11}" font-family="{SANS}" font-size="3.1" '
                    f'fill="#B0B0B8">{hint}</text>'
                )
            for k in range(3):
                yy = y + 16 + k * 6
                s += f'<line x1="{x + 3}" y1="{yy}" x2="{x + cw - 3}" y2="{yy}" stroke="{RULE}" stroke-width="0.3"/>'
    s += wline(16, 236, 110, "Sprint starts")
    s += wline(134, 236, 60, "Sprint ends")
    s += wline(16, 262, 178, "What I stop doing for these 90 days")
    s += foot("The 90-Day Sprint - free printable vision board template - MIT licensed")
    return s


# ---------------------------------------------------------------- 6. pocket 4up
def sheet_pocket():
    s = head("Pocket Cards (4 per page)", "Cut along the lines. One for the wallet, one for the mirror, two to give away.")
    cw, ch = 85, 110
    for i in range(4):
        x = 18 + (i % 2) * (cw + 4)
        y = 40 + (i // 2) * (ch + 6)
        s += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="3" fill="#FFFFFF" stroke="{RULE}" stroke-width="0.4" stroke-dasharray="1.6 1.4"/>'
        s += f'<rect x="{x + 6}" y="{y + 7}" width="{cw - 12}" height="46" rx="2" fill="{SOFT}" stroke="{RULE}" stroke-width="0.3"/>'
        s += (
            f'<text x="{x + cw / 2}" y="{y + 32}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="3.8" fill="#C7C7CC">one small picture</text>'
        )
        s += (
            f'<text x="{x + 6}" y="{y + 62}" font-family="{SANS}" font-size="3.5" '
            f'letter-spacing="0.5" fill="{ACC}">I AM SOMEONE WHO</text>'
        )
        for k in range(2):
            yy = y + 68 + k * 7
            s += f'<line x1="{x + 6}" y1="{yy}" x2="{x + cw - 6}" y2="{yy}" stroke="{RULE}" stroke-width="0.3"/>'
        s += (
            f'<text x="{x + 6}" y="{y + 88}" font-family="{SANS}" font-size="3.5" '
            f'letter-spacing="0.5" fill="{ACC}">NEXT STEP</text>'
        )
        s += f'<line x1="{x + 6}" y1="{y + 94}" x2="{x + cw - 6}" y2="{y + 94}" stroke="{RULE}" stroke-width="0.3"/>'
        s += (
            f'<text x="{x + 6}" y="{y + 104}" font-family="{SANS}" font-size="3.2" fill="{MUTED}">'
            f'visionboard.bemooore.com</text>'
        )
    s += foot("Pocket Cards - free printable vision board template - MIT licensed")
    return s


SHEETS = [
    ("six-zones", "Six Life Zones", "The classic. Six areas of life, one image each, plus the sentence that ties them together.", sheet_six_zones),
    ("one-goal", "One Goal, Loud", "For a single goal that deserves the whole page. One image, three reasons, one next action.", sheet_one_goal),
    ("year-wheel", "The 12-Month Wheel", "A word per month around a single word for the year. Fills up as the year goes.", sheet_year_wheel),
    ("now-next", "Now / Next", "An honest picture of today next to the chosen picture of later, and the habit between them.", sheet_now_next),
    ("sprint-90", "The 90-Day Sprint", "Three months, three proofs. A vision board that has a deadline attached.", sheet_sprint),
    ("pocket", "Pocket Cards", "Four wallet-sized cards on one page. For the mirror, the wallet, and two to give away.", sheet_pocket),
]

CTA = ("https://visionboard.bemooore.com/?utm_source=ghpages_templates&utm_medium=referral"
       "&utm_campaign=printable_templates")
CTA_TOOL = ("https://visionboard.bemooore.com/free-vision-board-maker/?utm_source=ghpages_templates"
            "&utm_medium=referral&utm_campaign=printable_templates")


def main():
    cards, sheets = [], []
    for slug, name, blurb, fn in SHEETS:
        svg = (f'<svg id="svg-{slug}" class="sheet" viewBox="0 0 {W} {H}" '
               f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{name} printable vision board template">'
               f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>{fn()}</svg>')
        cards.append(f'''<article class="card" id="{slug}">
  <div class="card-head">
    <h3>{name}</h3>
    <p>{blurb}</p>
  </div>
  <div class="preview">{svg}</div>
  <div class="actions">
    <button class="btn primary" data-print="{slug}">Print this sheet</button>
    <button class="btn" data-svg="{slug}" data-name="{slug}">Download SVG</button>
    <button class="btn" data-png="{slug}" data-name="{slug}">Download PNG</button>
  </div>
</article>''')
        sheets.append(slug)

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>6 Free Printable Vision Board Templates (PDF-ready, A4 &amp; US Letter) - MIT licensed</title>
<meta name="description" content="Six free printable vision board templates you can print straight from the browser on A4 or US Letter. No signup, no email, MIT licensed. Download as SVG or PNG, or generate one from your own goals.">
<link rel="canonical" href="https://pittner.github.io/vision-board-templates/">
<meta property="og:type" content="website">
<meta property="og:title" content="6 Free Printable Vision Board Templates - no signup, MIT licensed">
<meta property="og:description" content="Print-ready A4 and US Letter vision board sheets. Print from the browser, or download SVG/PNG. Free and MIT licensed.">
<meta property="og:url" content="https://pittner.github.io/vision-board-templates/">
<style>
:root{{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#6D28D9;--bg:#FBFAF9}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
a{{color:var(--acc)}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
header.hero{{padding:56px 0 28px}}
h1{{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}}
.lede{{font-size:18px;color:#374151;max-width:64ch;margin:0 0 22px}}
.meta{{font-size:14px;color:var(--muted)}}
.bar{{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:22px 0 0}}
.btn{{appearance:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}}
.btn:hover{{border-color:var(--acc);color:var(--acc)}}
.btn.primary{{background:var(--acc);border-color:var(--acc);color:#fff}}
.btn.primary:hover{{background:#5B21B6;color:#fff}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:26px;padding:14px 0 40px}}
.card{{background:#fff;border:1px solid var(--rule);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
.card-head{{padding:18px 20px 4px}}
.card-head h3{{margin:0 0 6px;font:600 19px/1.25 Georgia,serif}}
.card-head p{{margin:0;font-size:14px;color:var(--muted)}}
.preview{{padding:14px 20px}}
.preview svg{{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:6px}}
.actions{{margin-top:auto;padding:6px 20px 20px;display:flex;gap:8px;flex-wrap:wrap}}
section.block{{padding:34px 0;border-top:1px solid var(--rule)}}
section.block h2{{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}}
section.block p{{max-width:70ch;color:#374151}}
ol.how{{max-width:70ch;color:#374151;padding-left:20px}}
ol.how li{{margin:8px 0}}
.offer{{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:24px;margin:8px 0 0}}
.offer h2{{margin-top:0}}
footer{{padding:30px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}}
.faq h3{{font:600 16px/1.4 inherit;margin:18px 0 4px}}
.faq p{{margin:0;color:#374151}}
@media print{{
  body{{background:#fff}}
  .wrap>*:not(.printzone),.card-head,.actions,.preview svg:not(.printing){{display:none!important}}
  .printzone{{display:block!important}}
  .printzone svg{{width:100%;height:auto;display:block;border:0}}
}}
@page{{size:A4 portrait;margin:0}}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Six free printable vision board templates</h1>
  <p class="lede">Print-ready sheets you can send to a printer straight from this page. No signup, no email address, no watermark. Every sheet is plain SVG under an MIT licence, so you can edit it, remix it, or put it in a workshop deck.</p>
  <p class="meta">A4 and US Letter &middot; browser print &middot; SVG and PNG download &middot; MIT licensed</p>
  <div class="bar">
    <button class="btn primary" id="pageA4" aria-pressed="true">Paper: A4</button>
    <button class="btn" id="pageLetter" aria-pressed="false">Paper: US Letter</button>
    <a class="btn" href="{CTA_TOOL}" data-cta="hero_free_tool">Make a digital one instead</a>
  </div>
</header>

<div class="grid">
{chr(10).join(cards)}
</div>

<section class="block">
  <h2>How to use a printed vision board</h2>
  <ol class="how">
    <li>Pick the sheet that matches your moment. A new year wants the wheel, a breakup or a job change wants <a href="#now-next">Now / Next</a>, one obsession wants <a href="#one-goal">One Goal, Loud</a>.</li>
    <li>Print it. Plain paper is fine, 120&nbsp;g feels better under glue.</li>
    <li>Fill the picture areas first and the writing lines second. Images decide what you want, words decide what you do.</li>
    <li>Write a real next action with a real date on it. A board without a next step is a mood board.</li>
    <li>Put it where you already look every day. The fridge and the inside of a wardrobe door beat a drawer.</li>
  </ol>
</section>

<section class="block">
  <div class="offer">
    <h2>Do not want to cut out magazines?</h2>
    <p>These sheets are deliberately empty, because a printed board is something you fill by hand. If you would rather answer a few questions and have the images made for you, the same people who published these templates run a generator: you write your goals, it returns a finished board plus a 1080&times;1920 phone lock-screen wallpaper and one concrete next step. First preview is free and needs no e-mail address, the full-resolution unlock is a one-off &euro;8.99.</p>
    <p>
      <a class="btn primary" href="{CTA}" data-cta="offer_paid">See the generated version</a>
      <a class="btn" href="{CTA_TOOL}" data-cta="offer_free_tool">Free browser maker, no signup</a>
    </p>
  </div>
</section>

<section class="block faq">
  <h2>Questions</h2>
  <h3>Is this really free?</h3>
  <p>Yes. The sheets are MIT licensed. Print them, sell the workshop you run with them, put them in a client pack. Attribution is welcome and not required.</p>
  <h3>Can I get a PDF?</h3>
  <p>Use the print button and choose &ldquo;Save as PDF&rdquo; in the print dialog. That produces a vector PDF at the exact paper size, which is better than any PDF we could host.</p>
  <h3>Will it print correctly on US Letter?</h3>
  <p>Switch the paper toggle at the top before printing. The sheets are drawn at A4 proportions and are scaled to fit Letter with a small margin, so nothing is cut off.</p>
  <h3>Where is the source?</h3>
  <p>On <a href="https://github.com/pittner/vision-board-templates">GitHub</a>. The whole page is one static HTML file with inline SVG and no build step.</p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="{CTA}" data-cta="footer_paid">visionboard.bemooore.com</a> &middot;
  sister projects:
  <a href="https://pittner.github.io/vision-board-prompts/">AI vision board prompts</a>,
  <a href="https://pittner.github.io/free-vision-board-maker/">free digital maker</a>,
  <a href="https://pittner.github.io/">all free tools</a>
</footer>
</div>

<div class="printzone" id="printzone" style="display:none"></div>

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{{"@type":"Question","name":"Are these vision board templates free?","acceptedAnswer":{{"@type":"Answer","text":"Yes. All six printable vision board templates are MIT licensed. You can print them, edit them, and use them in paid workshops. Attribution is welcome but not required."}}}},
{{"@type":"Question","name":"How do I get a PDF of the vision board template?","acceptedAnswer":{{"@type":"Answer","text":"Press the print button on any sheet and choose Save as PDF in the print dialog. That produces a vector PDF at the exact paper size."}}}},
{{"@type":"Question","name":"Do the templates print on US Letter as well as A4?","acceptedAnswer":{{"@type":"Answer","text":"Yes. Switch the paper toggle at the top of the page before printing. The sheets are scaled to fit US Letter with a small margin so nothing is cut off."}}}}
]}}
</script>

<script>
(function(){{
  var EP='https://visionboard.bemooore.com/api/event.php',P='ghpages_templates',engaged=false;
  function beacon(ev,label){{
    try{{
      var b=JSON.stringify({{event:ev,utm:P+' | '+label+' | '+location.search}});
      if(navigator.sendBeacon){{navigator.sendBeacon(EP,new Blob([b],{{type:'text/plain'}}));}}
      else{{fetch(EP,{{method:'POST',body:b,keepalive:true,mode:'no-cors'}});}}
    }}catch(e){{}}
  }}
  function engage(how){{ if(engaged)return; engaged=true; beacon('page_engaged',how); }}
  setTimeout(function(){{engage('dwell6s');}},6000);
  window.addEventListener('scroll',function(){{
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  }},{{passive:true}});
  document.addEventListener('click',function(e){{
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  }});

  // Paper size: swap the @page rule, because @page cannot be set from JS directly.
  var ps=document.createElement('style'); document.head.appendChild(ps);
  function paper(size){{
    ps.textContent='@page{{size:'+size+' portrait;margin:'+(size==='A4'?'0':'6mm')+'}}';
    document.getElementById('pageA4').classList.toggle('primary',size==='A4');
    document.getElementById('pageLetter').classList.toggle('primary',size!=='A4');
    document.getElementById('pageA4').setAttribute('aria-pressed',String(size==='A4'));
    document.getElementById('pageLetter').setAttribute('aria-pressed',String(size!=='A4'));
  }}
  paper('A4');
  document.getElementById('pageA4').onclick=function(){{paper('A4');beacon('cta_click','paper_a4');}};
  document.getElementById('pageLetter').onclick=function(){{paper('Letter');beacon('cta_click','paper_letter');}};

  function svgOf(slug){{ return document.getElementById('svg-'+slug); }}
  function serialize(slug){{
    var s=svgOf(slug).cloneNode(true); s.removeAttribute('class'); s.removeAttribute('id');
    s.setAttribute('xmlns','http://www.w3.org/2000/svg');
    s.setAttribute('width','210mm'); s.setAttribute('height','297mm');
    return '<?xml version="1.0" encoding="UTF-8"?>\\n'+new XMLSerializer().serializeToString(s);
  }}
  function save(blob,name){{
    var u=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=u;a.download=name;document.body.appendChild(a);a.click();
    setTimeout(function(){{URL.revokeObjectURL(u);a.remove();}},1500);
  }}
  document.addEventListener('click',function(e){{
    var b=e.target.closest('button'); if(!b)return;
    var slug;
    if((slug=b.getAttribute('data-print'))){{
      var z=document.getElementById('printzone');
      z.innerHTML=''; z.appendChild(svgOf(slug).cloneNode(true)); z.style.display='block';
      beacon('template_print',slug);
      window.print();
      setTimeout(function(){{z.style.display='none';z.innerHTML='';}},800);
    }} else if((slug=b.getAttribute('data-svg'))){{
      save(new Blob([serialize(slug)],{{type:'image/svg+xml'}}),'vision-board-'+slug+'.svg');
      beacon('template_download',slug+'|svg');
    }} else if((slug=b.getAttribute('data-png'))){{
      var img=new Image(), src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(serialize(slug))));
      img.onload=function(){{
        var c=document.createElement('canvas'); c.width=1654; c.height=2339; // A4 @ 200dpi
        var x=c.getContext('2d'); x.fillStyle='#fff'; x.fillRect(0,0,c.width,c.height);
        x.drawImage(img,0,0,c.width,c.height);
        c.toBlob(function(bl){{ save(bl,'vision-board-'+slug+'.png'); }},'image/png');
      }};
      img.src=src;
      beacon('template_download',slug+'|png');
    }}
  }});
}})();
</script>
</body>
</html>
'''
    out = pathlib.Path(__file__).with_name("index.html")
    out.write_text(page, encoding="utf-8")
    print("wrote", out, len(page), "bytes,", len(SHEETS), "sheets")


if __name__ == "__main__":
    main()
