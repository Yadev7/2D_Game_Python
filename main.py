from ursina import *

app = Ursina()


# Load textures and set up variables
player_texture = load_texture('assets/ball.jpg')
obstacle_texture = load_texture('assets/wallNew.jpg')
obstacle1_texture = load_texture('assets/wallNew.jpg')
obstacle_spacing = 2.5
obstacle_speed = 0.1
score = 0

last_game_score = score
scored_for_obstacle = False

obstacle_movement_enabled = True

# Create a background image
background = Entity(
    model='quad', texture='assets/bgame.jpg', scale=(16, 9), z=1)

# Create a background music
background_music = Audio('sounds/background_music.mp3',
                         loop=True, autoplay=True)

persia_level = Audio('sounds/persia.mp3', loop=False, autoplay=False)

game_over = Audio('sounds/game_over.mp3', loop=True, autoplay=False)

# Create a jump sound
jump_sound = Audio('sounds/jump_sound.mp3', loop=False, autoplay=False)

# Create a hit sound
hit_sound = Audio('sounds/hit_sound.mp3', loop=False, autoplay=False)


# Player entity
player = Entity(model='sphere', position=(-5, 1, 0),
                texture=player_texture, color=color.blue, scale=0.5, collider='box')
player.gravity = 0.2
player.jump_height = 3

# Obstacle list
obstacles = []

# Create initial obstacle
obstacle1 = Entity(model='cube', texture=obstacle_texture, color=color.brown, scale=(0.5, 3.5, 1),
                   position=(10, -1.2, 0), collider='box')
obstacles.append(obstacle1)

# UI elements
game_over_message = Text(text="Game Over!", color=color.white, scale=2, origin=(0, -3),
                         enabled=False)

restart = Text(text="Press 'r' to restart the game",  color=color.white, scale=2, origin=(0, -3),
                    enabled=False)

you_lose_message = Text(text="You Lose!", color=color.white, scale=2, origin=(0, -3),
                        enabled=False)

# Score
score_text = Text(text="Scoree: " + str(score), color=color.white,
                  scale=2, origin=(3.5, -9), enabled=True)

# Display the last game's score
your_score = Text(text="Your score: " + str(last_game_score), color=color.white,
                  scale=2, origin=(0, -1), enabled=False)

# Display the name of creator
creator = Text(text="Created by Yassine Abdelouafi ", color=color.yellow,
               scale=1, origin=(0, -18), enabled=True)

# level_number = Text(text="Level: " + str(level_number), color=color.white,
#                     scale=2, origin=(0, -3), enabled=True)

# Create a function to generate bold text


def create_bold_text(text, position, scale, color):
    for i in range(3):  # Draw text multiple times with slight offsets
        text_entity = Text(text=text, position=position +
                           (i, -i), scale=scale, color=color)
        text_entity.origin = text_entity.width / 2, text_entity.height / 2


# Functions


def restart_game():
    global obstacle_spawn_timer, score, obstacle_speed
    score = 0  # Reset score to 0

    background_music.play()
    background.texture = 'assets/bgame.jpg'
    player.texture = player_texture
    player.color = color.blue
    game_over_message.disable()

    game_over.stop()
    player.enable()
    score_text.text = "Score: " + str(score)  # Update the displayed score
    creator.text = "Created by Yassine Abdelouafi"
    # Reset player to the starting position
    game_over_message.disable()  # Disable the lose message when restarting
    # Create a new initial obstacle
    obstacle1 = Entity(model='cube', texture=obstacle1_texture, color=color.brown, scale=(
        0.5, 3.5, 1), position=(10, -1.2, 0), collider='box')
    obstacles.append(obstacle1)
    player.position = (-5, -1.4, 0)
    your_score.enabled = False
    if score == 0:
        obstacle_speed = 0.1


def move_obstacles():
    global score, scored_for_obstacle
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed
    if obstacles and obstacles[0].x < -10:
        old_obstacle = obstacles.pop(0)
        old_obstacle.disable()
        spawn_obstacle()
        scored_for_obstacle = False  # Allow scoring for the new obstacle


def spawn_obstacle():
    new_obstacle = Entity(model='cube', texture=obstacle_texture, color=color.brown, scale=(0.5, 3.5, 1),
                          position=(10, -1.2, 0), collider='box')
    obstacles.append(new_obstacle)


last_game_score = 0
# Define a function to stop the game


def stop_game():
    global obstacle_movement_enabled, last_game_score
    obstacle_movement_enabled = False
    player.disable()
    game_over_message.enable()
    held_keys['space'] = False
    obstacles.clear()  # Clear the list of obstacles
    last_game_score = score  # Store the last game's score
    score_text.text = "Score: " + str(score)  # Update the displayed score
    background_music.stop()
    game_over.play()


score_reached_zero = False
persia_level_playing = False


def update():

    global scored_for_obstacle, score, obstacle_movement_enabled, persia_level_playing

    if player.y > 0:
        player.y -= player.gravity
    else:
        player.y = 0

   # Check for collisions and update score
    for obstacle in obstacles:
        if player.intersects(obstacle).hit:
            hit_sound.play()
            background_music.stop()
            persia_level.stop()
            # persia_level.stop()
            game_over.play()
            # Stop the game and store the last game's score
            global obstacle_movement_enabled, last_game_score, obstacle_speed, background
            last_game_score = score
            your_score.enabled = True
            # print(last_game_score)
            obstacle_movement_enabled = False
            held_keys['space'] = False
            obstacles.remove(obstacle)
            obstacle.disable()
            player.disable()
            if score == 0 and last_game_score == 0:
                game_over_message.disable()
                your_score.text = "You Lose! Press 'r' to restart the game"
            else:
                game_over_message.enable()
                your_score.text = "Your score: " + str(last_game_score)
            score = 0
            score_text.text = "Score: " + str(score)

    # Check if player has cleared an obstacle and score
    if obstacles and player.x > obstacles[0].x + obstacle_spacing and not scored_for_obstacle:
        score += 1
        scored_for_obstacle = True
        score_text.text = "Score: " + str(score)
        score_text.enable()
        # # Check if the score is 5 and update obstacle_speed
        # if score == 10:
        #     obstacle_speed = 0.2  # Set the new obstacle speed value
        # if score == 50:
        #     obstacle_speed = 0.3  # Set the new obstacle speed value

        # if score == 100:
        #     obstacle_speed = 0.3  # Set the new obstacle speed value

        for obstacle in obstacles:
            obstacle.color = color.blue
            obstacle_speed = 0.1

        # Change the background to 'persia.jpg' when score is 10
        if score > 2:

            player.color = color.gold
            background.texture = 'assets/persia.jpg'
            obstacle_speed = 0.2
            persia_level.play()

            for obstacle in obstacles:
                obstacle.color = color.gold
                background_music.stop()
                persia_level_playing = True
    # Move player left and right
    if held_keys['left mouse']:
        player.x -= 0.1
    if held_keys['right mouse']:
        player.x += 0.1

    if held_keys['escape']:
        application.quit()

    # Jump when the spacebar is pressed
    if player.y == 0:
        if held_keys['middle mouse']:
            jump_sound.play()
            player.animate_y(player.jump_height, duration=0.2,
                             curve=curve.out_expo)

    # Move obstacles and spawn new obstacles
    move_obstacles()


# Key input
def input(key):
    if held_keys['r']:
        restart_game()


app.run()
