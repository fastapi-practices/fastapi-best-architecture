import os
import platform
import socket
import sys

from datetime import datetime
from datetime import timezone as tz

import psutil

from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool

from backend.app.admin.schema.monitor import (
    CpuInfo,
    DiskInfo,
    MemInfo,
    ServerMonitorInfo,
    ServiceInfo,
    SysInfo,
)
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsSuperUser
from backend.utils.format import fmt_bytes, fmt_seconds
from backend.utils.timezone import timezone

router = APIRouter()


@router.get('', summary='Server 监控', dependencies=[DependsSuperUser])
async def get_server_info() -> ResponseSchemaModel[ServerMonitorInfo]:  # ruff:ignore[complex-structure]
    def get_all_info() -> ServerMonitorInfo:  # ruff:ignore[complex-structure]
        # CPU 信息
        cpu_data = {
            'physical_num': psutil.cpu_count(logical=False) or 0,
            'logical_num': psutil.cpu_count(logical=True) or 0,
            'max_freq': 0.0,
            'min_freq': 0.0,
            'current_freq': 0.0,
            'usage': round(psutil.cpu_percent(interval=0.1), 2),
        }

        try:
            if hasattr(psutil, 'cpu_freq'):
                cpu_freq = psutil.cpu_freq()
                if cpu_freq:
                    cpu_data.update({
                        'max_freq': round(cpu_freq.max, 2),
                        'min_freq': round(cpu_freq.min, 2),
                        'current_freq': round(cpu_freq.current, 2),
                    })
        except Exception:
            pass

        cpu = CpuInfo(**cpu_data)

        # 内存信息
        mem = psutil.virtual_memory()
        gb_factor = 1024**3
        mem_info = MemInfo(
            total=round(mem.total / gb_factor, 2),
            used=round(mem.used / gb_factor, 2),
            free=round(mem.available / gb_factor, 2),
            usage=round(mem.percent, 2),
        )

        # 系统信息
        hostname = socket.gethostname()
        ip = '127.0.0.1'
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(0.5)
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
        except (TimeoutError, socket.gaierror, OSError):
            pass
        sys_info = SysInfo(name=hostname, os=platform.system(), ip=ip, arch=platform.machine())

        # 磁盘信息
        disk_list = []
        exclude_fstypes = {'overlay', 'overlay2', 'tmpfs', 'devtmpfs', 'shm', 'proc', 'sysfs', 'cgroup', 'cgroup2'}
        seen_devices = set()
        for partition in psutil.disk_partitions(all=False):
            # 跳过虚拟文件系统
            if partition.fstype.lower() in exclude_fstypes:
                continue
            # 跳过重复设备（同一设备的不同挂载点）
            if partition.device in seen_devices:
                continue
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                if usage:
                    seen_devices.add(partition.device)
                    disk_list.append(
                        DiskInfo(
                            dir=partition.mountpoint,
                            device=partition.device,
                            type=partition.fstype,
                            total=fmt_bytes(usage.total),
                            used=fmt_bytes(usage.used),
                            free=fmt_bytes(usage.free),
                            usage=f'{usage.percent:.2f}%',
                        )
                    )
            except (PermissionError, OSError):
                continue

        # 服务信息
        process = psutil.Process(os.getpid())
        proc_mem = process.memory_info()
        try:
            create_time = datetime.fromtimestamp(process.create_time(), tz=tz.utc)
            start_time = timezone.from_datetime(create_time)
        except (psutil.NoSuchProcess, OSError):
            start_time = timezone.now()

        elapsed = fmt_seconds(round((timezone.now() - start_time).total_seconds()))

        service = ServiceInfo(
            name='Python3',
            version=platform.python_version(),
            home=sys.executable,
            startup=timezone.to_str(start_time),
            elapsed=elapsed,
            cpu_usage=f'{process.cpu_percent(interval=0.1):.2f}%',
            mem_vms=fmt_bytes(proc_mem.vms),
            mem_rss=fmt_bytes(proc_mem.rss),
            mem_free=fmt_bytes(proc_mem.vms - proc_mem.rss),
        )

        return ServerMonitorInfo(cpu=cpu, mem=mem_info, sys=sys_info, disk=disk_list, service=service)

    data = await run_in_threadpool(get_all_info)
    return response_base.success(data=data)
