from utils.logger import log
import os
import importlib
import inspect
from pathlib import Path

def discover_plugins():
    plugins = {}

    # 获取当前文件所在的目录（插件目录）
    plugin_dir = Path(__file__).parent

    # 在插件目录中查找所有的 .py 文件
    plugin_files = plugin_dir.glob("*.py")

    # 遍历找到的所有 .py 文件
    for plugin_file in plugin_files:
        # 如果当前文件是 __init__.py，则跳过，不作处理
        if plugin_file.stem == "__init__":
            continue

        # 使用 importlib.import_module 动态导入当前 .py 文件对应的模块
        plugin_module = importlib.import_module(f"plugins.{plugin_file.stem}")

        # 使用 inspect.getmembers 遍历模块的所有成员
        for name, obj in inspect.getmembers(plugin_module):
            # 如果当前成员是一个函数，并且函数名以 "plugin_" 开头
            if inspect.isfunction(obj) and name.startswith("plugin_"):
                # 将函数名（去掉 "plugin_" 前缀）作为键，函数对象作为值，添加到插件字典中
                plugins[name[7:]] = obj

    log.info(f"Discovered {len(plugins)} plugins")
    return plugins