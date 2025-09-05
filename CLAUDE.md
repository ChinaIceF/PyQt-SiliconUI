# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

PyQt-SiliconUI 是一个基于 PyQt5/PySide6 的强大艺术化 UI 库，提供现代化的 UI 组件和动画效果。

## 开发命令

**安装依赖和库:**
```bash
python setup.py install
```

**运行示例画廊:**
```bash
python examples/Gallery\ for\ siui/start.py
```

**运行 My-TODOs 示例:**
```bash
python examples/My-TODOs/start.py
```

## 项目结构

```
PyQt-SiliconUI/
├── siui/                    # 核心 UI 库
│   ├── components/          # UI 组件
│   │   ├── button.py       # 按钮组件（已重构）
│   │   ├── container.py    # 容器组件（已重构）
│   │   ├── editor.py       # 输入编辑组件（已重构）
│   │   ├── graphic.py      # 图形相关组件
│   │   ├── label.py        # 标签和文本组件
│   │   ├── layout.py       # 布局组件
│   │   ├── menu_.py        # 菜单组件
│   │   ├── popover.py      # 弹出层组件
│   │   ├── progress_bar_.py # 进度条组件
│   │   └── slider_.py      # 滑块组件
│   └── core/               # 核心功能
│       ├── animation.py   # 动画工具
│       ├── event_filter.py # 事件过滤器
│       └── painter.py      # 绘图功能
├── examples/               # 示例代码
│   ├── Gallery for siui/   # 组件展示画廊
│   └── My-TODOs/          # To-Do 应用示例
└── setup.py               # 安装脚本
```

## 重要说明

1. **重构状态**: 项目正在进行大规模重构，优先使用 `siui/components/` 目录下标记为"已重构"的组件
2. **依赖**: 需要 PyQt5>=5.15.10, numpy, pyperclip
3. **开发状态**: Alpha 阶段，尚未发布到 PyPi
4. **许可证**: GPL-3.0

## 开发建议

- 优先使用重构后的组件（参见 README 中的重构模块列表）
- 避免使用旧的应用程序模板，等待重构完成
- 组件开发遵循 Qt 的布局系统
- 动画使用 `siui/core/animation.py` 中的工具