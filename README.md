
<p align="center">  
  
  <a href="#">
    <img src="https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/assets/readme/silicon_main.png?raw=true" alt="Logo"  >
  </a>
  
  <h2 align="center">PyQt-SiliconUI</h2>
  <p align="center">基于PyQt5的UI框架，灵动、优雅而轻便</p>
  
</p>   

# 写在最前面
## 代码质量
请注意，这是我接触 PyQt5 后的第一个较大项目，你将看到包括但不限于以下的史：  
* 时而正常时而离谱的命名
* 莫名重写 PyQt5 中具有的一些功能
* 手动调整布局

## 但是...
如果我们可以一起优化并丰富这个项目，我将感激不尽，欢迎你参与 Silicon UI 的开发！  

# 如何使用
## 运行 Silicon Gallery
下载源代码，解压并运行 ``start.py``，即可体验 Silicon UI 现有的功能和效果  
在 Silicon Gallery 中，你可以了解：
* 各种控件以及其样式
* 控件的信号属性
* 应用快速构建器（Silicon Glaze）的示例
* ***更多内容等待我们共同创造***

## 创建相似的 Silicon 应用
在 ``./ui.py`` 中，展示了一般 Silicon 应用的构建方法，其工作目录应具有以下结构：  
* **components 文件夹**，其中存放各个选项卡的界面
* **ui.py**，文件名取决于你的调用方式，重要的是其中应包含 Silicon 应用的构建类，并调用 components 文件夹以构建各个界面

## 在其他 PyQt5 项目中使用
Silicon UI 的控件并不仅限于在 Silicon 应用中使用，你可以在任意 PyQt5 项目中调用它们，并根据你的喜好进行自定义

# 声明
* 请注意，Silicon Gallery 使用了 FLATICON 的图标，**这些图标不应被认为是 Silicon UI 的一部分**，你可以前往 [FLATICON的网站](flaticon.com) 免注册、免下载其他文件、免费获取这些图标，但应在使用时注意遵守他们的有关条款规定  
* 如果你开发的应用运行在 Windows11 上，你可以直接使用 Fluent UI 中的 svg 文件作为图标使用  

