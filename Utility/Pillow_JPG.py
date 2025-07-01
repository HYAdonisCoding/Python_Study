from PIL import Image, ExifTags
import os

def correct_image_orientation(img):
    """
    确保图片方向正确
    :param img: 图片对象
    :return: 修正后的图片对象
    """
    try:
        # 获取EXIF数据
        exif = img._getexif()
        if exif is not None:
            for tag, value in exif.items():
                if tag == 274:  # 274是EXIF中的Orientation标签
                    if value == 3:
                        img = img.rotate(180, expand=True)
                    elif value == 6:
                        img = img.rotate(270, expand=True)
                    elif value == 8:
                        img = img.rotate(90, expand=True)
                    break
    except (AttributeError, KeyError, IndexError):
        # 如果图片没有EXIF数据，则跳过
        pass
    return img

def compress_image(image_path, output_path, quality=85):
    """
    压缩JPG图片并修正方向
    :param image_path: 输入图片路径
    :param output_path: 输出图片路径
    :param quality: 压缩质量，0-100（默认85）
    """
    with Image.open(image_path) as img:
        # 确保图片方向正确
        img = correct_image_orientation(img)
        # 保存图片时指定quality，进行无损压缩
        img.save(output_path, "JPEG", quality=quality, optimize=True)

def batch_compress_images(input_folder, output_folder, quality=85):
    """
    批量压缩文件夹中的所有JPG图片
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    :param quality: 压缩质量
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            print(f"正在压缩: {image_path}")
            compress_image(image_path, output_path, quality)


    print(f"压缩完成: {output_folder}")
if __name__ == "__main__":
    # 使用示例
    input_folder = "/Users/adam/Downloads/Picture"  # 输入图片文件夹路径
    output_folder = "/Users/adam/Downloads/compressed_Pictures"  # 输出图片文件夹路径
    batch_compress_images(input_folder, output_folder, quality=75)