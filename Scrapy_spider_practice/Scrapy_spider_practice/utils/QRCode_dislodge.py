import cv2
import numpy as np
import os


def remove_qr_code(image_path):
    # 读取图片
    img = cv2.imread(image_path)
    # 将图片转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 定义二维码可能的颜色范围（这里以黑色为主色调为例）
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    # 根据颜色范围创建掩码
    black_mask = cv2.inRange(hsv, lower_black, upper_black)

    # 对掩码进行形态学操作，去除噪声并连接相邻区域
    kernel = np.ones((5, 5), np.uint8)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_CLOSE, kernel)

    # 查找掩码中的轮廓
    contours, _ = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历轮廓，筛选出可能是二维码的矩形轮廓（根据面积和宽高比筛选）
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # 面积阈值，可根据实际情况调整
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h if h != 0 else 0
            if 0.8 <= aspect_ratio <= 1.2:  # 宽高比阈值，可根据实际情况调整
                # 使用周围像素填充二维码区域
                img[y:y + h, x:x + w] = cv2.mean(img[y - 10:y + h + 10, x - 10:x + w + 10])[:3].astype(np.uint8)

    return img


input_folder = '/Users/adam/Downloads/undispose'
output_folder = '/Users/adam/Downloads/disposed'

def doubao_dispose():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.png')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            processed_img = remove_qr_code(input_path)
            cv2.imwrite(output_path, processed_img)
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# import cv2
# import numpy as np

def gpt_dispose():
    # 读取图像
    image = cv2.imread('/Users/adam/Downloads/undispose/126.jpg')

    # 定义二维码区域的宽高和位置
    qr_width, qr_height = 150, 150  # 示例，您可以根据实际二维码大小进行调整

    # 去除左下角二维码区域
    left_qr_box = (0, image.shape[0] - qr_height, qr_width, image.shape[0])
    image[left_qr_box[1]:left_qr_box[3], left_qr_box[0]:left_qr_box[2]] = 255  # 用白色覆盖

    # 去除右下角二维码区域
    right_qr_box = (image.shape[1] - qr_width, image.shape[0] - qr_height, image.shape[1], image.shape[0])
    image[right_qr_box[1]:right_qr_box[3], right_qr_box[0]:right_qr_box[2]] = 255  # 用白色覆盖

    # 使用OpenCV的修复功能填补空白区域
    mask = np.zeros(image.shape[:2], np.uint8)
    mask[left_qr_box[1]:left_qr_box[3], left_qr_box[0]:left_qr_box[2]] = 255
    mask[right_qr_box[1]:right_qr_box[3], right_qr_box[0]:right_qr_box[2]] = 255
    image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

    # 保存修改后的图像
    cv2.imwrite('/Users/adam/Downloads/undispose/processed_126_inpainted.jpg', image)
#--------------------------------------------------------------------------------
if __name__ == "__main__":
    doubao_dispose()
    # gpt_dispose()