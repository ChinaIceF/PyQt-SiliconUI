
<p align="center">  
  
  <a href="#">
    <img src="https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/assets/readme/silicon_main.png?raw=true" alt="Logo"  >
  </a>
  
  <h2 align="center">PyQt-SiliconUI</h2>
  <p align="center">基于 PyQt5 的UI框架，灵动、优雅而轻便</p>

<p align="center">
    <a href="../README.md">English</a> | 简体中文
</p>

## 安装
下载该仓库，在命令行中输入以下命令：
```cmd
python setup.py install
```
> ⚠️ 由于本项目还在积极开发中，在发布正式版本前不能在 PyPi 上安装，敬请期待。


## 运行示例程序
运行 `examples/Gallery for siui/start.py` 来体验 PyQt-SiliconUI 提供的控件、组件和框架

### 重构计划
控件的重构即将完成。你可以在 Gallery 的 “重构控件” 页面试用。

 **请注意**，如果您近期想尝试 PyQt-SiliconUI 编写项目，**非常不推荐您使用除了 “重构控件” 以外的控件**。旧控件包含大量缺陷，正在逐步被重构控件取代。另外，应用模版也在重构计划内。将会在控件、组件的重构基本完成后着手实现。由于旧的应用模板存在大量的代码漏洞，功能的实现也非常丑陋，
**在应用模版重构完成前，不建议您正式使用 PyQt-SiliconUI 的应用模版搭建项目**

### 重构模块内容解释
以下列出了一些正在积极维护的模块。完全完成这些模块的实现后，将从仓库中移除旧的模块 / 包。

#### 控件
- `siui/components/button.py` 包含了重构的按钮控件
- `siui/components/container.py` 包含了重构的容器。新的容器全部采用 Qt 的 Layout 系统进行管理。
- `siui/components/container.py` 包含了重构的编辑框控件
- `siui/components/graphic.py` 包含图形代理控件，包装器等与图形代理相关的控件和功能
- `siui/components/label.py` 包含以展示简单文本和图像为功能的控件，以及一些暂未归类的控件
- `siui/components/layout.py` 包含流式布局，瀑布流布局的新实现。与重构的容器一样采用 Layout 系统进行管理
- `siui/components/menu_.py` 包含菜单组件
- `siui/components/popover.py` 包含一些 popover 类窗口的实现，例如日期选择器，时间选择器等
- `siui/components/progress_bar_.py` 包含重构的进度条控件
- `siui/components/slider_.py` 包含重构的滑块。例如水平滑块，滚动区域的滑块等

#### 功能
- `siui/core/animation.py` 包含重构的动画
- `siui/core/event_filter.py` 包含各种事件过滤器
- `siui/core/painter.py` 包含绘制相关功能的实现


## 另请参阅
一些基于 PyQt-SiliconUI 编写的项目:
* [My-TODOs](https://github.com/ChinaIceF/My-TODOs) - 简洁轻便的跨平台桌面待办小工具


## 许可证
PyQt-SiliconUI 使用 [GPLv3](../LICENSE) 许可证

版权所有 © 2024-2025 by ChinaIceF.


## 特别声明
用户阅读、下载、基于该软件开发或修改该软件，即代表用户已经理解并同意开源许可证声明的权利与限制，用户理解并同意不进行违反当地法律法规的开发或/和修改，若因用户的开发或/和修改违反了当地的法律，或是用户的开发或/和修改的传播和使用过程中违反了传播者和使用者所在地区适用的法律，或是造成了任何负面的个人或公众影响，用户应承担全部责任，本软件的开发者不承担任何责任。

