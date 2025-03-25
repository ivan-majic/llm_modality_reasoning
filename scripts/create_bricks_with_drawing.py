import random
import math
import json
import argparse
import matplotlib.pyplot as plt
import os


class Brick:
    '''Class to represent a brick in a 2D grid. Each brick has a position (x, y), a label, a shape, and a color.'''
    def __init__(self, x, y, label='None', shape='None', color='None'):
        self.x = x
        self.y = y
        self.label = label
        self.shape = shape
        self.color = color

    def __str__(self):
        '''Return a string representation of the brick.'''
        res = 'Brick at ({}, {}, {}, {}, {})'.format(self.x, self.y, self.label, self.shape, self.color)
        return res
    
    def get_position_description(self, bricks):
        '''Return a string describing the position of the brick relative to the other bricks.
        X is the horizontal axis, Y is the vertical axis.'''
        prev_brick = None
        for item in bricks:
            if item.x == self.x and abs(item.y - self.y) == 1:
                prev_brick = item
                break
            elif item.y == self.y and abs(item.x - self.x) == 1:
                prev_brick = item
                break
        
        if prev_brick is None:
            return "No adjacent brick found."
        
        x_diff = self.x - prev_brick.x
        y_diff = self.y - prev_brick.y

        if x_diff == 0 and y_diff == 1:
            return "The brick {} is above the brick {}.".format(self.label, prev_brick.label)
        elif x_diff == 0 and y_diff == -1:
            return "The brick {} is below the brick {}.".format(self.label, prev_brick.label)
        elif x_diff == 1 and y_diff == 0:
            return "The brick {} is to the right of the brick {}.".format(self.label, prev_brick.label)
        elif x_diff == -1 and y_diff == 0:
            return "The brick {} is to the left of the brick {}.".format(self.label, prev_brick.label)
        else:
            return "The brick {} is next to the brick {}, but not in any defined direction.".format(
                self.label, prev_brick.label
            ) 


def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def find_nearest_bricks(bricks, target, target_color="white"):
    min_distance = float('inf')
    nearest_brick = None
    for brick in bricks:
        if brick.color == target_color:
            dist = distance(brick, target)
            if dist < min_distance:
                min_distance = dist
                nearest_brick = brick
    return nearest_brick

def find_farthest_bricks(bricks, target, target_color="white"):
    max_distance = float('-inf')
    farthest_brick = None
    for brick in bricks:
        if brick.color == target_color:
            dist = distance(brick, target)
            if dist > max_distance:
                max_distance = dist
                farthest_brick = brick
    return farthest_brick

def build_bricks(n, m, min_height, shuffle):
    flags = [
        [97, 26],
        [48, 10],
        [65, 26],
    ]
    bricks = []
    colors = ['blue', 'yellow', 'white', 'orange', 'green', 'red']
    shapes = ['square', 'circle']
    label_list = [chr(i[0] + j) for i in flags for j in range(i[1])]
    
    if min_height is not None:
        column_heights = [random.randint(min_height, n) for _ in range(m)]
    else:
        column_heights = [n] * m
    
    num_bricks = sum(column_heights)
    if num_bricks <= 26:
        label_list = label_list[:26]
    elif num_bricks <= 36:
        label_list = label_list[:36]
    elif num_bricks > 62:
        raise ValueError("Too many bricks to assign unique labels with alphanumeric characters (lowercase and uppercase letters and digits 0-9).")
    

    f = 0
    for i in range(len(column_heights)):
        for j in range(column_heights[i]):
            color = random.choice(colors)
            # Initially assign shape from the list; here defaulting to square
            shape = shapes[0]
            if shuffle:
                random_element = random.choice(label_list)
                label_list.remove(random_element)
            else:
                if f <= 25:
                    random_element = chr(flags[0] + f)
                else:
                    random_element = chr(flags[1] + f - 26)
            bricks.append(Brick(i, j, random_element, shape, color))
            f += 1
    return bricks


def make_dict(dict_, brick, bricks):
    for item in bricks:
        if item.x == brick.x and item.y - brick.y == 1:
            dict_[item.label] = brick.label

def remove_bricks(brick, brick_dict, res):
    above_bricks = []
    for b, a in brick_dict.items():
        if a == brick:
            above_bricks.append(b)
    for b in above_bricks:
        res = remove_bricks(b, brick_dict, res)
    if brick not in brick_dict.keys():
        res = res + brick
        return res
    res = res + brick
    brick_dict.pop(brick)
    return res


def draw_bricks(bricks, filename, show=0, save=0, color=0, rotation=0, shape_type=None):
    """
    Draw the bricks with a specified rotation and shape type.
      - rotation: 0, 90, 180, or 270 (degrees clockwise). This rotates the grid.
      - shape_type: 'square' or 'circle'. If provided, this overrides the brick.shape.
    The labels are always drawn upright.
    Instead of drawing the original brick list, this function returns a new list of bricks
    whose positions have been transformed according to the rotation.
    """
    fig, ax = plt.subplots()

    # Determine the bounding box of the original bricks.
    min_x = min(brick.x for brick in bricks)
    max_x = max(brick.x for brick in bricks)
    min_y = min(brick.y for brick in bricks)
    max_y = max(brick.y for brick in bricks)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    def transform_coords(x, y, rotation):
        dx = x - min_x
        dy = y - min_y
        if rotation == 0:
            new_dx, new_dy = dx, dy
        elif rotation == 90:
            new_dx, new_dy = dy, width - 1 - dx
        elif rotation == 180:
            new_dx, new_dy = width - 1 - dx, height - 1 - dy
        elif rotation == 270:
            new_dx, new_dy = height - 1 - dy, dx
        else:
            new_dx, new_dy = dx, dy
        return new_dx, new_dy

    new_bricks = []
    transformed_positions = []
    # For each brick, compute the new position and draw it.
    for brick in bricks:
        new_x, new_y = transform_coords(brick.x, brick.y, rotation)
        # Create a new Brick with the transformed coordinates.
        new_brick = Brick(new_x, new_y, brick.label, brick.shape, brick.color)
        new_bricks.append(new_brick)
        transformed_positions.append((new_x, new_y))
        # Determine fill color.
        fill_color = brick.color if color else 'white'
        line_color = 'gray'
        draw_shape = shape_type if shape_type is not None else brick.shape
        if draw_shape == 'square':
            rect = plt.Rectangle((new_x, new_y), 1, 1, facecolor=fill_color, edgecolor=line_color, alpha=0.5)
            ax.add_patch(rect)
        elif draw_shape == 'circle':
            circ = plt.Circle((new_x + 0.5, new_y + 0.5), 0.5, facecolor=fill_color, edgecolor=line_color, alpha=0.5)
            ax.add_patch(circ)
        else:
            rect = plt.Rectangle((new_x, new_y), 1, 1, facecolor=fill_color, edgecolor=line_color, alpha=0.5)
            ax.add_patch(rect)
        # Always draw the label upright.
        plt.text(new_x + 0.5, new_y + 0.5, brick.label, ha='center', va='center', fontsize=12, color='black')

    xs = [pos[0] for pos in transformed_positions]
    ys = [pos[1] for pos in transformed_positions]
    ax.set_xlim(-1, max(xs) + 2)
    ax.set_ylim(-1, max(ys) + 2)
    ax.set_aspect('equal')
    plt.axis('off')
    if show:
        plt.show()
    if save:
        plt.savefig(filename)
        plt.close(fig)
    # Return the new set of bricks after transformation.
    return new_bricks



# def draw_bricks(bricks, filename, show=0, save=0, color=0, rotation=0, shape_type=None):
#     """
#     Draw the bricks with a specified rotation and shape type.
#       - rotation: 0, 90, 180, or 270 (degrees clockwise). This rotates the grid.
#       - shape_type: 'square' or 'circle'. If provided, this overrides the brick.shape.
#     The labels are always drawn upright.
#     """
#     fig, ax = plt.subplots()

#     # Calculate bounding box of original brick positions.
#     min_x = min(brick.x for brick in bricks)
#     max_x = max(brick.x for brick in bricks)
#     min_y = min(brick.y for brick in bricks)
#     max_y = max(brick.y for brick in bricks)
#     width = max_x - min_x + 1
#     height = max_y - min_y + 1

#     # Helper: transform original (x, y) to new coordinates based on rotation.
#     def transform_coords(x, y, rotation):
#         dx = x - min_x
#         dy = y - min_y
#         if rotation == 0:
#             new_dx, new_dy = dx, dy
#         elif rotation == 90:
#             new_dx, new_dy = dy, width - 1 - dx
#         elif rotation == 180:
#             new_dx, new_dy = width - 1 - dx, height - 1 - dy
#         elif rotation == 270:
#             new_dx, new_dy = height - 1 - dy, dx
#         else:
#             new_dx, new_dy = dx, dy
#         return new_dx, new_dy

#     transformed_positions = []
#     for brick in bricks:
#         new_x, new_y = transform_coords(brick.x, brick.y, rotation)
#         transformed_positions.append((new_x, new_y))
#         # Determine fill color.
#         fill_color = brick.color if color else 'white'
#         line_color = 'gray'
#         # Determine which shape to draw.
#         draw_shape = shape_type if shape_type is not None else brick.shape
#         if draw_shape == 'square':
#             rect = plt.Rectangle((new_x, new_y), 1, 1, facecolor=fill_color, edgecolor=line_color, alpha=0.5)
#             ax.add_patch(rect)
#         elif draw_shape == 'circle':
#             circ = plt.Circle((new_x + 0.5, new_y + 0.5), 0.5, facecolor=fill_color, edgecolor=line_color, alpha=0.5)
#             ax.add_patch(circ)
#         else:
#             rect = plt.Rectangle((new_x, new_y), 1, 1, facecolor=fill_color, edgecolor=line_color, alpha=0.5)
#             ax.add_patch(rect)
#         # Always draw the label upright at the center.
#         plt.text(new_x + 0.5, new_y + 0.5, brick.label, ha='center', va='center', fontsize=12, color='black')
    
#     # Set plot limits based on transformed positions.
#     xs = [pos[0] for pos in transformed_positions]
#     ys = [pos[1] for pos in transformed_positions]
#     ax.set_xlim(-1, max(xs) + 2)
#     ax.set_ylim(-1, max(ys) + 2)
#     ax.set_aspect('equal')
#     plt.axis('off')
#     if show:
#         plt.show()
#     if save:
#         plt.savefig(filename)
#         plt.close(fig)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test LLM planning abilities")

    parser.add_argument("--n", type=int, default=1, help="Number of rows")
    parser.add_argument("--m", type=int, default=1, help="Number of columns")
    parser.add_argument("--l_low", type=int, default=None, help="Minimum column height")
    parser.add_argument("--l_high", type=int, default=None, help="Maximum column length")
    parser.add_argument("--dim", type=int, default=1, help="Dimensions of the brick structure (1D or 2D)")
    parser.add_argument("--N", type=int, default=500, help="Number of iterations")
    parser.add_argument("--s", type=int, default=1, help="Shuffle label: 1 true, 0 false")
    parser.add_argument("--c", type=bool, default=False, help="Color or not")

    args = parser.parse_args()
    l_low = args.l_low 
    l_high = args.l_high
    n = args.n
    m = args.m
    dim = args.dim
    N = args.N
    shuffle_label = bool(args.s)
    color_flag = args.c
    data_list = []

    res_dir = f'data/brick_{dim}D_{N}_n{n}_m{m}/'
    image_dir = os.path.join(res_dir, 'images')
    save_path = os.path.join(res_dir, 'data.json')
    os.makedirs(image_dir, exist_ok=True)

    data_list = []
    for i in range(N):
        # Create your initial set of bricks (the “base” configuration).
        bricks = build_bricks(n, m, l_low, shuffle_label)
        brick_target = random.choice(bricks)
        
        # (Optional) Build dependency information.
        dict_above = {}
        for brick in bricks:
            make_dict(dict_above, brick, bricks)
        label = remove_bricks(brick_target.label, dict_above, '')
        
        # Prepare color options.
        color_options = [0]
        if color_flag:
            color_options.append(1)
        
        # For each rotation, shape, and color option, draw and describe the new brick set.
        for rot, rule in [
            [0, 'The bricks must now be grabbed from top to bottom, and if the lower brick is to be grabbed, the upper brick must be removed first. '], 
            [90, 'The bricks must now be grabbed from right to left, and if the left brick is to be grabbed, the brick on the right must be removed first.'],
            [180, 'The bricks must now be grabbed from bottom to top, and if the upper brick is to be grabbed, the lower brick must be removed first.'],
            [270, 'The bricks must now be grabbed from left to right, and if the right brick is to be grabbed, the brick on the left must be removed first.']
            ]:
            for shape in ['square', 'circle']:
                for col in color_options:
                    col_label = "color" if col else "bw"
                    image_filename = os.path.join(image_dir, f'img_{i}_{shape}_{rot}_{col_label}.png')
                    # Get the new brick positions after transformation.
                    new_bricks = draw_bricks(bricks, image_filename, show=0, save=1, color=col, rotation=rot, shape_type=shape)
                    
                    # Build a textual description for this particular image.
                    res = "There is a set of bricks. "
                    # You can collect additional info as needed, for example:
                    for idx, brick in enumerate(new_bricks):
                        if idx > 0:
                            res += brick.get_position_description(new_bricks[:idx])
                        else:
                            res += "For the brick {}, the color is {}. ".format(brick.label, brick.color)
                    res += "Now we have to get a specific brick. "
                    res += rule
                    # For simplicity, here we choose the target brick based on a fixed index.
                    # brick_target = new_bricks[char_index-1]
                    res += "How to get brick {}?".format(brick_target.label)
                    
                    # Build additional metadata (layout, colors per row, etc.)
                    brick_labels = []
                    brick_colors = []
                    for y in sorted(set(b.y for b in new_bricks)):
                        brick_labels.append(','.join([b.label for b in new_bricks if b.y == y]))
                        brick_colors.append(','.join([b.color for b in new_bricks if b.y == y]))
                    
                    # Create a new entry for this particular image.
                    data = {
                        "brick_layout": brick_labels,
                        "brick_colors": brick_colors,
                        "image": image_filename,
                        "target": brick_target.label,
                        "data": res,
                        "label": label,
                    }
                    data_list.append(data)
        
    dataset = {"testset": data_list}

    with open(save_path, 'w') as outfile:
        json.dump(data_list, outfile)


    # for i in range(N):
    #     list_char = []
    #     color_set = set()
    #     shape_set = set()
    #     flag = 65

    #     # For 1D, force n=1 or m=1.
    #     if dim == 1:
    #         if n > 1:
    #             m = 1
        
    #     for j in range(n * m):
    #         list_char.append(chr(flag + j))
    #     char_index = random.randint(1, 3)
        
    #     bricks = build_bricks(n, m, l_low, shuffle_label)
    #     color_options = [0]
    #     if color_flag:
    #         color_options.append(1)

    #     # Loop over rotations (0, 90, 180, 270) and shape types ('square', 'circle').
    #     for rot in [0, 90, 180, 270]:
    #         for shape in ['square', 'circle']:
    #             for col in color_options:
    #                 col_label = "color" if col else "bw"
    #                 image_filename = os.path.join(image_dir, f'img_{i}_{shape}_{rot}_{col_label}.png')
    #                 draw_bricks(bricks, image_filename, show=0, save=1, color=col, rotation=rot, shape_type=shape)

    #     for item in bricks:
    #         color_set.add(item.color)
    #         shape_set.add(item.shape)
    #     res = "There is a set of bricks. "
    #     color_list = list(color_set)
    #     shape_list = list(shape_set)
    #     shuffled = shuffle_label
        
    #     if shuffled:
    #         res_list = []
    #         for idx in range(len(bricks)):
    #             if idx > 0:
    #                 res_list.append(bricks[idx].get_position_description(bricks[:idx]))
    #             else:
    #                 res_list.append("For the brick {}, the color is {}. ".format(bricks[idx].label, bricks[idx].color))
    #         random.shuffle(res_list)
    #         for item in res_list:
    #             res = res + item
    #     else:
    #         for idx in range(len(bricks)):
    #             if idx > 0:
    #                 res = res + bricks[idx].get_position_description(bricks[:idx])
    #             else:
    #                 res = res + "For the brick {}, the color is {}. ".format(bricks[idx].label, bricks[idx].color)
    #     res = res + "Now we have to get a specific brick. "
    #     rule = 'The bricks must now be grabbed from top to bottom, and if the lower brick is to be grabbed, the upper brick must be removed first. '
    #     res = res + rule
    #     num = 3
    #     if num == 1:
    #         choiced_color = random.choice(color_list)
    #         brick_target = find_farthest_bricks(bricks, bricks[char_index-1], target_color=choiced_color)
    #         if brick_target.label == bricks[char_index-1].label:
    #             res = res + "How to get brick {}?".format(brick_target.label)
    #         else:
    #             res = res + "How to get the farthest {} brick of the brick {}".format(choiced_color, bricks[char_index-1].label) + "?"
    #     elif num == 2:
    #         choiced_color = random.choice(color_list)
    #         brick_target = find_nearest_bricks(bricks, bricks[char_index-1], target_color=random.choice(color_list))
    #         if brick_target.label == bricks[char_index-1].label:
    #             res = res + "How to get brick {}?".format(brick_target.label)
    #         else:
    #             res = res + "How to get the nearest {} brick of the brick {}".format(choiced_color, bricks[char_index-1].label) + "?"
    #     elif num == 3:
    #         brick_target = bricks[char_index-1]
    #         res = res + "How to get brick {}?".format(brick_target.label)
    #     dict_above = {}

    #     brick_labels = []
    #     brick_colors = []
    #     for y in set([brick.y for brick in bricks]):
    #         brick_labels.append(','.join([b.label for b in bricks if b.y == y]))
    #         brick_colors.append(','.join([b.color for b in bricks if b.y == y]))

    #     for item in bricks:
    #         make_dict(dict_above, item, bricks)
    #     label = ''
    #     label = remove_bricks(brick_target.label, dict_above, label)
    #     data = {
    #         "brick_layout": brick_labels,
    #         "brick_colors": brick_colors,
    #         "image": image_filename,
    #         "target": brick_target.label,
    #         "data": res,
    #         "label": label,
    #     }
    #     data_list.append(data)
    # dataset = {"testset": data_list}

    # with open(save_path, 'w') as outfile:
    #     json.dump(data_list, outfile)
