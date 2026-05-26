# ASR Skill：音频转录与 AI 稿件优化

一个音频转稿 Skill。它可以将录音转换为两个版本的文本：

- **逐字稿**：尽量保留原始表达和口语结构
- **AI 优化稿**：自动去除冗余、合并重复内容、优化表达逻辑

同时支持单人和多人音频处理，并生成可一键复制的结果页面。

## 功能

- 音频转文字
- 自动生成逐字稿和 AI 优化稿
- 自动判断单人或多人录音
- 单人录音直接输出正文
- 多人录音使用 `A：`、`B：`、`C：` 标注说话人
- 自动修正上下文明确的常见识别错误
- 生成带复制按钮的 HTML 结果页
- 对单人口播跳过不必要的人声分离，提高处理速度

## 输出示例

### 单人录音

```text
今天想和大家分享一下 AI 的学习路径。这是我从真实经历和踩坑过程中总结出来的……
```

### 多人录音

```text
A：你觉得这个方案最大的问题是什么？

B：我觉得主要问题还是数据来源和合规风险。

A：那 MVP 阶段可以先让用户手动输入数据。
```

## 输出规则

- 单人录音不添加说话人标签
- 多人录音使用 `A / B / C...` 标注说话人
- 逐字稿尽量接近原始录音
- AI 优化稿会删除口头语和重复表达，并整理内容结构
- 可复制文本中不包含“逐字稿”或“AI优化稿”等额外标题

## 安装

将仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/shimuyangly/ASR_skill.git ~/.codex/skills/audio-transcript-polish
```

## 使用

在 Codex 中上传或指定音频文件后，输入：

```text
使用 $audio-transcript-polish 处理这段音频，生成逐字稿和 AI 优化稿。
```

## 处理流程

```text
音频
  -> ASR 转录
  -> 判断单人 / 多人
  -> 必要时标注说话人
  -> 生成逐字稿
  -> 生成 AI 优化稿
  -> 输出一键复制页面
```

## 页面生成脚本

仓库包含 HTML 结果页生成脚本：

```bash
python3 scripts/make_copy_page.py \
  --title "录音标题" \
  --audio-label "example.m4a" \
  --transcript "example_逐字稿.txt" \
  --optimized "example_AI优化稿.txt" \
  --out "example_转录结果.html"
```

## 项目结构

```text
ASR_skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── make_copy_page.py
```

## 注意事项

- 转录效果会受到音频质量、背景噪声、专业术语和多人重叠说话等因素影响。
- AI 优化稿会对原始表达进行整理，重要信息建议结合逐字稿复核。
