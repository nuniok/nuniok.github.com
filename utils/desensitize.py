#!/usr/bin/python
# coding: utf-8
"""
File: desensitization.py
Author: noogel <noogel@163.com>
Date: 2019-10-26 14:57
Description: 图像数据脱敏
"""
import sys
import math
import os
import operator
from functools import reduce
from PIL import Image

TARGET_MAX_SIZE = 1024
TARGET_DIR = "source/resource/img/"
PREFIX = "图像处理"
EXT_MAX_SIZE = 40


def progressbar(cur, total, prefix="Process", ext=""):
    """
    处理进度条
    :param cur:
    :param total:
    :param prefix:
    :param ext:
    :return:
    """
    percent = '{:.2%}'.format(cur / total)
    process = '=' * int(math.floor(cur * 30 / total) - 1) + ('>' if cur != total else "=")
    ext = ext[:EXT_MAX_SIZE] if len(ext) >= EXT_MAX_SIZE else (ext + " " * (EXT_MAX_SIZE - len(ext)))
    sys.stdout.write('\r')
    sys.stdout.write("%s: [%-30s] %s | : %s" % (prefix, process, percent, ext))
    sys.stdout.flush()


def geometric_resize(size_tuple, target_max_size):
    """
    等比缩放
    :param size_tuple:
    :param target_max_size:
    :return:
    """
    source_width, source_height = size_tuple
    # if source_width <= target_max_size and source_height <= target_max_size:
    if source_width <= target_max_size:
        return size_tuple
    target_height = int(target_max_size / source_width * source_height)
    # target_width = int(target_max_size / source_height * source_width)
    # if target_height > target_max_size:
    #     return target_width, target_max_size
    # else:
    return target_max_size, target_height


def resize_and_desensitization(img_path):
    """缩放加基本脱敏"""
    if img_path.rsplit(".", 1)[-1] not in ("png", "jpg", "jpeg", "webp"):
        return "Invalid img."
    source_img = Image.open(img_path)
    source_size = source_img.size
    target_size = geometric_resize(source_size, TARGET_MAX_SIZE)
    if (hasattr(source_img, "_getexif") and source_img._getexif()) or target_size[0] != source_size[0]:
        source_img = source_img.resize(target_size)
        target_img = Image.new(source_img.mode, target_size)
        target_img.putdata(list(source_img.getdata()))
        target_img.save(img_path)
        return "Resize: {} -> {}.".format(
            source_size, target_size
        )
    return "Skip this img."


def run():
    """批量处理"""
    flatten_images = reduce(
        operator.__add__,
        [[os.path.join(root, file_name) for file_name in files] for root, _, files in os.walk(TARGET_DIR)]
    )
    image_count = len(flatten_images)
    for idx, img_path in enumerate(flatten_images):
        resp_img = resize_and_desensitization(img_path)
        progressbar(idx + 1, image_count, prefix=PREFIX, ext=resp_img)
    print("\n")


def test():
    img_path = "source/resource/img/15552247425780.jpg"
    import pdb; pdb.set_trace()
    resize_and_desensitization(img_path)


if __name__ == "__main__":
    run()
