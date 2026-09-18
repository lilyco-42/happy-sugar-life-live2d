# -*- coding: utf-8 -*-
"""裁切上半身立绘 + 填充正方形"""
from PIL import Image
import os

base = r"C:\Users\liuqi\Doubao\chats\2026-09-16\new-chat-2\live2d_hsl"
jobs = [("sato_live2d.png", "sato_upper.png"), ("shio_live2d.png", "shio_upper.png")]

for src, dst in jobs:
    img = Image.open(os.path.join(base, src)).convert("RGBA")
    w, h = img.size
    # 取顶部 78%（包含头+上半身）
    crop_h = int(h * 0.78)
    img_c = img.crop((0, 0, w, crop_h))
    # 填充为正方形（底部白底补全）
    side = max(w, crop_h)
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    canvas.paste(img_c, ((side - w) // 2, 0))
    out = os.path.join(base, dst)
    canvas.save(out)
    print(dst, canvas.size)
