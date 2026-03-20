import tkinter as tk
import time

filename = "A1_沟通"
# ========= 配置 =========
FILE_PATH = f"/Users/adam/Library/Mobile Documents/com~apple~CloudDocs/Documents/高项相关/论文2026/{filename}.md"
FONT_SIZE = 36
SCROLL_SPEED = 1
LINE_FOCUS = 10      # 屏幕中间高亮行
PAUSE_TIME = 4000    # 每段停顿时间(ms)

# ========= 读取并分段 =========
with open(FILE_PATH, "r", encoding="utf-8") as f:
    raw_text = f.read()

# 按句号分段（核心）
segments = [s.strip() for s in raw_text.split("。") if s.strip()]

# ========= UI =========
root = tk.Tk()
root.title("神器")
root.attributes("-fullscreen", True)

text_widget = tk.Text(
    root,
    font=("PingFang SC", FONT_SIZE),
    wrap="word",
    bg="black",
    fg="white",
    padx=100,
    pady=50
)
text_widget.pack(fill="both", expand=True)

# 高亮样式
text_widget.tag_configure("focus", foreground="yellow")
text_widget.tag_configure("dim", foreground="gray")

# ========= 状态 =========
current_idx = 0
is_paused = False
mode_hide = False   # 遮挡模式

# ========= 渲染函数 =========
def render():
    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)

    for i, seg in enumerate(segments):
        if mode_hide and i == current_idx:
            display = "████████████████████████"
        else:
            display = seg

        text_widget.insert(tk.END, display + "。\n\n")

    text_widget.config(state="disabled")

    highlight_line()

# ========= 高亮当前句 =========
def highlight_line():
    text_widget.tag_remove("focus", "1.0", tk.END)
    text_widget.tag_remove("dim", "1.0", tk.END)

    start = f"{current_idx*2+1}.0"
    end = f"{current_idx*2+2}.0"

    text_widget.tag_add("focus", start, end)
    # 自动滚动到当前高亮位置（关键修复）
    text_widget.see(start)

# ========= 自动播放 =========
def play():
    global current_idx
    if is_paused:
        return

    render()

    # 根据当前段落长度动态调整停顿时间（核心优化）
    if current_idx < len(segments):
        seg_len = len(segments[current_idx])
        dynamic_pause = max(1500, min(8000, seg_len * 80))
    else:
        dynamic_pause = PAUSE_TIME

    current_idx += 1
    if current_idx >= len(segments):
        return

    root.after(dynamic_pause, play)

# ========= 控制 =========
def toggle_pause(event=None):
    global is_paused
    is_paused = not is_paused
    if not is_paused:
        play()

def reset(event=None):
    global current_idx
    current_idx = 0
    render()

def toggle_hide(event=None):
    global mode_hide
    mode_hide = not mode_hide
    render()

def speed_up(event=None):
    global PAUSE_TIME
    PAUSE_TIME = max(500, PAUSE_TIME - 300)
    print("速度:", PAUSE_TIME)

def speed_down(event=None):
    global PAUSE_TIME
    PAUSE_TIME += 300
    print("速度:", PAUSE_TIME)

def quit_app(event=None):
    root.destroy()

# ========= 快捷键 =========
root.bind("<space>", toggle_pause)   # 暂停/继续
root.bind("r", reset)               # 重置
root.bind("h", toggle_hide)         # 遮挡模式（背诵神器）
root.bind("<Up>", speed_up)
root.bind("<Down>", speed_down)
root.bind("<Escape>", quit_app)

# ========= 启动 =========
render()
play()

root.mainloop()