import random

# Constants for the game world
WIDTH = 80
HEIGHT = 25
MIN_ROOM_SIZE = 6

# Constants for the BSP tree
TOP_LEFT = 1
TOP_RIGHT = 2
BOTTOM_LEFT = 3
BOTTOM_RIGHT = 4

class Node:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = None
        self.right = None

def generate_bsp_tree(node, depth):
    # Base case: if the node is too small, return
    if node.width < MIN_ROOM_SIZE or node.height < MIN_ROOM_SIZE:
        return

    # Randomly decide if we should split the node horizontally or vertically
    split_horizontally = random.random() < 0.5
    if split_horizontally:
        # Calculate the maximum possible split position
        max_split = node.height - MIN_ROOM_SIZE - 1
        if max_split <= MIN_ROOM_SIZE:
            return
        # Choose a random split position
        split = random.randint(MIN_ROOM_SIZE + 1, max_split)
        # Create the left and right nodes
        node.left = Node(node.x, node.y, node.width, split)
        node.right = Node(node.x, node.y + split, node.width, node.height - split)
    else:
        # Calculate the maximum possible split position
        max_split = node.width - MIN_ROOM_SIZE - 1
        if max_split <= MIN_ROOM_SIZE:
            return
        # Choose a random split position
        split = random.randint(MIN_ROOM_SIZE + 1, max_split)
        # Create the left and right nodes
        node.left = Node(node.x, node.y, split, node.height)
        node.right = Node(node.x + split, node.y, node.width - split, node.height)

    # Recursively generate the left and right nodes
    generate_bsp_tree(node.left, depth + 1)
    generate_bsp_tree(node.right, depth + 1)

def generate_game_world():
    game_world = [['#' for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Create the root node of the BSP tree
    root = Node(0, 0, WIDTH, HEIGHT)
    # Generate the BSP tree
    generate_bsp_tree(root, 0)

    # Use the BSP tree to create the game world
    create_game_world_from_bsp_tree(game_world, root)

    return game_world

def create_game_world_from_bsp_tree(game_world, node, node_type=None):
    # Base case: if the node is a leaf, create a room
    if node.left is None and node.right is None:
        create_room(game_world, node.x, node.y, node.width, node.height)
        return

    # Choose a random location for the corridor in the left node
    if node.left is not None:
        x = random.randint(node.left.x, node.left.x + node.left.width - 1)
        y = random.randint(node.left.y, node.left.y + node.left.height - 1)
        if node_type == TOP_LEFT:
            create_corridor_horizontally(game_world, x, y, node.right.x - x + 1)
        elif node_type == BOTTOM_LEFT:
            create_corridor_horizontally(game_world, x, y, node.right.x - x + 1)
            create_corridor_vertically(game_world, node.right.x, node.right.y, y - node.right.y + 1)
        else:
            create_corridor_vertically(game_world, x, y, node.right.y - y + 1)

    # Choose a random location for the corridor in the right node
    if node.right is not None:
        x = random.randint(node.right.x, node.right.x + node.right.width - 1)
        y = random.randint(node.right.y, node.right.y + node.right.height - 1)
        if node_type == TOP_RIGHT:
            create_corridor_horizontally(game_world, x, y, node.left.x - x + 1)
        elif node_type == BOTTOM_RIGHT:
            create_corridor_horizontally(game_world, x, y, node.left.x - x + 1)
            create_corridor_vertically(game_world, node.left.x, node.left.y, y - node.left.y + 1)
        else:
            create_corridor_vertically(game_world, x, y, node.left.y - y + 1)

    # Recursively create the left and right nodes
    if node.left is not None:
        if node_type == TOP_LEFT:
            create_game_world_from_bsp_tree(game_world, node.left, BOTTOM_LEFT)
        elif node_type == BOTTOM_LEFT:
            create_game_world_from_bsp_tree(game_world, node.left, TOP_LEFT)
        else:
            create_game_world_from_bsp_tree(game_world, node.left, TOP_LEFT)
    if node.right is not None:
        if node_type == TOP_RIGHT:
            create_game_world_from_bsp_tree(game_world, node.right, BOTTOM_RIGHT)
        elif node_type == BOTTOM_RIGHT:
            create_game_world_from_bsp_tree(game_world, node.right, TOP_RIGHT)
        else:
            create_game_world_from_bsp_tree(game_world, node.right, TOP_RIGHT)
        
        
            
def create_room(game_world, x, y, width, height):
    for i in range(x, x + width):
        for j in range(y, y + height):
            game_world[j][i] = '.'

def create_corridor_horizontally(game_world, x, y, length):
    for i in range(x, x + length):
        game_world[y][i] = '.'

def create_corridor_vertically(game_world, x, y, length):
    for i in range(y, y + length):
        game_world[i][x] = '.'

if __name__ == '__main__':
    game_world = generate_game_world()
    for row in game_world:
        print(''.join(row))