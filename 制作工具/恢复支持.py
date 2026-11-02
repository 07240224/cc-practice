"""Atomic no-replace installation. Only temporary directories created by us are removed."""
import ctypes
import errno
import os
from pathlib import Path
import shutil

def install_new_directory(source: Path, target: Path):
    if os.path.lexists(target):
        raise FileExistsError('目标已存在，未覆盖：' + str(target))
    if sys_platform_linux():
        libc = ctypes.CDLL(None, use_errno=True)
        rename = getattr(libc, 'renameat2', None)
        if rename is not None:
            rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
            rename.restype = ctypes.c_int
            if rename(-100, os.fsencode(source), -100, os.fsencode(target), 1) == 0:
                return
            error = ctypes.get_errno()
            if error not in (errno.ENOSYS, errno.EINVAL):
                raise OSError(error, os.strerror(error), str(target))
    if os.name == 'nt':
        os.rename(source, target)  # Windows rejects an existing destination.
        return
    # Portable fallback reserves the destination exclusively. The completion manifest is copied last.
    target.mkdir()
    try:
        completion = '恢复完成.json'
        for p in source.iterdir():
            if p.name == completion:
                continue
            q = target / p.name
            if p.is_dir():
                shutil.copytree(p, q)
            else:
                shutil.copy2(p, q)
        if (source / completion).exists():
            shutil.copy2(source / completion, target / completion)
    except BaseException:
        shutil.rmtree(target)  # This directory was created exclusively by this invocation.
        raise

def sys_platform_linux():
    import sys
    return sys.platform.startswith('linux')
