import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyberpunk City Night")

clock = pygame.time.Clock()
FPS = 120

# Colors
NIGHT_SKY = (10, 5, 30)
NEON_PINK = (255, 20, 147)
NEON_CYAN = (0, 255, 255)
NEON_PURPLE = (186, 85, 211)
NEON_ORANGE = (255, 165, 0)
BUILDING_DARK = (20, 20, 40)
WINDOW_YELLOW = (255, 255, 150)
WINDOW_CYAN = (100, 200, 255)
RAIN_BLUE = (150, 180, 220)

def create_building_texture(width, height, window_color):
    """Create a textured building with windows"""
    surface = pygame.Surface((width, height))
    
    # Building base - create concrete texture
    for y in range(height):
        for x in range(width):
            noise = random.randint(-10, 10)
            gray = 30 + noise
            surface.set_at((x, y), (gray, gray, gray + 10))
    
    # Add windows in a grid pattern
    window_width = 8
    window_height = 10
    spacing_x = 15
    spacing_y = 15
    
    for row in range(5, height - 10, spacing_y):
        for col in range(5, width - 10, spacing_x):
            # Randomly light up windows
            if random.random() > 0.3:
                brightness = random.choice([0.3, 0.6, 1.0])
                win_color = (
                    int(window_color[0] * brightness),
                    int(window_color[1] * brightness),
                    int(window_color[2] * brightness)
                )
                pygame.draw.rect(surface, win_color, 
                               (col, row, window_width, window_height))
                # Add glow effect
                glow_color = (
                    int(window_color[0] * brightness * 0.5),
                    int(window_color[1] * brightness * 0.5),
                    int(window_color[2] * brightness * 0.5)
                )
                pygame.draw.rect(surface, glow_color, 
                               (col - 1, row - 1, window_width + 2, window_height + 2), 1)
    
    return surface

def create_neon_sign_texture(width, height, text, color):
    """Create a glowing neon sign texture"""
    surface = pygame.Surface((width, height))
    surface.set_colorkey((0, 0, 0))
    surface.fill((0, 0, 0))
    
    # Create glow effect
    font = pygame.font.Font(None, 40)
    
    # Outer glow layers
    for offset in range(8, 0, -2):
        glow_alpha = 50 - offset * 5
        glow_color = (
            color[0] // 2,
            color[1] // 2,
            color[2] // 2
        )
        text_surface = font.render(text, True, glow_color)
        surface.blit(text_surface, (offset, height//2 - 10))
        surface.blit(text_surface, (-offset, height//2 - 10))
        surface.blit(text_surface, (0, height//2 - 10 + offset))
        surface.blit(text_surface, (0, height//2 - 10 - offset))
    
    # Main text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (0, height//2 - 10))
    
    return surface

def create_road_texture(width, height):
    """Create a wet asphalt road texture"""
    surface = pygame.Surface((width, height))
    
    # Base asphalt color with variation
    for y in range(height):
        for x in range(width):
            noise = random.randint(-15, 15)
            gray = 40 + noise
            # Add slight blue tint for wetness
            surface.set_at((x, y), (gray, gray, gray + 20))
    
    # Add road markings
    line_y = height // 2
    for x in range(0, width, 40):
        pygame.draw.rect(surface, (255, 255, 255), (x, line_y - 2, 20, 4))
    
    # Add puddle reflections (darker spots)
    for _ in range(20):
        puddle_x = random.randint(0, width)
        puddle_y = random.randint(0, height)
        puddle_size = random.randint(10, 30)
        for i in range(puddle_size, 0, -3):
            alpha = 50 + i
            pygame.draw.ellipse(surface, (20, 20, 50), 
                              (puddle_x - i, puddle_y - i//2, i*2, i))
    
    return surface

# Create textures
buildings = []
building_data = [
    (50, 150, 250, WINDOW_YELLOW),
    (180, 150, 300, WINDOW_CYAN),
    (320, 150, 200, WINDOW_YELLOW),
    (480, 150, 280, WINDOW_CYAN),
    (620, 150, 220, WINDOW_YELLOW),
    (770, 150, 180, WINDOW_CYAN),
]

for x, width, height, color in building_data:
    buildings.append({
        'x': x,
        'y': HEIGHT - height - 150,
        'texture': create_building_texture(width, height, color),
        'height': height
    })

# Create neon signs
neon_signs = [
    create_neon_sign_texture(150, 60, "CYBER", NEON_PINK),
    create_neon_sign_texture(150, 60, "TECH", NEON_CYAN),
    create_neon_sign_texture(150, 60, "NEON", NEON_PURPLE),
]

# Create road texture
road_texture = create_road_texture(WIDTH, 150)

# Rain drops
rain_drops = []
for _ in range(150):
    rain_drops.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'speed': random.uniform(8, 15),
        'length': random.randint(10, 20)
    })

# Flying car
car = {
    'x': -100,
    'y': HEIGHT // 6,
    'speed': 3
}

# Floating particles/sparks
particles = []
for _ in range(50):
    particles.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT // 2),
        'speed': random.uniform(0.2, 0.8),
        'size': random.randint(1, 3),
        'color': random.choice([NEON_PINK, NEON_CYAN, NEON_PURPLE, NEON_ORANGE]),
        'pulse': random.uniform(0, math.pi * 2)
    })

start_time = pygame.time.get_ticks()
ANIMATION_DURATION = 20000

running = True
while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    
    if elapsed_time > ANIMATION_DURATION:
        pygame.time.wait(1000)
        running = False
    
    time_normalized = elapsed_time / ANIMATION_DURATION
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Draw night sky with stars
    screen.fill(NIGHT_SKY)
    
    # Draw twinkling stars
    for _ in range(30):
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT // 2)
        star_brightness = int(150 + 105 * math.sin(elapsed_time * 0.005 + star_x))
        pygame.draw.circle(screen, (star_brightness, star_brightness, star_brightness), 
                         (star_x, star_y), 1)
    
    # Draw floating particles
    for particle in particles:
        particle['y'] += particle['speed']
        if particle['y'] > HEIGHT // 2:
            particle['y'] = 0
            particle['x'] = random.randint(0, WIDTH)
        
        particle['pulse'] += 0.1
        alpha_factor = (math.sin(particle['pulse']) + 1) / 2
        color = tuple(int(c * alpha_factor) for c in particle['color'])
        pygame.draw.circle(screen, color, 
                         (int(particle['x']), int(particle['y'])), particle['size'])
    
    # Draw buildings with textures
    for building in buildings:
        screen.blit(building['texture'], (building['x'], building['y']))
        
        # Add building edge highlights
        pygame.draw.line(screen, NEON_CYAN, 
                        (building['x'], building['y']),
                        (building['x'], building['y'] + building['height']), 2)
    
    # Draw neon signs on buildings
    sign_positions = [(100, 250), (300, 200), (550, 280)]
    for i, (sx, sy) in enumerate(sign_positions):
        # Flickering effect
        if random.random() > 0.05:
            flicker = math.sin(elapsed_time * 0.01 + i) * 0.2 + 0.8
            sign_surface = neon_signs[i].copy()
            sign_surface.set_alpha(int(255 * flicker))
            screen.blit(sign_surface, (sx, sy))
    
    # Draw flying car
    car['x'] += car['speed']
    if car['x'] > WIDTH + 100:
        car['x'] = -100
        car['y'] = random.randint(150, 350)
    
    car_y_wave = car['y'] + math.sin(elapsed_time * 0.003) * 10
    
    # Car body
    pygame.draw.rect(screen, (80, 80, 100), 
                    (int(car['x']), int(car_y_wave), 60, 20))
    # Car windows
    pygame.draw.rect(screen, NEON_CYAN, 
                    (int(car['x']) + 5, int(car_y_wave) + 5, 50, 10))
    # Glow underneath
    for i in range(3):
        glow_alpha = 100 - i * 30
        pygame.draw.line(screen, NEON_CYAN, 
                        (int(car['x']), int(car_y_wave) + 20 + i),
                        (int(car['x']) + 60, int(car_y_wave) + 20 + i), 1)
    
    # Draw road with texture
    screen.blit(road_texture, (0, HEIGHT - 150))
    
    # Draw rain
    for drop in rain_drops:
        drop['y'] += drop['speed']
        if drop['y'] > HEIGHT:
            drop['y'] = 0
            drop['x'] = random.randint(0, WIDTH)
        
        # Rain streak
        pygame.draw.line(screen, RAIN_BLUE,
                        (int(drop['x']), int(drop['y'])),
                        (int(drop['x'] - 2), int(drop['y'] - drop['length'])), 1)
    
    # Add reflection glow on road
    reflection_y = HEIGHT - 100
    for building in buildings:
        glow_x = building['x'] + building['texture'].get_width() // 2
        for i in range(5):
            alpha = 30 - i * 5
            color = (NEON_CYAN[0] // 4, NEON_CYAN[1] // 4, NEON_CYAN[2] // 4)
            pygame.draw.circle(screen, color,
                             (glow_x, reflection_y + i * 10), 30 - i * 5)
    
    # Draw timer with neon effect
    font = pygame.font.Font(None, 48)
    time_left = (ANIMATION_DURATION - elapsed_time) / 1000
    
    # Glow effect for timer
    for offset in range(4, 0, -1):
        glow_color = (NEON_PINK[0] // 2, NEON_PINK[1] // 2, NEON_PINK[2] // 2)
        timer_text = font.render(f"{time_left:.1f}s", True, glow_color)
        screen.blit(timer_text, (WIDTH - 140 + offset, 20))
        screen.blit(timer_text, (WIDTH - 140 - offset, 20))
    
    timer_text = font.render(f"{time_left:.1f}s", True, NEON_PINK)
    screen.blit(timer_text, (WIDTH - 140, 20))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()