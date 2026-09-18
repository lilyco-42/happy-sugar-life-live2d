#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_frames.py — 对 Stretchy 导出的动画帧做回归验证。

检测三件事（对应本项目三个历史 bug）：
  1. 眨眼帧：眼睛是否闭合（闭眼帧瞳孔玫红像素应显著低于睁眼帧）
  2. 非眨眼帧：是否有瞳孔（防止"一直白眼"——瞳孔被 x/y 轨道移出脸部）
  3. 转头帧：头部 alpha 包围盒中心偏移应 ≤ 3px（防止"分头"）

用法:
    python verify_frames.py <frame_dir> [--eye-box X1,Y1,X2,Y2] [--rose-thresh 500]

示例:
    python verify_frames.py sato_frames_v9\\Animation_1
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image


def rose_pixels(img, box):
    """统计眼睛区域内"玫红瞳孔"像素数（r 高 / g 低 / b 中）。"""
    crop = img.crop(box).convert("RGB")
    arr = np.array(crop)
    r, g, b = arr[..., 0].astype(int), arr[..., 1].astype(int), arr[..., 2].astype(int)
    return int(((r > 120) & (g < 110) & (b > 100) & (b < 190)).sum())


def alpha_center_x(img):
    """返回图像 alpha 非透明区域的包围盒中心 x（用于检测头部偏移）。"""
    alpha = img.split()[3]
    bbox = alpha.getbbox()
    if bbox is None:
        return None
    return (bbox[0] + bbox[2]) // 2


def main():
    ap = argparse.ArgumentParser(description="Verify Stretchy exported animation frames")
    ap.add_argument("frame_dir", help="Directory containing frame_0001.png ... frame_NNNN.png")
    ap.add_argument("--eye-box", default="320,175,450,235",
                    help="Eye region as X1,Y1,X2,Y2 (in frame pixel coords)")
    ap.add_argument("--rose-thresh", type=int, default=250,
                    help="Min rose pixels to consider 'pupil visible' (tune to your character)")
    args = ap.parse_args()

    frames = sorted(f for f in os.listdir(args.frame_dir) if f.startswith("frame_") and f.endswith(".png"))
    if not frames:
        print("No frames found in", args.frame_dir)
        sys.exit(1)

    box = tuple(int(v) for v in args.eye_box.split(","))
    rose = {}
    for f in frames:
        img = Image.open(os.path.join(args.frame_dir, f))
        rose[f] = rose_pixels(img, box)

    # 睁眼帧：瞳孔可见
    open_frames = [f for f in frames if rose[f] > args.rose_thresh]
    # 闭眼帧：瞳孔不可见（眨眼瞬间）
    closed_frames = [f for f in frames if rose[f] <= args.rose_thresh]

    n = len(frames)
    print(f"帧数: {n}  瞳孔可见(睁眼): {len(open_frames)}  瞳孔不可见(闭眼): {len(closed_frames)}")
    if not open_frames:
        print("✗ 没有任何帧显示瞳孔 —— '一直白眼'（检查 eyes 组 x/y 轨道是否被误加位移）")
        sys.exit(1)
    if len(open_frames) > n * 0.95:
        print("⚠ 几乎没有闭眼帧 —— 眨眼可能没生效（检查 eyes scaleY 关键帧）")
    else:
        print("✓ 眨眼正常：多数帧睁眼（有瞳孔），部分帧闭眼")

    # 转头偏移：对比第一帧与中点帧的 alpha 中心
    c0 = alpha_center_x(Image.open(os.path.join(args.frame_dir, frames[0])))
    mid = frames[len(frames) // 2]
    c1 = alpha_center_x(Image.open(os.path.join(args.frame_dir, mid)))
    if c0 is not None and c1 is not None:
        off = abs(c0 - c1)
        print(f"头部中心偏移: 帧1={c0}  {mid}={c1}  偏移={off}px  {'✓' if off <= 3 else '✗ 分头风险'}")
    else:
        print("⚠ 无法计算 alpha 中心（帧可能全透明）")

    print("\n睁眼帧示例:", open_frames[:3], " 闭眼帧示例:", closed_frames[:3])


if __name__ == "__main__":
    main()
