# -*- coding: utf-8 -*-

import os
import edge_tts
from docx import Document
import re
import os
import pypandoc
import asyncio
import shutil

def convert_pyp():
    # 设置文件夹路径
    
    """
    Converts all .docx files in the specified input folder to Markdown format 
    using Pandoc and saves them in the specified output folder.

    The function ensures the output folder exists and processes each .docx 
    file by converting it to a .md file with the same name. The conversion 
    progress is printed to the console.

    Note: Update the input_folder and output_folder paths as required.
    """

    input_folder = "/Users/adam/同步空间/高项论文2025/绩效域0/"# 替换为你的 Word 文件所在路径
    output_folder = "/Users/adam/同步空间/论文2025/" # 替换为转换后的 Markdown 存放路径
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历文件夹内的所有 .docx 文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".docx"):  # 只处理 .docx 文件
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name.replace(".docx", ".md"))

            # 使用 Pandoc 进行转换
            pypandoc.convert_file(input_path, 'md', outputfile=output_path)

            print(f"转换完成: {file_name} -> {output_path}")

    print("所有文件转换完成！")


# python3 "/Users/adam/Library/Mobile Documents/com~apple~CloudDocs/MWebDocuments/高项/tts.py"
filename = "B2_风险"
text_file_path = f"/Users/adam/Library/Mobile Documents/com~apple~CloudDocs/Documents/高项相关/论文2026/{filename}.md"
voice_type = "zh-CN-XiaoxiaoNeural" #"zh-CN-XiaoxiaoNeural"
'''
zh-CN-XiaoxiaoNeural               Female    News, Novel            Warm
zh-CN-XiaoyiNeural                 Female    Cartoon, Novel         Lively
zh-CN-YunjianNeural                Male      Sports, Novel          Passion
zh-CN-YunxiNeural                  Male      Novel                  Lively, Sunshine
zh-CN-YunxiaNeural                 Male      Cartoon, Novel         Cute
zh-CN-YunyangNeural                Male      News                   Professional, Reliable
zh-CN-liaoning-XiaobeiNeural       Female    Dialect                Humorous
zh-CN-shaanxi-XiaoniNeural         Female    Dialect                Bright
'''
voice_file_path = f"/Users/adam/Library/Mobile Documents/com~apple~CloudDocs/Documents/高项相关/音频2026/{filename}.mp3"

def readUTF8_batch_by_names(text_file_path, voice_type, filenames):
    """
    仅处理传入的文件名列表
    文本来自 text_file_path 所在目录
    音频统一输出到 voice_file_path 所在目录
    """
    print("🔥🔥🔥 我是 readUTF8_batch_by_names 新版本")
    print("🔥 filenames =", filenames)
    base_dir = os.path.dirname(text_file_path)
    output_dir = os.path.dirname(voice_file_path)
    os.makedirs(output_dir, exist_ok=True)

    # 构造待处理文件列表
    target_files = []
    for name in filenames:
        if not name.lower().endswith((".md", ".txt")):
            name += ".md"
        full_path = os.path.join(base_dir, name)
        if os.path.exists(full_path):
            target_files.append(name)
        else:
            print(f"⚠️ 文件不存在，已跳过: {name}")

    if not target_files:
        print("❌ 没有可处理的文件")
        return

    print(f"📄 待处理文件：{target_files}")

    def split_text(text, max_len=800):
        parts, buf = [], ""
        for ch in text:
            buf += ch
            if len(buf) >= max_len and ch in "。！？；":
                parts.append(buf.strip())
                buf = ""
        if buf.strip():
            parts.append(buf.strip())
        return parts

    async def process_one_file(txt_path, mp3_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        text = re.sub(r'!\[img\]\(.*?\)', '', text)
        text = text.replace("# ", "").replace("*", "").strip()

        parts = split_text(text)
        print(f"\n▶ {os.path.basename(txt_path)}：{len(parts)} 段")

        temp_files = []
        for idx, part in enumerate(parts, 1):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            tmp = os.path.join(script_dir, os.path.basename(mp3_path).replace(".mp3", f"_{idx}.mp3"))
            success = False
            n = 5
            for attempt in range(1, n+1):  # 最多重试 n 次
                try:
                    print(f"   🔄 第 {idx} 段尝试第 {attempt} 次")
                    communicate = edge_tts.Communicate(
                        text=part,
                        voice=voice_type,
                        rate="+35%"
                    )
                    await asyncio.wait_for(communicate.save(tmp), timeout=30)
                    temp_files.append(tmp)
                    success = True
                    break
                except asyncio.TimeoutError:
                    print(f"   ⏳ 第 {idx} 段超时 (第 {attempt} 次)")
                except Exception as e:
                    print(f"   ⚠️ 第 {idx} 段失败 (第 {attempt} 次): {e}")
                finally:
                    if not success and os.path.exists(tmp):
                        os.remove(tmp)

            if not success:
                print(f"   ❌ 第 {idx} 段重试 {n+1} 次仍失败，已放弃")
                continue

        with open(mp3_path, "wb") as final:
            for f in temp_files:
                with open(f, "rb") as pf:
                    final.write(pf.read())
                os.remove(f)

        print(f"✅ 完成：{os.path.basename(mp3_path)}")
        # 拷贝到 Music 目录
        music_dir = "/Users/adam/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album"
        iCloudDir = "/Users/adam/Library/Mobile Documents/com~apple~CloudDocs/Documents/高项相关/音频2026/"
        os.makedirs(music_dir, exist_ok=True)
        os.makedirs(iCloudDir, exist_ok=True)
        
        print("DEBUG src:", mp3_path)
        
        dst_path = os.path.join(music_dir, os.path.basename(mp3_path))
        shutil.copy2(mp3_path, dst_path)
        
        # 正确：从生成的 mp3_path 复制到 iCloud 目录，避免源文件和目标文件相同导致 SameFileError
        dst_path1 = os.path.join(iCloudDir, os.path.basename(mp3_path))
        
        # 避免源文件和目标文件相同导致 SameFileError
        if os.path.abspath(mp3_path) != os.path.abspath(dst_path1):
            shutil.copy2(mp3_path, dst_path1)
        else:
            print("⚠️ 跳过拷贝（源文件和目标文件相同）")

        print(f"🎵 已拷贝到 Music 目录: {dst_path}")
        print(f"☁️ 已拷贝到 iCloud 目录: {dst_path1}")

    async def run_all():
        for name in target_files:
            txt_path = os.path.join(base_dir, name)
            mp3_path = os.path.join(
                output_dir,
                os.path.splitext(name)[0] + ".mp3"
            )
            await process_one_file(txt_path, mp3_path)

    asyncio.run(run_all())
    print(f"\n🎉 全部完成，输出目录：{output_dir}")
    

def readUTF8_batch(text_file_path, voice_type):
    """
    扫描 text_file_path 所在目录
    找出文件名以 A-D 开头的文本文件
    逐个转换为 mp3
    """

    base_dir = os.path.dirname(text_file_path)

    # 输出音频统一放到 voice_file_path 所在目录
    output_dir = os.path.dirname(voice_file_path)
    os.makedirs(output_dir, exist_ok=True)

    # 只处理 A-D 开头的文件（大小写都算）
    target_files = sorted(
        f for f in os.listdir(base_dir)
        if re.match(r'^[A-Da-d]', f) and f.lower().endswith(('.txt', '.md'))
    )

    if not target_files:
        print("❌ 未找到 A-D 开头的文本文件")
        return

    print(f"📄 发现 {len(target_files)} 个待处理文件：")
    for f in target_files:
        print("  -", f)

    # 文本分段，防止 TTS 超长
    def split_text(text, max_len=800):
        parts, buf = [], ""
        for ch in text:
            buf += ch
            if len(buf) >= max_len and ch in "。！？；":
                parts.append(buf.strip())
                buf = ""
        if buf.strip():
            parts.append(buf.strip())
        return parts

    async def process_one_file(txt_path, mp3_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()

        # 清洗文本
        text = re.sub(r'!\[img\]\(.*?\)', '', text)
        text = text.replace("# ", "").replace("*", "").strip()

        parts = split_text(text)
        print(f"\n▶ {os.path.basename(txt_path)} 拆分为 {len(parts)} 段")

        temp_files = []

        for idx, part in enumerate(parts, 1):
            tmp_mp3 = mp3_path.replace(".mp3", f"_{idx}.mp3")
            print(f"   🔊 生成 {idx}/{len(parts)}")

            communicate = edge_tts.Communicate(
                text=part,
                voice=voice_type,
                rate="+35%"
            )
            await communicate.save(tmp_mp3)
            temp_files.append(tmp_mp3)

        # 合并 mp3
        with open(mp3_path, "wb") as final:
            for f in temp_files:
                with open(f, "rb") as pf:
                    final.write(pf.read())
                os.remove(f)

        print(f"✅ 完成：{os.path.basename(mp3_path)}")

    async def run_all():
        for filename in target_files:
            txt_path = os.path.join(base_dir, filename)
            mp3_path = os.path.join(
                output_dir,
                os.path.splitext(filename)[0] + ".mp3"
            )
            await process_one_file(txt_path, mp3_path)

    asyncio.run(run_all())

    print("\n🎉 所有音频生成完成")
    print(f"📂 音频输出目录：{output_dir}")
    
def readUTF8():


    # 读取文本文件
    with open(text_file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # 清洗文本
    text = re.sub(r'!\[img\]\(.*?\)', '', text)
    text = text.replace("# ", "")
    text = text.replace("*", "")
    text = text.strip()

    # 分段函数（避免超长文本导致 TTS 阻塞）
    def split_text(text, max_len=800):
        parts = []
        buf = ""
        for ch in text:
            buf += ch
            if len(buf) >= max_len and ch in "。！？；":
                parts.append(buf.strip())
                buf = ""
        if buf.strip():
            parts.append(buf.strip())
        return parts

    parts = split_text(text)
    print(f"文本已拆分为 {len(parts)} 段")

    async def run_tts():
        audio_files = []
        for idx, part in enumerate(parts, 1):
            out_file = voice_file_path.replace(".mp3", f"_{idx}.mp3")
            print(f"正在生成音频 {idx}/{len(parts)}")
            communicate = edge_tts.Communicate(
                text=part,
                voice=voice_type,
                rate="+35%"
            )
            await communicate.save(out_file)
            audio_files.append(out_file)

        # 合并 mp3
        with open(voice_file_path, "wb") as final:
            for f in audio_files:
                with open(f, "rb") as part_f:
                    final.write(part_f.read())
                os.remove(f)

    asyncio.run(run_tts())
    print(f"Complete {filename} exporting audio!🎉🎉🎉")
    output_dir = os.path.dirname(voice_file_path)
    print(f"音频输出目录: {output_dir}")

def readWord():
    # 读取文本文件
    # 打开 .docx 文件
    doc = Document(text_file_path)

    # 提取文本内容
    text_to_convert = "\n".join([paragraph.text for paragraph in doc.paragraphs]).replace("\n", "。")
    print(text_to_convert)

    # 对路径进行转义
    text_to_convert_escaped = shlex.quote(text_to_convert)
    voice_file_escaped = shlex.quote(voice_file_path)

    # 构建命令行
    # cmd = f"edge-tts --voice {voice_type} --text {text_to_convert_escaped} --write-media {voice_file_escaped}"
    cmd = f"edge-tts --pitch=+20Hz --rate=+20% --voice {voice_type} --text {text_to_convert_escaped} --write-media {voice_file_escaped}"
    print(cmd)

    # 执行命令
    os.system(cmd)


import os

def merge():
    """
    Merge all Markdown files in a specified folder into a single Markdown file.
    
    The function reads all .md files in the specified folder, ignoring any 
    files listed in the ignored_files set, and writes their content into 
    a single output file. Each file's content is preceded by its filename 
    as a section header.

    Note: Update the folder_path and output_file variables as required.
    """
    folder_path = "/Users/adam/Library/Mobile Documents/com~apple~CloudDocs/Documents/高项相关/论文2025/"  # 修改为你的实际路径
    output_file = os.path.join(folder_path, "论文集合 3.0.md")  # 使用绝对路径

    ignored_files = {"论文集.md", "论文集合.md"}  # 忽略列表，可添加更多文件名

    # 检查输出文件是否已存在，如果存在则删除
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"已删除旧的输出文件: {output_file}")
        
    # 创建输出文件并写入内容
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 添加标题
        outfile.write('''
        ---
        title: 论文集 3.0
        creator: 燕云少君
        publisher:  My iBooks
        rights: © 2025 Eason Hongyang, CC BY-NC
        ibooks:
        version: 3.4.0
        ---\n
        ''')  
        
        
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".md") and filename not in ignored_files:
                file_path = os.path.join(folder_path, filename)
                print(f"正在合并文件: {filename}")
                # 读取文件内容并写入输出文件
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(f"\n\n---\n\n")  # 分隔标题（可去掉）
                    outfile.write(infile.read())
                    print(f"合并完成: {filename}")
    print(f"所有文件合并完成！输出文件: {output_file}")
    
                
if __name__ == "__main__":
    try:
        readUTF8_batch_by_names(
            text_file_path,
            voice_type,
            filenames=[
                # "A1_沟通",
                # "A2_采购",
                # "A3_范围",
                # "A4_质量",
                # "B1_整合",
                # "B2_风险",
                # "B3_资源",
                # "C1_干系人",
                # "C2_进度",
                "C3_成本",
                # "a1_干系人绩效域",
                # "a2_度量绩效域",
                "b1_开发方法和生命周期绩效域",
                "b2_规划绩效域",
                # "b3_团队绩效域",
                "c1_项目工作绩效域",
                "c2_交付绩效域",
                # "c3_不确定性绩效域",
            ]
        )
        print(f"Complete!🎉🎉🎉")
    except KeyboardInterrupt:
        print("\n🛑 用户手动终止程序，已安全退出。")