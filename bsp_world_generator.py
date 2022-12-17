import random
import sys

# Constants for the game world
WIDTH = 80
HEIGHT = 80
MIN_ROOM_SIZE = 6
MAX_ROOM_SIZE = 15

'''game_world =  [[Tile('wall'), Tile('wall'), Tile('door'), Tile('wall'), Tile('door'), Tile('wall'), Tile('wall'), Tile('door'), Tile('wall'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('treasure', 'gold coins'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('floor'), Tile('wall')],
              [Tile('wall'), Tile('wall'), Tile('door'), Tile('wall'), Tile('door'), Tile('wall'), Tile('wall'), Tile('door'), Tile('wall'), Tile('wall')]]
'''

class Tile:
    def __init__(self, type, monster=None, treasure=None, additional=None):
        self.type = type
        self.monster = monster
        self.treasure = treasure
        self.additional = additional
        
class Node:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = None
        self.right = None

def generate_bsp_tree(node, depth):

    if node.width < MAX_ROOM_SIZE and node.height < MAX_ROOM_SIZE:
        print("node is acceptable size")
        print_node(node)
        return

    split_horizontally = random.random() < 0.5 
    
    if node.width < MAX_ROOM_SIZE:
        #cut height
        split_horizontally = True
    if node.height < MAX_ROOM_SIZE:
        #cut width
        split_horizontally = False
    
    if split_horizontally:
        # Calculate the maximum possible split position
        max_split = node.height - MIN_ROOM_SIZE
        #max_split = min(max_split, MAX_ROOM_SIZE - MIN_ROOM_SIZE)
        print(max_split)
        
        if max_split < MIN_ROOM_SIZE:
            print("returning from generate_bsp_tree")
            print_node(node)
            return
        # Choose a random split position
        split = random.randint(MIN_ROOM_SIZE, max_split)
        print("split: " + str(split))
        # Create the left and right nodes
        node.left = Node(node.x, node.y, node.width, split + 1) #13, 7, (8), (8) 
        node.right = Node(node.x, node.y + split, node.width, node.height - split)
        generate_bsp_tree(node.left, depth + 1)
        generate_bsp_tree(node.right, depth + 1)
    else:
        # Calculate the maximum possible split position
        max_split = node.width - MIN_ROOM_SIZE
        #max_split = min(max_split, MAX_ROOM_SIZE - MIN_ROOM_SIZE)
        print(max_split)
        
        if max_split < MIN_ROOM_SIZE:
            print("returning from generate_bsp_tree")
            print_node(node)
            return
        # Choose a random split position
        split = random.randint(MIN_ROOM_SIZE, max_split)
        print("split: " + str(split))
        # Create the left and right nodes
        node.left = Node(node.x, node.y, split + 1, node.height)
        node.right = Node(node.x + split, node.y, node.width - split, node.height)
        generate_bsp_tree(node.left, depth + 1)
        generate_bsp_tree(node.right, depth + 1)

def generate_game_world():
    game_world = [[Tile('floor') for _ in range(WIDTH)] for _ in range(HEIGHT)]
    # Create the root node of the BSP tree
    root = Node(0, 0, WIDTH, HEIGHT)
    # Generate the BSP tree
    generate_bsp_tree(root, 0)

    # Use the BSP tree to create the game world
    create_game_world_from_bsp_tree(game_world, root)

    return game_world

def print_node(node):
    for key, value in node.__dict__.items():
        print(f'{key}: {value}')
    
def create_game_world_from_bsp_tree(game_world, node):
    # Base case: if the node is a leaf, create a room
    if node.left is None and node.right is None:
        create_room(game_world, node.x, node.y, node.width-1, node.height-1)
        return

    if node.left is not None:
        create_game_world_from_bsp_tree(game_world, node.left)
    if node.right is not None:
        create_game_world_from_bsp_tree(game_world, node.right)
    
    if node.left is not None and node.right is not None:
        #left_room = get_room_in_node(node.left)
        right_room = get_room_in_node(node.right)
        #create_corridor(game_world, left_room, right_room)

# note this isn't used yet... But I think it might be useful (it basically doe's the same as
#　create_room(game_world, node.x+1, node.y+1, node.width-2, node.height-2)
def get_room_in_node(node):
    # Base case: if the node is a leaf, return the room coordinates
    if node.left is None and node.right is None:
        x = random.randint(node.x + 1, node.x + node.width - 2)
        y = random.randint(node.y + 1, node.y + node.height - 2)
        return x, y

    if node.left is not None:
        return get_room_in_node(node.left)
    if node.right is not None:
        return get_room_in_node(node.right)

def create_room(game_world, x, y, width, height):
    #print("create_room")
    #print(x)
    #print(y)
    #print(width)
    #print(height)
    for i in range(x, x + width + 1):
        game_world[i][y] = Tile('wall')
        game_world[i][y + height] = Tile('wall')
    for i in range(y, y + height + 1):
        game_world[x][i] = Tile('wall')
        game_world[x + width][i] = Tile('wall')

def create_corridor(game_world, start, end):
    x1, y1 = start
    x2, y2 = end
    
    # Choose a random point in the left room
    x1 = random.randint(x1, x1 + 1)
    y1 = random.randint(y1, y1 + 1)

    # Choose a random point in the right room
    x2 = random.randint(x2, x2 + 1)
    y2 = random.randint(y2, y2 + 1)

    # Connect the two points with a corridor
    if x1 == x2:
        # Vertical corridor
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_world[y][x1] = Tile('floor')
    else:
        # Horizontal corridor
        for x in range(min(x1, x2), max(x1, x2) + 1):
            game_world[y1][x] = Tile('floor')
            
def print_game_world(game_world):
    #sys.stdout.write('\x1b[2J')
    for row in game_world:
        rowText = '|'
        for tile in row:
            if(tile.type is 'floor'):
                rowText += ' '
            else:
                rowText += 'W'
            rowText += '|'
        print(rowText)

def get_a_world():
    game_world = generate_game_world()
    # lets revist this in a bit for debug purposes
    #print_game_world(game_world)
    return game_world




print_game_world(generate_game_world())