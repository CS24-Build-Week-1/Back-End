# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

from .models import Room
import pickle
import random

room_descriptions = pickle.load(open('./room_descriptions.p', 'rb'))

room_names = ['Amphitheater',
'Antechamber',
'Asylum',
'Atrium',
'Battlement',
'Belfry',
'Cave',
'Cavern',
'Chapel',
'Cloister',
'Coliseum',
'Courtyard',
'Depository',
'Foyer',
'Gallery',
'Garden',
'Garderobe',
'Greenhouse',
'Hideaway',
'Hold',
'Infirmary',
'Keep',
'Kitchen',
'Laboratory',
'Labrynth',
'Library',
'Minaret',
'Mine',
'Necropolis',
'Nursery',
'Observatory',
'Office',
'Ossuary',
'Oubliette',
'Pantry',
'Park',
'Passageway',
'Prison',
'Rampart',
'Repository',
'Room',
'Sanctum',
'Sepulcher',
'Spire',
'Stairwell',
'Steeple',
'Storage Room',
'Study',
'Sunroom',
'Temple',
'Threshold',
'Tower',
'Tunnel',
'Turret',
'Vault',
'Vestibule',
'Walkway',
'Dormitory',
'Eating hall',
'Master bedroom',
'Storeroom',
'Forge',
'Bath',
'Summoning room',
'Jail',
'Shrine',
'Courthall',
'Armory',
'Latrine',
'Guard post',
'Throne Room',
'Barracks',
'Pool/Well',
'Pantry/Storage',
'Wine Cellar',
'Meditation Room',
'Privy',
'Ballroom',
'Great Hall',
'Training Hall',
'Trophy Hall',
'Propylaeum',
'Conservatory',
'Kennel',
'Larder',
'Crematorium',
'Panopticon',
'Tomb',
'Crypt',
'Workshop',
'Foundry',
'Meeting Hall',
'Parlor',
'Sitting Room',
'Anteroom',
'Entrance Hall',
'Music Hall',
'Theater',
'Wardroom',
'Closet',
'War Room',
'Bedchamber',
'Cloakroom',
'Dressing Room',
'Studio',
'Linen Room',
'Boudoir',
'Refectory',
'Sewing Room',
'Buttery',
'Lavatory',
'Bakery',
]
class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.pos_x = pos_x
        self.pos_y = pos_y
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.pos_x}, {self.pos_y}) -> ({self.e_to.pos_x}, {self.e_to.pos_y})"
        return f"({self.pos_x}, {self.pos_y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        # (this will become 0 on the first step)
        pos_x = -1 
        pos_y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west


        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and pos_x < size_x - 1:
                room_direction = "e"
                pos_x += 1
            elif direction < 0 and pos_x > 0:
                room_direction = "w"
                pos_x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                pos_y += 1
                direction *= -1

            # Create a room in the given direction
            # room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
            room = Room(room_count, name = f'{random.choice(room_names)}', description=room_descriptions.pop()[:450], pos_x, pos_y)
            room.save()
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[pos_y][pos_x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)

            # Update iteration variables
            previous_room = room
            room_count += 1



    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 100
width = 10
height = 10
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
