# 🍬 Happy Sugar Life — 砂糖 & 盐 Live2D 真骨骼动画

> 从一张 AI 立绘到可循环播放的骨骼动画（转头 / 眨眼 / 呼吸），全流程可复现。
> From a single AI illustration to a loopable bone-animated character (head-turn / blink / breathe) — fully reproducible pipeline.

**成果演示 · Result**（`assets/sato_live2d_anim_v10.mp4`，48 帧 / 24fps / 2s 循环，**v10 = 骨骼关节全量校正版**）：

| 动画 | 骨骼 | 轨道 |
|---|---|---|
| 转头 | head 组 rotation | 0° → +6° → -6° → 0° |
| 眨眼 | eyes 组 scaleY | 1 → 0.05 → 1（只在瞬间闭合） |
| 呼吸 | torso 组 scaleY | 1 → 1.02 → 1 |

**可编辑工程 · Editable project**: `assets/sato_sugar_rig_v10.stretch`（在 [Stretchy Studio](https://editor.stretchy.studio/) 打开继续编辑；v9 历史版保留在 `assets/sato_sugar_rig_v9.stretch`）

**v10 更新（2026-09-18）**：校正 8 个偏位关节 —— 肩（leftArm/rightArm 从画面顶角 → 真实肩线）、肘（leftElbow/rightElbow → 腰侧肘位）、髋/膝（leftLeg/rightLeg/leftKnee/rightKnee 位置修正）。动画行为不变（转头/眨眼/呼吸），但手臂与腿的骨骼旋转中心已就位，后续可安全添加挥手/走路等肢体动画。

---

## 为什么做这个 · Why

用户想要《Happy Sugar Life》中 **松坂砂糖（Sato）** 和 **盐（Shio）** 的 Live2D 真骨骼动画——不是静态立绘、不是贴纸、不是 GIF 纸片人，而是**骨骼驱动、可循环、可在编辑器里继续改**的动画。本机没有可用的 Cubism Editor（splash 卡死），所以采用了完全在线的替代管线。

## 工具链 · Toolchain

| 步骤 | 工具 | 用途 |
|---|---|---|
| 1. 立绘 | 文生图（Doubao image_gen） | 生成砂糖 / 盐角色立绘 |
| 2. 抠图 | mediakit `remove-image-background` | 去背景 |
| 3. 方形裁切 | `scripts/make_upper.py` | 裁 1597×1597 上半身方形 |
| 4. AI 分层 | HuggingFace **See-through** Space | 单图 → 22 层 PSD |
| 5. 绑骨 | **Stretchy Studio**（editor.stretchy.studio） | 导入 PSD → 骨骼 → 网格 |
| 6. 动画 | Stretchy 时间轴 | 关键帧：rotation / scaleY |
| 7. 导出 | Stretchy Export frames → ffmpeg | 帧序列 → MP4 / GIF |

## 完整管线 · Pipeline

```
image_gen(立绘) → remove-image-background(抠图) → make_upper.py(裁方)
→ See-through Space(分层 PSD, 22 layers)
→ Stretchy Studio 3-step import(Review Mapping → Reorder → Adjust Joints)
→ 手动校正关节(见 docs/03-rigging.md)
→ 时间轴关键帧(见 docs/04-animation.md)
→ Export frames(48 PNG) → ffmpeg 合成 MP4/GIF
→ Save project(.stretch) 交付可编辑工程
```

每步细节见 `docs/`：
- [01-pipeline-overview.md](docs/01-pipeline-overview.md) — 管线总览与选型理由
- [02-layer-decomposition.md](docs/02-layer-decomposition.md) — See-through AI 分层（HF Space 用法 + 配额坑）
- [03-rigging.md](docs/03-rigging.md) — Stretchy 绑骨（**pivot 三原则**）
- [04-animation.md](docs/04-animation.md) — 动画制作（**轨道纪律**）
- [05-export-delivery.md](docs/05-export-delivery.md) — 导出帧 / 视频 / 工程
- [06-pitfalls.md](docs/06-pitfalls.md) — 踩坑全记录（v1→v9 血泪史）

## 核心经验 · Key Lessons（写给 Agent 的速查）

1. **head 的 pivot 必须在脖子根部** —— 否则转头时头绕画布底部旋转，产生 16px 平移错位，视觉上"头身分离"（用户俗称"分头"）。
2. **eyes 的 pivot 必须在眼睛中心** —— 否则眨眼（scaleY 缩放）时眼睛绕画布原点缩放，直接飞出画面（"眼睛不见了"）。
3. **动画只加该加的轨道** —— 转头只动 `rotation`、眨眼只动 `scaleY`、呼吸只动 `scaleY`。误加 `x/y` 位移关键帧会造成"幽灵位移"（本仓库 v9 修复的就是这个问题：eyes 组 x/y 被误加关键帧，瞳孔移出脸部只剩眼白 = "一直白眼"）。
4. **`visible` 轨道只接受布尔** —— 误写入 0.766 之类的值会导致图层半透明/闪变，全部改为 1。
5. **Stretchy 重载外部 .stretch**：GUI 保存的工程重载后动画保留（`Animation 1` 正常出现）；手动改 zip 里 `project.json` 的轨道值后再重载也正常（本项目 v8/v9 就用 zip 修改法直接修轨道，无需在 GUI 里逐帧改）。
6. **骨骼关节 pivot 全量校正（v10）**：自动绑骨/启发式骨架生成的肩、肘、髋、膝 pivot 常常不在真实关节位（如肩在画面顶角、膝比髋还高）。不用的关节当前动画看不出问题，一旦做肢体动画就会"部件飞走"。v10 已把 8 个关节全部校到真实位置：肩=neck 两侧肩线、肘=腰侧、髋=腰胯、膝=膝位（画布 768 坐标，leftArm/rightArm=(505,337)/(262,337)，leftElbow/rightElbow=(505,481)/(262,481)，髋/膝=(505,560)/(262,560) 与 (505,650)/(262,650)）。改法：Stretchy 保存工程 → 解包 zip → 改 `project.json` 中对应 group 的 `transform.pivotX/pivotY` → 重打包（textures 先写、project.json 最后写）→ 重新上传。

## 给 Agent 的可执行提示 · Machine-Readable Notes

- **`.stretch` 文件 = ZIP**：`project.json`（nodes / groups / animations）+ `textures/*.png`。重打包时 **textures 先写、project.json 最后写**（顺序影响加载）。
- **动画数据**：`animations[0].tracks[]`，每轨 `{nodeId, property, keyframes:[{time(ms), value, easing}]}`；时间轴 x→帧映射是分段线性（24fps，2000ms=48 帧）。
- **验证脚本**：`scripts/verify_frames.py` 用像素统计检查"白眼 / 眼睛消失 / 头部偏移"，脚本不依赖 Stretchy，可对导出的 PNG 帧做回归。
- **See-through Space**：每日 ZeroGPU 免费额度约 1–2 次，用完需等次日或登录 HF 账号；REST API（`/gradio_api/call/inference`）当前不可用，只能走 GUI 上传→Run→下载。

## 复现步骤 · Reproduce（5 分钟）

1. 准备任意**透明背景、方形**角色立绘（`scripts/make_upper.py` 可裁切）。
2. 打开 [See-through Space](https://24yearsold-see-through-demo.hf.space)，上传 PNG → Run → 下载 `seethrough_output.psd`。
3. 打开 [Stretchy Studio](https://editor.stretchy.studio/)，上传 PSD → 3 步导入向导 → **手动校正关节**（head→脖子、eyes→眼睛、肩肘→实际关节位）。
4. 切 Animation 模式 → 时间轴加关键帧（照抄 `assets/sato_sugar_rig_v10.stretch` 的轨道设置即可）。
5. Export frames（Sequence/PNG/24fps/Transparent/zip）→ ffmpeg 合成：
   ```bash
   ffmpeg -y -framerate 24 -i "frame_%04d.png" -c:v libx264 -pix_fmt yuv420p -crf 18 anim.mp4
   ```

## 目录 · Layout

```
.
├── README.md
├── docs/            # 六篇中文教程（含踩坑记录）
├── scripts/
│   ├── make_upper.py      # 立绘方形裁切
│   └── verify_frames.py   # 帧回归验证（白眼/分离/偏移检测）
└── assets/
    ├── sato_upper.png            # 砂糖立绘（1597² 透明底）
    ├── shio_upper.png            # 盐立绘（1597² 透明底）
    ├── sato_live2d_anim_v10.mp4   # 最新动画演示（v10 骨骼校正版）
    ├── sato_sugar_rig_v10.stretch # 最新可编辑工程（v10）
    ├── sato_live2d_anim_v9.mp4    # v9 动画（历史版）
    └── sato_sugar_rig_v9.stretch  # v9 工程（历史版）
```

## License

MIT
