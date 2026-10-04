#!/usr/bin/env python3
"""fastfetch風のプロファイルカードを生成し、index.html と fastfetch に書き出す。"""
import re
import unicodedata

E = "\x1b"
RESET, BOLD = f"{E}[0m", f"{E}[1m"
LOGO_C = f"{E}[1;36m"   # ロゴの色
KEY_C = f"{E}[1;36m"    # キーの色
DIM = f"{E}[90m"

# ── 左側のロゴ（カンマ） ─────────────────────
LOGO = r"""
  ___          ____  _                   _ 
 / _ \ _ __   / ___|| |_ __ _  __ _  ___| |
| | | | '_ \  \___ \| __/ _` |/ _` |/ _ \ |
| |_| | | | |  ___) | || (_| | (_| |  __/_|
 \___/|_| |_| |____/ \__\__,_|\__, |\___(_)
                              |___/
                           __
                          |  |
                          |  |
           _______________|  |
          (_______________    \
                   (______)    |
                   (______)    |
                    (_____)___/
""".strip("\n").split("\n")

# ── 右側の情報 ──────────────────────────────
USER, HOST = "commana", "github.io"
INFO = [
    ("My Name", "Naoya Hokazono"),
    ("Job Title", "QUSIS Engineer Team Chief (Technical Manager)"),
    ("QUSIS HP", "https://qusis.jp/"),
    ("OS", "Arch Linux x86_64"),
    ("Editor", "Neovim"),
    ("Langs", "Rust, C#, Kotlin, Python, QML(Qt)"),
    ("Location", "Japan"),
    ("GitHub", "github.com/CommaNaa"),
    ("Web", "commanaa.github.io/page/"),
]

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def width(s: str) -> int:
    """ANSIを除いた表示幅（全角は2）"""
    s = ANSI_RE.sub("", s)
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def build() -> str:
    title = f"{KEY_C}{USER}{RESET}@{KEY_C}{HOST}{RESET}"
    right = [title, "-" * width(title)]
    right += [f"{KEY_C}{k}{RESET}: {v}" for k, v in INFO]
    right.append("")
    right.append("".join(f"{E}[4{i}m   " for i in range(8)) + RESET)
    right.append("".join(f"{E}[10{i}m   " for i in range(8)) + RESET)

    logo_w = max(width(l) for l in LOGO) + 3
    rows = max(len(LOGO), len(right))
    out = []
    for i in range(rows):
        l = LOGO[i] if i < len(LOGO) else ""
        r = right[i] if i < len(right) else ""
        pad = " " * (logo_w - width(l))
        out.append(f"  {LOGO_C}{l}{RESET}{pad}{r}".rstrip())
    return "\n".join([""] + out + ["", ""])


if __name__ == "__main__":
    card = build()
    head = '<meta http-equiv="refresh" content="0;url=/page/"><!--'
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(head + f"\r{E}[2K" + card + f"-->\r{E}[2K")
    with open("fastfetch", "w", encoding="utf-8") as f:
        f.write(card)
    print(card)
