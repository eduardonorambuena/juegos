import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configurar pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Mi Primer Juego Mejorado')

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Cargar imágenes
spaceship_img = pygame.image.load("imagenes/spaceship.png.jpg")  # Asegúrate de que esta imagen exista
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))  # Ajusta el tamaño de la nave espacial

# Posición inicial de la nave espacial
player_pos = [400, 300]
player_size = 50

# Velocidad de la nave espacial y disparos
player_speed = 5
bullet_speed = 7

# Configurar disparos
bullets = []

# Configurar enemigos
enemy_size = 50
enemy_speed = 5
enemy_list = []

# Configurar puntuación
score = 0
font = pygame.font.SysFont("monospace", 35)

# Configurar sonido
pygame.mixer.music.load(r"musica/Y2meta.app - MASHLE_ MAGIC AND MUSCLES OP. 2 _ Bling-Bang-Bang-Born (Sub. Español + Romaji) (128 kbps).mp3")
pygame.mixer.music.play(-1)

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, 750)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < 600:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, pygame.Rect(bullet[0], bullet[1], 10, 5))

def update_bullet_positions(bullets):
    for bullet in bullets:
        bullet[1] -= bullet_speed

    # Eliminar balas fuera de la pantalla
    return [bullet for bullet in bullets if bullet[1] > 0]

def bullet_collision_check(bullets, enemy_list):
    for bullet in bullets:
        for enemy_pos in enemy_list:
            if detect_collision(bullet, enemy_pos):
                bullets.remove(bullet)
                enemy_list.remove(enemy_pos)
                return True
    return False

clock = pygame.time.Clock()

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_pos[0] + player_size // 2 - 5, player_pos[1]])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < 750:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < 550:
        player_pos[1] += player_speed

    screen.fill(BLACK)

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    bullets = update_bullet_positions(bullets)

    if bullet_collision_check(bullets, enemy_list):
        score += 1

    text = font.render("Puntuación: {0}".format(score), True, WHITE)
    screen.blit(text, (10, 10))

    if collision_check(enemy_list, player_pos):
        running = False

    # Dibujar enemigos y nave espacial
    draw_enemies(enemy_list)
    screen.blit(spaceship_img, (player_pos[0], player_pos[1]))
    draw_bullets(bullets)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
