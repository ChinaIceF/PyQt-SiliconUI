from setuptools import find_packages, setup

# 定义项目需要的依赖项
install_requires = [
    "PyQt5>=5.15.10",
    "numpy",
    "pyperclip",
]

# 定义项目元数据
setup(
    name = "PyQt-SiliconUI",
    version = "1.01",
    packages = find_packages(exclude = ["examples"]),  # 自动找到所有包
    data_files=[("./siui/gui/icons/packages", ["./siui/gui/icons/packages/fluent_ui_icon_filled.icons",
                                               "./siui/gui/icons/packages/fluent_ui_icon_regular.icons",
                                               "./siui/gui/icons/packages/fluent_ui_icon_light.icons"]),],
    include_package_data = True,
    install_requires = install_requires,  # 依赖项列表
    # 以下为可选元数据
    description = "A powerful and artistic UI library based on PyQt5 / PySide6",  # 包的简短描述
    long_description = open("README.md", encoding="utf-8").read(),  # 包的详细描述，通常来自README文件
    long_description_content_type = "text/markdown",  # README文件的格式
    url = "https://github.com/ChinaIceF/PyQt-SiliconUI",  # 项目主页
    author = "ChinaIceF",  # 作者名
    author_email = "ChinaIceF@outlook.com",  # 作者邮箱
    license = "GPL-3.0",  # 许可证
    classifiers=[  # 项目的分类信息
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL-3.0 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={  # 如果包是可执行的，定义入口点
        "console_scripts": [
            ""
        ],
    },
)
