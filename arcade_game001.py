"""
Sprite Collect Coins

Simple program to show basic sprite usage.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_collect_coins
"""

import random
import arcade

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
SPRITE_SCALING_ENEMY = 1
COIN_COUNT = 1500

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = "결전!! Jormungand VS Human!!"

class Jormungand(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        # Move the Jormungand
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1

class Coin(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.change_x = 0
        self.change_y = 0

    def update(self):

        # Move the Coin
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > SCREEN_WIDTH:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > SCREEN_HEIGHT:
            self.change_y *= -1


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.all_sprites_list = None
        self.player_list = None
        self.enemy_list = None
        self.coin_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.game_ended = False
        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        img = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.all_sprites_list.append(self.player_sprite)


        # 적을 만든다
        img = "요르문간드.png"
        self.enemy_sprite = Jormungand(img, SPRITE_SCALING_ENEMY)
        self.enemy_sprite.center_x = 500
        self.enemy_sprite.center_y = 500
        self.enemy_sprite.change_x = random.randrange(-3, 4)
        self.enemy_sprite.change_y = random.randrange(-3, 4)
        self.enemy_list.append(self.enemy_sprite)
        self.all_sprites_list.append(self.enemy_sprite)

        # 동전을 만든다
        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin(":resources:images/items/coinGold.png",
                                 SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            coin.change_y = random.randrange(-1, 1)
            coin.change_x = random.randrange(-1, 1)
            # Add the coin to the lists
            self.coin_list.append(coin)
            self.all_sprites_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.coin_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(text=output, start_x=10, start_y=20,
                         color=arcade.color.WHITE, font_size=14)

        if self.game_ended == True:
            if len(self.coin_list) == 0:
                output = f"Game Cleared!!! Your Final Score is: {self.score}"
                arcade.draw_text(text=output, start_x=10, start_y=30,
                                color=arcade.color.BLUE, font_size=14)
                output = f"이녀석 제법이구만!!"
                arcade.draw_text(text=output, start_x=self.enemy_sprite.center_x, start_y=self.enemy_sprite.center_y,
                                color=arcade.color.BLACK, font_size=9)
                output = f"o^0^o"
                arcade.draw_text(text=output, start_x=self.player_sprite.center_x, start_y=self.player_sprite.center_y,
                                color=arcade.color.BROWN, font_size=9)
            if self.score < -300:
                output = f"Game Over!!! Your Final Score is: {self.score}"
                arcade.draw_text(text=output, start_x=10, start_y=30,
                                color=arcade.color.RED, font_size=14)
                output = f"으하하하 멍청한 녀석!!!"
                arcade.draw_text(text=output, start_x=self.enemy_sprite.center_x, start_y=self.enemy_sprite.center_y,
                                color=arcade.color.BLACK, font_size=9)
                output = f"ㅠ-ㅠ"
                arcade.draw_text(text=output, start_x=self.player_sprite.center_x, start_y=self.player_sprite.center_y,
                                color=arcade.color.BROWN, font_size=9)


    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.game_ended == False:
            self.all_sprites_list.update()

            # Generate a list of all sprites that collided with the player.
            coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                self.coin_list)

            # Loop through each colliding sprite, remove it, and add to the score.
            for coin in coins_hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1

            # Generate a list of all sprites that collided with the player.
            enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                self.enemy_list)

            # Loop through each colliding sprite, remove it, and add to the score.
            for coin in enemy_hit_list:
                # coin.remove_from_sprite_lists()
                self.score -= 1
        
            if len(self.coin_list) == 0:
                self.game_ended = True
            if self.score < -300:
                self.game_ended = True



def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()