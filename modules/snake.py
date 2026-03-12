import pygame
from .ui import get_rot_img  # 假设 ui.py 在同级目录

class Snake:
    def __init__(self, start_pos, start_dir, skin_config, grid_size):
        self.body = [start_pos, [start_pos[0] - start_dir[0], start_pos[1]]]
        self.direction = start_dir
        self.grid_size = grid_size
        self.score = 0
        
        # 加载皮肤（从 SKINS 字典中获取文件名）
        self.head_img = self._load_img(skin_config['head'])
        self.body_img = self._load_img(skin_config['body'])
        
    def _load_img(self, path):
        import os
        if not os.path.exists(path): return None
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (self.grid_size, self.grid_size))

    def move(self, ate_food=False):
        # 计算新头部坐标
        new_head = [self.body[0][0] + self.direction[0], 
                    self.body[0][1] + self.direction[1]]
        self.body.insert(0, new_head)
        if not ate_food:
            self.body.pop()

    def change_direction(self, new_dir):
        # 防止 180 度直接掉头（例如向上时不能直接按向下）
        if (new_dir[0] * -1 != self.direction[0]) or (new_dir[1] * -1 != self.direction[1]):
            self.direction = new_dir

    def check_collision(self, width, height, other_snake_body=None):
        head = self.body[0]
        # 撞墙
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
        # 撞自己
        if head in self.body[1:]:
            return True
        # 撞对手（双人模式）
        if other_snake_body and head in other_snake_body:
            return True
        return False

    def draw(self, screen):
        for i, seg in enumerate(self.body):
            img = self.head_img if i == 0 else self.body_img
            # 确定旋转方向：头部用当前方向，身体用与前一节的相对方向
            if i == 0:
                rot_dir = self.direction
            else:
                rot_dir = [self.body[i-1][0] - seg[0], self.body[i-1][1] - seg[1]]
            
            rot_img = get_rot_img(img, rot_dir, self.grid_size)
            if rot_img:
                screen.blit(rot_img, (seg[0], seg[1]))