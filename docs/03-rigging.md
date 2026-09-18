# 03 · Stretchy 绑骨（pivot 三原则）

## 导入

Stretchy Studio（`editor.stretchy.studio`）上传 PSD 后走 **3 步向导**：

1. **Review Mapping**：检查图层标签（head / body / arm…），需要时勾选 Split Arms。
2. **Reorder Layers**：调整图层前后顺序（影响绘制顺序，也影响启发式骨骼的父级分配）。
3. **Adjust Joints**：拖动画布上的关节圆环校正位置，**Finish Setup** 完成。

> 启发式骨骼会按当前图层顺序重算父级和 pivot —— 所以**导入后再改图层顺序会覆盖你手动改过的关节位置**，注意顺序。

## 标准骨骼层级（testskeleton.json 结构）

```
root
└── rig_root
    ├── torso
    │   ├── neck
    │   │   └── head
    │   │       └── eyes        ← 眼睛挂在头下（缩放即眨眼）
    │   ├── leftArm → leftElbow
    │   └── rightArm → rightElbow
    └── bothLegs
```

## ⚠️ Pivot 三原则（本仓库最核心的经验）

### 原则 1：head 的 pivot 必须在脖子根部
- **症状**：转头时头与身体分离（"分头"），极其吓人。
- **根因**：启发式把 head 的 pivot 放在画布底部（例如 y=768），转头时头绕画布底旋转，产生 **16px 平移错位**，脖子处断开。
- **修复**：Adjust Joints 里选中 head 圆环，拖到脖子根部（下巴下方）。验证：转头 ±6° 时头部 alpha 包围盒中心偏移应降到 **1–3px**。

### 原则 2：eyes 的 pivot 必须在眼睛中心
- **症状**：眨眼时眼睛直接消失/飞出画面。
- **根因**：误拖 eyes 圆环 + Reset Transform 后 pivot 变 (0,0)（画布原点），scaleY 缩放时眼睛绕原点缩放，跑出脸部。
- **修复**：Adjust Joints 选中 eyes 组，把 INSPECTOR 的 **Pivot 设为眼睛中心**（本项目 768 画布为 (384, 345)）。

### 原则 3：肩/肘必须对准真实关节
- 肩在颈侧、肘在手臂弯折处。否则手臂动画（如果做）会像断肢摆动。

## 操作细节

- **拖动前先确认选中谁**：选中圆环后看 INSPECTOR 的 Group name 再拖，避免拖错（本项目踩过：把 eyes 圆环拖走导致 pivot 错乱）。
- **DWPose AI auto-rig 不可用时**：直接手动拖关节即可，效果一样。
- **验证方法**：导出单帧，用像素检测头部 alpha 包围盒中心（`scripts/verify_frames.py`），转头帧的中心偏移应 ≤ 3px。
