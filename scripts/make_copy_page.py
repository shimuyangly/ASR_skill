#!/usr/bin/env python3
"""Create a copy-friendly transcript HTML page."""

from __future__ import annotations

import argparse
import html
from pathlib import Path


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8").strip() + "\n"


def build_page(title: str, audio_label: str, transcript: str, optimized: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(title)} 转录结果</title>
<style>
  :root {{ color-scheme: light; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
  body {{ margin: 0; background: #f6f7f7; color: #232323; }}
  main {{ max-width: 1180px; margin: 0 auto; padding: 28px 20px 40px; }}
  header {{ display: flex; justify-content: space-between; gap: 16px; align-items: end; margin-bottom: 20px; }}
  h1 {{ font-size: 24px; margin: 0 0 6px; }}
  p {{ margin: 0; color: #666; line-height: 1.5; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
  section {{ background: #fff; border: 1px solid #d8dddc; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,.04); }}
  .bar {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px 14px; border-bottom: 1px solid #e0e5e4; background: #fbfcfc; }}
  h2 {{ font-size: 16px; margin: 0; }}
  button {{ border: 1px solid #245f6f; background: #245f6f; color: #fff; border-radius: 6px; padding: 8px 12px; font-size: 14px; cursor: pointer; }}
  button:active {{ transform: translateY(1px); }}
  textarea {{ box-sizing: border-box; width: 100%; height: 72vh; border: 0; padding: 14px; resize: vertical; font-size: 14px; line-height: 1.75; color: #222; background: #fff; }}
  .note {{ font-size: 13px; }}
  @media (max-width: 900px) {{ .grid {{ grid-template-columns: 1fr; }} textarea {{ height: 60vh; }} header {{ display: block; }} }}
</style>
</head>
<body>
<main>
  <header>
    <div>
      <h1>{html.escape(title)}</h1>
      <p>两个版本都支持一键复制。</p>
    </div>
    <p class="note">音频：{html.escape(audio_label)}</p>
  </header>
  <div class="grid">
    <section>
      <div class="bar"><h2>逐字稿</h2><button onclick="copyText('verbatim', this)">复制逐字稿</button></div>
      <textarea id="verbatim" spellcheck="false">{html.escape(transcript)}</textarea>
    </section>
    <section>
      <div class="bar"><h2>AI优化稿</h2><button onclick="copyText('optimized', this)">复制优化稿</button></div>
      <textarea id="optimized" spellcheck="false">{html.escape(optimized)}</textarea>
    </section>
  </div>
</main>
<script>
async function copyText(id, btn) {{
  const el = document.getElementById(id);
  el.focus(); el.select();
  await navigator.clipboard.writeText(el.value);
  const old = btn.textContent;
  btn.textContent = '已复制';
  setTimeout(() => btn.textContent = old, 1200);
}}
</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--audio-label", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--optimized", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    page = build_page(
        args.title,
        args.audio_label,
        read_text(args.transcript),
        read_text(args.optimized),
    )
    Path(args.out).write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
