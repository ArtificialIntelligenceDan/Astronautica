from astro_vars import *


# ARITHMETIC


def fceil(x):
    return floor(round(x, 5)) + 1


def frange(stop, start=float(0)):
    num_list = list()
    num_list.append(start)
    for i in range(int(fceil(start)), int(ceil(stop))):
        num_list.append(i)
    num_list.append(stop)
    return num_list


def lineq(pi, pf, x):
    xi, yi = pi
    xf, yf = pf
    m = (yf - yi) / (xf - xi)
    y = (m * (x - xi)) + yi
    return y


def find_relative_block_location(block_ind):
    z_change = floor(block_ind // (CHUNK_X * CHUNK_Y))
    y_change = floor((block_ind - (z_change * (CHUNK_X * CHUNK_Y))) // CHUNK_X)
    x_change = (block_ind - (z_change * (CHUNK_X * CHUNK_Y))) - (y_change * CHUNK_X)
    location = CHUNK_X - x_change, CHUNK_Y - y_change, 1 + z_change
    return location


def find_relative_player_location(player_location):
    px, py, pz = player_location
    mx, my, mz = MAX_COORDS
    rel_px = CHUNK_X - ((mx - px) - (floor((mx - px) / CHUNK_X) * CHUNK_X))
    rel_py = CHUNK_Y - ((my - py) - (floor((my - py) / CHUNK_Y) * CHUNK_Y))
    rel_pz = (ceil((mz - pz) / CHUNK_Z) * CHUNK_Z) - (mz - pz)
    relative_player_location = rel_px, rel_py, rel_pz
    return relative_player_location


def find_chunk_term_point(chunk_ind):
    mx, my, mz = MAX_COORDS
    chunk_term_point = mx - ((chunk_ind / WORLD_SIZE_X - floor(chunk_ind / WORLD_SIZE_X)) * WORLD_SIZE_X * CHUNK_X), \
                       my - (floor((chunk_ind - (WORLD_SIZE_Y * WORLD_SIZE_X *
                                                 range(WORLD_SIZE_Z)[int(floor(
                                                     chunk_ind / (WORLD_SIZE_X * WORLD_SIZE_Y)))])) / WORLD_SIZE_X)
                             * CHUNK_Y), \
                       ((floor(chunk_ind / (WORLD_SIZE_X * WORLD_SIZE_Y)) + 1) * CHUNK_Z) - mz
    return chunk_term_point


def find_block_location(block_ind, chunk_ind):
    cx, cy, cz = find_relative_block_location(block_ind)
    chunk_term_point = find_chunk_term_point(chunk_ind)
    block_location = chunk_term_point[0] - (CHUNK_X - cx), chunk_term_point[1] - (CHUNK_Y - cy), \
                     chunk_term_point[2] - (CHUNK_Z - cz)
    return block_location


def find_chunk_index(block_location):
    mx, my, mz = MAX_COORDS
    bx, by, bz = block_location
    ibx, iby, ibz = -bx + mx, -by + my, bz + mz - 1
    chunk_spot = floor(ibx / CHUNK_X), floor(iby / CHUNK_Y), floor(ibz / CHUNK_Z)
    chunk_ind = spot_to_ind(chunk_spot)
    return chunk_ind


def find_relative_block_index(block_location):
    bx, by, bz = block_location
    if not isinstance(bx, int) or not isinstance(by, int) or not isinstance(bz, int):
        bx, by, bz = int(ceil(bx)), int(ceil(by)), int(ceil(bz))
    rbx, rby, rbz = bx - (floor(bx / CHUNK_X) * CHUNK_X), by - (floor(by / CHUNK_Y) * CHUNK_Y), \
                    bz - (floor(bz / CHUNK_Z) * CHUNK_Z)
    if rbx == 0:
        rbx += CHUNK_X
    if rby == 0:
        rby += CHUNK_Y
    if rbz == 0:
        rbz += CHUNK_Z
    block = (CHUNK_X - rbx)
    row = (CHUNK_Y - rby)
    flat = rbz - 1
    block_ind = (flat * CHUNK_X * CHUNK_Y) + (row * CHUNK_X) + block
    return block_ind


def find_block(entity, orientation):
    ex, ey, ez = entity.location
    bix, biy, biz = entity.hit_box_boundaries[0]
    bfx, bfy, bfz = entity.hit_box_boundaries[1]

    blocks_found = set()

    if orientation == 'below':
        for bx in range(int(ceil(entity.hit_box_length) + 1)):
            for by in range(int(ceil(entity.hit_box_width)) + 1):
                block_location = int(ceil(bix)) + bx, int(ceil(biy)) + by, int(ceil(biz))
                chunk_ind, block_ind = find_chunk_index(block_location), find_relative_block_index(block_location)
                blocks_found.add((chunk_ind, block_ind))
    if orientation == 'above':
        for bx in range(int(ceil(entity.hit_box_length) + 1)):
            for by in range(int(ceil(entity.hit_box_width) + 1)):
                block_location = int(ceil(bix)) + bx, int(ceil(biy)) + by, int(ceil(bfz))
                chunk_ind, block_ind = find_chunk_index(block_location), find_relative_block_index(block_location)
                blocks_found.add((chunk_ind, block_ind))
    if orientation == 'north':
        for bx in frange(entity.hit_box_length):
            for bz in frange(entity.hit_box_height):
                block_location = int(ceil(bix + bx)), int(fceil(bfy)), int(fceil(biz + bz))
                chunk_ind, block_ind = find_chunk_index(block_location), find_relative_block_index(block_location)
                blocks_found.add((chunk_ind, block_ind))
    if orientation == 'south':
        for bx in frange(entity.hit_box_length):
            for bz in frange(entity.hit_box_height):
                block_location = int(ceil(bix + bx)), int(ceil(biy - 0.1)), int(fceil(biz + bz))
                chunk_ind, block_ind = find_chunk_index(block_location), find_relative_block_index(block_location)
                blocks_found.add((chunk_ind, block_ind))
    if orientation == 'west':
        for by in frange(entity.hit_box_length):
            for bz in frange(entity.hit_box_height):
                block_location = int(fceil(bfx)), int(ceil(biy + by)), int(fceil(biz + bz))
                chunk_ind, block_ind = find_chunk_index(block_location), find_relative_block_index(block_location)
                blocks_found.add((chunk_ind, block_ind))
    if orientation == 'east':
        for by in frange(entity.hit_box_length):
            for bz in frange(entity.hit_box_height):
                block_location = int(ceil(bix - 0.1)), int(ceil(biy + by)), int(fceil(biz + bz))
                chunk_ind, block_ind = find_chunk_index(block_location), find_relative_block_index(block_location)
                blocks_found.add((chunk_ind, block_ind))
    return blocks_found


def grid_to_screen_coords(grid_location, player_location):
    grid_x, grid_y, grid_z = grid_location
    px, py, pz = player_location
    rel_gx, rel_gy, rel_gz = grid_x - px, grid_y - py, grid_z - pz
    screen_x = grid_origin[0] - (rel_gx * y_gap_x_comp) - (rel_gy * x_gap_x_comp)
    screen_y = grid_origin[1] - (rel_gy * x_gap_y_comp) - (rel_gx * y_gap_y_comp) - (rel_gz * z_unit_length)
    return round(screen_x), round(screen_y)


def screen_to_grid_pos_key(grid_position):
    return grid_position[2]


def screen_to_grid_pos(screen_coords, player):
    grid_positions = []
    px, py, pz = player.location
    sx, sy = screen_coords

    sx_rel = grid_origin[0] - sx
    sy_rel = grid_origin[1] - sy

    gy_rel = sy_rel / x_gap_y_comp
    gx_rel = (sx_rel - (gy_rel * x_gap_x_comp)) / y_gap_x_comp
    bgx, bgy, bgz = round(gx_rel + px, 1), round(gy_rel + py, 1), round(pz, 1)

    t = -player.interact_radius
    while t <= player.interact_radius:  # WHY IS THIS INACCURATE
        gx = bgx + t
        gy = bgy + ((8 / 3) * t)
        gz = bgz + (-sqrt(3) * t)
        grid_pos = round(gx, 1), round(gy, 1), round(gz, 1)
        if distance(grid_pos, player.location) <= player.interact_radius and grid_pos not in grid_positions:
            grid_positions.append(grid_pos)
        t += 0.1  # KINDA EXPENSIVE, INCREASE ONLY IF ABSOLUTELY NECESSARY BECAUSE WILL CAUSE MORE INACCURACY

    return sorted(grid_positions, key=screen_to_grid_pos_key, reverse=True)


def find_special_angle(screen_coords, player_location):
    gx, gy, gz = -10, -10, -10
    csx, csy = screen_coords
    while gx < 10:
        while gy < 10:
            while gz < 10:
                gx, gy, gz = round(gx, 1), round(gy, 1), round(gz, 1)
                sx, sy = grid_to_screen_coords((gx, gy, gz), player_location)
                s = round(sx, 1), round(sy, 1)
                if s == (float(csx), float(csy)):
                    print((gx, gy, gz))
                gz += 0.1
            gz = -10
            gy += 0.1
        gy = -10
        gx += 0.1


def find_chunk_spot(chunk_ind):  # translates chunk_ind chunk-coordinate form (origin: top left corner)
    spot_z = floor(chunk_ind / (WORLD_SIZE_X * WORLD_SIZE_Y))
    spot_y = floor((chunk_ind - (spot_z * WORLD_SIZE_Y * WORLD_SIZE_X)) / WORLD_SIZE_X)
    spot_x = floor(chunk_ind - (spot_z * WORLD_SIZE_Y * WORLD_SIZE_X) - (spot_y * WORLD_SIZE_X))
    chunk_spot = (spot_x, spot_y, spot_z)
    return chunk_spot


def spot_to_ind(chunk_spot):  # translates chunk spot back into it's corresponding chunk_ind value
    spot_x = chunk_spot[0]
    spot_y = chunk_spot[1]
    spot_z = chunk_spot[2]
    if spot_x > WORLD_SIZE_X - 1 or spot_y > WORLD_SIZE_Y - 1 or spot_z > WORLD_SIZE_Z - 1:
        print('invalid')
    else:
        chunk_ind = (spot_z * WORLD_SIZE_X * WORLD_SIZE_Y) + (spot_y * WORLD_SIZE_X) + spot_x
        return chunk_ind


def distance(location1, location2):
    if len(location1) == 3 and len(location2) == 3:
        x1, y1, z1 = location1
        x2, y2, z2 = location2
        d = (((x2 - x1)**2) + ((y2 - y1)**2) + ((z2 - z1)**2))**(1/2)
        return d
    if len(location1) == 2 and len(location2) == 2:
        x1, y1 = location1
        x2, y2 = location2
        d = (((x2 - x1)**2) + ((y2 - y1)**2))**(1/2)
        return d


def chunk_ind_next(chunk_ind, orientation):
    if orientation == 'n':
        next_ind = chunk_ind - WORLD_SIZE_X
        if floor(chunk_ind / (WORLD_SIZE_X * WORLD_SIZE_Y)) != floor(next_ind / (WORLD_SIZE_X * WORLD_SIZE_Y)):
            print('north chunk not found')
            return None
        else:
            return next_ind
    if orientation == 's':
        next_ind = chunk_ind + WORLD_SIZE_X
        if floor(chunk_ind / (WORLD_SIZE_X * WORLD_SIZE_Y)) != floor(next_ind / (WORLD_SIZE_X * WORLD_SIZE_Y)):
            print('south chunk not found')
            return None
        else:
            return next_ind
    if orientation == 'w':
        next_ind = chunk_ind - 1
        if floor(chunk_ind / WORLD_SIZE_X) != floor(next_ind / WORLD_SIZE_X):
            print('west chunk not found')
            return None
        else:
            return next_ind
    if orientation == 'e':
        next_ind = chunk_ind + 1
        if floor(chunk_ind / WORLD_SIZE_X) != floor(next_ind / WORLD_SIZE_X):
            print('east chunk not found')
            return None
        else:
            return next_ind
    if orientation == 't':
        next_ind = chunk_ind + (WORLD_SIZE_X * WORLD_SIZE_Y)
        if next_ind > WORLD_SIZE_X * WORLD_SIZE_Y * WORLD_SIZE_Z:
            print('top chunk not found')
            return None
        else:
            return next_ind
    if orientation == 'b':
        next_ind = chunk_ind - (WORLD_SIZE_X * WORLD_SIZE_Y)
        if next_ind < 0:
            print('bottom chunk not found')
            return None
        else:
            return next_ind


def get_texture(block_id):
    block_ids = '0123456789abcdefghijklmnopqrstuvwxyz'
    return TEXTURE[block_ids.find(block_id)]


def write_chunk_list(layer):
    chunk_data = []
    if layer == 'bottom':
        for block_int in range(CHUNK_X * CHUNK_Y * CHUNK_Z):
            block_id = '2'
            chunk_data.append(block_id)
    if layer == 'top':
        for block_int in range(CHUNK_X * CHUNK_Y * CHUNK_Z):
            block_id = '0'
            chunk_data.append(block_id)
    return chunk_data


# DISPLAY


def make_line(magnitude, angle, origin, color):
    x_mag = round(magnitude * cos(radians(angle)))
    y_mag = round(magnitude * sin(radians(angle)))
    line = pygame.draw.aaline(WIN, color, origin, (origin[0] + x_mag, origin[1] + y_mag))
    return line


def draw_grid(x_unit_displacement, y_unit_displacement, z_unit_displacement):

    y_line_dp_y = y_unit_displacement * x_gap_y_comp  # alters y coordinates of red lines depending on game coordinates
    y_line_dp_x = y_unit_displacement * x_gap_x_comp  # alters x coordinates of red lines depending on game coordinates
    x_line_dp_y = x_unit_displacement * y_gap_y_comp  # alters y coordinates of blue lines depending on game coordinates
    x_line_dp_x = x_unit_displacement * y_gap_x_comp  # alters x coordinates of blue lines depending on game coordinates

    z_line_dp_y = z_unit_displacement * z_unit_length  # alters y coordinates of all lines depending on z coordinates

    if isinstance(y_unit_displacement, int):
        y_lines = width + 1
    else:
        y_lines = width
    if isinstance(x_unit_displacement, int):
        x_lines = length + 1
    else:
        x_lines = length

    z_line_negative = make_line(z_magnitude, z_angle, (grid_origin[0], grid_origin[1]), Z_GRID_COLOR)
    for line in range(y_lines):
        y_line = make_line(y_magnitude, y_angle, (grid_origin[0] + (x_gap_x_comp * line) + x_center_const + y_line_dp_x,
                                                  grid_origin[1] + (x_gap_y_comp * line) + y_center_const + y_line_dp_y
                                                  + z_line_dp_y)
                           , Y_GRID_COLOR)
    for line in range(x_lines):
        x_line = make_line(x_magnitude, x_angle, (grid_origin[0] + (y_gap_x_comp * line) + x_center_const + x_line_dp_x,
                                                  grid_origin[1] + (y_gap_y_comp * line) + y_center_const + x_line_dp_y
                                                  + z_line_dp_y)
                           , X_GRID_COLOR)
    z_line_positive = make_line(-z_magnitude, z_angle, (grid_origin[0], grid_origin[1]), Z_GRID_COLOR)

    pygame.draw.circle(WIN, BLUE, grid_origin, 3)


def manage_grid(player_location):
    x, y, z = player_location
    x_direction, y_direction = 0, 1
    x_unit_displacement = abs(x)
    y_unit_displacement = abs(y)
    z_unit_displacement = abs(z)
    while x_unit_displacement > 1:
        x_unit_displacement -= 1
    while y_unit_displacement > 1:
        y_unit_displacement -= 1
    while z_unit_displacement > 1:
        z_unit_displacement -= 1
    if x < 0:
        x_unit_displacement = 1 - x_unit_displacement
    if y < 0:
        y_unit_displacement = 1 - y_unit_displacement
    if z < 0:
        z_unit_displacement = 1 - z_unit_displacement

    draw_grid(x_unit_displacement, y_unit_displacement, z_unit_displacement)


def display_coordinates(player_location):
    px, py, pz = player_location
    draw_x = COORD_FONT.render(f'x:  {px:0.1f}', 1, X_GRID_COLOR)
    draw_y = COORD_FONT.render(f'y:  {py:0.1f}', 1, Y_GRID_COLOR)
    draw_z = COORD_FONT.render(f'z:  {pz:0.1f}', 1, Z_GRID_COLOR)
    WIN.blit(draw_x, (0, 340))
    WIN.blit(draw_y, (0, 360))
    WIN.blit(draw_z, (0, 380))


def display_advanced_info(player, clock):
    block_ind = find_block(player, 'below')
    chunk_ind = find_chunk_index(player.location)
    fps = str(int(clock.get_fps()))
    cx, cy, cz = find_relative_player_location(player.location)
    draw_chunk_ind = COORD_FONT.render(f'inside chunk #{chunk_ind}', 1, GRAY)
    draw_block_ind = COORD_FONT.render(f'standing on block #{block_ind}', 1, GRAY)
    draw_chunk_x = COORD_FONT.render(f'cx:  {cx:0.1f}', 1, X_GRID_COLOR)
    draw_chunk_y = COORD_FONT.render(f'cy:  {cy:0.1f}', 1, Y_GRID_COLOR)
    draw_chunk_z = COORD_FONT.render(f'cz:  {cz:0.1f}', 1, Z_GRID_COLOR)
    fps_text = COORD_FONT.render(fps, 1, pygame.Color("coral"))
    WIN.blit(draw_chunk_ind, (0, 400))
    WIN.blit(draw_chunk_x, (0, 425))
    WIN.blit(draw_chunk_y, (0, 450))
    WIN.blit(draw_chunk_z, (0, 475))
    WIN.blit(draw_block_ind, (0, 500))
    WIN.blit(fps_text, (WIDTH - 50, 10))
