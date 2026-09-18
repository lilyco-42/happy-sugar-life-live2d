# 05 · 导出与交付

## 导出帧序列

Stretchy **Export frames** 弹窗设置：

```
Type: Sequence
Format: PNG
Animation: Current
FPS: 24
Image Contains: Canvas area
Output Scale: 100
Background: Transparent
Export to: ZIP file
```

点 Export → 浏览器下载 `export(n).zip`（约 21MB，48 张 768×768 透明 PNG，路径 `Animation_1/frame_0001..0048.png`）。

## 合成视频 / GIF

```bash
# MP4（白底视频）
ffmpeg -y -framerate 24 -i "Animation_1/frame_%04d.png" -c:v libx264 -pix_fmt yuv420p -crf 18 anim.mp4

# GIF（透明→循环）
ffmpeg -y -framerate 24 -i "Animation_1/frame_%04d.png" -vf "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 anim.gif
```

## 保存可编辑工程

Save project 弹窗：
1. 切 **Download File** tab（默认是 Save to Library，只存浏览器 IndexedDB，不产生文件）。
2. 改工程名（如 `sato_sugar_rig_v9`）。
3. 点 **Save** → 下载 `.stretch`（约 2.3MB）。

> 同名文件再次保存会弹 Overwrite 确认。`.stretch` 可直接拖回 Stretchy 继续编辑（动画完整保留）。

## 交付给用户

- **动画演示**：MP4（优先，画质好）+ GIF（方便预览/嵌入）。
- **可编辑工程**：`.stretch` 文件。
- **教学文档**：说明怎么打开、怎么改、遇到问题怎么排查。
- **帧序列**：透明 PNG 包（给需要逐帧素材的场景）。

## 验证（交付前必做）

1. `scripts/verify_frames.py` 逐帧检查：眨眼帧眼睛闭合、非眨眼帧有瞳孔、转头帧头部中心偏移 ≤ 3px。
2. 播放合成视频目检一遍（重点：眼睛状态、头部是否分离、整体是否自然）。
3. 确认 `.stretch` 重载后动画仍在（`Animation 1` + head/eyes/torso 轨道）。
