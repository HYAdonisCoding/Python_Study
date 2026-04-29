import fitz  # PyMuPDF
from PIL import Image
import os

input_pdf_path = "/Users/adam/Documents/Document/高项/26年5月考试-高项课程资料包/03-【第一阶段-基础知识】-妍师手册（基础分册）/《信息系统项目管理师-妍师手册（基础分册）》V4.0.pdf"
output_dir = "/Users/adam/Documents/Document/output_pages"
output_pdf_path = "/Users/adam/Documents/Document/night_mode.pdf"

os.makedirs(output_dir, exist_ok=True)

pdf = fitz.open(input_pdf_path)
image_paths = []
def invert_pdf(): 
    

    
    for i, page in enumerate(pdf):
        print(f"Processing page {i+1}...")

        # 高清渲染
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)

        img_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 反色（黑底白字）
        img_inverted = Image.eval(img_pil, lambda x: 255 - x)

        # 轻微对比度优化（让文字更清晰）
        img_inverted = img_inverted.point(lambda x: x * 1.1)
        img_inverted = img_inverted.convert("L")

        img_path = f"{output_dir}/page_{i+1}.png"
        # 无损压缩 PNG（减小体积）
        img_inverted.save(img_path, format="PNG", optimize=True, compress_level=9)
        image_paths.append(img_path)

    pdf.close()

    print("All pages processed. Now merging into PDF...")

# 拼回 PDF
def convert_topdf():
    images = [Image.open(p).convert("RGB") for p in image_paths]

    if images:
        # 使用无损压缩（避免 JPEG 依赖，同时减小体积）
        images[0].save(
            output_pdf_path,
            save_all=True,
            append_images=images[1:],
            resolution=100.0,
            compression="tiff_deflate"
        )

    print(f"Done! Output PDF: {output_pdf_path}")

import subprocess

def compress_pdf(input_path, output_path):
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]

    subprocess.run(cmd, check=True)
    
if __name__ == "__main__":
    invert_pdf()
    convert_topdf()

    compress_pdf(
        "/Users/adam/Documents/Document/night_mode.pdf",
        "/Users/adam/Documents/Document/night_mode_compressed.pdf"
    )