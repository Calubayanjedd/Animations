import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Launch")

clock = pygame.time.Clock()
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
SPACE_BLACK = (5, 5, 15)
CLOUD_WHITE = (255, 255, 255)
GROUND_GREEN = (34, 139, 34)
GROUND_BROWN = (139, 90, 43)
CONCRETE_GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
ROCKET_WHITE = (240, 240, 240)
ROCKET_RED = (220, 20, 60)
FIRE_ORANGE = (255, 140, 0)
FIRE_YELLOW = (255, 215, 0)
FIRE_RED = (255, 69, 0)
SMOKE_GRAY = (169, 169, 169)
STAR_WHITE = (255, 255, 255)
WHITE = (255, 255, 255)
MOON_GRAY = (200, 200, 200)

def create_metal_texture(width, height):
    """Create metallic spaceship texture"""
    surface = pygame.Surface((width, height))
    
    # Base metal color with shine
    for y in range(height):
        for x in range(width):
            # Create metallic shine effect
            shine = int(20 * math.sin(x * 0.1) * math.cos(y * 0.1))
            noise = random.randint(-10, 10)
            base = 200 + shine + noise
            surface.set_at((x, y), (base, base, base + 20))
    
    # Add panel lines
    for y in range(0, height, 30):
        pygame.draw.line(surface, DARK_GRAY, (0, y), (width, y), 2)
    
    # Add rivets
    for y in range(15, height, 30):
        for x in range(15, width, 20):
            pygame.draw.circle(surface, DARK_GRAY, (x, y), 2)
            pygame.draw.circle(surface, (180, 180, 180), (x - 1, y - 1), 1)
    
    return surface

def create_concrete_texture(width, height):
    """Create launch pad concrete texture"""
    surface = pygame.Surface((width, height))
    
    # Base concrete color
    for y in range(height):
        for x in range(width):
            noise = random.randint(-15, 15)
            gray = 128 + noise
            surface.set_at((x, y), (gray, gray, gray + 5))
    
    # Add cracks
    for _ in range(20):
        crack_x = random.randint(0, width)
        crack_y = random.randint(0, height)
        crack_length = random.randint(30, 80)
        crack_angle = random.uniform(0, math.pi * 2)
        
        segments = 8
        prev_x, prev_y = crack_x, crack_y
        for i in range(segments):
            next_x = prev_x + math.cos(crack_angle) * (crack_length / segments)
            next_y = prev_y + math.sin(crack_angle) * (crack_length / segments)
            next_x += random.randint(-5, 5)
            next_y += random.randint(-5, 5)
            
            if 0 <= next_x < width and 0 <= next_y < height:
                pygame.draw.line(surface, DARK_GRAY, 
                               (int(prev_x), int(prev_y)), 
                               (int(next_x), int(next_y)), 2)
            prev_x, prev_y = next_x, next_y
    
    # Add scorch marks
    for _ in range(10):
        scorch_x = random.randint(0, width)
        scorch_y = random.randint(0, height)
        scorch_size = random.randint(20, 50)
        for i in range(scorch_size, 0, -3):
            darkness = int(100 * (i / scorch_size))
            pygame.draw.circle(surface, (darkness, darkness, darkness), 
                             (scorch_x, scorch_y), i)
    
    return surface

# Create textures
rocket_body_texture = create_metal_texture(80, 200)
launchpad_texture = create_concrete_texture(300, 100)

# Rocket parameters
rocket = {
    'x': WIDTH // 2,
    'y': HEIGHT - 200,
    'start_y': HEIGHT - 200,
    'velocity': 0,
    'acceleration': 0.15,
    'launched': False
}

# Flame particles
flames = []
smoke_particles = []

# Exhaust flames (bottom of rocket)
exhaust_flames = []

# Stars (for space)
stars = []
for _ in range(150):
    stars.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT // 2),
        'size': random.randint(1, 3),
        'twinkle': random.uniform(0, math.pi * 2)
    })

# Clouds
clouds = []
for _ in range(8):
    clouds.append({
        'x': random.randint(-100, WIDTH + 100),
        'y': random.randint(50, 250),
        'width': random.randint(80, 150),
        'speed': random.uniform(0.3, 0.8)
    })

# Moon
moon = {
    'x': WIDTH - 150,
    'y': 100,
    'radius': 50
}

# Countdown
countdown_time = 3000  # 3 seconds countdown
launch_time = None

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
    
    # Start countdown at 1 second, launch at 4 seconds
    if elapsed_time >= 1000 and not rocket['launched'] and launch_time is None:
        launch_time = elapsed_time
    
    if launch_time is not None and elapsed_time - launch_time >= countdown_time:
        rocket['launched'] = True
    
    # Calculate sky transition (blue to space)
    if rocket['launched']:
        transition = min(1.0, rocket['velocity'] * 0.15)
    else:
        transition = 0
    
    # Draw sky/space gradient
    for y in range(HEIGHT):
        # Sky to space transition
        sky_color = (
            int(SKY_BLUE[0] * (1 - transition) + SPACE_BLACK[0] * transition),
            int(SKY_BLUE[1] * (1 - transition) + SPACE_BLACK[1] * transition),
            int(SKY_BLUE[2] * (1 - transition) + SPACE_BLACK[2] * transition)
        )
        pygame.draw.line(screen, sky_color, (0, y), (WIDTH, y))
    
    # Draw stars (fade in as we go to space)
    if transition > 0.3:
        for star in stars:
            star['twinkle'] += 0.05
            brightness = (math.sin(star['twinkle']) + 1) / 2
            alpha = brightness * (transition - 0.3) / 0.7
            color = tuple(int(c * alpha) for c in STAR_WHITE)
            pygame.draw.circle(screen, color, (star['x'], star['y']), star['size'])
    
    # Draw moon (fade in)
    if transition > 0.5:
        moon_alpha = (transition - 0.5) / 0.5
        moon_color = tuple(int(c * moon_alpha) for c in MOON_GRAY)
        pygame.draw.circle(screen, moon_color, (moon['x'], moon['y']), moon['radius'])
        # Craters
        if moon_alpha > 0.5:
            pygame.draw.circle(screen, tuple(int(c * 0.8) for c in moon_color), 
                             (moon['x'] - 15, moon['y'] - 10), 8)
            pygame.draw.circle(screen, tuple(int(c * 0.8) for c in moon_color), 
                             (moon['x'] + 10, moon['y'] + 5), 12)
            pygame.draw.circle(screen, tuple(int(c * 0.8) for c in moon_color), 
                             (moon['x'] + 5, moon['y'] - 20), 6)
    
    # Draw clouds (fade out as we go to space)
    if transition < 0.8:
        for cloud in clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > WIDTH + 100:
                cloud['x'] = -100
            
            cloud_alpha = 1 - (transition / 0.8)
            cloud_color = tuple(int(c * cloud_alpha) for c in CLOUD_WHITE)
            
            # Cloud puffs
            pygame.draw.ellipse(screen, cloud_color, 
                              (int(cloud['x']), cloud['y'], cloud['width'], 40))
            pygame.draw.ellipse(screen, cloud_color, 
                              (int(cloud['x'] + 20), cloud['y'] - 15, cloud['width'] - 40, 40))
            pygame.draw.ellipse(screen, cloud_color, 
                              (int(cloud['x'] + 40), cloud['y'] - 10, cloud['width'] - 60, 35))
    
    # Draw ground (fade out as we go to space)
    if transition < 0.7:
        ground_alpha = 1 - (transition / 0.7)
        ground_color = tuple(int(GROUND_GREEN[i] * ground_alpha + SPACE_BLACK[i] * (1 - ground_alpha)) 
                           for i in range(3))
        pygame.draw.rect(screen, ground_color, (0, HEIGHT - 100, WIDTH, 100))
        
        # Ground details
        for _ in range(30):
            grass_x = random.randint(0, WIDTH)
            grass_y = HEIGHT - random.randint(80, 100)
            grass_color = tuple(int(c * ground_alpha * 0.7) for c in GROUND_GREEN)
            pygame.draw.line(screen, grass_color, 
                           (grass_x, grass_y), 
                           (grass_x, grass_y - random.randint(5, 15)), 1)
    
    # Draw launch pad
    if rocket['y'] > HEIGHT - 10:
        pad_alpha = min(1.0, (rocket['y'] - (HEIGHT - 500)) / 200)
        if pad_alpha > 0:
            launchpad_surface = launchpad_texture.copy()
            launchpad_surface.set_alpha(int(255 * pad_alpha))
            screen.blit(launchpad_surface, (WIDTH // 2 - 150, HEIGHT - 150))
            
            # Support towers
            tower_color = tuple(int(c * pad_alpha) for c in CONCRETE_GRAY)
            pygame.draw.rect(screen, tower_color, (WIDTH // 2 - 180, HEIGHT - 250, 20, 150))
            pygame.draw.rect(screen, tower_color, (WIDTH // 2 + 160, HEIGHT - 250, 20, 150))
            
            # Connecting bridges
            pygame.draw.rect(screen, tower_color, (WIDTH // 2 - 180, HEIGHT - 230, 40, 5))
            pygame.draw.rect(screen, tower_color, (WIDTH // 2 + 140, HEIGHT - 230, 40, 5))
    
    # Update rocket position
    if rocket['launched']:
        rocket['velocity'] += rocket['acceleration']
        rocket['y'] -= rocket['velocity']
    
    # Generate exhaust flames
    if rocket['launched']:
        for _ in range(8):
            flames.append({
                'x': rocket['x'] + random.randint(-15, 15),
                'y': rocket['y'] + 100,
                'velocity_y': random.uniform(2, 5),
                'velocity_x': random.uniform(-2, 2),
                'size': random.randint(8, 20),
                'life': random.randint(20, 40),
                'color_type': random.choice(['orange', 'yellow', 'red'])
            })
        
        # Smoke particles
        for _ in range(3):
            smoke_particles.append({
                'x': rocket['x'] + random.randint(-20, 20),
                'y': rocket['y'] + 100,
                'velocity_y': random.uniform(0.5, 1.5),
                'velocity_x': random.uniform(-1, 1),
                'size': random.randint(10, 25),
                'life': random.randint(40, 80)
            })
    
    # Draw smoke
    for smoke in smoke_particles[:]:
        smoke['y'] += smoke['velocity_y']
        smoke['x'] += smoke['velocity_x']
        smoke['life'] -= 1
        smoke['size'] += 0.3
        
        if smoke['life'] <= 0:
            smoke_particles.remove(smoke)
        else:
            alpha = smoke['life'] / 80
            color = tuple(int(SMOKE_GRAY[i] * alpha) for i in range(3))
            pygame.draw.circle(screen, color, 
                             (int(smoke['x']), int(smoke['y'])), int(smoke['size']))
    
    # Draw flames
    for flame in flames[:]:
        flame['y'] += flame['velocity_y']
        flame['x'] += flame['velocity_x']
        flame['life'] -= 1
        
        if flame['life'] <= 0:
            flames.remove(flame)
        else:
            alpha = flame['life'] / 40
            if flame['color_type'] == 'orange':
                color = tuple(int(FIRE_ORANGE[i] * alpha) for i in range(3))
            elif flame['color_type'] == 'yellow':
                color = tuple(int(FIRE_YELLOW[i] * alpha) for i in range(3))
            else:
                color = tuple(int(FIRE_RED[i] * alpha) for i in range(3))
            
            pygame.draw.circle(screen, color, 
                             (int(flame['x']), int(flame['y'])), int(flame['size']))
    
    # Draw rocket
    if rocket['y'] < HEIGHT + 100:
        # Nose cone (red)
        nose_points = [
            (rocket['x'], rocket['y'] - 40),
            (rocket['x'] - 40, rocket['y']),
            (rocket['x'] + 40, rocket['y'])
        ]
        pygame.draw.polygon(screen, ROCKET_RED, nose_points)
        pygame.draw.polygon(screen, (180, 0, 40), nose_points, 2)
        
        # Rocket body with texture
        rocket_surface = rocket_body_texture.copy()
        screen.blit(rocket_surface, (int(rocket['x'] - 40), int(rocket['y'])))
        
        # Fins
        left_fin = [
            (rocket['x'] - 40, rocket['y'] + 180),
            (rocket['x'] - 70, rocket['y'] + 200),
            (rocket['x'] - 40, rocket['y'] + 200)
        ]
        right_fin = [
            (rocket['x'] + 40, rocket['y'] + 180),
            (rocket['x'] + 70, rocket['y'] + 200),
            (rocket['x'] + 40, rocket['y'] + 200)
        ]
        pygame.draw.polygon(screen, ROCKET_RED, left_fin)
        pygame.draw.polygon(screen, ROCKET_RED, right_fin)
        pygame.draw.polygon(screen, (180, 0, 40), left_fin, 2)
        pygame.draw.polygon(screen, (180, 0, 40), right_fin, 2)
        
        # Window
        pygame.draw.circle(screen, SKY_BLUE, (int(rocket['x']), int(rocket['y'] + 30)), 12)
        pygame.draw.circle(screen, DARK_GRAY, (int(rocket['x']), int(rocket['y'] + 30)), 12, 2)
        
        # Engine nozzles
        pygame.draw.rect(screen, DARK_GRAY, 
                        (rocket['x'] - 30, rocket['y'] + 200, 20, 15))
        pygame.draw.rect(screen, DARK_GRAY, 
                        (rocket['x'] + 10, rocket['y'] + 200, 20, 15))
        
        # Vibration effect when launching
        if rocket['launched'] and rocket['velocity'] < 5:
            shake_x = random.randint(-2, 2)
            shake_y = random.randint(-2, 2)
            rocket['x'] += shake_x
            rocket['y'] += shake_y
    
    # Draw countdown
    if launch_time is not None and elapsed_time - launch_time < countdown_time:
        countdown_remaining = countdown_time - (elapsed_time - launch_time)
        countdown_number = int(countdown_remaining / 1000) + 1
        
        font = pygame.font.Font(None, 120)
        countdown_text = font.render(str(countdown_number), True, FIRE_RED)
        text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        
        # Glow effect
        for offset in range(5, 0, -1):
            glow_surface = font.render(str(countdown_number), True, FIRE_ORANGE)
            glow_surface.set_alpha(100 - offset * 15)
            screen.blit(glow_surface, (text_rect.x + offset, text_rect.y))
            screen.blit(glow_surface, (text_rect.x - offset, text_rect.y))
        
        screen.blit(countdown_text, text_rect)
    
    # Draw timer
    timer_font = pygame.font.Font(None, 42)
    time_left = (ANIMATION_DURATION - elapsed_time) / 1000
    timer_text = timer_font.render(f"{time_left:.1f}s", True, WHITE)
    screen.blit(timer_text, (WIDTH - 120, 20))
    
    # Launch status
    status_font = pygame.font.Font(None, 36)
    if not rocket['launched'] and launch_time is None:
        status = "READY FOR LAUNCH"
        color = FIRE_YELLOW
    elif launch_time is not None and not rocket['launched']:
        status = "LAUNCHING..."
        color = FIRE_ORANGE
    else:
        status = "LIFTOFF!"
        color = FIRE_RED
    
    status_text = status_font.render(status, True, color)
    screen.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 20))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()