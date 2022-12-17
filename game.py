import os
import tty
import sys
import termios

# Define some constants for the game
WALL_CHAR = u'\u2622'  # Full block character
DOOR_CHAR = u'\u2591'
PLAYER_CHAR = u'\u2622'  # Unicode character for 'person'
MONSTER_CHAR = u'\u2622'
TREASURE_CHAR = u'\u26cf'
FLOOR_CHAR = u'\u0020'

ROOM_WIDTH = 5
ROOM_HEIGHT = 5

class Tile:
    def __init__(self, type, monster=None, treasure=None, additional=None):
        self.type = type
        self.monster = monster
        self.treasure = treasure
        self.additional = additional
    
game_world = [[Tile('wall'), Tile('wall'), Tile('door'), Tile('wall'), Tile('door'), Tile('wall'), Tile('wall'), Tile('door'), Tile('wall'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('treasure', 'gold coins'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('wall'), Tile('door'), Tile('wall'), Tile('door'), Tile('wall'), Tile('wall'), Tile('door'), Tile('wall'), Tile('wall')]]


# Place the player in the center of the room
player_x = ROOM_WIDTH // 2
player_y = ROOM_HEIGHT // 2


old_settings = None
fd = None

# Function to draw the room to the terminal
def draw_game_world():
    # Clear the screen
    sys.stdout.write('\x1b[2J')

    tile_mapping = {
        'player' : PLAYER_CHAR,
        'wall': WALL_CHAR,
        'door': DOOR_CHAR,
        'floor': FLOOR_CHAR,
        'monster': MONSTER_CHAR,
        'treasure': TREASURE_CHAR,
    }
    
    for y, row in enumerate(game_world):
        for x, tile in enumerate(row):
            # Draw the player
            if x == player_x and y == player_y:
                sys.stdout.write(f'\x1b[{y + 1};{x + 1}H{PLAYER_CHAR}')
            # Draw other tiles using the mapping
            else:
                sys.stdout.write(f'\x1b[{y + 1};{x + 1}H{tile_mapping[tile.type]}')
                
    # Refresh the screen
    sys.stdout.flush()
   
def check_collision(player_x, player_y):
    # Get the tile the player is currently standing on
    tile = game_world[player_y][player_x]
    tile_type = tile.type
    additional_info = tile.additional
    
    if tile_type == 'wall':
        # Player cannot walk through walls
        return True
    elif tile_type == 'door':
        if additional_info == 'unlocked':
            # Player can walk through unlocked doors
            return False
        else:
            # Player cannot walk through locked doors
            return True
    else:
        # Player can walk on floor tiles
        return False 

# Function to move the player
def move_player(dx, dy):
    global player_x, player_y

    # Calculate the new position of the player
    new_x = player_x + dx
    new_y = player_y + dy

    if not check_collision(new_x, new_y):
        # Update the player's position and redraw the room
        player_x = new_x
        player_y = new_y
         
    draw_game_world()
    return True

# Main game loop
def main():
    global player_x, player_y

    # Save the terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    # Set the terminal to raw input mode
    new_settings = termios.tcgetattr(fd)
    new_settings[tty.LFLAG] &= ~(termios.ICANON | termios.ECHO)
    termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
    
    try:
        while True:
            # Wait for a key press
            ch = os.read(fd, 1)

            # Handle the arrow keys
            if ch == b'\x1b':
                ch2 = os.read(fd, 1)
                if ch2 == b'[':
                    ch3 = os.read(fd, 1)
                    if ch3 == b'A':
                        # Up arrow
                        move_player(0, -1)
                    elif ch3 == b'B':
                        # Down arrow
                        move_player(0, 1)
                    elif ch3 == b'C':
                        # Right arrow
                        move_player(1, 0)
                    elif ch3 == b'D':
                        # Left arrow
                        move_player(-1, 0)
                        
    finally:
        # Restore the terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == '__main__':
    # Initialize the room
    draw_game_world()
    
    # Run the main game loop
    try:
        main()  
    except KeyboardInterrupt:
        # Restore the terminal settings on exit
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.exit(0)