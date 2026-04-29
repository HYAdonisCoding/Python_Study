import fitz  # PyMuPDF
from PIL import Image
import io
import os
import math

input_pdf_path = "/Users/adam/Documents/Document/高项/26年5月考试-高项课程资料包/03-【第一阶段-基础知识】-妍师手册（基础分册）/《信息系统项目管理师-妍师手册（基础分册）》V4.0.pdf"

output_pdf_path = "/Users/adam/Documents/Document/night_mode_lightweight.pdf"


# =========================
# 自适应 DPI（核心优化）
# =========================
def calc_zoom(page, target_width=1400):
    """根据页面宽度自动选择缩放比例（避免过大体积）"""
    page_width = page.rect.width
    zoom = target_width / page_width
    return max(1.0, min(2.0, zoom))  # 限制在 1.0~2.0


def binarize(img: Image.Image, threshold=185):
    """自动二值化（提升对比 + 压缩体积关键）"""
    return img.convert("L").point(lambda x: 255 if x > threshold else 0)


def process_pdf():
    pdf = fitz.open(input_pdf_path)
    out_pdf = fitz.open()

    print(f"Total pages: {len(pdf)}")

    for i, page in enumerate(pdf):
        print(f"Processing page {i+1}/{len(pdf)}")

        # ===== 1. 自适应 DPI 渲染 =====
        zoom = calc_zoom(page)
        mat = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY, alpha=False)

        # ===== 2. 转 PIL（无 PNG 文件落地）=====
        img = Image.frombytes("L", [pix.width, pix.height], pix.samples)

        # ===== 3. 夜间模式核心：二值化 =====
        img = binarize(img)

        # ===== 4. 反色（夜间模式）=====
        img = Image.eval(img, lambda x: 255 - x)

        # ===== 5. 转回内存 PDF image =====
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG", optimize=True)
        img_bytes = img_bytes.getvalue()

        # ===== 6. 写入新 PDF =====
        rect = page.rect
        new_page = out_pdf.new_page(width=rect.width, height=rect.height)

        new_page.insert_image(rect, stream=img_bytes)

    pdf.close()

    # ===== 7. 输出 PDF =====
    out_pdf.save(output_pdf_path, deflate=True)
    out_pdf.close()

    print(f"\nDone!")
    print(f"Output: {output_pdf_path}")


if __name__ == "__main__":
    process_pdf()