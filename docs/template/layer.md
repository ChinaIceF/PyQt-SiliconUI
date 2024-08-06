# SiLayer
在应用界面上的可叠加容器，实现主界面、子界面、弹窗和侧边栏等等叠加场景。

|       |          |
|------:|:---------|
|   继承自 | SiWidget |
| 被继承对象 | -        |

## 公共方法
| 方法名                                      | 返回值类型    |
|:-----------------------------------------|:---------|
| setBody(SiWidget)                        | None     |
| body()                                   | SiWidget |
| setCloseUpperLayerOnDimClicked(on :bool) | None     |
| closeLayer()                             | None     |

## 信号
| 信号名           | 返回值类型 |
|:--------------|:------|
| closed        | None  |
| closedToUpper | bool  |
