import math
import random
from pygame import Rect
import pgzrun

WIDTH = 800
HEIGHT = 600
TITLE = "Forest Jump"

background = images.load("background")

# Estados do jogo
game_state = "menu"

# Sons e música (use seus próprios arquivos .wav/.mp3)
music_on = True

# Plataforma principal
platform = Rect((0, HEIGHT - 50), (WIDTH, 50))

# Personagem (só um retângulo por enquanto)
hero = Rect((100, HEIGHT - 100), (40, 40))
hero_color = (0, 200, 255)
hero_speed_x = 0
hero_speed_y = 0
gravity = 0.5
jump_strength = -10
on_ground = False

goal = Rect((700, HEIGHT - 100), (40, 40))  # Objetivo do jogo

# Obstáculos
obstacles = [
    Rect((200, HEIGHT - 100), (50, 50)),
    Rect((300, HEIGHT - 150), (50, 50)),
    Rect((500, HEIGHT - 100), (50, 50)),
    Rect((600, HEIGHT - 150), (50, 50)),
]

# Inimigos
enemies = [
    {"rect": Rect((400, platform.top - 40), (40, 40)), "speed": 2},  # No chão
    {"rect": Rect((600, platform.top - 40), (40, 40)), "speed": -3},  # No chão
]


# Botões do menu
class Button:
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = Rect((x, y), (width, height))
        self.action = action
        self.color = (0, 180, 0)

    def draw(self):
        screen.draw.filled_rect(self.rect, self.color)
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=32,
            color="black"
        )

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

def start_game():
    global game_state
    game_state = "playing"

def toggle_music():
    global music_on
    if music_on:
        music.play("bg")
        music_on = True
    else:
        music.stop()
        music_on = False

def exit_game():
    exit()

buttons = [
    Button("Começar jogo", 300, 200, 200, 50, start_game),
    Button("Música ON/OFF", 300, 270, 200, 50, toggle_music),
    Button("Sair", 300, 340, 200, 50, exit_game),
]

def restart_game():
    global game_state, hero, hero_speed_x, hero_speed_y, on_ground
    hero = Rect((100, HEIGHT - 100), (40, 40))  # Reinicia a posição do herói
    hero_speed_x = 0
    hero_speed_y = 0
    on_ground = False
    game_state = "menu"  # Volta para o menu inicial

# Botões da tela de vitória
winner_buttons = [
    Button("Restart", 300, 300, 200, 50, restart_game),
    Button("Sair", 300, 370, 200, 50, exit_game),
]

def draw():
    screen.clear()
    if game_state == "menu":
        music.play("bg")  # Toca a música de fundo no menu
        sounds.win.stop()
        screen.blit(background, (0, 0))
        screen.draw.text("FOREST JUMP", center=(WIDTH // 2, 100), fontsize=60, color="white")
        for button in buttons:
            button.draw()
    elif game_state == "playing":
        screen.blit(background, (0, 0))
        screen.draw.filled_rect(platform, (100, 255, 100))
        screen.draw.filled_rect(hero, hero_color)
        screen.draw.filled_rect(goal, (0, 255, 0))
        screen.draw.text("Press SPACE to jump", (10, 10), fontsize=24, color="white")

        # Desenhar obstáculos
        for obstacle in obstacles:
            screen.draw.filled_rect(obstacle, (255, 0, 0))

        # Desenhar inimigos
        for enemy in enemies:
            screen.draw.filled_rect(enemy["rect"], (255, 255, 0))

    elif game_state == "winner":
        screen.clear()
        sounds.win.play()
        screen.blit(background, (0, 0))
        screen.draw.text("Parabéns! Você venceu!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=60, color="black")
        for button in winner_buttons:
            button.draw()

def update():
    global hero_speed_y, on_ground, hero_speed_x, game_state  # Mova esta linha para o início da função

    if game_state == "playing":
        # Gravidade
        hero_speed_y += gravity
        hero.y += hero_speed_y

        # Movimento lateral
        hero.x += hero_speed_x

        # Colisão com o chão
        if hero.colliderect(platform):
            hero.bottom = platform.top
            hero_speed_y = 0
            on_ground = True
        else:
            on_ground = False

        # Colisão com obstáculos
        for obstacle in obstacles:
            if hero.colliderect(obstacle):
                if hero_speed_y > 0:
                    hero.bottom = obstacle.top + 0.5
                    hero_speed_y = 0
                    on_ground = True
                elif hero_speed_y < 0:
                    hero.top = obstacle.bottom
                    hero_speed_y = 0

                if hero_speed_x > 0 and hero.right >= obstacle.left and hero.left < obstacle.left:
                    hero.right = obstacle.left
                elif hero_speed_x < 0 and hero.left <= obstacle.right and hero.right > obstacle.right:
                    hero.left = obstacle.right

        # Impedir que saia da tela
        if hero.left < 0:
            hero.left = 0
        if hero.right > WIDTH:
            hero.right = WIDTH

        # Mover inimigos
        for enemy in enemies:
            enemy["rect"].x += enemy["speed"]

            # Inverter direção ao atingir as bordas da plataforma
            if enemy["rect"].left < platform.left or enemy["rect"].right > platform.right:
                enemy["speed"] *= -1

            # Colisão com o personagem
            if hero.colliderect(enemy["rect"]):
                reset_game()

        # Verificar colisão com o objetivo
        if hero.colliderect(goal):
            game_state = "winner"

def reset_game():
    global hero, hero_speed_x, hero_speed_y, on_ground
    hero = Rect((100, HEIGHT - 100), (40, 40))
    hero_speed_x = 0
    hero_speed_y = 0
    on_ground = False
    print("Você foi derrotado! Reiniciando o jogo...")

def on_key_down(key):
    global hero_speed_y, hero_speed_x
    if game_state == "playing":
        if key == keys.LEFT:
            hero_speed_x = -5
        elif key == keys.RIGHT:
            hero_speed_x = 5
        elif key == keys.SPACE and on_ground:
            hero_speed_y = jump_strength
            sounds.jump.play()  # Toca o som de pulo
            
def on_key_up(key):
    global hero_speed_x
    if game_state == "playing":
        if key in [keys.LEFT, keys.RIGHT]:
            hero_speed_x = 0

def on_mouse_down(pos):
    if game_state == "menu":
        for button in buttons:
            button.check_click(pos)
    elif game_state == "winner":
        for button in winner_buttons:
            button.check_click(pos)

pgzrun.go()