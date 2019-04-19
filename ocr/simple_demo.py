# @Time    : 2019/4/19 4:09
# @Author  : Noah
# @File    : simple_demo.py
# @Software: PyCharm
# @description: test the tesserocr about recognition picture
import tesserocr
from PIL import Image


def main():
    image = Image.open('test.jpg')
    image = image.convert('L')
    threshold = 120
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    result = tesserocr.image_to_text(image)
    print(result)


if __name__ == "__main__":
    main()
