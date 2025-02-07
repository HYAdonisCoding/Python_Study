from PIL import Image, ImageDraw, ImageOps
import os

# 定义要生成的图标尺寸
sizes = [(16, 16), (32, 32), (40, 40), (64, 64), (96, 96), (128, 128), (256, 256), (512, 512), (1024, 1024)]
# 源图标文件路径
source_icon_path = "/Users/adam/Pictures/Cavin Graphic.jpg"
# 输出目录
output_dir = "icons"


def generate_icons(source_path, sizes, output_dir):
    with Image.open(source_path) as img:
        for size in sizes:
            # 调整图像大小
            resized_img = img.resize(size, Image.LANCZOS)
            # 生成输出路径
            output_path = os.path.join(output_dir, f"icon_{size[0]}x{size[1]}.png")
            # 保存图像
            resized_img.save(output_path)

def generate_circular_icons(source_path, sizes, output_dir):
    with Image.open(source_path) as img:
        for size in sizes:
            # 调整图像大小
            resized_img = img.resize(size, Image.LANCZOS)

            # 创建圆形遮罩
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            diameter = min(size)  # 取宽高的最小值作为直径
            left = (size[0] - diameter) // 2
            top = (size[1] - diameter) // 2
            right = left + diameter
            bottom = top + diameter
            draw.ellipse((left, top, right, bottom), fill=255)

            # 应用圆形遮罩到调整大小后的图像
            circular_img = ImageOps.fit(resized_img, mask.size, centering=(0.5, 0.5))
            circular_img.putalpha(mask)

            # 生成输出路径
            output_path = os.path.join(output_dir, f"icon_{size[0]}x{size[1]}_circular.png")

            # 保存图像
            circular_img.save(output_path)
if __name__ == '__main__':
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    generate_circular_icons(source_icon_path, sizes, output_dir)