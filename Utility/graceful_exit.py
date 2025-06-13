# graceful_exit.py
import signal
import threading

stop_event = threading.Event()

def handle_interrupt(sig, frame):
    print("🔁 收到中断信号，准备优雅退出...")
    stop_event.set()

# 只在首次导入时注册 signal handler
signal.signal(signal.SIGINT, handle_interrupt)
signal.signal(signal.SIGTERM, handle_interrupt)