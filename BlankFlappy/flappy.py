import pygame
import random
import pygame.transform


# Inicjalizacja Pygame
pygame.init()

# Klasa reprezentująca ptaka
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/yellowbird-midflap.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 0
        self.gravity = 0.5

    def flap(self):
        self.velocity = -8

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

# Klasa reprezentująca rurę
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/pipe-green.png")
        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.passed = False

    def update(self):
        self.rect.x -= 3

# Ustawienia ekranu
WIDTH = 288
HEIGHT = 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Kolory
WHITE = (255, 255, 255)

# Wczytanie tła
background_image = pygame.image.load("assets/sprites/background-day.png")

# Grupa obiektów
all_sprites = pygame.sprite.Group()

# Tworzenie ptaka i dodawanie do grupy obiektów
bird = Bird(50, 200)
all_sprites.add(bird)

# Tworzenie rur i dodawanie do grupy obiektów
pipe_group = pygame.sprite.Group()

# Funkcja do generowania rur
def generate_pipes():
    pipe_gap = 200  # Odstęp pomiędzy rurami
    pipe_y = random.randint(-200, 0)
    pipe_bottom = Pipe(WIDTH, pipe_y,flipped=True)
    pipe_top = Pipe(WIDTH, pipe_y + pipe_bottom.rect.height + pipe_gap)
    pipe_group.add(pipe_bottom)
    pipe_group.add(pipe_top)
    all_sprites.add(pipe_bottom)
    all_sprites.add(pipe_top)


# Główna pętla gry
running = True
clock = pygame.time.Clock()
score = 0
pygame.font.init()
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # Aktualizacja obiektów
    all_sprites.update()

    # Sprawdzanie kolizji ptaka z rurami
    if pygame.sprite.spritecollide(bird, pipe_group, False):
        running = False

    # Sprawdzanie, czy ptak przeleciał przez rurę
    for pipe in pipe_group:
        if pipe.rect.right < bird.rect.left and not pipe.passed and pipe.rect.left < bird.rect.left:
            pipe.passed = True
            score += 1

    # Usuwanie rur, które wyszły poza ekran
    for pipe in pipe_group:
        if pipe.rect.right < 0:
            all_sprites.remove(pipe)
            pipe_group.remove(pipe)

    # Generowanie nowych rur
    if len(pipe_group) < 2:
        generate_pipes()

    # Sprawdzanie, czy ptak wyszedł poza ekran
    if bird.rect.y > HEIGHT:
        running = False

    # Rysowanie obiektów na ekranie
    screen.blit(background_image, (0, 0))  # Narysowanie tła
    all_sprites.draw(screen)

    # Wyświetlanie wyniku
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Aktualizacja ekranu
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
