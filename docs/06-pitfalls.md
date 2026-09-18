# 06 · 踩坑全记录（v1 → v10 血泪史）

> 每条都是真实踩过、验证过修复方案的记录。用户验收过程：v1"吓人"→ v2-v4 幅度/分头 → v6"还是分头"→ v7"眼睛不见了"→ v9"可以可以"→ v10 骨骼全量校正（用户确认"可以"）。

## v1 — 头部飞出画面（"吓人"）

- **现象**：播放时头飞出画面。
- **根因**：head 组 pivotY=768（画布最底边），旋转中心在底部。
- **修复**：直接改 `.stretch` 内 project.json 的 head pivotY 768→370；后续在 GUI 拖到脖子根部。

## v2 — 转头幅度大（"还是幅度很大"）

- **现象**：±12° 转头太夸张。
- **修复**：降为 ±6°；关键帧加 Ease Both 缓动。

## v3/v4 — 眼睛闪变 + 找不到可抄的工程

- **现象**：eyes visible 轨道出现 0/0.75/0.95 闪烁值。
- **修复**：visible 全置 True。
- **额外发现**：GitHub 无公开 .stretch 工程可"抄"，官方可参考的是 `docs/testskeleton.json`（标准骨架层级）；**Stretchy 重载外部手改的 .stretch 会丢动画**（"No animations"）—— 但本项目后来验证：**GUI 保存的 .stretch 重载不丢动画，手改 zip 轨道值再重载也正常**（v8/v9 用此法直接修轨道成功）。

## v5/v6 — "分头"（头身分离）

- **现象**：转头时头与身体断开，16px 平移错位。
- **根因**：head 旋转中心在画布底部。
- **修复**：Adjust Joints 手动把 head 关节圆环拖到脖子根部（选中后确认 INSPECTOR Group name 再拖，避免拖错）。验证：头部中心偏移 1–3px。

## v7 — "眼睛都不见了"

- **现象**：眨眼时眼睛飞出画面/消失。
- **根因**：误拖 eyes 圆环 + Reset Transform 把 eyes pivot 重置成 (0,0)，眨眼（scaleY）时眼睛绕画布原点缩放。
- **修复**：Adjust Joints 选中 eyes 组，把 INSPECTOR 的 **Pivot 设为 (384, 345)**（眼睛位置）。

## v8 — 修复 visible 但没解决"一直白眼"

- **现象**：视频里眼睛大部分时间只有眼白（"白眼"），用户："眼睛是眨一下 不是 一直白眼"。
- **初步修复**：把 eyes 组 visible 轨道异常值（0→1→0.766）全改 1 —— 但导出帧仍"白眼"，说明另有原因。
- **教训**：visible 是表象，**真正根因在 x/y 位移轨道**。

## v9 — 根治"一直白眼" ✅（用户验收通过）

- **真根因**：eyes 组的 **x/y 位移轨道被误加了关键帧**（458ms 起 y 移到 +40px），瞳孔被移出脸部区域、被衣领遮挡，只剩眼白 → "白眼"。
- **修复**：把 eyes 组 x/y 轨道所有关键帧值改为 0（眼睛保持原位），只保留 scaleY 眨眼轨道。
- **验证**：帧1 玫红瞳孔（睁眼）、帧8 闭眼、帧24 玫红瞳孔（睁眼）—— **全程眼睛正常，只在眨眼瞬间闭合**。

## v10 — 骨骼关节 pivot 全量校正 ✅（用户确认）

- **现象**：对比 Stretchy 官方 `testskeleton.json` 后发现，启发式骨架生成的 **肩/肘/髋/膝 pivot 不在真实关节位**：leftArm=(652.8,92.16)、rightArm=(115.2,92.16) 在画面顶角；leftElbow=(510.7,561.5)、rightElbow=(249.6,561.5) 在画面下方；leftKnee=(482.55,441.6)、rightKnee=(282.95,441.6) **膝比髋还高**（leftLeg y=458.8）。
- **影响**：当前动画只动 head/eyes/torso，肢体关节偏位不暴露；但一旦做挥手/走路动画，部件会绕错误中心旋转"飞走"。
- **修复**（8 个关节全部校正，画布 768 坐标）：
  - 肩：leftArm/rightArm → **(505,337) / (262,337)**（neck 两侧肩线）
  - 肘：leftElbow/rightElbow → **(505,481) / (262,481)**（腰侧肘位）
  - 髋：leftLeg/rightLeg → **(505,560) / (262,560)**
  - 膝：leftKnee/rightKnee → **(505,650) / (262,650)**
- **操作方式**（"使用软件自己搞"）：先在 Stretchy GUI 里选中 leftArm/rightArm（DRAW ORDER 图层项）→ INSPECTOR 的 Pivot X/Y 直接改数值；肘/腿不是图层，GUI 点不中（被部件遮挡）→ 改走 zip 法：Save project 下载 .stretch → 解包改 `project.json` 各 group 的 `transform.pivotX/pivotY` → 重打包（textures 先写、project.json 最后写）→ 重新上传。
- **验证**：Edit 模式骨骼标签全部移到真实关节位；动画三轨完整保留；帧1 玫红眼眸睁眼 / 帧8 闭眼 / 帧24 睁眼——动画行为与 v9 一致，**pivot 修正不破坏现有动画**。

## 通用经验清单

| 坑 | 一句话修法 |
|---|---|
| head 分头 | head pivot 拖到脖子根部 |
| 眼睛消失 | eyes pivot 设回眼睛中心 (384,345) |
| 一直白眼 | 检查 eyes 的 x/y 轨道是否有非 0 关键帧，归零 |
| 肩/肘/髋/膝偏位 | 解包 zip 改 group 的 pivotX/pivotY（v10 坐标表见上） |
| visible 闪变 | visible 轨道全改 1（布尔） |
| AI 自动绑骨报错 | ONNX 损坏 → 手动拖关节 |
| 重载丢动画 | GUI 保存的 .stretch 正常；手改 zip 后 textures 先写、project.json 后写 |
| HF 分层没额度 | 每日 1–2 次，次日或登录 HF 账号 |
| React 输入框改值无效 | 用原生 value setter + input/change/keydown/Enter/blur 全事件 |
