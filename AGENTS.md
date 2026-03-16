# AGENTS.md - 代码库指南

## 项目概述
zulin 项目 - Python 项目

## 构建/运行/测试命令

### 项目初始化
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate
```

### 依赖管理
```bash
# 安装依赖
pip install -r requirements.txt

# 导出依赖
pip freeze > requirements.txt

# 安装单个包
pip install <package-name>
```

### 代码质量工具
```bash
# 安装工具
pip install black flake8 mypy pytest

# 格式化代码
black .

# 代码检查
flake8 .

# 类型检查
mypy .

# 运行测试
pytest

# 运行单个测试
pytest tests/test_module.py::test_function_name
```

### 运行项目
```bash
# 激活虚拟环境并启动后端服务 (Windows)
cd backend
venv\Scripts\activate
python main.py

# 启动前端服务
cd frontend && npm run dev
```

### 手动启动说明
- 前后端服务都需要手动启动，不会自动运行
- 后端运行在 http://localhost:8000
- 前端运行在 http://localhost:5173

## 代码风格指南

### 命名约定
- **变量**: 蛇形命名法 (snake_case)，如 `user_name`, `total_count`
- **函数**: 蛇形命名法，动词开头，如 `get_user_by_id`, `calculate_total`
- **类**: 大驼峰命名法 (PascalCase)，如 `UserService`, `DataLoader`
- **常量**: 全大写下划线分隔，如 `MAX_SIZE`, `DEFAULT_TIMEOUT`
- **私有属性**: 单下划线前缀，如 `_internal_cache`

### 导入规范
```python
# 顺序：标准库 -> 第三方库 -> 本地模块
import os
import sys
from pathlib import Path

import requests
from flask import Flask

from .utils import helper
from .models import User
```

### 代码格式化
- 使用 **4 空格** 缩进（Python 标准）
- 每行最大长度 **88 字符**（Black 默认）
- 导入后空一行，类/函数定义间空两行
- 使用 Black 进行自动格式化

### 类型注解
```python
# 函数签名必须包含类型注解
def greet_user(name: str, age: int) -> str:
    return f"Hello, {name}"

# 使用 Optional 表示可为空
from typing import Optional, List, Dict

def find_user(user_id: int) -> Optional[User]:
    ...

# 复杂类型
def process_data(items: List[Dict[str, any]]) -> Dict[str, List[int]]:
    ...
```

### 错误处理
```python
# 使用具体的异常类型
try:
    result = api_call()
except requests.exceptions.RequestException as e:
    logger.error(f"API 调用失败：{e}")
    raise

# 自定义异常
class ValidationError(Exception):
    pass

# 使用上下文管理器
with open("file.txt", "r") as f:
    content = f.read()
```

### 文档字符串
```python
def calculate_total(items: List[float], tax_rate: float) -> float:
    """计算含税总额

    Args:
        items: 商品列表
        tax_rate: 税率 (0-1 之间)

    Returns:
        含税总额

    Raises:
        ValueError: 当税率不在有效范围内时
    """
    if not 0 <= tax_rate <= 1:
        raise ValueError("税率必须在 0-1 之间")
    return sum(items) * (1 + tax_rate)
```

### 日志记录
```python
import logging

logger = logging.getLogger(__name__)

# 使用适当的日志级别
logger.debug("调试信息")
logger.info("正常信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")
```

## 现有规则文件
- 无 Cursor 规则 (.cursor/rules/)
- 无 Copilot 规则 (.github/copilot-instructions.md)

## Git 工作流
```bash
# 创建新分支
git checkout -b feature/feature-name

# 提交代码
git add .
git commit -m "类型：简短描述"

# 推送分支
git push origin feature/feature-name
```

### 提交信息格式
```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

## 注意事项
- 提交前确保通过所有测试
- 不要提交敏感信息（.env, 密钥等）
- 保持提交原子化，一次提交只做一件事

## 服务启动/停止规则
- **禁止** 自动启动、关闭或重启前后端服务
- 需要启动/重启服务时，**必须提示用户手动操作**
- 后端服务运行在 http://localhost:8000
- 前端服务运行在 http://localhost:5173
