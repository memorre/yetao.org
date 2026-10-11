"""Rebuild noto-sans-sc-subset.woff2 after changing the Chinese text in index.html.

    pip install fonttools brotli
    curl -LO "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf"
    python fonts/build-subset.py "NotoSansSC[wght].ttf"

Keeps only the Chinese characters and full-width punctuation that index.html uses, and only the
400-600 weight range the page needs, so the file stays small. Noto Sans SC is licensed under the
SIL Open Font License (OFL.txt).
"""
import re
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = Path(__file__).resolve().parent
# Same ranges as the unicode-range of the @font-face rule in index.html.
CJK = re.compile("[⺀-⿟　-〿㐀-䶿一-鿿豈-﫿＀-￯]")

html = (HERE.parent / "index.html").read_text(encoding="utf-8")
chars = "".join(sorted(set(CJK.findall(html))))

font = instancer.instantiateVariableFont(TTFont(sys.argv[1]), {"wght": (400, 600)})
options = subset.Options()
options.flavor = "woff2"
options.layout_features = ["*"]
options.name_IDs = ["*"]
subsetter = subset.Subsetter(options)
subsetter.populate(text=chars)
subsetter.subset(font)

out = HERE / "noto-sans-sc-subset.woff2"
font.flavor = "woff2"
font.save(out)
print(f"{len(chars)} characters -> {out.name} ({out.stat().st_size / 1024:.0f} KB)")
