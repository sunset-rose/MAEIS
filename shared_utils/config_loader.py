from functools import lru_cache
import importlib

@lru_cache(maxsize=128)
def get_conf(*args):
    """
    所有配置都集中在config.py中。
    """
    res = []
    for arg in args:
        r = getattr(importlib.import_module('config'), arg)
        res.append(r)
    if len(res) == 1: return res[0]
    return res