import os

from PIL import Image

from werkzeug.utils import secure_filename

import cv2
import numpy as np

widthNum = 0.905
heightNum = 0.905

# 需要处理的文件
watermarkName = "watermark.png"

# 当前文件所在路径
basepath = os.path.dirname(__file__)

# 注意：没有的文件夹一定要先创建，不然会提示没有该路径
upload_path = os.path.join(basepath, './static/photo', secure_filename(watermarkName))

# 使用Opencv转换一下图片格式和名称
img = cv2.imread(upload_path, 1)
newPath = os.path.join(basepath, './static/photo', 'new.jpg')
hight, width, _ = img.shape[0:3]
# 切割，根据实际水印位置而定，[y0:1，x0:x1]为下面裁剪用法，裁剪完后可以用上面的方法输出查看一下
cropped = img[int(hight * heightNum):hight, int(width * widthNum):width]
cv2.imwrite(newPath, cropped)
imgSY = cv2.imread(newPath, 1)
# 照片二值化解决，把[200,200,200]-[250,250,250]之外的色调变为0
thresh = cv2.inRange(imgSY, np.array([140, 140, 140]), np.array([150, 150, 150]))
# 创建结构和尺寸的数据元素
kernel = np.ones((3, 3), np.uint8)
# 拓展待修补地区
hi_mask = cv2.dilate(thresh, kernel, iterations=10)
specular = cv2.inpaint(imgSY, hi_mask, 5, flags=cv2.INPAINT_TELEA)
# 保存去除水印的残图
cv2.imwrite(newPath, specular)

#  用PIL的paste函数把残图粘贴在原图上得到新图
imgSY = Image.open(newPath)
img = Image.open(upload_path)
img.paste(imgSY, (int(width * widthNum), int(hight * heightNum), width, hight))
img.save(upload_path)
img = cv2.imread(upload_path)
cv2.imwrite(os.path.join(basepath, './static/photo', 'result.jpg'), img)
# os.remove(os.path.join(basepath, './static/photo', 'new.jpg'))
# os.remove(os.path.join(basepath, './static/photo', secure_filename(watermarkName)))
