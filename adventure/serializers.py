from rest_framework import serializers, viewsets
from .models import Room

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('title', 'description', 'n_to', 's_to', 'e_to', 'w_to')

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()