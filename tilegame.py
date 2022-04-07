import pygame
import pygame.locals
from json import load
from os.path import exists
from random import randint

if exists("settings.json"):
    with open("settings.json") as f:
        settings = load(f)
else:
    print("There needs to be a settings.json file with the settings to run this game")
    exit()

class Game:

    health = 100
    win = False
    lose = False
    fight_chance = 0
    right = False
    left = False
    up = False
    down = False
    draw = None
    
    def __init__(self, screen, size):
        self.screen = screen
        img = pygame.image.load(settings["grass"]).convert()
        d = min(img.get_width(), img.get_height())
        self.grass = pygame.transform.scale(img.subsurface((0, 0, d, d)), (50, 50))
        self.xsize = settings["xscale"] * self.grass.get_width()
        self.ysize = settings["yscale"] * self.grass.get_height()
        self.player = pygame.transform.scale(pygame.image.load(settings["player"]).convert_alpha(), (20, 40))
        self.weapon = pygame.transform.scale(pygame.image.load(settings["weapon"]).convert_alpha(), (25, 25))
        img = pygame.image.load(settings["monster"]).convert()
        img = img.subsurface((0, 0, img.get_width(), img.get_height() - 20))
        self.monster = pygame.transform.scale(img, (40, 40))
        self.beat_monster = pygame.transform.scale(img, (40, 10))
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.size = size - 1
        coords = []
        for x in range(size):
            for y in range(size):
                coords.append((x, y))
        rand = lambda: coords.pop(randint(0, len(coords) - 1))
        self.player_x, self.player_y = rand()
        self.trophy = rand()
        self.weapons = set()
        for _ in range(settings["weapons"]):
            self.weapons.add(rand())
        self.monsters = set()
        for _ in range(settings["monsters"]):
            self.monsters.add(rand())

    def move(self, keys):
        move = False
        if keys[pygame.K_RIGHT]:
            if not self.right and self.player_x < self.size:
                self.right = True
                self.player_x += 1
                move = True
        else:
            self.right = False
        if keys[pygame.K_LEFT]:
            if not self.left and self.player_x > 0:
                self.left = True
                self.player_x -= 1
                move = True
        else:
            self.left = False
        if keys[pygame.K_UP]:
            if not self.up and self.player_y > 0:
                self.up = True
                self.player_y -= 1
                move = True
        else:
            self.up = False
        if keys[pygame.K_DOWN]:
            if not self.down and self.player_y < self.size:
                self.down = True
                self.player_y += 1
                move = True
        else:
            self.down = False
        if move:
            self.draw = None
            self.check_tile()
        elif self.draw:
            self.screen.blit(*self.draw)

    def check_tile(self):
        coord = self.player_x, self.player_y
        if coord == self.trophy:
            print("YOU FOUND THE TROPHY AND WON!")
            self.win = True
        elif coord in self.monsters:
            if randint(0, 100) <= self.fight_chance:
                self.monsters.remove(coord)
                self.fight_chance += 4
                self.draw = self.beat_monster, (self.player_x * self.xsize + 25, self.player_y * self.ysize + 5)
                self.screen.blit(*self.draw)
                print(f"You found a monster and beat it! You gained 4% attack! You have {self.fight_chance}% attack.")
            else:
                self.health -= 10
                self.draw = self.monster, (self.player_x * self.xsize + 25, self.player_y * self.ysize + 5)
                self.screen.blit(*self.draw)
                if self.health > 0:
                    print(f"You ran into a monster and it dealt 10 damage to you! You have {self.health} health.")
                else:
                    print("You ran into a monster and it killed you. GAME OVER.")
                    self.lose = True
        elif coord in self.weapons:
            self.fight_chance += 10
            self.weapons.remove(coord)
            self.draw = self.weapon, (self.player_x * self.xsize + 25, self.player_y * self.ysize + 5)
            self.screen.blit(*self.draw)
            print(f"You found a weapon and gained 10% attack! You have {self.fight_chance}% attack.")

def play():
    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    g = Game(screen, 9)
    screen.fill((0, 0, 0))
    while not (g.win or g.lose):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                g.lose = True
        for x in range(9):
            for y in range(9):
                screen.blit(g.grass, (x * g.xsize, y * g.ysize))
        screen.blit(g.player, (g.player_x * g.xsize + 10, g.player_y * g.ysize + 5))
        g.move(pygame.key.get_pressed())
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    while input("Play? [Y/N]: ").upper() == "Y":
        play()
