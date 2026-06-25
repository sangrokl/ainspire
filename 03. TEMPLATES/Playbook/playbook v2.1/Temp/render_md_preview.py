import markdown, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(__file__).resolve().parent / "md_preview"
OUT.mkdir(exist_ok=True)

FILES = [
    "CLAUDE.md",
    "README.md",
    "18_commercial_storyboard_playbook_v2/00_core.md",
    "18_commercial_storyboard_playbook_v2/01_planning_G1-G11.md",
    "18_commercial_storyboard_playbook_v2/02_production_G12-G17.md",
    "18_commercial_storyboard_playbook_v2/03_reference_enhance-prompts.md",
    "18_commercial_storyboard_playbook_v2/04_reference_lessons-appendix.md",
]

CSS = """
body { font-family: -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
       max-width: 880px; margin: 0 auto; padding: 32px 24px 80px; line-height: 1.65; color: #1a1a1a; }
h1 { border-bottom: 3px solid #333; padding-bottom: 10px; }
h2 { border-bottom: 1px solid #ddd; padding-bottom: 6px; margin-top: 40px; }
h3 { margin-top: 28px; color: #333; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 0.95em; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; vertical-align: top; }
th { background: #f2f2f2; }
code { background: #f5f5f5; padding: 1px 5px; border-radius: 4px; font-size: 0.9em; }
pre { background: #1e1e1e; color: #d4d4d4; padding: 14px; border-radius: 6px; overflow-x: auto; }
pre code { background: none; color: inherit; padding: 0; }
blockquote { border-left: 4px solid #4a90d9; margin: 16px 0; padding: 4px 16px; background: #f7faff; color: #333; }
hr { border: none; border-top: 1px solid #ddd; margin: 32px 0; }
a { color: #1a73e8; }
.nav { background: #fafafa; border: 1px solid #ddd; padding: 10px 16px; border-radius: 6px; margin-bottom: 24px; font-size: 0.9em; }
.nav a { margin-right: 14px; }
"""

NAV = '<div class="nav">' + " | ".join(
    f'<a href="{pathlib.Path(f).name.replace(".md", ".html")}">{pathlib.Path(f).name}</a>' for f in FILES
) + "</div>"

for rel in FILES:
    src = ROOT / rel
    text = src.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])
    html = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<title>{pathlib.Path(rel).name}</title>
<style>{CSS}</style></head>
<body>
{NAV}
{body}
</body></html>"""
    out_name = pathlib.Path(rel).name.replace(".md", ".html")
    (OUT / out_name).write_text(html, encoding="utf-8")
    print("wrote", out_name)

print("\nOpen:", OUT / "CLAUDE.html")
