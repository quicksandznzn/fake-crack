import cv2
import numpy as np
from matplotlib import pyplot as plt
import requests
from PIL import Image
from io import BytesIO


def opencv_match_template_coord(bg_path, slide_block_path, tmp_path):
    """
        opencv 模板匹配 计算二维位置
    :param bg_path:  背景图
    :param slide_block_path: 滑动块
    :param tmp_path: tmp
    :return: x,y
    """
    # 读取图片
    bg = cv2.imread(bg_path)
    slide_block = cv2.imread(slide_block_path)
    # 灰度处理
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    slide_block = cv2.cvtColor(slide_block, cv2.COLOR_BGR2GRAY)
    slide_block = abs(255 - slide_block)
    cv2.imwrite(tmp_path, slide_block)
    # 去掉滑块黑色部分 # 0表示黑色，1表示高亮部分
    slide_block = slide_block[slide_block.any(1)]
    # 匹配->cv图像匹配算法 match匹配,Template模板;精度高，速度慢的方法
    result = cv2.matchTemplate(bg, slide_block, cv2.TM_CCOEFF_NORMED)
    # 返回的是一维的位置，最大值索引
    index_max = np.argmax(result)
    # 反着推最大值的二维位置，和opencv是相反的
    x, y = np.unravel_index(index_max, result.shape)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("----------------------------")
    print("min_val", min_val)
    print("max_val", max_val)
    print("min_loc", min_loc)
    print("max_loc", max_loc)
    print("----------------------------")
    h, w = slide_block.shape[:2]
    bottom_right = (max_loc[0] + w, max_loc[1] + h)
    # cv2.circle(result, max_loc, 10, 0, 2)
    # 画矩形|
    cv2.rectangle(bg, max_loc, bottom_right, (0, 255, 0), 2)
    plt.subplot(121), plt.imshow(result, cmap="gray")
    plt.subplot(122), plt.imshow(bg, cmap="gray")
    plt.show()

    return x, y


def download_image(filepath, img_url):
    """
        download image
    :param filepath: save path
    :param img_url: img_url
    :return: image
    """
    response = requests.get(url=img_url)
    new_im: Image = Image.open(BytesIO(response.content))
    new_im.convert("RGB")
    new_im.save(filepath)
    return new_im


if __name__ == "__main__":
    bg_path = "../file/image/bg.png"
    slide_block_path = "../file/image/block.png"
    tmp_path = "../file/tmp.png"
    x, y = opencv_match_template_coord(
        bg_path=bg_path, slide_block_path=slide_block_path, tmp_path=tmp_path
    )
    print(x, y)
