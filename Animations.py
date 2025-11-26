import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Underwater Scene")

clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
OCEAN_BLUE = (10, 50, 100)
LIGHT_BLUE = (30, 100, 150)
SAND_COLOR = (194, 178, 128)
CORAL_PINK = (255, 127, 80)
CORAL_PURPLE = (138, 43, 226)
FISH_ORANGE = (255, 140, 0)
FISH_YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
SEAWEED_GREEN = (34, 139, 34)

def create_sand_texture(width, height):
    """Create a sandy ocean floor texture"""
    surface = pygame.Surface((width, height))
    base_color = SAND_COLOR
    
    for y in range(height):
        for x in range(width):
            variation = random.randint(-15, 15)
            color = (
                max(0, min(255, base_color[0] + variation)),
                max(0, min(255, base_color[1] + variation)),
                max(0, min(255, base_color[2] + variation))
            )
            surface.set_at((x, y), color)
    
    # Add some darker spots for depth
    for _ in range(50):
        spot_x = random.randint(0, width)
        spot_y = random.randint(0, height)
        spot_size = random.randint(2, 5)
        pygame.draw.circle(surface, (150, 130, 90), (spot_x, spot_y), spot_size)
    
    return surface

def create_coral_texture(width, height, base_color):
    """Create a textured coral surface"""
    surface = pygame.Surface((width, height))
    surface.set_colorkey(BLACK)
    
    for y in range(height):
        for x in range(width):
            # Create bumpy texture
            noise = int(20 * math.sin(x * 0.3) * math.cos(y * 0.3))
            color = (
                max(0, min(255, base_color[0] + noise)),
                max(0, min(255, base_color[1] + noise)),
                max(0, min(255, base_color[2] + noise))
            )
            surface.set_at((x, y), color)
    
    return surface

def create_fish_texture(width, height):
    """Create a fish with scale texture"""
    surface = pygame.Surface((width, height))
    surface.set_colorkey(BLACK)
    surface.fill(BLACK)
    
    # Draw fish body
    pygame.draw.ellipse(surface, FISH_ORANGE, (5, height//4, width-10, height//2))
    
    # Draw scales
    for row in range(3):
        for col in range(5):
            x = 10 + col * 12
            y = height//4 + 5 + row * 10
            shade = random.randint(200, 255)
            pygame.draw.circle(surface, (shade, 120, 0), (x, y), 4, 1)
    
    # Draw tail
    points = [(width-10, height//2), (width, height//4), (width, 3*height//4)]
    pygame.draw.polygon(surface, FISH_YELLOW, points)
    
    # Draw eye
    pygame.draw.circle(surface, WHITE, (15, height//3), 4)
    pygame.draw.circle(surface, BLACK, (15, height//3), 2)
    
    return surface

# Create textures
sand_texture = create_sand_texture(WIDTH, 80)
coral1_texture = create_coral_texture(60, 80, CORAL_PINK)
coral2_texture = create_coral_texture(50, 70, CORAL_PURPLE)
fish_texture = create_fish_texture(60, 30)

# Animation parameters
start_time = pygame.time.get_ticks()
ANIMATION_DURATION = 20000  # 20 seconds

# Fish parameters
fish_x = -70
fish_y = HEIGHT // 3

# Bubble parameters
bubbles = []
for _ in range(15):
    bubbles.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(HEIGHT//2, HEIGHT),
        'speed': random.uniform(0.5, 2.0),
        'size': random.randint(2, 6),
        'wobble': random.uniform(0, 2 * math.pi)
    })

# Seaweed parameters
seaweed_positions = [100, 250, 400, 550, 700]

running = True
while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    
    # Check if animation is complete
    if elapsed_time > ANIMATION_DURATION:
        pygame.time.wait(1000)
        running = False
    
    # Normalized time (0 to 1)
    time_normalized = elapsed_time / ANIMATION_DURATION
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Create gradient ocean background
    for y in range(HEIGHT):
        color_factor = y / HEIGHT
        color = (
            int(OCEAN_BLUE[0] + (LIGHT_BLUE[0] - OCEAN_BLUE[0]) * color_factor),
            int(OCEAN_BLUE[1] + (LIGHT_BLUE[1] - OCEAN_BLUE[1]) * color_factor),
            int(OCEAN_BLUE[2] + (LIGHT_BLUE[2] - OCEAN_BLUE[2]) * color_factor)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))
    
    # Draw sandy ocean floor
    screen.blit(sand_texture, (0, HEIGHT - 80))
    
    # Draw coral formations (textured)
    screen.blit(coral1_texture, (150, HEIGHT - 150))
    screen.blit(coral2_texture, (300, HEIGHT - 140))
    screen.blit(coral1_texture, (500, HEIGHT - 160))
    screen.blit(coral2_texture, (650, HEIGHT - 145))
    
    # Draw swaying seaweed
    for pos in seaweed_positions:
        sway = math.sin(time_normalized * 6 + pos * 0.01) * 15
        for i in range(5):
            segment_y = HEIGHT - 80 - i * 15
            segment_x = pos + sway * (i / 5)
            thickness = 8 - i
            pygame.draw.circle(screen, SEAWEED_GREEN, (int(segment_x), segment_y), thickness)
    
    # Animate fish swimming across screen
    fish_x = -70 + (WIDTH + 140) * time_normalized
    fish_wave = math.sin(time_normalized * 10) * 30
    fish_y = HEIGHT // 3 + fish_wave
    
    screen.blit(fish_texture, (int(fish_x), int(fish_y)))
    
    # Animate bubbles rising
    for bubble in bubbles:
        bubble['y'] -= bubble['speed']
        bubble['x'] += math.sin(bubble['wobble'] + elapsed_time * 0.003) * 0.5
        bubble['wobble'] += 0.02
        
        # Reset bubble when it reaches top
        if bubble['y'] < 0:
            bubble['y'] = HEIGHT
            bubble['x'] = random.randint(0, WIDTH)
        
        # Draw bubble with transparency effect
        pygame.draw.circle(screen, LIGHT_BLUE, (int(bubble['x']), int(bubble['y'])), bubble['size'], 1)
        pygame.draw.circle(screen, WHITE, (int(bubble['x'] - 1), int(bubble['y'] - 1)), bubble['size'] // 3)
    
    # Draw timer
    font = pygame.font.Font(None, 36)
    time_left = (ANIMATION_DURATION - elapsed_time) / 1000
    timer_text = font.render(f"Time: {time_left:.1f}s", True, WHITE)
    screen.blit(timer_text, (10, 10))
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()