"""
Noah Garcia

Period 4

Asteroid Dodge

The user utilizes w,a,s,d to move around and dodge asteroids that spawn at the
top of the screen. If the spaceship collides with an asteroid, they get a game
over screen, a score, and play again button. If they survive 50 asteroids, they
get a victory screen, a score, and a play again button.

Inputs - w,a,s,d to move spaceship and mouse click to play again
"""

# Import the libraries
import pygame
import random
import sys

pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Dodge")

# Set the colors needed in the game to constants
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Set up the clock
clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont(None, 48)

# Create and draw the ship
ship_img = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.polygon(ship_img, WHITE, [(25, 0), (0, 50), (50, 50)])
ship_rect = ship_img.get_rect()

class Asteroid(pygame.sprite.Sprite):
    """
    Creates the asteroids that the player has to dodge
    """
    def __init__(self, survived_counter):
        """
        Creates the asteroids
        :param image: the asteroid is drawn on the screen
        :param rect:
        :param rect.x: the randomized x positon of the asteroid
        :param rect.y: the y position of the asteroid
        :param speed: the random speed of the asteroid
        :param survived_counter: the amount of asteroids survived
        """
        super().__init__()
        self.image = pygame.Surface((40, 40))
        pygame.draw.circle(self.image, RED, (20, 20), 20)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = -40
        self.speed = random.randint(20, 30)
        self.survived_counter = survived_counter

    def update(self):
        """
        Determines if an asteroid is survived

        Params:
            - none
        """
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.survived_counter[0] += 1
            self.kill()

def draw_text(text, size, color, center):
    """
    Creates a text label that outputs on the screen

    Params:
        text - the text to be displayed
        size - the size of the text
        color - the color of the displayed text
        center - where the text is placed on the screen
    Returns:
        - a text displayed on the pygame screen
    """    
    font_obj = pygame.font.SysFont(None, size)
    surface = font_obj.render(text, True, color)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)

def draw_button(text, rect, color):
    """
    Creates and draws a button

    Params:
        text - the text displayed on the button
        rect - where the button is displayed on the screen
        color - the color of the button
    Returns:
        - a button with text displayed on the screen
    """
    pygame.draw.rect(screen, color, rect)
    draw_text(text, 36, WHITE, rect.center)

def main():
    """
    Sets up player movement, determines if the game is won or lost, sets up the
    background, draws all the text and buttons, counts the number of asteroids
    survived, keeps track of the player's score.

    Params:
        - none

    Returns:
        - a working asteroid dodging game
    """

    # Sets the variables needed for the game
    ship_rect.center = (WIDTH // 2, HEIGHT - 60)
    speed = 5
    asteroid_group = pygame.sprite.Group()
    survived = [0]
    asteroid_timer = 0
    game_over = False
    victory = False

    # Creates the background
    while True:
        screen.fill(BLACK)

        # If the game is exited, the game ends
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Determines if a key is pressed and if w,a,s,d are, then the player
        # moves
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            ship_rect.x -= speed
        if keys[pygame.K_d]:
            ship_rect.x += speed
        if keys[pygame.K_w]:
            ship_rect.y -= speed
        if keys[pygame.K_s]:
            ship_rect.y += speed

        ship_rect.clamp_ip(screen.get_rect())

        asteroid_timer += 1
        if asteroid_timer >= 30:
            asteroid_group.add(Asteroid(survived))
            asteroid_timer = 0

        asteroid_group.update()

        
        # Determines if the player collides with an asteroid or not
        for asteroid in asteroid_group:
            if ship_rect.colliderect(asteroid.rect):
                game_over = True
                break

        # Draws the text label showing how many asteroids survived
        screen.blit(ship_img, ship_rect)
        asteroid_group.draw(screen)
        draw_text(f"Survived: {survived[0]}/50", 32, WHITE, (120, 30))

        # If the player survives 50 asteroids, they win
        if survived[0] >= 50:
            victory = True

        # If the player collides with an asteroid, they lose
        if game_over or victory:
            break

        pygame.display.flip()
        clock.tick(FPS)

    while True:
        screen.fill(BLACK)
        # If the user collides with an asteroid
        if game_over:
            draw_text("GAME OVER", 64, RED, (WIDTH // 2, HEIGHT // 3))
            draw_text("SCORE: " + str(survived[0]), 40, WHITE, (WIDTH // 2, HEIGHT // 2.5))

        # If the user survives 50 asteroids
        else:
            draw_text("VICTORY!", 64, GREEN, (WIDTH // 2, HEIGHT // 3))
            draw_text("SCORE: " + str(survived[0]), 40, WHITE, (WIDTH // 2, HEIGHT // 2.5))

        # Draws the play again button
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
        draw_button("Play Again", button_rect, GREEN)

        # Keeps track of mouse position
        for event in pygame.event.get():\
            # Closes the game window if the window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If the play again button is clicked, the game restarts
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(FPS)

while True:
    main()



