import pygame
import random

# 初始化 Pygame
pygame.init()

# 屏幕大小
screen_width = 300
screen_height = 600
block_size = 30

# 颜色定义
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (0, 255, 255)
]

# 形状定义
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# 游戏网格
grid = [[0 for _ in range(screen_width // block_size)] for _ in range(screen_height // block_size)]

# 形状类
class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(shapes)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# 绘制网格
def draw_grid(surface):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, colors[grid[y][x]], (x * block_size, y * block_size, block_size, block_size), 0)

# 检查碰撞
def check_collision(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape.shape):
        for x, cell in enumerate(row):
            if cell:
                try:
                    if grid[y + shape.y + off_y][x + shape.x + off_x] or x + shape.x + off_x < 0 or x + shape.x + off_x >= screen_width // block_size:
                        return True
                except IndexError:
                    return True
    return False

# 锁定形状
def lock_shape(shape):
    for y, row in enumerate(shape.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + shape.y][x + shape.x] = shape.color

# 清除行
def clear_rows():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < screen_height // block_size:
        grid.insert(0, [0 for _ in range(screen_width // block_size)])

# 主游戏循环
def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    current_shape = Shape(3, 0)
    fall_time = 0
    fall_speed = 0.3

    running = True
    while running:
        screen.fill((0, 0, 0))
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 2000 >= fall_speed:
            fall_time = 0
            current_shape.y += 1
            if check_collision(current_shape, (0, 0)):
                current_shape.y -= 1
                lock_shape(current_shape)
                clear_rows()
                current_shape = Shape(3, 0)
                if check_collision(current_shape, (0, 0)):
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_shape.x -= 1
                    if check_collision(current_shape, (0, 0)):
                        current_shape.x += 1
                if event.key == pygame.K_RIGHT:
                    current_shape.x += 1
                    if check_collision(current_shape, (0, 0)):
                        current_shape.x -= 1
                if event.key == pygame.K_DOWN:
                    current_shape.y += 1
                    if check_collision(current_shape, (0, 0)):
                        current_shape.y -= 1
                if event.key == pygame.K_UP:
                    current_shape.rotate()
                    if check_collision(current_shape, (0, 0)):
                        for _ in range(3):  # 旋转回去
                            current_shape.rotate()

        draw_grid(screen)
        for y, row in enumerate(current_shape.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, colors[current_shape.color],
                                     ((current_shape.x + x) * block_size, (current_shape.y + y) * block_size, block_size, block_size), 0)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()



