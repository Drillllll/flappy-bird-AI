import random
import pygame.transform
import neat
import os
import matplotlib.pyplot as plt

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

# # Grupa obiektów
all_sprites = pygame.sprite.Group()
#
# # Tworzenie ptaka i dodawanie do grupy obiektów
# bird = Bird(50, 200)
# all_sprites.add(bird)

# Tworzenie rur i dodawanie do grupy obiektów
pipe_group = pygame.sprite.Group()

#Statystyki
my_stats = []


# Funkcja do generowania rur
def generate_pipes():
    pipe_gap = 90 # Odstęp pomiędzy rurami
    pipe_y = random.randint(-200, 0)
    pipe_bottom = Pipe(WIDTH, pipe_y, flipped=True)
    pipe_top = Pipe(WIDTH, pipe_y + pipe_bottom.rect.height + pipe_gap)
    pipe_group.add(pipe_bottom)
    pipe_group.add(pipe_top)
    all_sprites.add(pipe_bottom)
    all_sprites.add(pipe_top)


# Główna pętla gry
def eval_genomes(genomes, config):

    nets = []
    ge = []
    # bird = Bird(50, 200)
    birds = []
    # all_sprites.add(bird)
    running = True
    clock = pygame.time.Clock()
    score = 0
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(50, 200))
        g.fitness = 0
        ge.append(g)

    if(len(pipe_group) > 0):
        for p in pipe_group:
            pipe_group.remove(p)
            all_sprites.remove(p)

    while running and len(birds) > 0:
        clock.tick(10000)

        # Generowanie nowych rur
        if len(pipe_group) < 2:
            generate_pipes()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         bird.flap()

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipe_group) > 1 and birds[0].rect.x > pipe_group.sprites()[1].rect.x + pipe_group.sprites()[
                1].image.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        # Aktualizacja obiektów !!!!! dla kazdego ptatak
        for x, bird in enumerate(birds):
            bird.update()
            ge[x].fitness += 0.1
            if not pipe_group.sprites()[0].passed:
                output = nets[x].activate((bird.rect.y, abs(bird.rect.y - pipe_group.sprites()[1].rect.y),
                                           abs(bird.rect.y - pipe_group.sprites()[0].rect.y)))
                if output[0] > 0.5:
                    bird.flap()
            else:
                if abs(bird.rect.y - HEIGHT) < 200:
                    bird.flap()


        all_sprites.update()

        # Sprawdzanie kolizji ptaka z rurami
        for x, bird in enumerate(birds):
            if pygame.sprite.spritecollide(bird, pipe_group, False):  # Collision
                ge[x].fitness -= 1
                #HEHEHEE
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                # running = False

            # Sprawdzanie, czy ptak przeleciał przez rurę
            for pipe in pipe_group:
                if pipe.rect.right < bird.rect.left and not pipe.passed and pipe.rect.left < bird.rect.left:
                    pipe.passed = True
                    score += 1
                    ge[x].fitness += 10

            # Sprawdzanie, czy ptak wyszedł poza ekran
            if bird.rect.y > HEIGHT or bird.rect.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
                # running = False

        # Usuwanie rur, które wyszły poza ekran
        for pipe in pipe_group:
            if pipe.rect.right < 0:
                all_sprites.remove(pipe)
                pipe_group.remove(pipe)

        # # Generowanie nowych rur
        # if len(pipe_group) < 2:
        #     generate_pipes()

        # Rysowanie obiektów na ekranie
        screen.blit(background_image, (0, 0))  # Narysowanie tła
        all_sprites.draw(screen)

        #print("Ile jest w tablicy: ", len(birds))
        #i = 0
        for bird in birds:
            screen.blit(bird.image, bird.rect)
            #i += 1
            #print("PTAK ",i, " X: ", bird.rect.x, " Y: ", bird.rect.y)
        #print("Ile sie wyswietlaa: ", i)


        # Wyświetlanie wyniku
        score_text = font.render("Score: " + str(score/2), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Aktualizacja ekranu
        pygame.display.flip()
        #clock.tick(60)
    my_stats.append(score/2)




def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 20)

    # show final stats
    #print('\nBest genome:\n{!s}'.format(winner))

    for i in range(len(my_stats)):
        print(my_stats[i])

    # Tworzenie wykresu punktowego
    plt.scatter(range(len(my_stats)), my_stats)

    # Dodanie etykiet osi x i y
    plt.xlabel('Generacja')
    plt.ylabel('Wynik')

    # Wyświetlenie wykresu
    plt.show()


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
