import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

# 导入动作处理器以注册 Socket.IO 事件
from backend.app.task.actions import task_worker_status as task_worker_status
