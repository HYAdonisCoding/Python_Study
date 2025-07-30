from RainBot_RedNote import XHSBot
from RainBot_juejin import JuejinBot
from RainBot_bilibili import BilibiliBot
import threading

def run_bot(bot_cls, name):
    print(f"[{name}] started...")
    bot = bot_cls()
    bot.run()
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