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
    print("generate_bsp_tree")
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
    print("generate_game_world")
    game_world = [['#' for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Create the root node of the BSP tree
    root = Node(0, 0, WIDTH, HEIGHT)
    # Generate the BSP tree
    generate_bsp_tree(root, 0)

    # Use the BSP tree to create the game world
    create_game_world_from_bsp_tree(game_world, root)

    return game_world

def create_game_world_from_bsp_tree(game_world, node):
    print("create_game_world_from_bsp_tree")
    # Base case: if the node is a leaf, create a room
    if node.left is None and node.right is None:
        create_room(game_world, node.x, node.y, node.width, node.height)
        return

    if node.left is not None:
        create_game_world_from_bsp_tree(game_world, node.left)
    if node.right is not None:
        create_game_world_from_bsp_tree(game_world, node.right)
    
    if node.left is not None and node.right is not None:
        left_room = get_room_in_node(node.left)
        right_room = get_room_in_node(node.right)
        create_corridor(game_world, left_room, right_room)

def get_room_in_node(node):
    print("get_room_in_node")
    # Base case: if the node is a leaf, return the room coordinates
    if node.left is None and node.right is None:
        x = random.randint(node.x + 1, node.x + node.width - 2)
        y = random.randint(node.y + 1, node.y + node.height - 2)
        return x, y

    # Recursively search for a room in the left or right node
    if node.left is not None:
        room = get_room_in_node(node.left)
        if room is not None:
            return room
    if node.right is not None:
        room = get_room_in_node(node.right)
        if room is not None:
            return room

def create_room(game_world, x, y, width, height):
    print("create_room")
    for i in range(x + 1, x + width - 1):
        for j in range(y + 1, y + height - 1):
            game_world[j][i] = '.'

def create_corridor(game_world, start, end):
    print("create_corridor")
    x1, y1 = start
    x2, y2 = end
    if x1 == x2:
        create_corridor_vertically(game_world, x1, y1, y2 - y1)
    elif y1 == y2:
        create_corridor_horizontally(game_world, x1, y1, x2 - x1)
    else:
        # Choose a random direction to go first
        if random.random() < 0.5:
            create_corridor_horizontally(game_world, x1, y1, x2 - x1)
            create_corridor_vertically(game_world, x2, y1, y2 - y1)
        else:
            create_corridor_vertically(game_world, x1, y1, y2 - y1)
            create_corridor_horizontally(game_world, x1, y2, x2 - x1)
            
def create_corridor_horizontally(game_world, x, y, length):
    print("create_corridor_horizontally")
    for i in range(x, x + length):
        game_world[y][i] = '.'

def create_corridor_vertically(game_world, x, y, length):
    print("create_corridor_vertically")
    for i in range(y, y + length):
        game_world[i][x] = '.'

def print_game_world(game_world):
    print("print_game_world")
    for row in game_world:
        print(''.join(row))

def main():
    print("main")
    game_world = generate_game_world()
    print_game_world(game_world)

if __name__ == '__main__':
    main()



