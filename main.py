import pygame
import sys
import random
import os

# 导入你拆分的模块
from modules.ui import *
from modules.engine import *
from modules.snake import Snake

# --- 1. 基础配置与路径初始化 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH, HEIGHT = 800, 800
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇大冒险 - 模块化专业版")
clock = pygame.time.Clock()

# --- 2. 资源加载函数 (适配新的目录结构) ---
def load_asset_img(name):
    # 假设图片都在 assets/images 文件夹下
    path = os.path.join(BASE_DIR, "assets", "images", name)
    if not os.path.exists(path): return None
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE))
    except: return None

# 字体加载
FONT_HUGE = load_mac_font(90, True)
FONT_BIG  = load_mac_font(40)
FONT_STD  = load_mac_font(24)

# 皮肤配置 (路径已指向 assets/images)
SKINS = [
    {"name": "方块小狗", "head": "head1.png", "body": "body1.png", "color": (0, 0, 0)},
    {"name": "松鼠小屎羊", "head": "head2.png", "body": "body2.png", "color": (0, 0, 0)},
    {"name": "邪恶牛爷爷", "head": "head3.png", "body": "body3.png", "color": (0, 0, 0)},
    {"name": "奶婷哈哈", "head": "head4.png", "body": "body4.png", "color": (0, 0, 0)},
    {"name": "六小蛋", "head": "head5.png", "body": "body5.png", "color": (0, 0, 0)}
]

# 全局状态
p1_skin_idx = 0
p2_skin_idx = 1

# 加载通用素材
food_img = load_asset_img("food.png")
super_img = load_asset_img("superfood.png")
eat_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "eat.wav")) if os.path.exists("assets/sounds/eat.wav") else None

# --- 3. 皮肤选择逻辑 (保持不变但调用 ui 模块) ---
def pick_skin_ui(title_text):
    current_pick = 0
    while True:
        screen.fill(COLOR_BG)
        draw_center_text(screen, title_text, FONT_BIG, COLOR_TITLE, -150, WIDTH, HEIGHT)
        skin = SKINS[current_pick]
        draw_center_text(screen, f"当前选择：{skin['name']}", FONT_BIG, skin['color'], -50, WIDTH, HEIGHT)
        
        # 预览
        preview_img = load_asset_img(skin['head'])
        if preview_img:
            img = pygame.transform.scale(preview_img, (100, 100))
            screen.blit(img, img.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
        
        draw_center_text(screen, "左右键切换 | 回车确认", FONT_STD, COLOR_SUB, 180, WIDTH, HEIGHT)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]: current_pick = (current_pick - 1) % len(SKINS)
                if event.key in [pygame.K_RIGHT, pygame.K_d]: current_pick = (current_pick + 1) % len(SKINS)
                if event.key == pygame.K_RETURN: return current_pick
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

# --- 4. 核心游戏循环 (使用 Snake 类重构) ---
def game_loop(mode):
    high = get_high()
    
    # 核心：实例化 Snake 对象
    # 注意：这里传入的是 skin 的配置，Snake 类内部会去加载图片
    # 为了让 Snake 类能找到图片，我们需要传完整路径给它
    p1_cfg = SKINS[p1_skin_idx].copy()
    p1_cfg['head'] = os.path.join("assets", "images", p1_cfg['head'])
    p1_cfg['body'] = os.path.join("assets", "images", p1_cfg['body'])
    p1 = Snake([200, 400], [GRID_SIZE, 0], p1_cfg, GRID_SIZE)
    
    p2 = None
    if mode == 1:
        p2_cfg = SKINS[p2_skin_idx].copy()
        p2_cfg['head'] = os.path.join("assets", "images", p2_cfg['head'])
        p2_cfg['body'] = os.path.join("assets", "images", p2_cfg['body'])
        p2 = Snake([600, 400], [-GRID_SIZE, 0], p2_cfg, GRID_SIZE)

    foods = [[random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE)] for _ in range(5 if mode==1 else 1)]
    running = True
    
    while running:
        current_fps = 10 + (p1.score // 3)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                # P1 控制
                if event.key == pygame.K_w: p1.change_direction([0, -GRID_SIZE])
                if event.key == pygame.K_s: p1.change_direction([0, GRID_SIZE])
                if event.key == pygame.K_a: p1.change_direction([-GRID_SIZE, 0])
                if event.key == pygame.K_d: p1.change_direction([GRID_SIZE, 0])
                # P2 控制
                if mode == 1:
                    if event.key == pygame.K_UP:    p2.change_direction([0, -GRID_SIZE])
                    if event.key == pygame.K_DOWN:  p2.change_direction([0, GRID_SIZE])
                    if event.key == pygame.K_LEFT:  p2.change_direction([-GRID_SIZE, 0])
                    if event.key == pygame.K_RIGHT: p2.change_direction([GRID_SIZE, 0])

        # 移动逻辑
        for s in ([p1, p2] if mode == 1 else [p1]):
            ate = False
            for i, f in enumerate(foods):
                if s.body[0] == f:
                    s.score += 1
                    ate = True
                    foods[i] = [random.randrange(0, WIDTH, GRID_SIZE), random.randrange(0, HEIGHT, GRID_SIZE)]
                    if eat_sound: eat_sound.play()
            s.move(ate)

        # 碰撞检测
        if p1.check_collision(WIDTH, HEIGHT, p2.body if p2 else None): running = False
        if mode == 1 and p2.check_collision(WIDTH, HEIGHT, p1.body): running = False

        # 绘制
        screen.fill(COLOR_BG)
        for f in foods:
            if food_img: screen.blit(food_img, f)
            else: pygame.draw.rect(screen, COLOR_DANGER, (f[0], f[1], GRID_SIZE, GRID_SIZE))
        
        p1.draw(screen)
        if mode == 1: p2.draw(screen)
        
        # HUD
        hud = f"P1: {p1.score}" + (f" | P2: {p2.score}" if mode==1 else f" | High: {high}")
        screen.blit(FONT_STD.render(hud, True, COLOR_TITLE), (20, 20))
        
        pygame.display.flip()
        clock.tick(current_fps)

    if p1.score > high: save_high(p1.score)

def main():
    while True:
        screen.fill(COLOR_BG)
        draw_center_text(screen, "贪吃蛇大冒险", FONT_HUGE, COLOR_TITLE, -150, WIDTH, HEIGHT)
        
        # 简单菜单逻辑... (此处省略，建议根据上面的 pick_skin_ui 逻辑自行填充)
        game_loop(0) # 暂时直接进入单人模式测试

if __name__ == "__main__":
    main()