# coding=utf-8
import urllib

import requests
from PIL import Image  # 图像处理模块, pip install pillow
from bs4 import BeautifulSoup
import pygame
import os
import random

def getJPGs(url):
    # 使用 BeautifulSoup 解析 HTML
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    # 查找 class 为 BDE_Image 的图片标签
    image_tags = soup.find_all("img", class_="BDE_Image")
    # 提取图片链接
    image_urls = [img["src"] for img in image_tags]
    return image_urls


def downloadJPG(imgUrl, fileName):
    response = requests.get(imgUrl)
    with open(fileName, 'wb') as f:
        f.write(response.content)


def batchDownloadJPGs(imgUrls, path='pixels/'):
    if not os.path.exists(path):
        os.mkdir(path)

    count = 0
    for url in imgUrls:
        downloadJPG(url, ''.join([path, '{0}.jpg'.format(count)]))
        print('number: ' + str(count))
        count = count + 1


def get_text_position(text):
    pygame.init()
    font_size = 30  # 字体大小pygame.init()  # 模块的初始化  为什么  pygame不是我开发的, 我们用的别人  python语法  三原色
    font = pygame.font.Font('msyh.ttc', font_size)
    print(font)  # 字体的渲染
    # True 锯齿化   rgb 颜色 由三原色组成  黑  白
    font_text = font.render(text, True, (0, 0, 0), (255, 255, 255))
    print(font_text)  # 获取字体的宽高
    height = font_text.get_height()  # 高度
    width = font_text.get_width()  # 宽度
    print('height: ', height)
    print('width: ', width)  # 根据什么逻辑贴图  像素点
    image_row_list = []
    shrink_part = 1
    for x in range(height // shrink_part):
        image_col_list = []
        for y in range(width // shrink_part):
            val = 0
            for i in range(shrink_part):
                for j in range(shrink_part):
                    x_index = x * shrink_part + i
                    y_index = y * shrink_part + j
                    val += font_text.get_at((y_index, x_index))[0]
            val //= shrink_part * shrink_part
            if val != 255:  # 如果像素点不是白色
                image_col_list.append(1)  # 黑色添加数据1
            else:
                image_col_list.append(0)  # 白色添加数据0
        image_row_list.append(image_col_list)

    return list(image_row_list)


def drawImage(image_list):
    width_len = len(image_list[0])  # 列表的宽
    height_len = len(image_list)  # # 列表的高# 创建图片
    new_image = Image.new('RGB', (width_len * 100, height_len * 100), (255, 255, 255))  # 贴图
    img_size = 100  # 初始图片尺寸
    for row in range(height_len):
        for clo in range(width_len):
            if image_list[row][clo] == 1:  # 如过列表的值为1, 就贴图# 读取图片
                source_image = Image.open('pixels/' + random.choice(os.listdir(r'pixels')))# 修改图片的大小
                source_image = source_image.resize((img_size, img_size), Image.LANCZOS)# 将图片复制到new_image
                new_image.paste(source_image, (clo * img_size, row * img_size))# 照片强保存
    print('正在生成照片墙...')
    new_image.save('output_1.png')
    print('保存完毕, 请在当前文件项目下查找')


if __name__ == "__main__":
    url = 'https://tieba.baidu.com/p/8594160102'
    jpgs = getJPGs(url)
    batchDownloadJPGs(jpgs)
    list = get_text_position('教师节快乐')
    drawImage(list)