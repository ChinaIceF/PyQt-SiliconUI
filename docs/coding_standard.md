# 代码规范
创建于 2024.10.25

为了提高可读性和可维护性，新编写的 PyQt-SiliconUI 代码将遵守以下规范。

## 命名规范
### 命名法
* 变量名采用 snake_case。
* 方法名沿袭 PyQt 特点，采用 lowerCamelCase
* 类名采用 UpperCamelCase
* 旗标类、枚举类和常量采用全大写命名

### 命名构成
#### 变量名
* 采用正常英文语序命名，例如 `day_counter`, `month_counter`, `year_counter`
* 具有大量语义类似，而类型不同的变量，将强调的类型提前作为前缀，例如 `container_name`, `label_name`
* 变量名与方法名冲突时，变量名后加 `_` 后缀，如 `self.name()`, `self.name_`


## 控件 / 组件类
约定模版化的方法和其功能。

### _initWidget()
初始化组件中需要用到的控件，仅做声明，不包含样式表，几何信息等。

### _initStyle()
初始化样式表、字体、颜色等外观相关的属性到自身以及 `_initWidget()` 声明的控件中。

### _initLayout()
初始化布局。除了使用 `QLayout` 外，几何信息也在这里定义，包括位置和大小。

### _initAnimation()
初始化动画。包括 `QPropertyAnimation` 和 `SiAnimation`，在这里完成他们的初始化和信号绑定。
例如：
```python
def _initAnimation(self):
    self.animation = SiExpAnimation(self)
    self.animation.setFactor(1/8)
    self.animation.setBias(0.2)
    self.animation.setTarget(self.idle_color)
    self.animation.setCurrent(self.idle_color)
    self.animation.ticked.connect(self.animate)
```

### \_\_init\_\_()
* 初始化变量。
* 依次调用 `_initWidget()` `_initStyle()` `_initLayout()` `_initAnimation()`。