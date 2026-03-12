import pygame
import os

# 颜色常量
COLOR_BG, COLOR_TITLE, COLOR_SUB = (245, 245, 247), (29, 29, 31), (134, 134, 139)
COLOR_ACCENT, COLOR_DANGER = (0, 113, 227), (255, 59, 48)

def load_mac_font(size, bold=False):
    paths = ["/System/Library/Fonts/STHeiti Medium.ttc", "/System/Library/Fonts/PingFang.ttc"]
    for p in paths:
        if os.path.exists(p): return pygame.font.Font(p, size)
    return pygame.font.SysFont("Arial Unicode MS", size, bold=bold)

def draw_center_text(screen, text, font, color, y_off, width, height):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(width//2, height//2 + y_off))
    screen.blit(surf, rect)

def get_rot_img(img, direction, grid_size):
    if img is None: return None
    base_angle = -90 
    if direction == [0, -grid_size]: return pygame.transform.rotate(img, base_angle + 90)
    if direction == [0, grid_size]:  return pygame.transform.rotate(img, base_angle - 90)
    if direction == [-grid_size, 0]: return pygame.transform.rotate(img, base_angle + 180)
    return pygame.transform.rotate(img, base_angle)