from django.core.management.base import BaseCommand, CommandError
from adventure.models import Item, Room
import random

random.seed(5)


MAX_X = 20
MAX_Y = 20
CREATE_RATE = .55



class Command(BaseCommand):
    def handle(self, *args, **options):

        Item.objects.all().delete()

        for x in range(MAX_X):
            for y in range(MAX_Y):
                # Is there a room?
                room = Room.objects.filter(pos_x=x, pos_y=y).first()
                if room is not None and random.random() <= CREATE_RATE:
                    Item.spawn_item(room=room)
