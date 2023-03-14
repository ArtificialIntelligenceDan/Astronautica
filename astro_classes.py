from astro_functions import *


# MECHANICS


class Hitbox:

    def __init__(self, obj, obj_type, boundaries):
        self.obj = obj
        self.obj_type = obj_type

        self.resistance = 1
        # 2: absolute elasticity (perfectly inverts incoming velocities)
        # >1: elasticity (bounciness)
        # 1: absolute resistance (zeroes all incoming velocities)
        # <1: partial resistance (slows incoming velocities, simulates viscosity for liquids)
        # 0: no resistance (does not affect incoming velocities, simulates vacuum or simple atmosphere)

        self.boundaries_old = boundaries
        self.xi_old, self.xf_old = boundaries[0]
        self.yi_old, self.yf_old = boundaries[1]
        self.zi_old, self.zf_old = boundaries[2]
        self.boundaries = boundaries
        self.xi, self.xf = boundaries[0]
        self.yi, self.yf = boundaries[1]
        self.zi, self.zf = boundaries[2]

    def update_vars(self):
        self.boundaries[0] = [self.xi, self.xf]
        self.boundaries[1] = [self.yi, self.yf]
        self.boundaries[2] = [self.zi, self.zf]
        self.boundaries_old[0] = [self.xi_old, self.xf_old]
        self.boundaries_old[1] = [self.yi_old, self.yf_old]
        self.boundaries_old[2] = [self.zi_old, self.zf_old]

        self.xi_old, self.xf_old = self.xi, self.xf
        self.yi_old, self.yf_old = self.yi, self.yf
        self.zi_old, self.zf_old = self.zi, self.zf

    def collide(self, hitbox):
        if self.xi < hitbox.xi < self.xf or self.xi < hitbox.xf < self.xf or \
                self.yi < hitbox.yi < self.yf or self.yi < hitbox.yf < self.yf or \
                self.zi < hitbox.zi < self.zf or self.zi < hitbox.zf < self.zf or \
                self.xi_old < hitbox.xi < self.xi or self.xf_old < hitbox.xf < self.xf or \
                self.yi_old < hitbox.yi < self.yi or self.yf_old < hitbox.yf < self.yf or \
                self.zi_old < hitbox.zi < self.zi or self.zf_old < hitbox.zf < self.zf:
            return True
        else:
            return False

    def handle_collision(self, hitbox):
        # The purpose of the following lineq() nested functions can be described using example 'zf_eq_xi':
        # 'zf' is the output value of the function, and describes the z-position of the top side of the hitbox of 'self'
        # at x-position 'xi' of hitbox
        # 'xi' is the input of the function (output of nested lineq), and describes the x-position of the eastern side
        # of the hitbox of 'hitbox' at z-position 'self.zf'
        zf_eq_xi = lineq((self.xi, self.zf), (self.xf, self.zf),
                         lineq((hitbox.zi, hitbox.xi), (hitbox.zf, hitbox.xi), self.zf))
        zf_eq_xf = lineq((self.xi, self.zf), (self.xf, self.zf),
                         lineq((hitbox.zi, hitbox.xf), (hitbox.zf, hitbox.xf), self.zf))
        zi_eq_xi = lineq((self.xi, self.zi), (self.xf, self.zi),
                         lineq((hitbox.zi, hitbox.xi), (hitbox.zf, hitbox.xi), self.zi))
        zi_eq_xf = lineq((self.xi, self.zi), (self.xf, self.zi),
                         lineq((hitbox.zi, hitbox.xf), (hitbox.zf, hitbox.xf), self.zi))
        xf_eq_zi = lineq((self.zi, self.xf), (self.zf, self.xf),
                         lineq((hitbox.xi, hitbox.zi), (hitbox.xf, hitbox.zi), self.xf))
        xf_eq_zf = lineq((self.zi, self.xf), (self.zf, self.xf),
                         lineq((hitbox.xi, hitbox.zf), (hitbox.xf, hitbox.zf), self.xf))
        xi_eq_zi = lineq((self.zi, self.xi), (self.zf, self.xi),
                         lineq((hitbox.xi, hitbox.zi), (hitbox.xf, hitbox.zi), self.xi))
        xi_eq_zf = lineq((self.zi, self.xi), (self.zf, self.xi),
                         lineq((hitbox.xi, hitbox.zf), (hitbox.xf, hitbox.zf), self.xi))
        yf_eq_zi = lineq((self.zi, self.yf), (self.zf, self.yf),
                         lineq((hitbox.yi, hitbox.zi), (hitbox.yf, hitbox.zi), self.yf))
        yf_eq_zf = lineq((self.zi, self.yf), (self.zf, self.yf),
                         lineq((hitbox.yi, hitbox.zf), (hitbox.yf, hitbox.zf), self.yf))
        yi_eq_zi = lineq((self.zi, self.yi), (self.zf, self.yi),
                         lineq((hitbox.yi, hitbox.zi), (hitbox.yf, hitbox.zi), self.yi))
        yi_eq_zf = lineq((self.zi, self.yi), (self.zf, self.yi),
                         lineq((hitbox.yi, hitbox.zf), (hitbox.yf, hitbox.zf), self.yi))

        if self.collide(hitbox):
            if self.obj_type == 'block' and hitbox.obj_type == 'block':
                pass
            elif self.obj_type == 'block' and hitbox.obj_type == 'entity':
                pass
            elif self.obj_type == 'entity' and hitbox.obj_type == 'block':
                pass
            elif self.obj_type == 'entity' and hitbox.obj_type == 'entity':
                pass

    def draw(self, color, player_location):
        lines = (
            ((self.xf, self.yf, self.zf), (self.xi, self.yf, self.zf)),
            ((self.xi, self.yf, self.zf), (self.xi, self.yi, self.zf)),
            ((self.xi, self.yi, self.zf), (self.xf, self.yi, self.zf)),
            ((self.xf, self.yi, self.zf), (self.xf, self.yf, self.zf)),
            ((self.xf, self.yf, self.zf), (self.xf, self.yf, self.zi)),
            ((self.xi, self.yf, self.zf), (self.xi, self.yf, self.zi)),
            ((self.xi, self.yi, self.zf), (self.xi, self.yi, self.zi)),
            ((self.xf, self.yi, self.zf), (self.xf, self.yi, self.zi)),
            ((self.xf, self.yf, self.zi), (self.xi, self.yf, self.zi)),
            ((self.xi, self.yf, self.zi), (self.xi, self.yi, self.zi)),
            ((self.xi, self.yi, self.zi), (self.xf, self.yi, self.zi)),
            ((self.xf, self.yi, self.zi), (self.xf, self.yf, self.zi))
        )
        for i in range(len(lines)):
            pygame.draw.aaline(WIN, color, grid_to_screen_coords(lines[i][0], player_location),
                               grid_to_screen_coords(lines[i][1], player_location))


# mobile hitbox (for player, npc, creature, vehicle, dropped item, etc)
class EntityHitbox:
    def __init__(self, entity, bounds, permeable):
        self.entity = entity
        self.bounds = bounds
        self.permeable = permeable


# stationary hitbox (for blocks, geographical features, etc.)
class TileHitbox:
    def __init__(self, tile, shape, scale):
        self.tile = tile
        self.shape = shape
        self.scale = scale

        # WHAT TO DO NEXT:
        # - shape starts off as cell (no angled sides), allow player to change this if desired
        # - require dimension input (length, width, height) to define cell bounds
        # - have a plane equation to represent each side (bound) of the cell
        # - allow player to alter "slope" of each face if desired
        # - special_shapes are various presets with pre-inputted slopes to define common shapes
        # - probably limit total sides to 6 (2 per axis, or in other words an 'initial' and 'final' bound)

        self.special_shapes = [
            'slant_un', 'slant_ue', 'slant_us', 'slant_uw', 'slant_dn', 'slant_de', 'slant_ds', 'slant_dw',
            'slant_une', 'slant_unw', 'slant_use', 'slant_usw', 'slant_bne', 'slant_bnw', 'slant_bse', 'slant_bsw'
            'pyramid'
        ]  # defined as having non-flat planes as one or more of its bounds -- EXPERIMENTAL
        self.basic_shapes = ['cell', 'slab_b', 'slab_t', 'slab_n', 'slab_e', 'slab_s']  # has all flat planes as bounds

        self.resistance = 1
        # 2: absolute elasticity (perfectly inverts incoming velocities)
        # >1: elasticity (bounciness)
        # 1: absolute resistance (zeroes all incoming velocities)
        # <1: partial resistance (slows incoming velocities, simulates viscosity for liquids)
        # 0: no resistance (does not affect incoming velocities, simulates vacuum or simple atmosphere)

        self.suction = 0
        self.suction_path = ''

    def set_resistance(self, resistance):
        if isinstance(resistance, str):
            if resistance == 'solid':
                self.resistance = 1
            if resistance == 'viscous':
                self.resistance = 0.8
            if resistance == 'liquid':
                self.resistance = 0.5
            if resistance == 'gas':
                self.resistance = 0
        else:
            if resistance < 0:
                print('tile resistance cannot be less than zero')
            else:
                self.resistance = resistance

    def set_suction(self, suction):
        self.suction = suction

    def change_shape(self, new_shape):
        self.shape = new_shape


# ENTITY


class Entity(pygame.sprite.Sprite):

    def __init__(self, location, direction):
        super().__init__()


class Player(pygame.sprite.Sprite):

    def __init__(self, location, direction):
        super().__init__()
        self.x = location[0]
        self.y = location[1]
        self.z = location[2]
        self.location = self.x, self.y, self.z

        self.hit_box_length = 0.7
        self.hit_box_width = 0.7
        self.hit_box_height = 1.9
        self.hit_box_boundaries = (round(self.x - (self.hit_box_length / 2), 1),
                                   round(self.y - (self.hit_box_width / 2), 1), round(self.z, 1)), \
                                  (round(self.x + (self.hit_box_length / 2), 1),
                                   round(self.y + (self.hit_box_width / 2), 1), round(self.z + self.hit_box_height, 1))

        self.x_speed = 0.15  # in units per tick
        self.y_speed = 0.15  # in units per tick

        self.x_vel = 0
        self.y_vel = 0
        self.vel = round(sqrt(self.x_vel**2 + self.y_vel**2), 1)

        self.initial_jump_speed = 0.2  # in units per tick
        self.z_velocity = 0
        self.z_speed_max = 0.5
        self.on_ground = False
        self.collide_ceiling = False
        self.collide_north = False
        self.collide_south = False
        self.collide_east = False
        self.collide_west = False

        self.direction = [direction[0], direction[1]]

        self.frame_rate = 0.1  # fraction of total time sprite frame is shown for one game tick

        self.idle_width, self.idle_height = 23, 55

        self.idle_image_origin = grid_origin[0] - (self.idle_width // 2), grid_origin[1] - self.idle_height + 5
        self.idle_forward = pygame.transform.scale(pygame.image.load(r'assets\textures\player_idle_forward.png'),
                                                   (self.idle_width, self.idle_height))
        self.idle_left = pygame.transform.scale(pygame.image.load(r'assets\textures\player_idle_left.png'),
                                                   (self.idle_width, self.idle_height))
        self.idle_right = pygame.transform.scale(pygame.image.load(r'assets\textures\player_idle_right.png'),
                                                (self.idle_width, self.idle_height))
        self.idle_backward = pygame.transform.scale(pygame.image.load(r'assets\textures\player_idle_backward.png'),
                                                (self.idle_width, self.idle_height))

        self.run_width, self.run_height = 25, 47
        self.run_image_origin = grid_origin[0] - (self.run_width // 2), grid_origin[1] - self.run_height + 5

        self.run_total_frames = 4

        self.run_forward_frame_progress = 0
        self.run_forward = []
        for frame_num in range(4):
            frame = pygame.transform.scale(
                pygame.image.load(rf'assets\textures\player_run_forward-{frame_num + 1}.png'),
                (self.run_width, self.run_height))
            self.run_forward.append(frame)

        self.run_back_frame_progress = 0
        self.run_back = []
        for frame_num in range(4):
            frame = pygame.transform.scale(
                pygame.image.load(rf'assets\textures\player_run_back-{frame_num + 1}.png'),
                (self.run_width, self.run_height))
            self.run_back.append(frame)

        self.side_run_width, self.side_run_height = 34, 57
        self.side_run_image_origin = grid_origin[0] - (self.side_run_width // 2), \
                                     grid_origin[1] - self.side_run_height + 5

        self.run_left_frame_progress = 0
        self.run_left = []
        for frame_num in range(4):
            frame = pygame.transform.scale(
                pygame.image.load(rf'assets\textures\player_run_left-{frame_num + 1}.png'),
                (self.side_run_width, self.side_run_height))
            self.run_left.append(frame)

        self.run_right_frame_progress = 0
        self.run_right = []
        for frame_num in range(4):
            frame = pygame.transform.scale(
                pygame.image.load(rf'assets\textures\player_run_right-{frame_num + 1}.png'),
                (self.side_run_width, self.side_run_height))
            self.run_right.append(frame)

        self.run_upper_left_frame_progress = 0
        self.run_upper_left = []
        for frame_num in range(4):
            frame = pygame.transform.scale(
                pygame.image.load(rf'assets\textures\player_run_upper_left-{frame_num + 1}.png'),
                (self.run_width, self.run_height))
            self.run_upper_left.append(frame)

        self.rect = pygame.Rect(grid_origin[0] + (self.idle_width // 2), grid_origin[1] - self.idle_height,
                                self.idle_width, self.idle_height)

        self.interact_radius = 6    # blocks

        self.inv = Inventory()

    def update_location(self, new_location):
        self.x = round(new_location[0], 2)
        self.y = round(new_location[1], 2)
        self.z = round(new_location[2], 2)
        self.location = new_location
        self.hit_box_boundaries = (round(self.x - (self.hit_box_length / 2), 1),
                                   round(self.y - (self.hit_box_width / 2), 1), round(self.z, 1)), \
                                  (round(self.x + (self.hit_box_length / 2), 1),
                                   round(self.y + (self.hit_box_width / 2), 1), round(self.z + self.hit_box_height, 1))

    def draw(self, action):
        if action == 'idle':
            if self.direction == [1, 0]:
                WIN.blit(self.idle_left, self.idle_image_origin)
            if self.direction == [-1, 0]:
                WIN.blit(self.idle_right, self.idle_image_origin)
            if self.direction == [0, 1]:
                WIN.blit(self.idle_forward, self.idle_image_origin)
            if self.direction == [0, -1]:
                WIN.blit(self.idle_backward, self.idle_image_origin)
            if self.direction == [1, 1] or [-1, -1] or [1, -1] or [-1, 1]:
                pass
        if action == 'run':
            if self.direction == [1, 1]:
                frame = int(floor(self.run_upper_left_frame_progress))
                WIN.blit(self.run_upper_left[frame], self.run_image_origin)
                self.run_upper_left_frame_progress += self.frame_rate
                if self.run_upper_left_frame_progress >= len(self.run_upper_left):
                    self.run_upper_left_frame_progress *= 0
                if round(self.run_upper_left_frame_progress, 1) % 2 == 0:
                    step_sound = random.choice(step_sounds)
                    pygame.mixer.Sound.play(step_sound)
            elif self.direction == [0, -1] or self.direction == [1, -1] or self.direction == [-1, -1]:
                frame = int(floor(self.run_back_frame_progress))
                WIN.blit(self.run_back[frame], self.run_image_origin)
                self.run_back_frame_progress += self.frame_rate
                if self.run_back_frame_progress >= len(self.run_back):
                    self.run_back_frame_progress *= 0
                if round(self.run_back_frame_progress, 1) % 2 == 0:
                    step_sound = random.choice(step_sounds)
                    pygame.mixer.Sound.play(step_sound)
            elif self.direction == [1, 0]:
                frame = int(floor(self.run_left_frame_progress))
                WIN.blit(self.run_left[frame], self.side_run_image_origin)
                self.run_left_frame_progress += self.frame_rate
                if self.run_left_frame_progress >= len(self.run_left):
                    self.run_left_frame_progress *= 0
                if round(self.run_left_frame_progress, 1) % 2 == 0:
                    step_sound = random.choice(step_sounds)
                    pygame.mixer.Sound.play(step_sound)
            elif self.direction == [-1, 0]:
                frame = int(floor(self.run_right_frame_progress))
                WIN.blit(self.run_right[frame], self.side_run_image_origin)
                self.run_right_frame_progress += self.frame_rate
                if self.run_right_frame_progress >= len(self.run_right):
                    self.run_right_frame_progress *= 0
                if round(self.run_right_frame_progress, 1) % 2 == 0:
                    step_sound = random.choice(step_sounds)
                    pygame.mixer.Sound.play(step_sound)
            else:
                frame = int(floor(self.run_forward_frame_progress))
                WIN.blit(self.run_forward[frame], self.run_image_origin)
                self.run_forward_frame_progress += self.frame_rate
                if self.run_forward_frame_progress >= len(self.run_forward):
                    self.run_forward_frame_progress *= 0
                if round(self.run_forward_frame_progress, 1) % 2 == 0:
                    step_sound = random.choice(step_sounds)
                    pygame.mixer.Sound.play(step_sound)

    def draw_hit_box(self):
        bix, biy, biz = self.hit_box_boundaries[0]
        bfx, bfy, bfz = self.hit_box_boundaries[1]
        hit_box_grid_lines = (
            ((bfx, bfy, bfz), (bix, bfy, bfz)),
            ((bix, bfy, bfz), (bix, biy, bfz)),
            ((bix, biy, bfz), (bfx, biy, bfz)),
            ((bfx, biy, bfz), (bfx, bfy, bfz)),
            ((bfx, bfy, bfz), (bfx, bfy, biz)),
            ((bix, bfy, bfz), (bix, bfy, biz)),
            ((bix, biy, bfz), (bix, biy, biz)),
            ((bfx, biy, bfz), (bfx, biy, biz)),
            ((bfx, bfy, biz), (bix, bfy, biz)),
            ((bix, bfy, biz), (bix, biy, biz)),
            ((bix, biy, biz), (bfx, biy, biz)),
            ((bfx, biy, biz), (bfx, bfy, biz))
        )
        for i in range(len(hit_box_grid_lines)):
            pygame.draw.aaline(WIN, YELLOW, grid_to_screen_coords(hit_box_grid_lines[i][0], self.location),
                               grid_to_screen_coords(hit_box_grid_lines[i][1], self.location))

    def draw_interact_field(self):
        xz_circle_width = (self.interact_radius * x_unit_length) * 2
        xz_circle_height = (self.interact_radius * z_unit_length) * 2
        xz_circle_origin = grid_origin[0] - (self.interact_radius * x_unit_length), \
                           grid_origin[1] - (self.idle_height // 2) - (self.interact_radius * z_unit_length)

        xz_circle_surface = pygame.Surface((xz_circle_width, xz_circle_height), pygame.SRCALPHA)
        xz_circle_rect = pygame.Rect((0, 0), (xz_circle_width, xz_circle_height))
        pygame.draw.ellipse(xz_circle_surface, BLUE, xz_circle_rect, 4)

        WIN.blit(xz_circle_surface, xz_circle_origin)

        xy_circle_width = round(((((self.interact_radius * y_unit_length * sin(radians(60)))**2) +
                                  ((self.interact_radius * y_unit_length * cos(radians(60))) +
                                   (self.interact_radius * x_unit_length))**2)**(1/2)) / (2**(1/2))) * 2
        xy_width_angle = round(atan((y_unit_length * sin(radians(60))) /
                                    ((y_unit_length * cos(radians(60))) + x_unit_length)))
        xy_circle_height = round(((((self.interact_radius * y_unit_length * sin(radians(60)))**2) +
                                  (-(self.interact_radius * y_unit_length * cos(radians(60))) +
                                   (self.interact_radius * x_unit_length))**2)**(1/2)) / (2**(1/2))) * 2
        xy_circle_center = grid_origin[0], grid_origin[1] - (self.idle_height // 2)

        xy_circle_surface = pygame.Surface((xy_circle_width, xy_circle_height), pygame.SRCALPHA)
        xy_circle_rect = pygame.Rect(0, 0, xy_circle_width, xy_circle_height)
        pygame.draw.ellipse(xy_circle_surface, BLUE, xy_circle_rect, 4)
        xy_circle_surface_rotated = pygame.transform.rotate(xy_circle_surface, 25)
        xy_circle_rect = xy_circle_surface_rotated.get_rect(center=xy_circle_center)

        WIN.blit(xy_circle_surface_rotated, xy_circle_rect)

        make_line(self.interact_radius * y_unit_length, x_angle,
                  ((WIDTH // 2), (HEIGHT // 2) - (self.idle_height // 2)), BLUE)
        make_line(-(self.interact_radius * y_unit_length), x_angle,
                  ((WIDTH // 2), (HEIGHT // 2) - (self.idle_height // 2)), BLUE)

        make_line(self.interact_radius * x_unit_length, y_angle,
                  ((WIDTH // 2), (HEIGHT // 2) - (self.idle_height // 2)), BLUE)
        make_line(-(self.interact_radius * x_unit_length), y_angle,
                  ((WIDTH // 2), (HEIGHT // 2) - (self.idle_height // 2)), BLUE)

        make_line(self.interact_radius * z_unit_length, z_angle,
                  ((WIDTH // 2), (HEIGHT // 2) - (self.idle_height // 2)), BLUE)
        make_line(-(self.interact_radius * z_unit_length), z_angle,
                  ((WIDTH // 2), (HEIGHT // 2) - (self.idle_height // 2)), BLUE)

    def check_block(self, planet, orientation):
        blocks_info = list(find_block(self, orientation))
        block_ids = []
        solid_blocks = 0
        if len(blocks_info) > 0:
            for block_info in blocks_info:
                chunk_ind = block_info[0]
                block_ind = block_info[1]
                block_id = ''
                for block in planet.chunk(chunk_ind):
                    if block.ind == block_ind:
                        block_id = block_id + block.id
                if block_id == '':
                    block_id = block_id + '0'
                if block_id == '0':
                    pass
                else:
                    solid_blocks += 1
        if orientation == 'below':
            if solid_blocks > 0:
                self.on_ground = True
            else:
                self.on_ground = False
            return block_ids
        if orientation == 'above':
            if solid_blocks > 0:
                self.collide_ceiling = True
            else:
                self.collide_ceiling = False
            return block_ids
        if orientation == 'north':
            if solid_blocks > 0:
                self.collide_north = True
            else:
                self.collide_north = False
            return block_ids
        if orientation == 'south':
            if solid_blocks > 0:
                self.collide_south = True
            else:
                self.collide_south = False
            return block_ids
        if orientation == 'west':
            if solid_blocks > 0:
                self.collide_west = True
            else:
                self.collide_west = False
            return block_ids
        if orientation == 'east':
            if solid_blocks > 0:
                self.collide_east = True
            else:
                self.collide_east = False
            return block_ids

    def initiate_jump(self):
        if self.on_ground:
            self.z_velocity += self.initial_jump_speed
        else:
            pass

    def render(self, keys_pressed):

        if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_s] and\
                not keys_pressed[pygame.K_a] or keys_pressed[pygame.K_w] and keys_pressed[pygame.K_a] and\
                not keys_pressed[pygame.K_s] and not keys_pressed[pygame.K_d] or keys_pressed[pygame.K_s] and\
                keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_a] or\
                keys_pressed[pygame.K_s] and keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_w] and\
                not keys_pressed[pygame.K_d]:
            self.x_speed = 0.1
            self.y_speed = 0.1

        if keys_pressed[pygame.K_w]:
            if self.collide_north:
                self.y = ceil(self.y) - (self.hit_box_length / 2)
            else:
                self.y += self.y_speed
            if self.direction[1] < 1:
                self.direction[1] += 1
        if keys_pressed[pygame.K_s]:
            if self.collide_south:
                self.y = floor(self.y) + (self.hit_box_length / 2) + 0.1
            else:
                self.y -= self.y_speed
            if self.direction[1] > -1:
                self.direction[1] -= 1
        if keys_pressed[pygame.K_a]:
            if self.collide_west:
                self.x = ceil(self.x) - (self.hit_box_length / 2)
            else:
                self.x += self.x_speed
            if self.direction[0] < 1:
                self.direction[0] += 1
        if keys_pressed[pygame.K_d]:
            if self.collide_east:
                self.x = floor(self.x) + (self.hit_box_length / 2) + 0.1
            else:
                self.x -= self.x_speed
            if self.direction[0] > -1:
                self.direction[0] -= 1

        if not keys_pressed[pygame.K_w] and not keys_pressed[pygame.K_s] and not keys_pressed[pygame.K_a] and not \
                keys_pressed[pygame.K_d]:
            self.draw('idle')
            self.x_vel = 0
            self.y_vel = 0
        else:
            if self.direction[0] == 1:
                self.x_vel = self.x_speed
            elif self.direction[0] == -1:
                self.x_vel = -self.x_speed
            if self.direction[1] == 1:
                self.y_vel = self.y_speed
            elif self.direction[1] == -1:
                self.y_vel = -self.y_speed

            if self.collide_east or self.collide_west:
                self.x_vel = 0
            if self.collide_north or self.collide_south:
                self.y_vel = 0

            if self.on_ground:
                self.draw('run')
            else:
                self.draw('idle')

        if self.direction[0] and self.direction[1] != 0:  # this determines which direction the player faces
            if keys_pressed[pygame.K_a] and keys_pressed[pygame.K_w] or \
                    not keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_w]:
                pass
            else:
                if keys_pressed[pygame.K_a]:
                    self.direction[0] = 1
                    self.direction[1] = 0
                if keys_pressed[pygame.K_w]:
                    self.direction[0] = 0
                    self.direction[1] = 1
            if keys_pressed[pygame.K_d] and keys_pressed[pygame.K_w] or \
                    not keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_w]:
                pass
            else:
                if keys_pressed[pygame.K_d]:
                    self.direction[0] = -1
                    self.direction[1] = 0
                if keys_pressed[pygame.K_w]:
                    self.direction[0] = 0
                    self.direction[1] = 1
            if keys_pressed[pygame.K_a] and keys_pressed[pygame.K_s] or \
                    not keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_s]:
                pass
            else:
                if keys_pressed[pygame.K_a]:
                    self.direction[0] = 1
                    self.direction[1] = 0
                if keys_pressed[pygame.K_s]:
                    self.direction[0] = 0
                    self.direction[1] = -1
            if keys_pressed[pygame.K_d] and keys_pressed[pygame.K_s] or \
                    not keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_s]:
                pass
            else:
                if keys_pressed[pygame.K_d]:
                    self.direction[0] = -1
                    self.direction[1] = 0
                if keys_pressed[pygame.K_w]:
                    self.direction[0] = 0
                    self.direction[1] = 1

        self.z += self.z_velocity
        if not self.on_ground:
            if self.z_velocity > -self.z_speed_max:
                self.z_velocity -= GRAVITY
        if self.on_ground and self.z_velocity < 0:
            self.z_velocity = 0
            self.z = ceil(self.z)
        if not self.on_ground and self.z_velocity > 0 and self.collide_ceiling:
            self.z = floor(self.z + self.hit_box_height) - self.hit_box_height
            self.z_velocity = 0

        self.x_speed = 0.15
        self.y_speed = 0.15
        self.update_location((self.x, self.y, self.z))


# GUI


class Cursor:

    def __init__(self):
        self.image_width = 0
        self.image_height = 0
        self.image = pygame.image.load(rf'assets\textures\cursor.png').convert_alpha()
        self.location = pygame.mouse.get_pos()
        self.rect = self.image.get_rect(center=self.location)

        self.selected_blocks = []

    def update_pos(self):
        pos = pygame.mouse.get_pos()
        self.location = pos
        self.rect = self.image.get_rect(center=self.location)

    def draw(self):
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        WIN.blit(self.image, self.rect)


class Icon(pygame.sprite.Sprite):
    def __init__(self, image, size, center):
        super().__init__()
        self.image = image
        self.image_orig = self.image
        self.size = size
        self.size_base = size
        self.cx, self.cy = center
        self.rect = self.image.get_rect(center=(self.cx, self.cy))
        self.scale = 1
        self.scale_min, self.scale_max = 1, 1.05
        self.scale_change = 0.01
        self.scale_accel = 0.002
        self.selected = False

    def update_vars(self):
        size_old_x, size_old_y = self.size_base
        self.size = round(size_old_x * self.scale), round(size_old_y * self.scale)
        self.image = pygame.transform.scale(self.image_orig, self.size)
        self.rect = self.image.get_rect(center=(self.cx, self.cy))

        if Cursor().rect.colliderect(self.rect):
            self.selected = True
        else:
            self.selected = False

    def handle_select1(self):
        if self.selected:
            if self.scale < self.scale_max:
                self.scale += self.scale_change
            else:
                self.scale = self.scale_max
        elif not self.selected:
            if self.scale > self.scale_min:
                self.scale -= self.scale_change
            else:
                self.scale = self.scale_min

    def draw(self, surf):
        surf.blit(self.image, self.rect)


class PlanetIcon(pygame.sprite.Sprite):
    def __init__(self, name, directory, size, center, rotation_speed):
        super().__init__()
        self.name = name
        self.size = size
        self.center = center

        self.current_frame = 3
        self.frames = len(os.listdir(directory))

        self.images = []
        for i in range(self.frames):
            frame_string = ''
            if i < 10:
                frame_string = f'00{i}'
            if 10 <= i < 100:
                frame_string = f'0{i}'
            if 100 <= i < 1000:
                frame_string = f'{i}'
            img = pygame.image.load(directory + '\\' + name + '-' + frame_string + '.png')
            img = pygame.transform.scale(img, size)
            self.images.append(img)

        self.icon = Icon(self.images[self.current_frame], size, center)

        self.rotation_speed = rotation_speed

        self.tick = 0

    def update_vars(self):
        self.icon.update_vars()

    def handle_planet(self):
        img = self.images[self.current_frame]
        self.icon.image = img
        self.icon.image_orig = img
        if self.rotation_speed >= 1:
            if self.tick % 1 == 0:
                self.current_frame += self.rotation_speed
            if self.current_frame >= self.frames:
                self.current_frame = 0
        if 0 < self.rotation_speed < 1:
            if self.tick % (1 // self.rotation_speed) == 0:
                self.current_frame += 1
            if self.current_frame >= self.frames:
                self.current_frame = 0
        if -1 < self.rotation_speed < 0:
            if self.tick % (1 // -self.rotation_speed) == 0:
                self.current_frame -= 1
            if self.current_frame < 0:
                self.current_frame = self.frames
        if self.rotation_speed <= -1:
            if self.tick % 1 == 0:
                self.current_frame += self.rotation_speed
            if self.current_frame < 0:
                self.current_frame = self.frames - 1
        if self.rotation_speed == 0:
            pass

        self.icon.handle_select1()

        self.tick += 1

    def draw(self, surf):
        self.icon.draw(surf)


class Slider(pygame.sprite.Sprite):
    def __init__(self, text_dir, knob_size, slider_size, center):
        super().__init__()
        self.slider_image = pygame.image.load(rf'assets\textures\slider.png').convert_alpha()
        self.slider_image_orig = self.slider_image
        self.slider_size = slider_size
        self.slider_size_base = slider_size

        self.cx, self.cy = center
        self.knob_x_min = self.cx - (self.slider_size[0] // 2) + 5
        self.knob_x_max = self.cx + (self.slider_size[0] // 2) - 5
        self.knob_percent = 75
        self.knob_pos = round((self.knob_x_max - self.knob_x_min) * (self.knob_percent / 100))
        self.slider_rect = self.slider_image.get_rect(center=(self.cx, self.cy))

        self.knob_img = pygame.image.load(rf'assets\textures\knob.png')
        self.knob = Icon(self.knob_img, knob_size, (self.knob_x_min + self.knob_pos, self.cy))

        self.text = pygame.image.load(text_dir).convert_alpha()
        self.text_rect = self.text.get_rect(center=(self.cx, self.cy - 15))

        self.scale_min, self.scale_max = 1, 1.05
        self.scale_change = 0.01
        self.scale_accel = 0.002
        self.selected = False
        self.slidable = False

    def update_vars(self):
        self.knob.cx, self.knob.cy = self.knob_x_min + self.knob_pos, self.cy
        self.knob.update_vars()
        self.slider_rect = self.slider_image.get_rect(center=(self.cx, self.cy))
        self.text_rect = self.text.get_rect(center=(self.cx, self.cy - 25))
        self.knob_percent = (self.knob_pos / (self.knob_x_max - self.knob_x_min)) * 100

    def handle_slider(self):
        self.knob.handle_select1()
        if self.slidable:
            self.knob.selected = True
            if self.knob_x_min < Cursor().location[0] < self.knob_x_max:
                self.knob_pos = Cursor().location[0] - self.knob_x_min
            elif Cursor().location[0] < self.knob_x_min:
                self.knob_pos = 0
            elif Cursor().location[0] > self.knob_x_max:
                self.knob_pos = self.knob_x_max - self.knob_x_min

    def draw(self, surf):
        surf.blit(self.text, self.text_rect)
        surf.blit(self.slider_image, self.slider_rect)
        self.knob.draw(surf)


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.m0 = pygame.image.load(rf'assets\textures\menu0.png').convert_alpha()
        self.m0_size = 305, 465
        self.m0_location0 = WIDTH - self.m0_size[0] - 10, -self.m0_size[1]

        self.mx, self.my = WIDTH - self.m0_size[0] - 10, -self.m0_size[1]
        self.menu0_rect = self.m0.get_rect(topleft=self.m0_location0)
        self.p0 = pygame.image.load(rf'assets\textures\pause0.png')
        self.p1 = pygame.image.load(rf'assets\textures\pause1.png')
        self.p2 = pygame.image.load(rf'assets\textures\play0.png')
        self.p3 = pygame.image.load(rf'assets\textures\play1.png')
        self.p_size = 70, 70
        self.p_location = self.mx + (self.m0_size[0] - self.p_size[0]), self.my + (self.m0_size[1] + 5)

        self.p_rect = self.p0.get_rect(topleft=self.p_location)
        self.p_selected = False

        self.resume_img = pygame.image.load(rf'assets\textures\resume.png')
        self.resume = Icon(self.resume_img, (200, 40), (self.mx + 100 + 50, self.my + 20 + 30))

        self.view_map_img = pygame.image.load(rf'assets\textures\view_map.png')
        self.view_map = Icon(self.view_map_img, (195, 30),
                             (self.mx + 100 + 50, self.my + 20 + 30 + 50))

        self.settings_img = pygame.image.load(rf'assets\textures\settings.png')
        self.settings = Icon(self.settings_img, (190, 30),
                             (self.mx + 100 + 50, self.my + 20 + 30 + 100))

        self.quick_save_img = pygame.image.load(rf'assets\textures\quick_save.png')
        self.quick_save = Icon(self.quick_save_img, (230, 35),
                             (self.mx + 100 + 50, self.my + 20 + 30 + 150))

        self.save_quit_img = pygame.image.load(rf'assets\textures\save_quit.png')
        self.save_quit = Icon(self.save_quit_img, (230, 35),
                             (self.mx + 100 + 50, self.my + 20 + 30 + 200))

        self.sfx = Slider(rf'assets\textures\sfx.png', (30, 30), (240, 15),
                          (self.mx + 100 + 50, self.my + 20 + 30 + 300))
        self.music = Slider(rf'assets\textures\music.png', (30, 30), (240, 15),
                            (self.mx + 100 + 50, self.my + 20 + 30 + 350))

        self.icons = [self.resume, self.view_map, self.settings, self.quick_save, self.save_quit]

        self.sliders = [self.sfx, self.music]

        self.drop_rate = 30
        self.rise_rate = 0

        self.cursor_over = False
        self.is_dropped = False

    def update_vars(self):
        for index, icon in enumerate(self.icons):
            icon.cx, icon.cy = self.mx + 100 + 50, self.my + 20 + 30 + (index * 60)
        for index, slider in enumerate(self.sliders):
            slider.cx, slider.cy = self.mx + 100 + 50, self.my + 20 + 30 + 320 + (50 * index)

        self.menu0_rect = self.m0.get_rect(topleft=(self.mx, self.my))
        self.p_rect = self.p0.get_rect(topleft=self.p_location)
        self.p_location = self.mx + (self.m0_size[0] - self.p_size[0]), self.my + (self.m0_size[1] + 5)
        self.update_icons()

        if Cursor().rect.colliderect(self.menu0_rect):
            self.cursor_over = True
        else:
            self.cursor_over = False

        if Cursor().rect.colliderect(self.p_rect):
            self.p_selected = True
        else:
            self.p_selected = False

    def handle_movement(self):
        if self.is_dropped:
            self.drop()
            self.handle_icons()
        else:
            self.rise()

    def update_icons(self):
        for icon in self.icons:
            icon.update_vars()
        for slider in self.sliders:
            slider.update_vars()

    def handle_icons(self):
        for icon in self.icons:
            icon.handle_select1()
        for slider in self.sliders:
            slider.handle_slider()

    def draw_icons(self):
        for icon in self.icons:
            icon.draw(WIN)
        for slider in self.sliders:
            slider.draw(WIN)

    def drop(self):
        if self.my < 0:
            self.my += self.drop_rate
            if self.drop_rate > 1:
                self.drop_rate -= 1
        else:
            self.my = 0

    def rise(self):
        if self.my > self.m0_location0[1]:
            self.my -= self.drop_rate
            self.drop_rate += 1
        else:
            self.my = self.m0_location0[1]

    def draw(self):
        self.update_vars()
        WIN.blit(self.m0, (self.mx, self.my))
        self.draw_icons()
        if self.is_dropped:
            if Cursor().rect.colliderect(self.p_rect):
                WIN.blit(self.p3, self.p_location)
            else:
                WIN.blit(self.p2, self.p_location)
        else:
            if Cursor().rect.colliderect(self.p_rect):
                WIN.blit(self.p1, self.p_location)
            else:
                WIN.blit(self.p0, self.p_location)


class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.button0_dir = rf'assets\textures\inv_button-0.png'
        self.button1_dir = rf'assets\textures\inv_button-1.png'
        self.button0 = pygame.image.load(self.button0_dir).convert_alpha()
        self.button1 = pygame.image.load(self.button1_dir).convert_alpha()
        self.image = self.button0
        self.rect = self.button0.get_rect()
        self.size = [round(0.33*self.rect.width), round(0.33*self.rect.height)]
        self.x, self.y = 10, 10

        self.selected = False
        self.clicked = False

        self.click_duration = 0

    def update_vars(self):
        if Cursor().rect.colliderect(self.rect):
            self.selected = True
        else:
            self.selected = False
        self.button0 = pygame.transform.scale(self.button0, self.size)
        self.button1 = pygame.transform.scale(self.button1, self.size)
        if self.clicked:
            self.image = self.button1
            self.click_duration += 1
            if self.click_duration == (FPS // 8):
                self.click_duration = 0
                self.clicked = False
        else:
            self.image = self.button0
        self.rect = self.button0.get_rect()

    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))


class GodInventory(pygame.sprite.Sprite):
    def __init(self):
        super().__init__()


# WORLD


class Background(pygame.sprite.Sprite):
    def __init__(self, directory):
        super().__init__()
        self.file_type = directory[:-4]
        self.bg_type = ''
        self.bg_size = WIDTH, HEIGHT
        self.animated = False
        self.img = os.listdir(directory)

        if len(self.img) == 1:
            pass
        else:
            self.animated = True

        if self.animated:
            for i in self.img:
                img = pygame.image.load(i).convert_alpha()
                img = pygame.transform.scale(img, self.bg_size)
                self.img.append(img)
        else:
            self.img = pygame.image.load(directory + '\\' + self.img[0])
            self.img = pygame.transform.scale(self.img, self.bg_size)

    def draw(self, surf):
        if self.animated:
            pass
        else:
            surf.blit(self.img, (0, 0))


class Block(pygame.sprite.Sprite):

    def __init__(self, block_id, block_ind, chunk_ind):
        super().__init__()   # ROOT CAUSE OF LAG - FIND WAY TO REDUCE BLOCK CREATION PER FRAME
        self.id = block_id
        self.ind = block_ind
        self.chunk_ind = chunk_ind
        self.location = find_block_location(self.ind, self.chunk_ind)
        self.x, self.y, self.z = self.location
        self.screen_x = grid_origin[0] - (self.x * y_gap_x_comp) - \
                        (self.y * x_gap_x_comp) + x_gap_x_comp
        self.screen_y = grid_origin[1] - (self.y * x_gap_y_comp) - \
                        (self.x * y_gap_y_comp) - (self.z * z_unit_length)

        self.hit_box_length = 1
        self.hit_box_width = 1
        self.hit_box_height = 1
        self.hit_box_boundaries = (self.x - self.hit_box_length, self.y - self.hit_box_width, self.z),\
                                  (self.x, self.y, self.z + self.hit_box_height)
        self.texture_path = get_texture(self.id)
        self.image = pygame.image.load(self.texture_path).convert_alpha()
        self.image_copy = self.image.copy()

        # ALPHA SETTINGS
        self.in_front = False
        self.trans = False

        self.alpha = 255
        self.alpha_min = 25
        self.alpha_max = 255

        self.highlight = pygame.image.load(r'assets\textures\block_highlight_bright.png').convert_alpha()

        self.rect = self.image.get_rect()

        self.is_selected = False
        self.face_select = ''

        self.resistance = 1

    def selected(self, face):
        cx, cy = Cursor().location
        if face == 'f':  # FRONT OR SOUTH
            if self.select_border(face, 'l', cy) < cx < self.select_border(face, 'r', cy) and \
                    self.select_border(face, 't', cx) < cy < self.select_border(face, 'b', cx):
                return True
            else:
                return False
        if face == 'r':  # RIGHT OR EAST
            if self.select_border(face, 'l', cy) < cx < self.select_border(face, 'r', cy) and \
                    self.select_border(face, 't', cx) < cy < self.select_border(face, 'b', cx):
                return True
            else:
                return False
        if face == 't':  # TOP OR ABOVE
            if self.select_border(face, 'l', cx) < cy < self.select_border(face, 'r', cx) and \
                    self.select_border(face, 't', cx) < cy < self.select_border(face, 'b', cx):
                return True
            else:
                return False
        if face == 'np':  # NO PREFERENCE
            if self.select_border('f', 'l', cy) < cx < self.select_border('f', 'r', cy) and \
                    self.select_border('f', 't', cx) < cy < self.select_border('f', 'b', cx):
                return True
            elif self.select_border('r', 'l', cy) < cx < self.select_border('r', 'r', cy) and \
                    self.select_border('r', 't', cx) < cy < self.select_border('r', 'b', cx):
                return True
            elif self.select_border('t', 'r', cx) < cy < self.select_border('t', 'l', cx) and \
                    self.select_border('t', 't', cx) < cy < self.select_border('t', 'b', cx):
                return True
            else:
                return False

    def blit_alpha(self, surface, image, location, alpha):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((image.get_width(), image.get_height()))
        temp.blit(surface, (-x, -y))
        temp.blit(image, (0, 0))
        temp.set_alpha(alpha)
        surface.blit(temp, location)

    def draw(self, screen):
        if self.trans:
            if self.alpha > self.alpha_min:
                self.alpha -= 10
            self.blit_alpha(screen, self.image, self.rect, self.alpha)
        else:
            if self.alpha < self.alpha_max:
                self.alpha += 10
                self.blit_alpha(screen, self.image, self.rect, self.alpha)
            else:
                screen.blit(self.image, self.rect)
        if self.is_selected:
            screen.blit(self.highlight, self.rect)
        self.is_selected = False
        self.face_select = ''

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def update_grid_displacement(self, player_location):
        px, py, pz = player_location
        rel_grid_x, rel_grid_y, rel_grid_z = self.x - px, self.y - py, self.z - pz
        self.screen_x = grid_origin[0] - (rel_grid_x * y_gap_x_comp) - (rel_grid_y * x_gap_x_comp) + x_gap_x_comp
        self.screen_y = grid_origin[1] - (rel_grid_y * x_gap_y_comp) - (rel_grid_x * y_gap_y_comp) \
                        - (rel_grid_z * z_unit_length)
        self.rect.x = round(self.screen_x)
        self.rect.y = round(self.screen_y)

    def destroy(self, tool):
        pass

    def select_border(self, face, border, var):
        if face == 'r':
            if border == 'l':
                x = x_unit_length + self.screen_x
                return x
            if border == 'r':
                x = x_unit_length + abs(x_gap_x_comp) + self.screen_x
                return x
            if border == 't':
                y = (-(sqrt(3)) * ((var - self.screen_x) - abs(x_gap_x_comp) - x_unit_length)) + self.screen_y
                return y
            if border == 'b':
                y = ((-(sqrt(3)) * ((var - self.screen_x) - abs(x_gap_x_comp) - x_unit_length)) + z_unit_length)\
                    + self.screen_y
                return y
        if face == 't':
            if border == 'l':
                y = (-(sqrt(3)) * ((var - self.screen_x) - abs(x_gap_x_comp))) + self.screen_y
                return y
            if border == 'r':
                y = (-(sqrt(3)) * ((var - self.screen_x) - abs(x_gap_x_comp) - x_unit_length)) + self.screen_y
                return y
            if border == 't':
                y = self.screen_y
                return y
            if border == 'b':
                y = x_gap_y_comp + self.screen_y
                return y
        if face == 'f':
            if border == 'l':
                x = self.screen_x
                return x
            if border == 'r':
                x = x_unit_length + self.screen_x
                return x
            if border == 't':
                y = x_gap_y_comp + self.screen_y
                return y
            if border == 'b':
                y = x_gap_y_comp + z_unit_length + self.screen_y
                return y


class Chunk(pygame.sprite.Group):
    def __init__(self, chunk_ind, planet):
        super().__init__()
        self.ind = chunk_ind
        self.planet = planet
        self.planet_file = self.planet.file
        self.planet_data = self.planet.data

        self.is_full = False

        self.term_point = MAX_COORDS[0] - ((self.ind / WORLD_SIZE_X - floor(
            self.ind / WORLD_SIZE_X)) * WORLD_SIZE_X * CHUNK_X), MAX_COORDS[1] - (floor(
            (self.ind - (WORLD_SIZE_Y * WORLD_SIZE_X * range(WORLD_SIZE_Z)[int(floor(
                self.ind / (WORLD_SIZE_X * WORLD_SIZE_Y)))])) / WORLD_SIZE_X) * CHUNK_Y), \
                          ((floor(self.ind / (WORLD_SIZE_X * WORLD_SIZE_Y)) + 1) * CHUNK_Z) - MAX_COORDS[2]

    def block_sort_key(self, block):
        return block.ind

    def fill(self):
        for i in range(CHUNK_X * CHUNK_Y * CHUNK_Z):
            block_id = self.planet_data[self.ind][i]
            if block_id == '0':
                pass
            else:
                if self.planet.is_obscured(self.ind, i, 'all'):
                    pass
                else:
                    block = Block(block_id, i, self.ind)
                    self.add(block)
        self.is_full = True

    def reassign(self, new_ind):
        for block in self:
            block.kill()
        self.empty()
        self.ind = new_ind
        self.fill()

    def refresh(self):
        for block in self:
            block.kill()
        self.fill()

    def block_exists(self, block_ind):
        found = False
        for block in self:
            if block.ind == block_ind:
                found = True
                return True
        if not found:
            return False

    def block(self, block_ind):
        found = False
        for block in self:
            if block.ind == block_ind:
                found = True
                return block
        if not found:
            return ValueError

    def update_grid_displacement(self, player_location):
        for block in self:
            block.update_grid_displacement(player_location)

    def update_file(self):
        self.planet_file.seek(0)
        json.dump(self.planet_data, self.planet_file)

    def add_block(self, block_id, block_ind):
        if self.block_exists(block_ind):
            pass
        else:
            self.planet_data[self.ind][block_ind] = block_id
            self.refresh()

    def remove_block(self, block_ind):
        if self.block_exists(block_ind):
            self.planet_data[self.ind][block_ind] = '0'
            self.refresh()
        else:
            pass


class Planet:

    def __init__(self, save, name, directory):
        # ARGS
        self.save = save
        self.name = name
        self.directory = directory
        # FILE
        self.file = open(self.directory, 'r+')
        self.data = json.load(self.file)
        # BLOCKS
        self.blocks_front = []
        self.blocks_trans = []
        self.selected_blocks = []
        # CHUNKS
        self.player_chunk_spot = ''
        self.chunk_ind_in_range_old = set()
        self.chunk_ind_in_range = set()
        self.chunk_ind_arrived = []
        self.chunk_ind_departed = []
        self.chunks_in_range = []
        self.chunk_ind_visited = set()
        self.spot_x, self.spot_y, self.spot_z = 0, 0, 0
        # ENTITIES
        self.entities = []
        # PLAYER
        self.spawn_point = (0, 0, 0)
        # TRACKING
        self.tick = 0

    def chunk_exists(self, chunk_ind):
        found = False
        for chunk in self.chunks_in_range:
            if chunk.ind == chunk_ind:
                found = True
            else:
                pass
        return found

    def chunk(self, chunk_ind):
        found = False
        for chunk in self.chunks_in_range:
            if chunk.ind == chunk_ind:
                found = True
                return chunk
            else:
                pass
        if not found:
            print('chunk out of range')
            return None

    def handle_block_selection(self):
        self.selected_blocks.clear()
        grid_coords = screen_to_grid_pos(Cursor().location, self.save.player)  # most expensive
        for coord in grid_coords:   # second most expensive
            gx, gy, gz = coord
            g_coord = ceil(gx), ceil(gy), ceil(gz)
            chunk_ind = find_chunk_index(g_coord)
            block_ind = find_relative_block_index(g_coord)
            if self.chunk_exists(chunk_ind):
                if self.chunk(chunk_ind).block_exists(block_ind):
                    if self.data[chunk_ind][block_ind] != '0' and not self.is_obscured(chunk_ind, block_ind, 'all') and\
                            not self.chunk(chunk_ind).block(block_ind) in self.blocks_trans:
                        block = self.chunk(chunk_ind).block(block_ind)
                        if block.selected('f') and not self.is_obscured(block.chunk_ind, block.ind, 'f'):
                            block.face_select = 'f'
                        if block.selected('r') and not self.is_obscured(block.chunk_ind, block.ind, 'r'):
                            block.face_select = 'r'
                        if block.selected('t') and not self.is_obscured(block.chunk_ind, block.ind, 't'):
                            block.face_select = 't'
                        self.selected_blocks.append(block)
                        block.is_selected = True
                        break

    def is_obscured(self, chunk_ind, block_ind, face):
        if self.data[chunk_ind][block_ind] != '0':
            max_ind = (CHUNK_X * CHUNK_Y * CHUNK_Z) - 1
            tot_blocks = CHUNK_X * CHUNK_Y * CHUNK_Z

            block_east = block_ind + 1
            chunk_east = chunk_ind
            if block_east % CHUNK_X == 0:
                block_east -= CHUNK_X
                chunk_east += 1

            block_west = block_ind - 1
            chunk_west = chunk_ind
            if (block_west + 1) % CHUNK_X == 0:
                block_west += CHUNK_X
                chunk_west -= 1

            block_south = block_ind + CHUNK_X
            chunk_south = chunk_ind
            if floor(block_south / (CHUNK_X * CHUNK_Y)) != floor(block_ind / (CHUNK_Y * CHUNK_Y)):
                block_south -= CHUNK_X * CHUNK_Y
                chunk_south += WORLD_SIZE_X

            block_north = block_ind - CHUNK_X
            chunk_north = chunk_ind
            if fceil(block_north / (CHUNK_X * CHUNK_Y)) != fceil(block_ind / (CHUNK_Y * CHUNK_Y)):
                block_north += CHUNK_X * CHUNK_Y
                chunk_north -= WORLD_SIZE_X

            block_top = block_ind + (CHUNK_X * CHUNK_Y)
            chunk_top = chunk_ind
            if block_top > max_ind:
                block_top -= tot_blocks
                chunk_top += WORLD_SIZE_X * WORLD_SIZE_Y

            block_below = block_ind - (CHUNK_X * CHUNK_Y)
            chunk_below = chunk_ind
            if block_below < 0:
                block_below += tot_blocks
                chunk_below -= WORLD_SIZE_X * WORLD_SIZE_Y

            if face == 'all':
                if self.data[chunk_east][block_east] != '0' and self.data[chunk_south][block_south] != '0' and \
                        self.data[chunk_top][block_top] != '0' and self.data[chunk_west][block_west] != '0' and \
                        self.data[chunk_north][block_north] != '0' and self.data[chunk_below][block_below] != '0':
                    return True
                else:
                    return False
            if face == 'e':
                if self.data[chunk_east][block_east] != '0':
                    return True
                else:
                    return False
            if face == 'w':
                if self.data[chunk_west][block_west] != '0':
                    return True
                else:
                    return False
            if face == 's':
                if self.data[chunk_south][block_south] != '0':
                    return True
                else:
                    return False
            if face == 'n':
                if self.data[chunk_north][block_north] != '0':
                    return True
                else:
                    return False
            if face == 't':
                if self.data[chunk_top][block_top] != '0':
                    return True
                else:
                    return False
            if face == 'b':
                if self.data[chunk_below][block_below] != '0':
                    return True
                else:
                    return False
        else:
            return False

    def generate(self):
        file = open(self.directory, 'w')
        data = []
        for i in range(WORLD_SIZE_X * WORLD_SIZE_Y * WORLD_SIZE_Z // 2):
            chunk_data = write_chunk_list('bottom')
            data.append(chunk_data)
        for i in range(WORLD_SIZE_X * WORLD_SIZE_Y * WORLD_SIZE_Z // 2):
            chunk_data = write_chunk_list('top')
            data.append(chunk_data)
        json.dump(data, file)
        file.close()

    def handle_render_rate(self, rate):
        if len(self.chunk_ind_departed) and len(self.chunk_ind_arrived) > rate - 1:
            for i in range(rate):
                chunk = self.chunk(self.chunk_ind_departed[0])
                if chunk in self.chunks_in_range:
                    chunk.reassign(self.chunk_ind_arrived[0])
                    self.chunk_ind_arrived.remove(self.chunk_ind_arrived[0])
                    self.chunk_ind_departed.remove(self.chunk_ind_departed[0])

    def render_chunks(self, player):
        px, py, pz = player.location
        self.chunk_ind_in_range.clear()

        if self.tick % 15 == 0:
            self.player_chunk_spot = find_chunk_spot(find_chunk_index((ceil(px), ceil(py), ceil(pz))))

        max_spot_difference_x = RENDER_DISTANCE
        max_spot_difference_y = RENDER_DISTANCE
        max_spot_difference_z = MAX_COORDS[2] // CHUNK_Z

        max_spot_x = self.player_chunk_spot[0] + max_spot_difference_x
        if max_spot_x > WORLD_SIZE_X - 1:
            max_spot_x = WORLD_SIZE_X - 1
        max_spot_y = self.player_chunk_spot[1] + max_spot_difference_y
        if max_spot_y > WORLD_SIZE_Y - 1:
            max_spot_y = WORLD_SIZE_Y - 1
        max_spot_z = self.player_chunk_spot[2] + max_spot_difference_z
        if max_spot_z > WORLD_SIZE_Z - 1:
            max_spot_z = WORLD_SIZE_Z - 1
        min_spot_x = self.player_chunk_spot[0] - max_spot_difference_x
        if min_spot_x < 0:
            min_spot_x = 0
        min_spot_y = self.player_chunk_spot[1] - max_spot_difference_y
        if min_spot_y < 0:
            min_spot_y = 0
        min_spot_z = self.player_chunk_spot[2] - max_spot_difference_z
        if min_spot_z < 0:
            min_spot_z = 0

        if self.tick == 0:
            self.spot_x, self.spot_y, self.spot_z = min_spot_x, min_spot_y, min_spot_z
            spot_z = min_spot_z
            while spot_z < max_spot_z:
                spot_y = min_spot_y
                while spot_y < max_spot_y:
                    spot_x = min_spot_x
                    while spot_x < max_spot_x:
                        if distance(self.player_chunk_spot, (spot_x, spot_y, spot_z)) < RENDER_DISTANCE:
                            chunk_ind = spot_to_ind((spot_x, spot_y, spot_z))
                            self.chunk_ind_in_range.add(chunk_ind)
                            chunk = Chunk(chunk_ind, self)
                            chunk.fill()
                            self.chunks_in_range.append(chunk)
                        else:
                            pass
                        spot_x += 1
                    spot_y += 1
                spot_z += 1
            self.chunk_ind_in_range_old = self.chunk_ind_in_range.copy()
        if self.tick > 0:
            spot_z = min_spot_z
            while spot_z < max_spot_z:
                spot_y = min_spot_y
                while spot_y < max_spot_y:
                    spot_x = min_spot_x
                    while spot_x < max_spot_x:
                        if distance(self.player_chunk_spot, (spot_x, spot_y, spot_z)) < RENDER_DISTANCE:
                            chunk_ind = spot_to_ind((spot_x, spot_y, spot_z))
                            self.chunk_ind_in_range.add(chunk_ind)
                        else:
                            pass
                        spot_x += 1
                    spot_y += 1
                spot_z += 1

            for i in self.chunk_ind_in_range.difference(self.chunk_ind_in_range_old):
                self.chunk_ind_arrived.append(i)
                '''print(f'arrived {i}')'''

            for i in self.chunk_ind_in_range_old.difference(self.chunk_ind_in_range):
                self.chunk_ind_departed.append(i)
                '''print(f'departed {i}')'''

            # FOUND THE ISSUE! THESE MUST STAY EQUAL BUT THEY DO NOT WHEN THE PLAYER REACHES THE WORLD BOUNDARY.
            # RESOLVE THIS BY FIRST PREVENTING THE DEPARTED LIST FROM FILLING UP WITH CHUNKS THAT LEAVE RENDER DISTANCE.
            # THESE CHUNKS HAVE NO NEW INDEXES TO BE REASSIGNED TO, HENCE WHY THERE IS A CRASH REGARDING THE ABSENCE OF
            # A TARGETED LIST ITEM.

            self.handle_render_rate(10)
            self.handle_block_selection()
            self.blocks_front.clear()
            self.blocks_trans.clear()

            self.spot_z += 1
            if self.spot_z == max_spot_z:
                self.spot_z = min_spot_z
                self.spot_y += 1
            if self.spot_y == max_spot_y:
                self.spot_y = min_spot_y
                self.spot_x += 1
            if self.spot_x == max_spot_x:
                self.spot_x = min_spot_x

        self.tick += 1

        self.chunk_ind_in_range_old = self.chunk_ind_in_range.copy()

    def chunk_sort_key(self, chunk):
        return chunk.ind

    def draw_blocks_behind(self, player):
        if self.tick > 0:
            for chunk in sorted(self.chunks_in_range, key=self.chunk_sort_key):
                if chunk is None:
                    pass
                else:
                    if chunk.is_full:
                        chunk.update_grid_displacement(player.location)
                        for block in chunk:
                            bsx, bsy = block.screen_x, block.screen_y
                            bx, by, bz = block.location
                            px, py, pz = player.location

                            p_center_s_coords = grid_to_screen_coords((px, py, pz +
                                                                       (player.hit_box_height / 2)),
                                                                      player.location)

                            if by <= ceil(py) and bz > pz: # add bx <= ceil(px) if needed
                                self.blocks_front.append(block)
                                block.in_front = True
                                if distance((bsx, bsy), p_center_s_coords) < (5 * z_unit_length) and\
                                        by <= ceil(py) - 1 and self.save.game.trans_blocks:
                                    self.blocks_trans.append(block)
                                    block.trans = True
                            else:
                                block.draw(WIN)
                        chunk.update()
                    else:
                        pass
        else:
            pass

    def draw_blocks_front(self):
        for block in self.blocks_front:
            block.draw(WIN)
            block.in_front = False
        for block in self.blocks_trans:
            block.trans = False

    def save_data(self):
        self.file.seek(0)
        json.dump(self.data, self.file)


class Save:

    def __init__(self, name, game):
        super().__init__()
        self.name = name
        self.game = game

        self.player = Player((0, 0, 2), SPAWN_DIRECTION)
        self.player_file = rf'assets\saves\{name}\player_data.json'

        self.planet1 = Planet(self, 'planet1', rf'assets\saves\{name}\planet1_data.json')
        self.current_planet = self.planet1

    def load(self):
        pass

    def save(self):
        pass


class Title:

    def __init__(self):
        self.bg = Background(rf'assets\textures\starry_bg')
        self.p1 = PlanetIcon('planet1', rf'assets\textures\planet1', (250, 250), ((3*WIDTH) // 4, HEIGHT // 2),
                             (1/2))
        self.p2 = PlanetIcon('planet2', rf'assets\textures\planet2', (250, 250), (WIDTH // 4, HEIGHT // 2),
                             0)

        self.icons = [self.p1, self.p2]

    def handle_icons(self):
        for icon in self.icons:
            icon.handle_planet()
            icon.update_vars()


# PRIMARY


class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        if not os.path.exists(r'assets\textures\mmm.jfif'):
            print('lmao')
            self.running = False
        self.saves = [Save('save1', self)]
        self.current_save = self.saves[0]

        self.cursor = Cursor()
        self.menu = Menu()
        self.title = Title()

        self.left_click = 1
        self.right_click = 3
        self.middle_click = 2

        self.trans_blocks = True

    def run(self):
        if self.current_save == '':
            pass
        else:
            save = self.current_save
            planet = save.current_planet
            player = save.player
            pygame.mixer.music.load(to_the_stars)
            pygame.mixer.music.play(-1)
        while self.running:
            self.clock.tick(FPS)
            if self.current_save == '':
                mouse_pressed = pygame.mouse.get_pressed()
                keys_pressed = pygame.key.get_pressed()
                self.cursor.update_pos()
                self.title.handle_icons()
                self.handle_title_events(keys_pressed, mouse_pressed)
                self.draw_window(keys_pressed)
            else:
                mouse_pressed = pygame.mouse.get_pressed()
                keys_pressed = pygame.key.get_pressed()
                self.cursor.update_pos()
                planet.render_chunks(player)
                self.handle_events(player, mouse_pressed)
                self.menu.handle_movement()
                player.inv.update_vars()
                self.draw_window(keys_pressed)
                player.check_block(planet, 'below')
                player.check_block(planet, 'north')
                player.check_block(planet, 'south')
                player.check_block(planet, 'east')
                player.check_block(planet, 'west')
                player.check_block(planet, 'above')

    def change_save(self, new_save):
        self.current_save = new_save

    def handle_title_events(self, keys_pressed, mouse_pressed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == self.left_click:
                    if self.title.p1.icon.selected:
                        self.current_save = self.saves[0]

    def handle_events(self, player, mouse_pressed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_save.current_planet.save_data()
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.Sound.play(menu_slide_sound)
                    self.menu.is_dropped = not self.menu.is_dropped
                if event.key == pygame.K_SPACE:
                    player.initiate_jump()
            if mouse_pressed[self.left_click - 1]:
                if self.menu.sfx.knob.selected:
                    self.menu.sfx.slidable = True
                if self.menu.music.knob.selected:
                    self.menu.music.slidable = True
                    pygame.mixer.music.set_volume(self.menu.music.knob_percent / 100)
            if not mouse_pressed[self.left_click - 1]:
                self.menu.sfx.slidable = False
                self.menu.music.slidable = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == self.left_click:
                    if player.inv.selected:
                        player.inv.clicked = True
                        player.inv.image = player.inv.button1
                    if self.menu.cursor_over or self.menu.p_selected:
                        if self.menu.resume.selected:
                            pygame.mixer.Sound.play(menu_slide_sound)
                            self.menu.is_dropped = False
                        if self.menu.quick_save.selected:
                            self.current_save.current_planet.save_data()
                        if self.menu.save_quit.selected:
                            self.current_save.current_planet.save_data()
                            self.current_save = ''
                        if self.menu.p_selected:
                            pygame.mixer.Sound.play(menu_slide_sound)
                            self.menu.is_dropped = not self.menu.is_dropped
                    else:
                        for block in self.current_save.current_planet.selected_blocks:
                            pygame.mixer.Sound.play(break_sound)
                            self.current_save.current_planet.chunk(block.chunk_ind).remove_block(block.ind)
                            for o in 'nswetb':  # for loop loads in blocks of surrounding chunks upon being exposed
                                next_chunk_ind = chunk_ind_next(block.chunk_ind, o)
                                if next_chunk_ind is not None:
                                    self.current_save.current_planet.chunk(next_chunk_ind).refresh()
                if event.button == self.right_click:
                    for block in self.current_save.current_planet.selected_blocks:
                        bx, by, bz = block.location
                        if block.face_select == 'r':
                            bx -= 1
                            c_ind = find_chunk_index((bx, by, bz))
                            b_ind = find_relative_block_index((bx, by, bz))
                            pygame.mixer.Sound.play(place_sound)
                            self.current_save.current_planet.chunk(c_ind).add_block('2', b_ind)
                        if block.face_select == 'f':
                            by -= 1
                            c_ind = find_chunk_index((bx, by, bz))
                            b_ind = find_relative_block_index((bx, by, bz))
                            pygame.mixer.Sound.play(place_sound)
                            self.current_save.current_planet.chunk(c_ind).add_block('2', b_ind)
                        if block.face_select == 't':
                            bz += 1
                            c_ind = find_chunk_index((bx, by, bz))
                            b_ind = find_relative_block_index((bx, by, bz))
                            pygame.mixer.Sound.play(place_sound)
                            self.current_save.current_planet.chunk(c_ind).add_block('2', b_ind)
                        else:
                            pass
                if event.button == self.middle_click:
                    self.trans_blocks = not self.trans_blocks
            if event.type == pygame.VIDEORESIZE:
                pass

    def draw_window(self, keys_pressed):
        if self.current_save == '':
            title = self.title
            pygame.draw.rect(WIN, WHITE, BG)
            title.bg.draw(WIN)
            for icon in title.icons:
                icon.draw(WIN)

            self.cursor.draw()
            pygame.display.flip()
        else:
            save = self.current_save
            planet = save.current_planet
            player = save.player

            pygame.draw.rect(WIN, WHITE, BG)

            planet.draw_blocks_behind(player)

            player.render(keys_pressed)

            planet.draw_blocks_front()

            display_coordinates(player.location)

            display_advanced_info(player, self.clock)

            player.draw_hit_box()

            """WIN.blit(FOG, (0, 0))"""

            self.menu.draw()
            player.inv.draw(WIN)

            self.cursor.draw()

            pygame.display.flip()

    def new_save(self, name):
        save = Save(name)
        self.saves.append(save)

    def delete_save(self, name):
        for save in self.saves:
            if save.name == name:
                self.saves.remove(save)