![logo](docs/cccc.png)

---

# 路桥设计脚本 + XML标准数据格式定义

## XML标准数据模式定义
>定义一套完备的XML模式（*.xsd）,描述项目结构。
- 项目
  - info.xml 
    > 项目信息
  - align.xml
    > 路线名称、编号、设计参数
  - bridge.xml
    > 桥梁名称、编号
  - shape.xml
    > 已注册构件名称、编号
  - span.xml
    > 桥跨布置表
  - sub.xml
  - sup.xml
  - found.xml
  - ...
  

## 路桥设计 Python 脚本
> 将原来的 SmartRoadBridge.Alignment 库的核心算法迁移到 Python 库。并给用户提供一套命令流，用于生成XML标准数据格式文件。

## C# GUI 用户交互程序
> 脚本的GUI壳，支持脚本生成和解析。

## 数据库和 XML
> XML和数据库可双向同步。


