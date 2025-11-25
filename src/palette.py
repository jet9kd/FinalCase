#!/usr/bin/env python3
"""
palette.py
Simple color histogram and dominant palette generator.

Usage:
  python src/palette.py assets/sample.jpg output --colors 6
"""
import sys
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import argparse

def make_output_dir(path):
    os.makedirs(path, exist_ok=True)

def save_histogram(img: Image.Image, outpath: str):
    arr = np.array(img)
    if arr.ndim == 2:  # grayscale
        plt.figure(figsize=(6,3))
        plt.hist(arr.ravel(), bins=256)
        plt.title("Grayscale Histogram")
        plt.tight_layout()
        plt.savefig(outpath)
        plt.close()
        return
    # RGB channels
    chans = ('red','green','blue')
    plt.figure(figsize=(8,4))
    colors = ('r','g','b')
    for i, color in enumerate(colors):
        plt.hist(arr[:,:,i].ravel(), bins=256, color=color, alpha=0.5, label=chans[i])
    plt.legend()
    plt.title("RGB Histograms")
    plt.xlabel("Pixel value")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def get_adaptive_palette(img: Image.Image, n_colors: int):
    # Convert to P mode with adaptive (Pillow does color quantization)
    pal_img = img.convert('P', palette=Image.ADAPTIVE, colors=n_colors)
    palette = pal_img.getpalette()  # list of RGB triplets flattened
    # palette list length = 768 (256*3) usually; take first n_colors
    colors = []
    for i in range(n_colors):
        r = palette[3*i]
        g = palette[3*i+1]
        b = palette[3*i+2]
        colors.append((r or 0, g or 0, b or 0))
    return colors

def save_palette_swatches(colors, outpath, sw=100, sh=100):
    n = len(colors)
    img = Image.new('RGB', (sw*n, sh))
    for i, c in enumerate(colors):
        block = Image.new('RGB', (sw, sh), c)
        img.paste(block, (i*sw, 0))
    img.save(outpath)

def generate_html(original_path, hist_path, palette_path, outpath):
    html = f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>Palette Visualizer</title>
<style>
body{{font-family: sans-serif; padding:20px}}
img{{max-width: 100%; height: auto; border: 1px solid #ddd}}
.container{{display:flex; gap:20px; flex-wrap:wrap}}
.card{{width:320px}}
</style>
</head>
<body>
<h1>Color Histogram & Palette Visualizer</h1>
<p>Input image: {os.path.basename(original_path)}</p>
<div class="container">
  <div class="card"><h3>Original</h3><img src="{os.path.basename(original_path)}" alt="original"></div>
  <div class="card"><h3>Histogram</h3><img src="{os.path.basename(hist_path)}" alt="histogram"></div>
  <div class="card"><h3>Palette</h3><img src="{os.path.basename(palette_path)}" alt="palette"></div>
</div>
</body>
</html>"""
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input image path")
    parser.add_argument("outdir", help="output directory")
    parser.add_argument("--colors", type=int, default=6, help="number of dominant colors")
    args = parser.parse_args()

    inp = args.input
    outdir = args.outdir
    n_colors = args.colors

    if not os.path.exists(inp):
        print(f"Input image not found: {inp}", file=sys.stderr)
        sys.exit(2)
    make_output_dir(outdir)
    # load image
    img = Image.open(inp).convert("RGB")

    # save a copy of original (in case input is outside)
    base_orig = os.path.join(outdir, os.path.basename(inp))
    img.save(base_orig)

    hist_path = os.path.join(outdir, "histogram.png")
    palette_path = os.path.join(outdir, "palette.png")
    html_path = os.path.join(outdir, "index.html")

    save_histogram(img, hist_path)
    colors = get_adaptive_palette(img, n_colors)
    save_palette_swatches(colors, palette_path)
    generate_html(base_orig, hist_path, palette_path, html_path)

    print("Generated:", hist_path, palette_path, html_path)

if __name__ == "__main__":
    main()
