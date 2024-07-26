
<p align="center">  
  
  <a href="#">
    <img src="https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/assets/readme/silicon_main.png?raw=true" alt="Logo"  >
  </a>
  
  <h2 align="center">PyQt-SiliconUI</h2>
  <p align="center">基于 PyQt5 的UI框架，灵动、优雅而轻便</p>

<p align="center">
    <a href="../README.md">English</a> | 简体中文
</p>

## 写在最前面
### 重构已完成
* 基本上全部控件已经重构并置入`siui`软件包内，我们将在不久后弃用 `SiliconUI` 软件包
* 新的软件包`siui`提供更多的接口和更规范的项目结构，并将全局变量集成在总线，便于全局动态风格管理和信号处理

### 正在编写新的 Silicon Gallery
* 正在基于新的软件包重写 Gallery，这可能需要一段时间

## 如何使用
### 运行 Silicon Gallery
* 下载源代码，解压并安装  
```cmd
python setup.py install
```
* 运行`./examples/Gallery for siui/start.py`即可体验 Silicon UI 现有的功能和效果  

### 创建相似的 Silicon 应用
* 根据我们提供的模板，你可以轻松创建于 Silicon Gallery 风格相似的应用，只需要用 `siui.templates.application.SiliconApplication` 代替正常项目中 `QMainWindow`，并调用方法来创建页面即可

### 在其他项目中使用
* Silicon UI 的控件并不仅限于在 Silicon 应用中使用，你可以在任意项目中调用它们，并据你喜好进行自定义

## License
* 本项目遵循 GPL-3.0 License，详见[这里](LICENSE)  
* 同时，本项目仅允许非商业开源使用。对于商业使用，敬请期待购买商用许可的版本。

## 声明
* 请注意，Silicon Gallery 使用了 FLATICON 的图标，**这些图标不应被认为是 Silicon UI 的一部分**，你可以前往 [FLATICON的网站](https://flaticon.com) 免注册、免下载其他文件、免费获取这些图标，但应在使用时注意遵守他们的有关条款规定  
* 如果你开发的应用运行在 Windows11 上，你可以直接使用 Fluent UI 中的 svg 文件作为图标使用  

