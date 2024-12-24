from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
from io import BytesIO

# 创建空的PDF writer对象
writer = PdfWriter()

# 加载PDF文件并转换为图像
# 将PDF转换为图像
images1 = convert_from_path("/Users/adam/Downloads/MPr9L2dkx4OAJql0AADheZvEH3Q230.pdf", dpi=300)
images2 = convert_from_path("/Users/adam/Downloads/MPr92mdjyGyAGs5hAAPBboPvmvI850 copy.pdf", dpi=300)

# 创建新的空白PDF页面
packet = BytesIO()
c = canvas.Canvas(packet)
c.setPageSize((595, 842))  # A4纸大小

# 设置页边距（假设边距为20 points）
margin = 20
width, height = 595, 842  # A4纸的宽度和高度

# 调整图像大小以适应纸张，并留出边距
img_width = width - 2 * margin
img_height = height / 2 - margin  # 每个图像占页面的一半高度，减去边距

# 保存PDF页面的第一张图像（来自第一个PDF文件）
img_path1 = "/tmp/image1.jpg"
images1[0].save(img_path1, 'JPEG')
c.drawImage(img_path1, margin, height / 2 + margin, width=img_width, height=img_height)  # 绘制第一个图像

# 保存PDF页面的第二张图像（来自第二个PDF文件）
img_path2 = "/tmp/image2.jpg"
images2[0].save(img_path2, 'JPEG')
c.drawImage(img_path2, margin, margin, width=img_width, height=img_height)  # 绘制第二个图像

# 保存新的页面
c.save()

# 读取合成后的PDF页面
packet.seek(0)
new_pdf = PdfReader(packet)

# 将合成的页面写入新的PDF
writer.add_page(new_pdf.pages[0])

# 将新PDF保存到文件
with open("merged_invoice.pdf", "wb") as f:
    writer.write(f)