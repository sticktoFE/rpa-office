'''创建消息基类，保存属性及获取属性值的方法'''
global _global_dict
_global_dict = {}


def set_var(name, value):  # 设置保存的数据
    _global_dict[name] = value


def get_var(name):  # 提取保存的数据
    try:
        return _global_dict[name]
    except KeyError:
        return False
