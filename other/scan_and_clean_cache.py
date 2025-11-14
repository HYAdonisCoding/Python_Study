from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout
from PySide6.QtCore import Signal, QObject
import sys
import os
import shutil
import threading

class CleanerApp(QWidget):
    class Logger(QObject):
        log_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mac 缓存清理助手")
        layout = QVBoxLayout()
        self.output = QTextEdit()
        layout.addWidget(QLabel("🧹 一键清理 Xcode / 系统 / App 缓存"))
        layout.addWidget(self.output)
        btn_layout = QHBoxLayout()
        btn = QPushButton("🎬 开始清理")
        btn.clicked.connect(self.run_clean)
        btn_layout.addWidget(btn)
        exit_btn = QPushButton("🦅 退出程序")
        exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(exit_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.logger = self.Logger()
        self.logger.log_signal.connect(self.append_log)

    def append_log(self, message):
        self.output.append(message)

    def run_clean(self):
        paths = {
            "Xcode DerivedData": os.path.expanduser('~/Library/Developer/Xcode/DerivedData'),
            "Xcode Archives": os.path.expanduser('~/Library/Developer/Xcode/Archives'),
            "Xcode iOS DeviceSupport": os.path.expanduser('~/Library/Developer/Xcode/iOS DeviceSupport'),
            "CoreSimulator Devices": os.path.expanduser('~/Library/Developer/CoreSimulator/Devices'),
            "系统缓存": os.path.expanduser('~/Library/Caches'),
            "用户日志": os.path.expanduser('~/Library/Logs'),
            "Safari 缓存": os.path.expanduser('~/Library/Caches/com.apple.Safari'),
            "Chrome 缓存": os.path.expanduser('~/Library/Caches/Google/Chrome'),
            "Firefox 缓存": os.path.expanduser('~/Library/Caches/Firefox'),
            "Homebrew 缓存": os.path.expanduser('~/Library/Caches/Homebrew'),
            "临时文件": '/tmp',
            "Android Studio 缓存": os.path.expanduser('~/Library/Caches/AndroidStudio'),
            "Android Studio 配置": os.path.expanduser('~/Library/Application Support/Google/AndroidStudio'),
            "VSCode 缓存": os.path.expanduser('~/Library/Application Support/Code/Cache'),
            "VSCode 用户数据": os.path.expanduser('~/Library/Application Support/Code/User'),
            "IntelliJ IDEA 缓存": os.path.expanduser('~/Library/Caches/IntelliJIdea'),
            "IntelliJ IDEA 配置": os.path.expanduser('~/Library/Application Support/JetBrains/IntelliJIdea2023.1'),
        }

        def clean():
            total_freed = 0
            self.logger.log_signal.emit("开始扫描...")

            for name, path in paths.items():
                if not os.path.exists(path) or not os.listdir(path):
                    continue  # 目录不存在或为空，跳过

                # 只有有文件或子目录时才打印清理信息
                self.logger.log_signal.emit(f"清理: {name} ({path})")

                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if not os.access(item_path, os.W_OK):
                        self.logger.log_signal.emit(f"跳过无权限删除: {item_path}")
                        continue
                    try:
                        if os.path.isdir(item_path):
                            size = self.get_size(item_path)
                            shutil.rmtree(item_path)
                            total_freed += size
                            self.logger.log_signal.emit(f"删除目录: {item_path} ({size / (1024*1024):.2f} MB)")
                        else:
                            size = os.path.getsize(item_path)
                            os.remove(item_path)
                            total_freed += size
                            self.logger.log_signal.emit(f"删除文件: {item_path} ({size / (1024*1024):.2f} MB)")
                    except Exception:
                        continue

            freed_mb = total_freed / (1024 * 1024)
            if freed_mb > 0:
                self.logger.log_signal.emit(f"✅ 清理完成！释放空间约 {freed_mb:.2f} MB")
            else:
                self.logger.log_signal.emit("✅ 清理完成！没有发现可删除的文件或目录")

        self.clean_safari_cache(self.logger.log_signal.emit)
        threading.Thread(target=clean, daemon=True).start()
    def get_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total_size += os.path.getsize(fp)
                except Exception:
                    pass
        return total_size
    def clean_safari_cache(self, log_callback):
        safari_cache = os.path.expanduser("~/Library/Caches/com.apple.Safari")
        if not os.path.exists(safari_cache):
            log_callback("Safari 缓存目录不存在，跳过")
            return

        def delete_cache():
            try:
                for item in os.listdir(safari_cache):
                    path = os.path.join(safari_cache, item)
                    try:
                        if os.path.isfile(path) or os.path.islink(path):
                            os.remove(path)
                            log_callback(f"已删除文件: {path}")
                        elif os.path.isdir(path):
                            shutil.rmtree(path, ignore_errors=True)
                            log_callback(f"已删除目录: {path}")
                    except PermissionError:
                        log_callback(f"⚠️ 无权限删除: {path}, 已跳过")
                    except Exception as e:
                        log_callback(f"⚠️ 删除失败: {path}, 错误: {e}")
                log_callback("✅ Safari 缓存清理完成")
            except Exception as e:
                log_callback(f"⚠️ 清理 Safari 缓存失败: {e}")

        threading.Thread(target=delete_cache, daemon=True).start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CleanerApp()
    w.resize(400, 300)
    w.show()
    sys.exit(app.exec())