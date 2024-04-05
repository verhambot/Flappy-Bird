# Python program for Flappy Bird


# Import libraries
import pygame
import os
import random

# Initialize Pygame
pygame.init()


# Load images
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]
START_BIRD_IMGS = [
    pygame.transform.scale(
        pygame.image.load(os.path.join("imgs", "bird1.png")), (272, 192)
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("imgs", "bird2.png")), (272, 192)
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("imgs", "bird3.png")), (272, 192)
    ),
    pygame.transform.scale(
        pygame.image.load(os.path.join("imgs", "bird2.png")), (272, 192)
    ),
]

# Load fonts
SCORE_MENU_FONT = pygame.font.Font(os.path.join("fonts", "JetBrains.ttf"), 30)
END_FONT = pygame.font.Font(os.path.join("fonts", "JetBrains.ttf"), 50)
START_FONT = pygame.font.Font(os.path.join("fonts", "JetBrains.ttf"), 70)

# Define colour constants (rgb)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (94, 226, 112)

# Define window dimensions
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 550, 800

# Define frame rate
FPS = 30


# Bird class
class Bird:

    # Define constant values
    IMGS = BIRD_IMGS
    MAX_UP_TILT = 25
    TILT_VEL = 12
    IMG_TIME = 5

    # Init function
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.tilt_deg = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.health_count = 250

    # Function to make bird jump
    def jump(self):

        # Set tick count to 0 (reset)
        self.tick_count = 0

        # Give bird an upward velocity
        self.vel = -10

    # Function to move bird
    def move(self):

        # Increment tick count
        self.tick_count += 1

        # Calculate displacement
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # Limit maximum displacement to 15
        if displacement >= 15:
            displacement = 15

        # Increase height by displacement
        self.y += displacement

        # If bird is moving up, tilt bird upwards
        if displacement < 0:
            self.tilt_deg = self.MAX_UP_TILT

        # If bird is moving down, tilt bird downwards (90 deg)
        else:
            if self.tilt_deg > -90:
                self.tilt_deg -= self.TILT_VEL

    # Function to draw bird
    def draw(self, win):

        # Increase image count
        self.img_count += 1

        # Set bird image based on image count to animate the bird
        if self.img_count < self.IMG_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.IMG_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.IMG_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.IMG_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.IMG_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If bird is moving down, set bird image to be non-animated
        if self.tilt_deg <= -85:
            self.img = self.IMGS[1]
            self.img_count = self.IMG_TIME * 2

        # Rotate image around its center
        rotated_img, rotated_rect = rotateImg(self.img, self.tilt_deg, self.x, self.y)

        # Draw bird on window
        win.blit(rotated_img, rotated_rect)

    # Function to get mask of bird - pixel perfect collision
    def getMask(self):

        return pygame.mask.from_surface(self.img)


# Pipe class
class Pipe:

    # Define constant values
    PIPE_GAP = 200
    PIPE_VEL = 5

    # Init function
    def __init__(self, x):

        self.x = x
        self.height = 0

        self.top_loc = 0
        self.bottom_loc = 0

        self.TOP_PIPE = pygame.transform.flip(PIPE_IMG, False, True)
        self.BOTTOM_PIPE = PIPE_IMG

        self.has_passed = False

        self.setHeight()

    # Function to randomly set height of pipes
    def setHeight(self):

        # Generate random value for pipe height
        self.height = random.randrange(50, 450)

        # Set y-coordinate of top pipe and bottom pipe
        self.top = self.height - self.TOP_PIPE.get_height()
        self.bottom = self.height + self.PIPE_GAP

    # Function to move pipe
    def move(self):

        # Change x-coordinate by pipe velocity
        self.x -= self.PIPE_VEL

    # Function to draw pipe
    def draw(self, win):

        # Draw top pipe and bottom pipe on window
        win.blit(self.TOP_PIPE, (self.x, self.top))
        win.blit(self.BOTTOM_PIPE, (self.x, self.bottom))

    # Function to get mask of pipe - pixel perfect collision
    def getMask(self):

        return (
            pygame.mask.from_surface(self.TOP_PIPE),
            pygame.mask.from_surface(self.BOTTOM_PIPE),
        )


# Base class
class Base:

    # Define constant values
    BASE_VEL = 5
    BASE_WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    # Init function
    def __init__(self, y):

        self.y = y
        self.x1 = 0
        self.x2 = self.BASE_WIDTH

    # Function to move base
    def move(self):

        # Change x-coordinate by base velocity
        self.x1 -= self.BASE_VEL
        self.x2 -= self.BASE_VEL

        # Reset base positions - to make base appear moving
        if self.x1 + self.BASE_WIDTH < 0:
            self.x1 = self.x2 + self.BASE_WIDTH

        if self.x2 + self.BASE_WIDTH < 0:
            self.x2 = self.x1 + self.BASE_WIDTH

    # Function to draw base
    def draw(self, win):

        # Draw both bases on window
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


# Function to rotate image around center
def rotateImg(img, tilt, x, y):

    new_img = pygame.transform.rotate(img, tilt)
    new_rect = new_img.get_rect(center=img.get_rect(topleft=(x, y)).center)

    return new_img, new_rect


# Function to check if bird collides with pipe
def maskCollide(bird, pipe):

    # Get masks of bird and pipe
    bird_mask = bird.getMask()
    top_mask, bottom_mask = pipe.getMask()

    # Calculate offset (distance) between bird and pipes
    top_offset = (pipe.x - bird.x, pipe.top - round(bird.y))
    bottom_offset = (pipe.x - bird.x, pipe.bottom - round(bird.y))

    # Check collision points or overlap points
    top_point = bird_mask.overlap(top_mask, top_offset)
    bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)

    # If collision point or overlap point exists, return True
    if top_point or bottom_point:
        return True

    # Else, return False
    return False


# Function to draw Start Screen
def drawStartScreen(win):

    start_screen = True

    # Set image count and image time for bird
    start_screen_bird_count = 0
    start_screen_bird_time = 5

    while start_screen:

        for event in pygame.event.get():

            # If event is QUIT, then end program
            if event.type == pygame.QUIT:
                start_screen = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                # If 'q' is pressed, then end program
                if event.key == pygame.K_q:
                    start_screen = False
                    pygame.quit()
                    quit()

                # If 'SPACEBAR' is pressed, the end Start Screen loop
                if event.key == pygame.K_SPACE:
                    start_screen = False

        # Draw background image on window
        win.blit(BG_IMG, (0, -120))

        # Render some text
        title = START_FONT.render("Flappy Bird", True, BLACK)
        play_game = SCORE_MENU_FONT.render("Press SPACEBAR to play", True, BLACK)
        pause_game = SCORE_MENU_FONT.render("Press 'k' to pause", True, BLACK)

        # Draw some text on window
        win.blit(title, (int(WIN_WIDTH // 2 - title.get_width() // 2), 30))
        win.blit(play_game, (int(WIN_WIDTH // 2 - play_game.get_width() // 2), 400))
        win.blit(pause_game, (int(WIN_WIDTH // 2 - pause_game.get_width() // 2), 450))

        # Limit bird count to 19
        if start_screen_bird_count > 19:
            start_screen_bird_count = 0

        # Draw enlarged bird on Start Screen
        win.blit(
            START_BIRD_IMGS[start_screen_bird_count // start_screen_bird_time],
            (
                int(
                    WIN_WIDTH // 2
                    - START_BIRD_IMGS[
                        start_screen_bird_count // start_screen_bird_time
                    ].get_width()
                    // 2
                ),
                140,
            ),
        )

        # Increase bird count
        start_screen_bird_count += 1

        # Update pygame display
        pygame.display.update()


# Function to draw Pause Screen
def drawPauseScreen(win):

    pause_screen = True

    while pause_screen:

        # Render some text
        paused_text = START_FONT.render("PAUSED", True, BLACK)
        play_game = SCORE_MENU_FONT.render("Press SPACEBAR to play", True, BLACK)

        # Draw text on window
        win.blit(paused_text, (int(WIN_WIDTH // 2 - paused_text.get_width() // 2), 200))
        win.blit(play_game, (int(WIN_WIDTH // 2 - play_game.get_width() // 2), 400))

        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == pygame.QUIT:
                pause_screen = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                # If 'SPACEBAR' is pressed, continue the game
                if event.key == pygame.K_SPACE:
                    pause_screen = False

                if event.key == pygame.K_q:
                    pause_screen = False
                    pygame.quit()
                    quit()

        # Update display
        pygame.display.update()


# Function to draw End Screen
def drawEndScreen(win):

    global score

    # Get previous high score
    high_score = getHighScore()

    end_screen = True

    while end_screen:

        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == pygame.QUIT:
                end_screen = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                # If 'p' is pressed, continue the game
                if event.key == pygame.K_p:
                    end_screen = False

                if event.key == pygame.K_q:
                    end_screen = False
                    pygame.quit()
                    quit()

        # Render some text
        play_again = SCORE_MENU_FONT.render("Press 'p' to return to Start", True, BLACK)

        end_game = START_FONT.render("You died!", True, BLACK)

        current_score = SCORE_MENU_FONT.render(
            "Your score : {}".format(score), True, BLACK
        )

        high_score_display = SCORE_MENU_FONT.render(
            "High score : " + str(high_score), True, BLACK
        )

        # Draw background image on window
        win.blit(BG_IMG, (0, -120))

        # Draw text on window
        win.blit(play_again, (int(WIN_WIDTH // 2 - play_again.get_width() // 2), 400))
        win.blit(end_game, (int(WIN_WIDTH // 2 - end_game.get_width() // 2), 30))
        win.blit(
            current_score, (int(WIN_WIDTH // 2 - current_score.get_width() // 2), 200)
        )
        win.blit(
            high_score_display,
            (int(WIN_WIDTH // 2 - high_score_display.get_width() // 2), 300),
        )

        # Update display
        pygame.display.update()

    # When end screen quits, run the game again
    main()


# Function to get high score
def getHighScore():

    global score

    # Open high score file in read mode
    score_sheet = open("high_score.txt", "r")

    # Read the high score file
    high_score = score_sheet.readline()

    # If current score is greater than high score, then write current score to high score file
    if int(score) > int(high_score):

        # Close file
        score_sheet.close()

        # Open file in write mode and write current score to file
        score_sheet = open("high_score.txt", "w")
        score_sheet.write(str(int(score)))
        score_sheet.close()

    # Return high score
    return high_score


# Function to draw main game window
def drawMainWindow(win, bird, base, pipes, score):

    # Draw background image on window
    win.blit(BG_IMG, (0, -120))

    # Draw bird on window
    bird.draw(win)

    # Cycle through pipes list and access each Pipe object
    for pipe in pipes:

        # Draw each pipe
        pipe.draw(win)

    # Render score text and draw on window
    score_display = SCORE_MENU_FONT.render("Score : {}".format(score), True, WHITE)
    win.blit(score_display, (350, 10))

    # Draw the base
    base.draw(win)

    # Render and draw health of bird
    health_display = SCORE_MENU_FONT.render(
        "{}".format(int(bird.health_count / 250 * 100)), True, BLACK
    )
    win.blit(
        health_display,
        (470 + int((WIN_WIDTH - 480) // 2 - health_display.get_width() // 2), 730),
    )

    # Draw health bar
    pygame.draw.rect(win, RED, (10, 740, 450, 20))
    pygame.draw.rect(win, GREEN, (10, 740, 450 * bird.health_count // 250, 20))

    # Update display
    pygame.display.update()


# Function to run the game
def main():

    global score

    # Initialize game window
    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Flappy Bird")

    # Initialize clock
    clock = pygame.time.Clock()

    # Draw Start Screen
    drawStartScreen(win)

    run_game = True

    # Create bird, pipe, and base objects
    bird = Bird(230, 350)
    base = Base(680)
    pipes = [Pipe(600)]

    # Set initial score to 0
    score = 0

    # Variable the introduce some delay between death of bird and end of game
    delay_after_death = 0

    while run_game:

        # Variable to add a new pipe
        add_new_pipe = False

        # Run the game at a set FPS
        clock.tick(FPS)

        for event in pygame.event.get():

            # Check for QUIT events
            if event.type == pygame.QUIT:
                run_game = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    run_game = False

                # If 'k' is pressed, then pause the game
                if event.key == pygame.K_k:
                    drawPauseScreen(win)

        # Get a list of keys which are pressed
        pressed_keys = pygame.key.get_pressed()

        # If 'SPACEBAR' is pressed, then make the bird jump
        if pressed_keys[pygame.K_SPACE]:
            bird.jump()

        # Move bird
        bird.move()

        # Move the base
        base.move()

        # Access each pipe
        for pipe in pipes:

            # Move each pipe
            pipe.move()

            # If pipe moves off-screen, then remove it
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                pipes.pop(pipes.index(pipe))

            # If bird passes a pipe, then add a new pipe and increment score
            if not pipe.has_passed and bird.x > pipe.x + PIPE_IMG.get_width():
                pipe.has_passed = True
                add_new_pipe = True
                score += 1

            # If a pipe collides with a bird, then decrement the health of the bird
            if maskCollide(bird, pipe):

                if bird.health_count > 0:
                    bird.health_count -= 1

        # Add a new pipe by appending a Pipe object to the pipes list
        if add_new_pipe:
            pipes.append(Pipe(600))

        # If the bird collides with the base or moves off-screen, set health to 0
        if (
            bird.y + bird.img.get_height() > base.y
            or bird.y + bird.img.get_height() < 0
        ):
            bird.health_count = 0

        # If bird's health is less than or equal to 0, then increment delay_after_death variable
        if bird.health_count <= 0:

            delay_after_death += 1

            # Once delay_after_death variable becomes >= FPS (meaning that 1 second has passed), then draw the End Screen
            if delay_after_death >= FPS:
                run_game = False
                drawEndScreen(win)

        # Draw the main game window and all objects
        drawMainWindow(win, bird, base, pipes, score)

    # Once loop quits, quit Pygame and the program
    pygame.quit()
    quit()


# Running the main game function
main()
