# 04 · 动画制作（轨道纪律）

## 三种基础动画

| 动画 | 操作组 | 属性 | 关键帧（时间 ms / 值） |
|---|---|---|---|
| 转头 | head | rotation | 0→0，500→+6，1000→-6，2000→0 |
| 眨眼 | eyes | scaleY | 250→1，333→0.05，375→0.05，417→1 |
| 呼吸 | torso | scaleY | 0→1，541→1.02，1041→1，1583→1.02，2000→1 |

（24fps，动画总长 2000ms = 48 帧）

## 时间轴操作流程（GUI）

1. 切 **Animation** 模式。
2. 点时间轴标尺移动 playhead 到目标帧。
3. 选中目标组（画布上点组圆环，或图层树点组名）。
4. 改 INSPECTOR 里的 Rotation / ScaleY 值（React 输入框：输入后按 Enter 生效）。
5. **点击该组的时间轴轨道行**（选中轨道）→ 按 `K` 插入关键帧（出现菱形即成功）。
6. 重复 2–5 在多个时间点打关键帧，形成动画曲线。

## ⚠️ 轨道纪律（本项目最贵的教训）

**做动画时只给"该给的属性"加关键帧：**

- 转头 → 只加 `rotation`
- 眨眼 → 只加 `scaleY`
- 呼吸 → 只加 `scaleY`

**严禁误加：**
- **`x` / `y` 位移**：误加会让图层"幽灵位移"。本项目 v9 修复的就是这个 —— eyes 组的 x/y 轨道被误加了关键帧（458ms 起 y 移到 +40px），瞳孔被移出脸部、被衣领遮挡，只剩眼白 → 用户看到"一直白眼"。
- **`visible`**：只接受布尔。误写入 0.766 之类数值会让图层半透明/闪变，全部改回 1。
- **`opacity`**：除非要做淡入淡出，否则保持 1。

## 动画曲线

Stretchy 默认 **Ease Both**（三次贝塞尔 [0.42,0,0.58,1]，S 形缓入缓出），转头自带柔和过渡。关键帧右键菜单可改 Linear / Ease In / Ease Out / Stepped / Custom。

## 检查动画数据（不依赖 GUI）

`.stretch` 是 ZIP，读 `project.json`：

```python
import zipfile, json
with zipfile.ZipFile("sato_sugar_rig_v9.stretch") as z:
    proj = json.loads(z.read("project.json"))
for tr in proj["animations"][0]["tracks"]:
    print(tr["nodeId"], tr["property"], [k["value"] for k in tr["keyframes"]])
```

一眼扫出异常轨道（如 eyes 的 x/y 出现非 0 值、visible 出现非 1 值）。修完重打包：**textures 先写、project.json 最后写**。
