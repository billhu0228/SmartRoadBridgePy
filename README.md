
---

# SrbPy + *.srb

SrbPy 是一个 Python/C++ 混合的道路与桥梁设计包，支持 Windows AMD64、
macOS Apple Silicon 和 macOS Intel，要求 Python 3.9 或更高版本。

## 安装

```bash
python -m pip install srbpy
```

## 本地开发

构建 C++ 扩展需要支持 C++17 的编译器。Windows 使用 MSVC；macOS 使用
Xcode Command Line Tools 中的 Apple Clang。CMake 和 Ninja 会由构建后端在
需要时安装，也可以预先安装到虚拟环境中。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
pytest
```

构建发布产物：

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

## XML中间交换格式

基于xml的标准数据格式请参考 [详细说明](./docs/standards/中间交换文件格式标准.md) 。

## SrbPy
 
提供了两个子模块：
 
 - 路线模块(srbpy.alignment)，用于解析EICAD路线数据包并解析.
 - 模型(srbpy.model), 用于建模。

用法及包详情请参考[文档](https://smartroadbridgepy.readthedocs.io/zh_CN/latest/srbpy.html#module-srbpy) 。
