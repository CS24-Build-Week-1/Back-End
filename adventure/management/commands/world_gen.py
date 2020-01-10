from django.core.management.base import BaseCommand, CommandError
from adventure.models import Room
import random
import pickle


random.seed(5)

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

MAX_X = 20
MAX_Y = 20
CREATE_RATE = 0.50

class Command(BaseCommand):
    def handle(self, *args, **options):

        class Room():
            total = 0
            def __init__(self, title, description, x, y, n=None, s=None, e=None, w=None):
                self.n_to = n
                self.s_to = s
                self.e_to = e
                self.w_to = w
                self.pos_x = x
                self.pos_y = y
                self.total += 1
                self.id = Room.total
            def connectRooms(self, destinationRoom, direction):
                destinationRoomID = destinationRoom.id
                if direction == "n":
                    self.n_to = destinationRoomID
                elif direction == "s":
                    self.s_to = destinationRoomID
                elif direction == "e":
                    self.e_to = destinationRoomID
                elif direction == "w":
                    self.w_to = destinationRoomID
                else:
                    print("Invalid direction")
                    return
        def show_grid(grid):
            for row in grid:
                roomline = []
                doorline = []
                for room in row:
                    if room is None:
                        roomline.append('  ')
                        doorline.append('  ')
                    else:
                        if room.e_to is not None:
                            roomline.append('O-')
                        else:
                            roomline.append('O ')
                        if room.s_to is not None:
                            doorline.append('| ')
                        else:
                            doorline.append('  ')
                print(''.join(roomline))
                print(''.join(doorline))
        # put into handle:
        width = 20
        grid = []
        for y in range(width):
            row = []
            for x in range(width):
                if random.random() <= CREATE_RATE:
                    room = row.append(Room(title = f'{random.choice(room_names)}', description=room_descriptions.pop()[:450], x = x, y = y))
                    if room is not None:
                        # row.append(room(x, y))
                        room.save()
                    grid.append(row)
                x = width // 2
                y = width // 2
                history = []
                visited = set()
                while len(visited) < width ** 2:
                    # print('start loop')
                    # show_grid(grid)
                    # print('x', x)
                    # print('y', y)
                    r = grid[y][x]
                    visited.add(r)
                    n = grid[y - 1][x] if y > 0 else None
                    s = grid[y + 1][x] if y < width - 1 else None
                    e = grid[y][x + 1] if x < width - 1 else None
                    w = grid[y][x - 1] if x > 0 else None
                    # print(n, s, e, w)
                    directions = []
                    if n is not None and n not in visited:
                        directions.append('n')
                    if s is not None and s not in visited:
                        directions.append('s')
                    if e is not None and e not in visited:
                        directions.append('e')
                    if w is not None and w not in visited:
                        directions.append('w')
                    # print(directions)
                    if len(directions) == 0: # backtrack
                        # print('backtrack', history)
                        go_back = history.pop()
                        # go the opposite way!
                        if go_back == 'n':
                            y += 1
                        if go_back == 's':
                            y -= 1
                        if go_back == 'e':
                            x -= 1
                        if go_back == 'w':
                            x += 1
                    else: # boldly go
                        # print('boldly go')
                        direction = random.choice(directions)
                        history.append(direction)
                        if direction == 'n':
                            r.connectRooms(n, 'n')
                            y -= 1
                            n.connectRooms(r, 's')
                        if direction == 's':
                            r.connectRooms(s, 's')
                            y += 1
                            s.connectRooms(r, 'n')
                        if direction == 'e':
                            r.connectRooms(e, 'e')
                            x += 1
                            e.connectRooms(r, 'w')
                        if direction == 'w':
                            r.connectRooms(w, 'w')
                            x -= 1
                            w.connectRooms(r, 'e')
                show_grid(grid)