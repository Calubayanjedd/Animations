import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magical Portal Temple")

clock = pygame.time.Clock()
FPS = 60

# Colors
DEEP_PURPLE = (20, 0, 40)
MAGIC_PURPLE = (138, 43, 226)
MAGIC_CYAN = (0, 255, 255)
MAGIC_PINK = (255, 105, 180)
GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)
STONE_GRAY = (105, 105, 105)
DARK_STONE = (70, 70, 70)
MOSS_GREEN = (85, 107, 47)
CRYSTAL_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)

def create_stone_texture(width, height):
    """Create ancient stone brick texture"""
    surface = pygame.Surface((width, height))
    
    # Base stone color with weathering
    for y in range(height):
        for x in range(width):
            noise = random.randint(-20, 20)
            base = 85 + noise
            surface.set_at((x, y), (base, base, base + 5))
    
    # Draw brick pattern
    brick_height = 25
    brick_width = 50
    
    for row in range(0, height, brick_height):
        offset = brick_width // 2 if (row // brick_height) % 2 else 0
        for col in range(-brick_width, width + brick_width, brick_width):
            x = col + offset
            # Brick outlines
            pygame.draw.rect(surface, DARK_STONE, 
                           (x, row, brick_width - 2, brick_height - 2), 1)
            
            # Add cracks
            if random.random() > 0.7:
                crack_start_x = x + random.randint(5, brick_width - 10)
                crack_start_y = row + random.randint(5, brick_height - 10)
                crack_length = random.randint(5, 15)
                pygame.draw.line(surface, DARK_STONE,
                               (crack_start_x, crack_start_y),
                               (crack_start_x + crack_length, crack_start_y + crack_length), 1)
    
    # Add moss patches
    for _ in range(30):
        moss_x = random.randint(0, width)
        moss_y = random.randint(0, height)
        moss_size = random.randint(3, 8)
        for i in range(moss_size):
            pygame.draw.circle(surface, MOSS_GREEN, 
                             (moss_x + random.randint(-5, 5), 
                              moss_y + random.randint(-5, 5)), 
                             random.randint(1, 3))
    
    return surface

def create_rune_texture(size):
    """Create glowing magical rune"""
    surface = pygame.Surface((size, size))
    surface.set_colorkey((0, 0, 0))
    surface.fill((0, 0, 0))
    
    center = size // 2
    
    # Draw mystical symbol
    # Outer circle
    pygame.draw.circle(surface, MAGIC_CYAN, (center, center), size // 2 - 2, 2)
    
    # Inner star pattern
    points = []
    for i in range(8):
        angle = i * (math.pi * 2 / 8)
        if i % 2 == 0:
            radius = size // 3
        else:
            radius = size // 6
        x = center + math.cos(angle) * radius
        y = center + math.sin(angle) * radius
        points.append((int(x), int(y)))
    
    pygame.draw.polygon(surface, MAGIC_PURPLE, points, 2)
    
    # Center circle
    pygame.draw.circle(surface, MAGIC_PINK, (center, center), size // 8)
    
    # Add glow
    for i in range(3, 0, -1):
        pygame.draw.circle(surface, (80, 20, 120), (center, center), size // 2 - 2 + i * 2, 1)
    
    return surface

def create_crystal_texture(width, height):
    """Create glowing crystal texture"""
    surface = pygame.Surface((width, height))
    surface.set_colorkey((0, 0, 0))
    surface.fill((0, 0, 0))
    
    # Crystal facets
    points = [
        (width // 2, 0),
        (width, height // 3),
        (width * 3 // 4, height),
        (width // 4, height),
        (0, height // 3)
    ]
    
    pygame.draw.polygon(surface, CRYSTAL_BLUE, points)
    
    # Add internal facet lines
    for i in range(len(points)):
        pygame.draw.line(surface, WHITE, points[i], (width // 2, height // 2), 1)
    
    # Highlight
    pygame.draw.circle(surface, WHITE, (width // 2, height // 4), 3)
    
    return surface

# Create textures
temple_wall_left = create_stone_texture(200, 500)
temple_wall_right = create_stone_texture(200, 500)
ground_texture = create_stone_texture(WIDTH, 150)

# Create runes
runes = []
rune_positions = [
    (150, 200), (750, 200), (150, 350), (750, 350)
]
for pos in rune_positions:
    runes.append({
        'texture': create_rune_texture(60),
        'x': pos[0],
        'y': pos[1],
        'pulse': random.uniform(0, math.pi * 2)
    })

# Create crystals
crystals = []
crystal_positions = [
    (100, HEIGHT - 200), (800, HEIGHT - 220), (200, HEIGHT - 180), (700, HEIGHT - 190)
]
for pos in crystal_positions:
    crystals.append({
        'texture': create_crystal_texture(30, 40),
        'x': pos[0],
        'y': pos[1],
        'glow_phase': random.uniform(0, math.pi * 2)
    })

# Portal parameters
portal_center_x = WIDTH // 2
portal_center_y = HEIGHT // 2
portal_radius = 120

# Energy particles orbiting portal
particles = []
for _ in range(100):
    particles.append({
        'angle': random.uniform(0, math.pi * 2),
        'distance': random.uniform(50, 150),
        'speed': random.uniform(0.02, 0.05),
        'size': random.randint(2, 5),
        'color': random.choice([MAGIC_PURPLE, MAGIC_CYAN, MAGIC_PINK])
    })

# Lightning bolts from portal
lightning_bolts = []

# Floating orbs
orbs = []
for _ in range(8):
    orbs.append({
        'x': random.randint(100, WIDTH - 100),
        'y': random.randint(100, 300),
        'float_offset': random.uniform(0, math.pi * 2),
        'float_speed': random.uniform(0.02, 0.04),
        'size': random.randint(8, 15),
        'color': random.choice([MAGIC_PURPLE, MAGIC_CYAN, MAGIC_PINK, GOLD])
    })

# Torch flames
torches = [
    {'x': 100, 'y': 150},
    {'x': 800, 'y': 150}
]

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
    
    # Draw gradient background (deep purple sky)
    for y in range(HEIGHT):
        color_factor = y / HEIGHT
        color = (
            int(DEEP_PURPLE[0] + (MAGIC_PURPLE[0] - DEEP_PURPLE[0]) * color_factor * 0.3),
            int(DEEP_PURPLE[1] + (MAGIC_PURPLE[1] - DEEP_PURPLE[1]) * color_factor * 0.3),
            int(DEEP_PURPLE[2] + (MAGIC_PURPLE[2] - DEEP_PURPLE[2]) * color_factor * 0.3)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))
    
    # Draw stars
    for _ in range(50):
        star_x = random.randint(0, WIDTH)
        star_y = random.randint(0, HEIGHT // 2)
        if random.random() > 0.5:
            pygame.draw.circle(screen, WHITE, (star_x, star_y), 1)
    
    # Draw ground
    screen.blit(ground_texture, (0, HEIGHT - 150))
    
    # Draw temple walls
    screen.blit(temple_wall_left, (0, HEIGHT - 650))
    screen.blit(temple_wall_right, (WIDTH - 200, HEIGHT - 650))
    
    # Draw glowing runes on walls
    for rune in runes:
        rune['pulse'] += 0.05
        pulse_alpha = (math.sin(rune['pulse']) + 1) / 2
        glow_size = int(70 + 10 * pulse_alpha)
        
        # Glow effect
        for i in range(5, 0, -1):
            glow_surf = pygame.Surface((glow_size, glow_size))
            glow_surf.set_colorkey((0, 0, 0))
            glow_surf.fill((0, 0, 0))
            glow_color = (
                int(MAGIC_CYAN[0] * pulse_alpha * 0.3),
                int(MAGIC_CYAN[1] * pulse_alpha * 0.3),
                int(MAGIC_CYAN[2] * pulse_alpha * 0.3)
            )
            pygame.draw.circle(glow_surf, glow_color, (glow_size // 2, glow_size // 2), glow_size // 2)
            screen.blit(glow_surf, (rune['x'] - glow_size // 2, rune['y'] - glow_size // 2))
        
        screen.blit(rune['texture'], (rune['x'] - 30, rune['y'] - 30))
    
    # Draw portal
    # Portal rings
    for ring in range(5, 0, -1):
        ring_radius = portal_radius + ring * 10
        ring_alpha = (math.sin(elapsed_time * 0.003 + ring) + 1) / 2
        color = (
            int(MAGIC_PURPLE[0] * ring_alpha),
            int(MAGIC_PURPLE[1] * ring_alpha),
            int(MAGIC_PURPLE[2] * ring_alpha)
        )
        pygame.draw.circle(screen, color, (portal_center_x, portal_center_y), 
                         ring_radius, 3)
    
    # Portal center (swirling effect)
    for i in range(20):
        angle = (elapsed_time * 0.005 + i * (math.pi * 2 / 20)) % (math.pi * 2)
        radius = portal_radius - i * 6
        if radius > 0:
            x = portal_center_x + math.cos(angle) * radius
            y = portal_center_y + math.sin(angle) * radius
            color_index = i / 20
            color = (
                int(MAGIC_PURPLE[0] * (1 - color_index) + MAGIC_CYAN[0] * color_index),
                int(MAGIC_PURPLE[1] * (1 - color_index) + MAGIC_CYAN[1] * color_index),
                int(MAGIC_PURPLE[2] * (1 - color_index) + MAGIC_CYAN[2] * color_index)
            )
            pygame.draw.circle(screen, color, (int(x), int(y)), 5)
    
    # Orbiting particles
    for particle in particles:
        particle['angle'] += particle['speed']
        x = portal_center_x + math.cos(particle['angle']) * particle['distance']
        y = portal_center_y + math.sin(particle['angle']) * particle['distance']
        
        # Trail effect
        trail_length = 5
        for t in range(trail_length):
            trail_angle = particle['angle'] - t * 0.1
            trail_x = portal_center_x + math.cos(trail_angle) * particle['distance']
            trail_y = portal_center_y + math.sin(trail_angle) * particle['distance']
            trail_alpha = 1 - (t / trail_length)
            trail_color = tuple(int(c * trail_alpha) for c in particle['color'])
            pygame.draw.circle(screen, trail_color, (int(trail_x), int(trail_y)), 
                             max(1, particle['size'] - t))
        
        pygame.draw.circle(screen, particle['color'], (int(x), int(y)), particle['size'])
    
    # Random lightning from portal
    if random.random() > 0.95:
        target_x = random.randint(100, WIDTH - 100)
        target_y = random.randint(100, HEIGHT - 200)
        lightning_bolts.append({
            'x': target_x,
            'y': target_y,
            'life': 5
        })
    
    # Draw lightning
    for bolt in lightning_bolts[:]:
        bolt['life'] -= 1
        if bolt['life'] <= 0:
            lightning_bolts.remove(bolt)
        else:
            alpha = bolt['life'] / 5
            color = tuple(int(c * alpha) for c in MAGIC_CYAN)
            
            # Jagged lightning line
            steps = 10
            prev_x, prev_y = portal_center_x, portal_center_y
            for i in range(steps):
                t = (i + 1) / steps
                x = portal_center_x + (bolt['x'] - portal_center_x) * t + random.randint(-10, 10)
                y = portal_center_y + (bolt['y'] - portal_center_y) * t + random.randint(-10, 10)
                pygame.draw.line(screen, color, (int(prev_x), int(prev_y)), (int(x), int(y)), 2)
                prev_x, prev_y = x, y
    
    # Draw crystals
    for crystal in crystals:
        crystal['glow_phase'] += 0.05
        glow = (math.sin(crystal['glow_phase']) + 1) / 2
        
        # Glow
        for i in range(5, 0, -1):
            glow_color = (
                int(CRYSTAL_BLUE[0] * glow * 0.3),
                int(CRYSTAL_BLUE[1] * glow * 0.3),
                int(CRYSTAL_BLUE[2] * glow * 0.3)
            )
            pygame.draw.circle(screen, glow_color, 
                             (crystal['x'] + 15, crystal['y'] + 20), 
                             30 + i * 3)
        
        screen.blit(crystal['texture'], (crystal['x'], crystal['y']))
        
        # Light beam to portal
        if glow > 0.7:
            pygame.draw.line(screen, CRYSTAL_BLUE, 
                           (crystal['x'] + 15, crystal['y']),
                           (portal_center_x, portal_center_y), 1)
    
    # Draw floating orbs
    for orb in orbs:
        orb['float_offset'] += orb['float_speed']
        float_y = orb['y'] + math.sin(orb['float_offset']) * 20
        
        # Glow
        for i in range(3, 0, -1):
            glow_color = tuple(int(c * 0.3) for c in orb['color'])
            pygame.draw.circle(screen, glow_color, 
                             (int(orb['x']), int(float_y)), 
                             orb['size'] + i * 4)
        
        pygame.draw.circle(screen, orb['color'], 
                         (int(orb['x']), int(float_y)), orb['size'])
    
    # Draw torch flames
    for torch in torches:
        flame_height = 20 + 10 * math.sin(elapsed_time * 0.01)
        flame_points = [
            (torch['x'], torch['y']),
            (torch['x'] - 10, torch['y'] + flame_height),
            (torch['x'], torch['y'] + flame_height - 5),
            (torch['x'] + 10, torch['y'] + flame_height)
        ]
        pygame.draw.polygon(screen, ORANGE, flame_points)
        pygame.draw.polygon(screen, GOLD, [
            (torch['x'], torch['y']),
            (torch['x'] - 5, torch['y'] + flame_height // 2),
            (torch['x'], torch['y'] + flame_height // 2 - 3),
            (torch['x'] + 5, torch['y'] + flame_height // 2)
        ])
        
        # Glow
        pygame.draw.circle(screen, (255, 100, 0), (torch['x'], torch['y'] + 10), 25)
    
    # Draw timer with magical glow
    font = pygame.font.Font(None, 48)
    time_left = (ANIMATION_DURATION - elapsed_time) / 1000
    
    # Glow effect
    for offset in range(4, 0, -1):
        glow_color = (100, 50, 150)
        timer_text = font.render(f"{time_left:.1f}s", True, glow_color)
        screen.blit(timer_text, (WIDTH // 2 - 50 + offset, 20))
        screen.blit(timer_text, (WIDTH // 2 - 50 - offset, 20))
    
    timer_text = font.render(f"{time_left:.1f}s", True, MAGIC_CYAN)
    screen.blit(timer_text, (WIDTH // 2 - 50, 20))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()