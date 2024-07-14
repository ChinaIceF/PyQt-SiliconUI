
<p align="center">  
  
  <a href="#">
    <img src="https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/assets/readme/silicon_main.png?raw=true" alt="Logo"  >
  </a>
  
  <h2 align="center">PyQt-SiliconUI</h2>
  <p align="center">基于 PyQt5 的UI框架，灵动、优雅而轻便</p>


## 写在最前面
### 注意：重构进行中
#### 目的与计划
  为了便于使用和开发，本项目目前正在进行彻头彻尾的重构，届时，我们暂时停止对新功能的开发，而将注意力集中在将`SiliconUI`中的模块优化并迁移到`siui`中。  
#### 可能的影响
* 考虑到重构的彻底性，你可能需要熟悉项目的新结构以重新掌握使用SiliconUI。 
* 部分方法名和类名可能会被修改，同样地，你也需要在你的项目中更改这些命名
#### 最后...
  为你造成的不便敬请谅解，欢迎你参与项目重构  

## 如何使用
### 运行 Silicon Gallery
* 下载源代码，解压并安装  
```cmd
python setup.py install
```
* 运行`./examples/Gallery/start.py`即可体验 Silicon UI 现有的功能和效果  

在 Silicon Gallery 中，你可以了解：
* 各种控件以及其样式
* 控件的信号属性
* 应用快速构建器（Silicon Glaze）的示例
* ***更多内容等待我们共同创造***

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

