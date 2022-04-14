from rest_framework import serializers

from realestate_app.models import County, Race, State


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['race_id', 'race_name']


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['state_id', 'state_name', 'state_ref_id']


class CountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = ['county_id', 'county_name', 'state']
