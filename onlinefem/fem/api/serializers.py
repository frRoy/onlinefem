from rest_framework import serializers

from onlinefem.fem.models import FEM


class FEMSerializer(serializers.ModelSerializer):
    class Meta:
        model = FEM
        fields = ('id', 'name', 'email', 'message')
