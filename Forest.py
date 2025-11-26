import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Scene")

clock = pygame.time.Clock()
FPS = 400

# Colors
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BROWN = (101, 67, 33)
DARK_BROWN = (70, 40, 20)
LEAF_GREEN = (50, 205, 50)
FLOWER_PINK = (255, 182, 193)
FLOWER_YELLOW = (255, 255, 0)
BUTTERFLY_ORANGE = (255, 140, 0)
BUTTERFLY_BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def create_bark_texture(width, height):
    """Create a realistic tree bark texture"""
    surface = pygame.Surface((width, height))
    
    # Base brown color
    for y in range(height):
        for x in range(width):
            variation = random.randint(-20, 20)
            color = (
                max(0, min(255, BROWN[0] + variation)),
                max(0, min(255, BROWN[1] + variation)),
                max(0, min(255, BROWN[2] + variation))
            )
            surface.set_at((x, y), color)
    
    # Add vertical bark lines
    for x in range(0, width, 8):
        offset = random.randint(-3, 3)
        for y in range(0, height, 3):
            line_x = x + offset + int(math.sin(y * 0.1) * 2)
            if 0 <= line_x < width:
                pygame.draw.circle(surface, DARK_BROWN, (line_x, y), 1)
    
    # Add knots and texture
    for _ in range(8):
        knot_x = random.randint(5, width - 5)
        knot_y = random.randint(5, height - 5)
        knot_size = random.randint(3, 8)
        pygame.draw.circle(surface, DARK_BROWN, (knot_x, knot_y), knot_size, 2)
    
    return surface

def create_grass_texture(width, height):
    """Create textured grass ground"""
    surface = pygame.Surface((width, height))
    
    # Base grass color with variation
    for y in range(height):
        for x in range(width):
            variation = random.randint(-15, 15)
            color = (
                max(0, min(255, GRASS_GREEN[0] + variation)),
                max(0, min(255, GRASS_GREEN[1] + variation)),
                max(0, min(255, GRASS_GREEN[2] + variation))
            )
            surface.set_at((x, y), color)
    
    # Add grass blades
    for _ in range(200):
        blade_x = random.randint(0, width)
        blade_y = random.randint(0, height)
        blade_height = random.randint(3, 8)
        pygame.draw.line(surface, DARK_GREEN, (blade_x, blade_y), 
                        (blade_x + random.randint(-2, 2), blade_y - blade_height), 1)
    
    return surface

def draw_butterfly(surface, x, y, time, scale=1.0):
    """Draw an animated butterfly"""
    wing_flap = abs(math.sin(time * 10)) * 15
    
    # Left wing
    left_wing = [
        (x - 15 * scale, y),
        (x - 25 * scale - wing_flap * scale, y - 15 * scale),
        (x - 20 * scale - wing_flap * scale, y + 10 * scale),
    ]
    pygame.draw.polygon(surface, BUTTERFLY_ORANGE, left_wing)
    pygame.draw.polygon(surface, BUTTERFLY_BLACK, left_wing, 2)
    
    # Right wing
    right_wing = [
        (x + 15 * scale, y),
        (x + 25 * scale + wing_flap * scale, y - 15 * scale),
        (x + 20 * scale + wing_flap * scale, y + 10 * scale),
    ]
    pygame.draw.polygon(surface, BUTTERFLY_ORANGE, right_wing)
    pygame.draw.polygon(surface, BUTTERFLY_BLACK, right_wing, 2)
    
    # Body
    pygame.draw.ellipse(surface, BUTTERFLY_BLACK, 
                       (x - 3 * scale, y - 10 * scale, 6 * scale, 20 * scale))
    
    # Antennae
    pygame.draw.line(surface, BUTTERFLY_BLACK, 
                    (x - 2 * scale, y - 10 * scale), 
                    (x - 5 * scale, y - 18 * scale), 1)
    pygame.draw.line(surface, BUTTERFLY_BLACK, 
                    (x + 2 * scale, y - 10 * scale), 
                    (x + 5 * scale, y - 18 * scale), 1)

def draw_flower(surface, x, y, color):
    """Draw a simple flower"""
    # Stem
    pygame.draw.line(surface, DARK_GREEN, (x, y), (x, y + 30), 3)
    
    # Petals
    for angle in range(0, 360, 72):
        rad = math.radians(angle)
        petal_x = x + math.cos(rad) * 8
        petal_y = y + math.sin(rad) * 8
        pygame.draw.circle(surface, color, (int(petal_x), int(petal_y)), 5)
    
    # Center
    pygame.draw.circle(surface, FLOWER_YELLOW, (x, y), 4)

# Create textures
tree_bark = create_bark_texture(80, 200)
grass_texture = create_grass_texture(WIDTH, 120)

# Animation parameters
start_time = pygame.time.get_ticks()
ANIMATION_DURATION = 20000  # 20 seconds

# Butterfly flight path
butterfly_path_radius = 150

# Falling leaves
leaves = []
for _ in range(20):
    leaves.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(-HEIGHT, 0),
        'speed': random.uniform(0.5, 1.5),
        'rotation': random.uniform(0, 360),
        'rotation_speed': random.uniform(-5, 5),
        'size': random.randint(4, 8)
    })

# Flowers
flowers = []
for _ in range(15):
    flowers.append({
        'x': random.randint(50, WIDTH - 50),
        'y': HEIGHT - 100 + random.randint(-10, 10),
        'color': random.choice([FLOWER_PINK, FLOWER_YELLOW, (255, 100, 180)]),
        'growth': 0
    })

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
    
    # Draw sky
    screen.fill(SKY_BLUE)
    
    # Draw textured grass ground
    screen.blit(grass_texture, (0, HEIGHT - 120))
    
    # Draw tree with textured bark
    tree_x = WIDTH // 4
    tree_y = HEIGHT - 320
    screen.blit(tree_bark, (tree_x, tree_y))
    
    # Draw tree crown
    for i in range(3):
        crown_y = tree_y - 30 - i * 40
        crown_size = 100 + i * 20
        # Add swaying effect
        sway = math.sin(time_normalized * 4 + i) * 5
        pygame.draw.circle(screen, LEAF_GREEN, 
                         (int(tree_x + 40 + sway), int(crown_y)), crown_size)
        pygame.draw.circle(screen, DARK_GREEN, 
                         (int(tree_x + 40 + sway), int(crown_y)), crown_size, 2)
    
    # Animate butterfly flying in a path
    butterfly_center_x = WIDTH // 2
    butterfly_center_y = HEIGHT // 3
    butterfly_x = butterfly_center_x + math.cos(time_normalized * 2 * math.pi * 2) * butterfly_path_radius
    butterfly_y = butterfly_center_y + math.sin(time_normalized * 2 * math.pi * 2) * butterfly_path_radius * 0.6
    
    draw_butterfly(screen, int(butterfly_x), int(butterfly_y), time_normalized)
    
    # Animate falling leaves
    for leaf in leaves:
        leaf['y'] += leaf['speed']
        leaf['x'] += math.sin(leaf['y'] * 0.01) * 0.5
        leaf['rotation'] += leaf['rotation_speed']
        
        # Reset leaf when it falls off screen
        if leaf['y'] > HEIGHT:
            leaf['y'] = -20
            leaf['x'] = random.randint(0, WIDTH)
        
        # Draw leaf
        leaf_points = []
        for angle in range(0, 360, 90):
            rad = math.radians(angle + leaf['rotation'])
            px = leaf['x'] + math.cos(rad) * leaf['size']
            py = leaf['y'] + math.sin(rad) * leaf['size'] * 0.6
            leaf_points.append((int(px), int(py)))
        
        pygame.draw.polygon(screen, (255, 200, 0), leaf_points)
        pygame.draw.polygon(screen, (200, 150, 0), leaf_points, 1)
    
    # Animate flowers growing
    for flower in flowers:
        if flower['growth'] < 1.0:
            flower['growth'] = min(1.0, flower['growth'] + 0.008)
        
        if flower['growth'] > 0:
            scale_y = flower['growth']
            scaled_y = flower['y'] + 30 * (1 - scale_y)
            draw_flower(screen, flower['x'], int(scaled_y), flower['color'])
    
    # Draw sun
    sun_x = WIDTH - 100
    sun_y = 80
    pygame.draw.circle(screen, FLOWER_YELLOW, (sun_x, sun_y), 30)
    # Sun rays
    for angle in range(0, 360, 45):
        rad = math.radians(angle + time_normalized * 50)
        ray_end_x = sun_x + math.cos(rad) * 50
        ray_end_y = sun_y + math.sin(rad) * 50
        pygame.draw.line(screen, FLOWER_YELLOW, (sun_x, sun_y), 
                        (int(ray_end_x), int(ray_end_y)), 3)
    
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