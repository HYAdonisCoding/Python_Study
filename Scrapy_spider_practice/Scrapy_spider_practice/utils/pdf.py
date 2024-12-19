from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
from io import BytesIO

# 创建空的PDF writer对象
writer = PdfWriter()

# 加载PDF文件并转换为图像
# 将PDF转换为图像
images1 = convert_from_path("/Users/adam/Downloads/MPr92mdjyGyAGs5hAAPBboPvmvI850 copy 2.pdf", dpi=300)
images2 = convert_from_path("/Users/adam/Downloads/MPr92mdjyGyAGs5hAAPBboPvmvI850 copy.pdf", dpi=300)

# 创建新的空白PDF页面
packet = BytesIO()
c = canvas.Canvas(packet)
c.setPageSize((595, 842))  # A4纸大小

# 保存PDF页面的第一张图像（来自第一个PDF文件）
img_path1 = "/tmp/image1.jpg"
images1[0].save(img_path1, 'JPEG')
c.drawImage(img_path1, 0, 420, width=595, height=421)  # 调整图像位置和大小

# 保存PDF页面的第二张图像（来自第二个PDF文件）
img_path2 = "/tmp/image2.jpg"
images2[0].save(img_path2, 'JPEG')
c.drawImage(img_path2, 0, 0, width=595, height=421)  # 调整图像位置和大小

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