from rest_framework import serializers

from realestate_app.models import Race


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ('race_id', 'race_name')
