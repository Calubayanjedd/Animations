import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lo-Fi Aesthetic Room")

clock = pygame.time.Clock()
FPS = 60

# Aesthetic Color Palette
SOFT_PURPLE = (162, 155, 254)
SOFT_PINK = (255, 198, 255)
SOFT_BLUE = (189, 224, 254)
CREAM = (255, 250, 240)
PEACH = (255, 218, 185)
LAVENDER = (230, 230, 250)
MINT = (189, 252, 201)
CORAL = (255, 183, 178)
DEEP_BLUE = (67, 97, 238)
GOLDEN = (255, 223, 186)
WOOD_BROWN = (139, 90, 60)
DARK_WOOD = (101, 67, 33)
PLANT_GREEN = (119, 221, 119)
DARK_GREEN = (34, 139, 34)

def create_wood_texture(width, height):
    """Create wooden desk/floor texture"""
    surface = pygame.Surface((width, height))
    
    # Base wood color with grain
    for y in range(height):
        for x in range(width):
            # Wood grain pattern
            grain = int(10 * math.sin(y * 0.1) * math.cos(x * 0.05))
            noise = random.randint(-8, 8)
            color_val = WOOD_BROWN[0] + grain + noise
            surface.set_at((x, y), (
                max(50, min(255, color_val)),
                max(40, min(255, int(color_val * 0.65))),
                max(20, min(255, int(color_val * 0.43)))
            ))
    
    # Add wood lines
    for _ in range(15):
        line_y = random.randint(0, height)
        line_darkness = random.randint(20, 40)
        for x in range(width):
            wave = int(3 * math.sin(x * 0.02 + line_y))
            y_pos = line_y + wave
            if 0 <= y_pos < height:
                current_color = surface.get_at((x, y_pos))
                new_color = tuple(max(0, c - line_darkness) for c in current_color[:3])
                surface.set_at((x, y_pos), new_color)
    
    return surface

def create_book_spine_texture(width, height, color):
    """Create book spine with title texture"""
    surface = pygame.Surface((width, height))
    
    # Base color with slight variation
    for y in range(height):
        for x in range(width):
            noise = random.randint(-5, 5)
            surface.set_at((x, y), tuple(max(0, min(255, c + noise)) for c in color))
    
    # Add spine lines
    pygame.draw.line(surface, tuple(max(0, c - 30) for c in color), 
                    (2, 0), (2, height), 1)
    pygame.draw.line(surface, tuple(max(0, c - 30) for c in color), 
                    (width - 2, 0), (width - 2, height), 1)
    
    # Add title lines (decorative)
    for i in range(3):
        y_pos = height // 4 + i * 8
        pygame.draw.line(surface, GOLDEN, (5, y_pos), (width - 5, y_pos), 2)
    
    return surface

def create_wall_texture(width, height):
    """Create soft textured wall"""
    surface = pygame.Surface((width, height))
    
    # Soft gradient base
    for y in range(height):
        color_factor = y / height
        color = (
            int(LAVENDER[0] + (SOFT_PURPLE[0] - LAVENDER[0]) * color_factor * 0.3),
            int(LAVENDER[1] + (SOFT_PURPLE[1] - LAVENDER[1]) * color_factor * 0.3),
            int(LAVENDER[2] + (SOFT_PURPLE[2] - LAVENDER[2]) * color_factor * 0.3)
        )
        for x in range(width):
            noise = random.randint(-3, 3)
            final_color = tuple(max(0, min(255, c + noise)) for c in color)
            surface.set_at((x, y), final_color)
    
    return surface

def draw_plant(surface, x, y, time):
    """Draw animated potted plant"""
    # Pot
    pot_points = [
        (x - 20, y + 30),
        (x - 15, y),
        (x + 15, y),
        (x + 20, y + 30)
    ]
    pygame.draw.polygon(surface, CORAL, pot_points)
    pygame.draw.polygon(surface, tuple(max(0, c - 40) for c in CORAL), pot_points, 2)
    
    # Soil
    pygame.draw.ellipse(surface, DARK_WOOD, (x - 15, y - 5, 30, 10))
    
    # Leaves with gentle sway
    leaves = 8
    for i in range(leaves):
        angle = (i / leaves) * math.pi * 2
        sway = math.sin(time * 2 + i) * 0.1
        leaf_angle = angle + sway
        
        leaf_length = 35 + (i % 3) * 8
        end_x = x + math.cos(leaf_angle) * leaf_length
        end_y = y - abs(math.sin(leaf_angle)) * leaf_length
        
        # Leaf stem
        pygame.draw.line(surface, DARK_GREEN, (x, y), (int(end_x), int(end_y)), 3)
        
        # Leaf shape
        leaf_size = 12 + (i % 2) * 4
        pygame.draw.ellipse(surface, PLANT_GREEN, 
                          (int(end_x - leaf_size/2), int(end_y - leaf_size/2), 
                           leaf_size, leaf_size))
        pygame.draw.ellipse(surface, DARK_GREEN, 
                          (int(end_x - leaf_size/2), int(end_y - leaf_size/2), 
                           leaf_size, leaf_size), 1)

def draw_mug(surface, x, y, steam_particles):
    """Draw coffee mug with steam"""
    # Mug body
    pygame.draw.rect(surface, SOFT_PINK, (x - 20, y, 40, 35))
    pygame.draw.rect(surface, tuple(max(0, c - 40) for c in SOFT_PINK), 
                    (x - 20, y, 40, 35), 2)
    
    # Handle
    pygame.draw.arc(surface, SOFT_PINK, (x + 15, y + 5, 15, 25), 
                   -math.pi/2, math.pi/2, 3)
    
    # Coffee surface
    pygame.draw.ellipse(surface, (101, 67, 33), (x - 18, y + 2, 36, 10))
    
    # Heart latte art
    pygame.draw.circle(surface, CREAM, (x - 5, y + 6), 4)
    pygame.draw.circle(surface, CREAM, (x + 5, y + 6), 4)
    points = [(x - 8, y + 7), (x, y + 12), (x + 8, y + 7)]
    pygame.draw.polygon(surface, CREAM, points)

# Create textures
wall_texture = create_wall_texture(WIDTH, HEIGHT // 2)
desk_texture = create_wood_texture(WIDTH, 200)
floor_texture = create_wood_texture(WIDTH, 300)

# Books
books = []
book_colors = [SOFT_PURPLE, CORAL, MINT, SOFT_PINK, SOFT_BLUE, PEACH]
book_x = 100
for i in range(8):
    width = random.randint(25, 40)
    height = random.randint(120, 160)
    books.append({
        'texture': create_book_spine_texture(width, height, random.choice(book_colors)),
        'x': book_x,
        'y': 350 - height,
        'width': width,
        'height': height
    })
    book_x += width + 2

# Floating particles (dust in light)
particles = []
for _ in range(40):
    particles.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT // 2),
        'speed_y': random.uniform(0.2, 0.5),
        'speed_x': random.uniform(-0.1, 0.1),
        'size': random.randint(1, 3),
        'alpha': random.uniform(0.3, 0.8)
    })

# Steam particles
steam_particles = []

# Window rain drops
rain_drops = []
for _ in range(30):
    rain_drops.append({
        'x': random.randint(520, 720),
        'y': random.randint(80, 280),
        'length': random.randint(15, 30),
        'speed': random.uniform(1, 3)
    })

# Fairy lights
fairy_lights = []
for i in range(12):
    fairy_lights.append({
        'x': 50 + i * 70,
        'y': 50,
        'phase': random.uniform(0, math.pi * 2),
        'color': random.choice([SOFT_PINK, SOFT_BLUE, GOLDEN, MINT])
    })

# Music notes
music_notes = []

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
    
    # Draw textured wall
    screen.blit(wall_texture, (0, 0))
    
    # Draw window with view
    window_rect = (520, 80, 200, 200)
    
    # Window - sky view
    sky_gradient = pygame.Surface((200, 200))
    for y in range(200):
        color_factor = y / 200
        color = (
            int(SOFT_BLUE[0] + (SOFT_PURPLE[0] - SOFT_BLUE[0]) * color_factor),
            int(SOFT_BLUE[1] + (SOFT_PURPLE[1] - SOFT_BLUE[1]) * color_factor),
            int(SOFT_BLUE[2] + (SOFT_PURPLE[2] - SOFT_BLUE[2]) * color_factor)
        )
        pygame.draw.line(sky_gradient, color, (0, y), (200, y))
    screen.blit(sky_gradient, (520, 80))
    
    # Rain on window
    for drop in rain_drops:
        drop['y'] += drop['speed']
        if drop['y'] > 280:
            drop['y'] = 80
            drop['x'] = random.randint(520, 720)
        pygame.draw.line(screen, SOFT_BLUE, 
                        (int(drop['x']), int(drop['y'])),
                        (int(drop['x'] + 2), int(drop['y'] + drop['length'])), 2)
    
    # Window frame
    pygame.draw.rect(screen, CREAM, window_rect, 8)
    pygame.draw.line(screen, CREAM, (620, 80), (620, 280), 8)
    pygame.draw.line(screen, CREAM, (520, 180), (720, 180), 8)
    
    # Draw fairy lights
    for light in fairy_lights:
        light['phase'] += 0.05
        brightness = (math.sin(light['phase']) + 1) / 2
        
        # Glow
        for i in range(3, 0, -1):
            glow_color = tuple(int(c * brightness * 0.4) for c in light['color'])
            pygame.draw.circle(screen, glow_color, (light['x'], light['y']), 8 + i * 2)
        
        # Light bulb
        color = tuple(int(c * (0.6 + brightness * 0.4)) for c in light['color'])
        pygame.draw.circle(screen, color, (light['x'], light['y']), 6)
        
        # Wire
        if light['x'] < WIDTH - 70:
            pygame.draw.line(screen, DARK_WOOD, 
                           (light['x'], light['y']), 
                           (light['x'] + 70, light['y']), 2)
    
    # Draw floating particles
    for particle in particles:
        particle['y'] += particle['speed_y']
        particle['x'] += particle['speed_x']
        
        if particle['y'] > HEIGHT // 2:
            particle['y'] = 0
            particle['x'] = random.randint(0, WIDTH)
        
        alpha = int(255 * particle['alpha'] * (math.sin(elapsed_time * 0.001 + particle['x']) * 0.5 + 0.5))
        color = (*GOLDEN[:3], alpha)
        pygame.draw.circle(screen, GOLDEN, 
                         (int(particle['x']), int(particle['y'])), particle['size'])
    
    # Draw floor
    screen.blit(floor_texture, (0, HEIGHT - 300))
    
    # Draw desk
    screen.blit(desk_texture, (0, 350))
    
    # Draw desk items
    
    # Laptop
    laptop_x, laptop_y = 400, 280
    # Screen
    pygame.draw.rect(screen, DEEP_BLUE, (laptop_x, laptop_y, 140, 100))
    # Screen glow
    pygame.draw.rect(screen, SOFT_BLUE, (laptop_x + 5, laptop_y + 5, 130, 90))
    
    # Code lines on screen
    for i in range(6):
        line_width = random.randint(60, 120)
        pygame.draw.rect(screen, SOFT_PURPLE, 
                        (laptop_x + 10, laptop_y + 10 + i * 13, line_width, 8))
    
    # Keyboard
    pygame.draw.rect(screen, tuple(max(0, c - 20) for c in DEEP_BLUE), 
                    (laptop_x - 10, laptop_y + 100, 160, 40))
    
    # Books on desk
    for book in books:
        screen.blit(book['texture'], (book['x'], book['y']))
    
    # Plant
    draw_plant(screen, 150, 320, time_normalized)
    
    # Coffee mug with steam
    mug_x, mug_y = 320, 310
    
    # Generate steam particles
    if random.random() > 0.7:
        steam_particles.append({
            'x': mug_x + random.randint(-5, 5),
            'y': mug_y,
            'speed': random.uniform(0.5, 1.0),
            'life': 100,
            'size': random.randint(3, 6)
        })
    
    # Draw steam
    for steam in steam_particles[:]:
        steam['y'] -= steam['speed']
        steam['x'] += math.sin(steam['y'] * 0.1) * 0.5
        steam['life'] -= 1
        
        if steam['life'] <= 0:
            steam_particles.remove(steam)
        else:
            alpha = steam['life'] / 100
            color = tuple(int(c * alpha) for c in CREAM)
            pygame.draw.circle(screen, color, 
                             (int(steam['x']), int(steam['y'])), steam['size'])
    
    draw_mug(screen, mug_x, mug_y, steam_particles)
    
    # Vinyl record player
    vinyl_x, vinyl_y = 680, 300
    # Base
    pygame.draw.rect(screen, WOOD_BROWN, (vinyl_x - 40, vinyl_y, 80, 50))
    # Record
    rotation = elapsed_time * 0.001
    pygame.draw.circle(screen, (20, 20, 20), (vinyl_x, vinyl_y + 15), 35)
    pygame.draw.circle(screen, DARK_WOOD, (vinyl_x, vinyl_y + 15), 5)
    # Grooves
    for r in range(30, 10, -4):
        pygame.draw.circle(screen, (40, 40, 40), (vinyl_x, vinyl_y + 15), r, 1)
    
    # Music notes floating
    if random.random() > 0.97:
        music_notes.append({
            'x': vinyl_x + random.randint(-20, 20),
            'y': vinyl_y,
            'life': 100,
            'type': random.choice(['♪', '♫'])
        })
    
    font = pygame.font.Font(None, 36)
    for note in music_notes[:]:
        note['y'] -= 1
        note['life'] -= 1
        
        if note['life'] <= 0:
            music_notes.remove(note)
        else:
            alpha = note['life'] / 100
            color = tuple(int(c * alpha) for c in SOFT_PURPLE)
            note_text = font.render(note['type'], True, color)
            screen.blit(note_text, (int(note['x']), int(note['y'])))
    
    # Cat sleeping on desk corner
    cat_x, cat_y = 750, 330
    # Body
    pygame.draw.ellipse(screen, PEACH, (cat_x, cat_y, 80, 40))
    # Head
    head_bob = math.sin(elapsed_time * 0.002) * 2
    pygame.draw.circle(screen, PEACH, (cat_x + 20, int(cat_y + 10 + head_bob)), 18)
    # Ears
    pygame.draw.polygon(screen, PEACH, [
        (cat_x + 12, cat_y + head_bob),
        (cat_x + 7, cat_y - 8 + head_bob),
        (cat_x + 17, cat_y + 5 + head_bob)
    ])
    pygame.draw.polygon(screen, PEACH, [
        (cat_x + 28, cat_y + head_bob),
        (cat_x + 33, cat_y - 8 + head_bob),
        (cat_x + 23, cat_y + 5 + head_bob)
    ])
    # Closed eyes (sleeping)
    pygame.draw.arc(screen, (0, 0, 0), (cat_x + 12, cat_y + 12 + head_bob, 6, 4), 
                   0, math.pi, 2)
    pygame.draw.arc(screen, (0, 0, 0), (cat_x + 20, cat_y + 12 + head_bob, 6, 4), 
                   0, math.pi, 2)
    # ZZZ
    zzz_font = pygame.font.Font(None, 24)
    zzz_y = cat_y - 20 + math.sin(elapsed_time * 0.003) * 5
    zzz_text = zzz_font.render("Z z z", True, SOFT_PURPLE)
    screen.blit(zzz_text, (cat_x + 40, int(zzz_y)))
    
    # Aesthetic timer
    timer_font = pygame.font.Font(None, 42)
    time_left = (ANIMATION_DURATION - elapsed_time) / 1000
    
    # Soft glow
    for offset in range(3, 0, -1):
        glow_color = SOFT_PURPLE
        timer_text = timer_font.render(f"{time_left:.1f}s", True, glow_color)
        timer_surface = timer_text.copy()
        timer_surface.set_alpha(100 - offset * 30)
        screen.blit(timer_surface, (WIDTH // 2 - 45 + offset, 15))
        screen.blit(timer_surface, (WIDTH // 2 - 45 - offset, 15))
    
    timer_text = timer_font.render(f"{time_left:.1f}s", True, CREAM)
    screen.blit(timer_text, (WIDTH // 2 - 45, 15))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()