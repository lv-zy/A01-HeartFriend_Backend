

import os
from uuid import uuid4

def random_avatar_path(instance, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 生成一个随机文件名
    filename = f'{uuid4()}.{ext}'
    # 返回文件存储的路径
    return os.path.join('avatars', filename)

def random_postpic_path(instance, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 生成一个随机文件名
    filename = f'{uuid4()}.{ext}'
    # 返回文件存储的路径
    return os.path.join('posts', filename)
