import os
from RainBot_RedNote import XHSBot
from RainBot_juejin import JuejinBot
from RainBot_bilibili import BilibiliBot
import threading


def run_bot(bot_cls, name):
    print(f"[{name}] started...")

    bot = None
    try:
        bot = bot_cls()
        bot.run()
    except KeyboardInterrupt:
        print(f"[{name}] 收到中断信号，正在退出...")
    except Exception as e:
        print(f"[{name}] 程序发生异常: {e}")

    finally:
        if bot and bot.comment_db:
            try:
                bot.comment_db.close()
                print(f"[{name}] comment_db 连接已关闭")
            except Exception as e:
                print(f"[{name}] 关闭 comment_db 失败: {e}")
        print(f"[{name}] ended...")


if __name__ == "__main__":
    threads = [
        threading.Thread(target=run_bot, args=(JuejinBot, "JuejinBot")),
        threading.Thread(target=run_bot, args=(XHSBot, "XHSBot")),
        # threading.Thread(target=run_bot, args=(BilibiliBot, "BilibiliBot")),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("所有任务完成，准备关机...")
    # os.system("sudo shutdown -h now")
