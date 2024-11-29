# -*- coding: utf-8 -*-

# letter = 'qe,q,SOS,o,p6,a,s,d,燕云,鹿明,小鹿,辛勤'
# size = 50
# color = 'yellow'
# speed(10, 200)
# rain()
# website('Cavin的代码雨')
# https://kp101.cn/b2c-python-h5/page/code-rain?share_btn=1&share_guide=1&type=share&content=8680877-1732712030066-code-rain.json

import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置窗口大小和标题
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("代码雨 - 界面调速和控制")

# 定义字体和颜色
FONT_SIZE = 20
FONT = pygame.font.Font(None, FONT_SIZE)
BUTTON_FONT = pygame.font.Font(None, 36)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 定义字符集
CHARS = "qe,q,SOS,o,p6,a,s,d,燕云,鹿明,小鹿,辛勤".split(",")

# 创建列数和每列的掉落位置
columns = WIDTH // FONT_SIZE
drops = [random.randint(-20, 0) for _ in range(columns)]

# 默认速度（通过滑块调整）
speed = 30  # 初始速度（帧率控制）

# 滑块设置
slider_x = 50  # 滑块轨道起点X坐标
slider_y = HEIGHT - 50  # 滑块轨道Y坐标
slider_width = 700  # 滑块轨道长度
slider_height = 10  # 滑块轨道高度
knob_radius = 10  # 滑块的圆形拖动按钮半径
knob_x = slider_x + int((speed / 100) * slider_width)  # 滑块初始位置（根据默认速度计算）
dragging = False  # 拖动状态

# 开始/暂停按钮设置
button_width, button_height = 150, 50
button_x = (WIDTH - button_width) // 2  # 按钮居中
button_y = HEIGHT - 120
is_paused = False  # 初始为运行状态

# 刷新速度控制
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    screen.fill(BLACK)  # 清屏

    # 绘制代码雨（如果未暂停）
    if not is_paused:
        for i in range(columns):
            char = random.choice(CHARS)
            char_surface = FONT.render(char, True, YELLOW)

            x = i * FONT_SIZE
            y = drops[i] * FONT_SIZE
            screen.blit(char_surface, (x, y))

            if random.random() > 0.95:
                drops[i] = 0
            else:
                drops[i] += 1

    # 绘制滑块轨道
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height))
    # 绘制滑块按钮
    pygame.draw.circle(screen, WHITE, (int(knob_x), slider_y + slider_height // 2), knob_radius)

    # 显示速度数值
    speed_text = FONT.render(f"Speed: {speed}", True, WHITE)
    screen.blit(speed_text, (slider_x, slider_y - 30))

    # 绘制按钮
    button_color = GREEN if is_paused else RED
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
    button_text = BUTTON_FONT.render("Start" if is_paused else "Pause", True, WHITE)
    text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(button_text, text_rect)

    # 根据滑块位置调整速度
    speed = max(1, int((knob_x - slider_x) / slider_width * 100))  # 速度范围：1-100

    # 更新屏幕
    pygame.display.flip()
    clock.tick(speed)  # 根据速度控制帧率

    # 事件监听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 鼠标按下事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # 判断是否点击了滑块按钮
            if (slider_y <= mouse_y <= slider_y + slider_height and
                    knob_x - knob_radius <= mouse_x <= knob_x + knob_radius):
                dragging = True
            # 判断是否点击了按钮
            if (button_x <= mouse_x <= button_x + button_width and
                    button_y <= mouse_y <= button_y + button_height):
                is_paused = not is_paused  # 切换开始/暂停状态

        # 鼠标松开事件
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # 鼠标移动事件
        if event.type == pygame.MOUSEMOTION and dragging:
            knob_x = max(slider_x, min(slider_x + slider_width, event.pos[0]))

pygame.quit()