#!/usr/bin/env python3
"""Generate the teacher praise wall HTML page."""

import json
import os
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"

# Directory layout: 主讲老师好评墙/王淏然老师2025届学生好评整理/...
TEACHER_NAME = "王淏然"
YEARS = [
    ("2025届", "王淏然老师2025届学生好评整理"),
    ("2028届", "王淏然老师2028届学生好评整理"),
]


def collect_reviews():
    reviews = []
    for year, folder in YEARS:
        folder_path = ROOT / folder
        if not folder_path.exists():
            print(f"Warning: folder not found: {folder_path}")
            continue
        for f in sorted(folder_path.iterdir()):
            if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
                rel = quote(f"{folder}/{f.name}")
                reviews.append(
                    {
                        "year": year,
                        "src": rel,
                        "title": f.stem,
                    }
                )
    return reviews


def render_html(reviews):
    data_json = json.dumps(reviews, ensure_ascii=False)
    total = len(reviews)
    year_counts = {}
    for r in reviews:
        year_counts[r["year"]] = year_counts.get(r["year"], 0) + 1

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{TEACHER_NAME}老师 · 学员好评墙</title>
  <style>
    :root {{
      --bg: #f6f7f9;
      --card-bg: #ffffff;
      --primary: #1e5dbc;
      --primary-light: #e8f0fc;
      --accent: #ff6b35;
      --text: #1f2937;
      --text-muted: #6b7280;
      --border: #e5e7eb;
      --shadow: 0 4px 20px rgba(0,0,0,0.06);
      --radius: 12px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }}
    header {{
      background: linear-gradient(135deg, #1e5dbc 0%, #3b82f6 100%);
      color: #fff;
      padding: 48px 20px 36px;
      text-align: center;
      position: relative;
      overflow: hidden;
    }}
    header::before {{
      content: "";
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 80% 20%, rgba(255,255,255,0.18) 0%, transparent 40%);
    }}
    header h1 {{
      margin: 0 0 8px;
      font-size: clamp(28px, 5vw, 42px);
      font-weight: 700;
      position: relative;
    }}
    header p {{
      margin: 0 auto;
      max-width: 640px;
      font-size: 16px;
      opacity: 0.92;
      position: relative;
    }}
    .stats {{
      display: flex;
      justify-content: center;
      gap: 16px;
      flex-wrap: wrap;
      margin-top: 24px;
      position: relative;
    }}
    .stat {{
      background: rgba(255,255,255,0.15);
      backdrop-filter: blur(4px);
      padding: 10px 20px;
      border-radius: 999px;
      font-size: 14px;
    }}
    .stat strong {{
      font-size: 20px;
      margin-right: 4px;
    }}

    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 16px 64px;
    }}

    .filters {{
      display: flex;
      justify-content: center;
      gap: 10px;
      margin-bottom: 28px;
      flex-wrap: wrap;
    }}
    .filters button {{
      border: 1px solid var(--border);
      background: var(--card-bg);
      color: var(--text);
      padding: 8px 18px;
      border-radius: 999px;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s ease;
    }}
    .filters button:hover {{
      border-color: var(--primary);
      color: var(--primary);
    }}
    .filters button.active {{
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }}

    .wall {{
      column-count: 1;
      column-gap: 16px;
    }}
    @media (min-width: 520px) {{ .wall {{ column-count: 2; }} }}
    @media (min-width: 860px) {{ .wall {{ column-count: 3; }} }}
    @media (min-width: 1200px) {{ .wall {{ column-count: 4; }} }}

    .card {{
      break-inside: avoid;
      background: var(--card-bg);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow: hidden;
      margin-bottom: 16px;
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      position: relative;
    }}
    .card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    .card img {{
      display: block;
      width: 100%;
      height: auto;
      background: #f0f0f0;
    }}
    .card .caption {{
      padding: 12px 14px;
      font-size: 13px;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
    }}
    .card .caption .year-tag {{
      display: inline-block;
      background: var(--primary-light);
      color: var(--primary);
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 999px;
      margin-bottom: 6px;
      font-weight: 600;
    }}
    .card .caption .title {{
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      color: var(--text);
      line-height: 1.5;
    }}

    .empty {{
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
    }}

    .lightbox {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.9);
      z-index: 1000;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      padding: 20px;
    }}
    .lightbox.open {{ display: flex; }}
    .lightbox img {{
      max-width: 100%;
      max-height: 82vh;
      border-radius: 8px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }}
    .lightbox .lb-caption {{
      color: #fff;
      margin-top: 14px;
      max-width: 900px;
      text-align: center;
      font-size: 15px;
      opacity: 0.9;
    }}
    .lightbox .close,
    .lightbox .nav {{
      position: absolute;
      background: rgba(255,255,255,0.12);
      border: none;
      color: #fff;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      font-size: 22px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }}
    .lightbox .close:hover,
    .lightbox .nav:hover {{ background: rgba(255,255,255,0.25); }}
    .lightbox .close {{ top: 16px; right: 16px; }}
    .lightbox .prev {{ left: 16px; top: 50%; transform: translateY(-50%); }}
    .lightbox .next {{ right: 16px; top: 50%; transform: translateY(-50%); }}

    footer {{
      text-align: center;
      padding: 0 20px 40px;
      color: var(--text-muted);
      font-size: 13px;
    }}

    .loading {{
      text-align: center;
      padding: 40px;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>
  <header>
    <h1>{TEACHER_NAME}老师 · 学员好评墙</h1>
    <p>真实学员反馈，见证点滴进步。每一张截图背后，都是努力与成长的故事。</p>
    <div class="stats">
      <div class="stat"><strong id="total-stat">{total}</strong>条好评</div>
      <div class="stat"><strong id="y2025-stat">{year_counts.get('2025届', 0)}</strong>2025届</div>
      <div class="stat"><strong id="y2028-stat">{year_counts.get('2028届', 0)}</strong>2028届</div>
    </div>
  </header>

  <main class="container">
    <div class="filters" role="tablist" aria-label="届别筛选">
      <button class="active" data-filter="all" role="tab" aria-selected="true">全部</button>
      <button data-filter="2025届" role="tab" aria-selected="false">2025届</button>
      <button data-filter="2028届" role="tab" aria-selected="false">2028届</button>
    </div>

    <div class="wall" id="wall"></div>
    <div class="empty" id="empty" style="display:none;">暂无该分类的好评</div>
  </main>

  <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="图片预览">
    <button class="close" aria-label="关闭">&times;</button>
    <button class="nav prev" aria-label="上一张">&#10094;</button>
    <button class="nav next" aria-label="下一张">&#10095;</button>
    <img id="lb-img" src="" alt="好评截图" />
    <div class="lb-caption" id="lb-caption"></div>
  </div>

  <footer>
    数据整理自本地好评截图，持续更新中。
  </footer>

  <script>
    const reviews = {data_json};
    const wall = document.getElementById('wall');
    const empty = document.getElementById('empty');
    const filterButtons = document.querySelectorAll('.filters button');
    const lightbox = document.getElementById('lightbox');
    const lbImg = document.getElementById('lb-img');
    const lbCaption = document.getElementById('lb-caption');

    let currentFilter = 'all';
    let visibleReviews = [];
    let currentIndex = 0;

    function createCard(review, index) {{
      const card = document.createElement('div');
      card.className = 'card';
      card.setAttribute('data-year', review.year);
      card.setAttribute('data-index', index);
      card.innerHTML = `
        <img loading="lazy" src="${{review.src}}" alt="${{review.title}}" />
        <div class="caption">
          <div class="year-tag">${{review.year}}</div>
          <div class="title">${{review.title}}</div>
        </div>
      `;
      card.addEventListener('click', () => openLightbox(index));
      return card;
    }}

    function render(filter) {{
      wall.innerHTML = '';
      visibleReviews = filter === 'all'
        ? reviews
        : reviews.filter(r => r.year === filter);

      if (visibleReviews.length === 0) {{
        empty.style.display = 'block';
      }} else {{
        empty.style.display = 'none';
        visibleReviews.forEach((r, i) => wall.appendChild(createCard(r, i)));
      }}
    }}

    filterButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterButtons.forEach(b => {{
          b.classList.remove('active');
          b.setAttribute('aria-selected', 'false');
        }});
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        currentFilter = btn.getAttribute('data-filter');
        render(currentFilter);
      }});
    }});

    function openLightbox(index) {{
      currentIndex = index;
      const r = visibleReviews[index];
      lbImg.src = r.src;
      lbCaption.textContent = `[${{r.year}}] ${{r.title}}`;
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    }}

    function closeLightbox() {{
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
      lbImg.src = '';
    }}

    function showPrev(e) {{
      if (e) e.stopPropagation();
      if (visibleReviews.length <= 1) return;
      currentIndex = (currentIndex - 1 + visibleReviews.length) % visibleReviews.length;
      openLightbox(currentIndex);
    }}

    function showNext(e) {{
      if (e) e.stopPropagation();
      if (visibleReviews.length <= 1) return;
      currentIndex = (currentIndex + 1) % visibleReviews.length;
      openLightbox(currentIndex);
    }}

    document.querySelector('.lightbox .close').addEventListener('click', closeLightbox);
    document.querySelector('.lightbox .prev').addEventListener('click', showPrev);
    document.querySelector('.lightbox .next').addEventListener('click', showNext);
    lightbox.addEventListener('click', (e) => {{
      if (e.target === lightbox) closeLightbox();
    }});

    document.addEventListener('keydown', (e) => {{
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') showPrev();
      if (e.key === 'ArrowRight') showNext();
    }});

    render('all');
  </script>
</body>
</html>
"""


def main():
    reviews = collect_reviews()
    html = render_html(reviews)
    OUT.write_text(html, encoding="utf-8")
    print(f"Generated {OUT} with {len(reviews)} reviews.")


if __name__ == "__main__":
    main()
