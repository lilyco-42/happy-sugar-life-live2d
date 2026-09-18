# 02 · See-through AI 分层（单图 → PSD）

## 是什么

[HuggingFace 官方 See-through Space](https://24yearsold-see-through-demo.hf.space) 用 SOTA 分层模型把单张角色立绘自动分解成可动图层，输出 PSD（本项目得到 **22 层**，768×768）。

## 操作步骤（纯浏览器）

1. 打开 Space → 拖入透明底方形 PNG（1597² 会先被 Space 缩到 768²）。
2. 点 **Run** → 等进度条走完（约 30–60 秒）。
3. 下载 `seethrough_output.psd`。

## 输出层结构（砂糖示例）

```
front hair / head → f._head       前发
eyes → i._eyes（irides-l/r 瞳孔）  ← 瞳孔单独成组，这是眨眼的关键
head → e._head（eyelash/eyewhite/eyebrow/mouth/nose/face/ears）
torso → t._torso（topwear 外套）
neck → n._neck
root → b._root（bottomwear 裙摆）
back hair → head（后发）
headwear → head（发饰）
handwear-l/r → leftArm/rightArm
```

> 注意：瞳孔（irides）被分在 `eyes` 组，而眼白（eyewhite）在 `head` 组 —— 眨眼动画只需缩放 `eyes` 组（瞳孔压扁），眼白不动，视觉上就是"闭眼"。

## 坑与限制

- **每日 ZeroGPU 免费额度约 1–2 次**：用完当天就不能再跑，需等次日或登录 HF 账号（登录入口在 `https://huggingface.co/login?next=/settings/zero-gpu-explorers`）。
- **REST API 不可用**：`/gradio_api/call/inference` 返回报错，只能走 GUI 上传 → Run → 下载。
- **镜像 Space**（`pan2jay/see-through-demo`、`Zhatei/see-through-demo`）常报 `Runtime error / Memory limit exceeded (16Gi)`，不可靠。
- 若分层结果部分图层错位/缺失，可重跑一次（结果有随机性），或接受后用 Stretchy 的图层重排修复。

## 备选（本仓库未用，但可行）

Stretchy 首页也内置了 "Layer-ify your image" 入口（同一个 See-through 模型）。若主 Space 挂了，可以在 Stretchy 里直接上传单图让它分层。
