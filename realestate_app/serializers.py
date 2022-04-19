from rest_framework import serializers

from realestate_app.models import County, Race, RaceError, RaceEstimate, State


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


class RaceEstimateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RaceEstimate
        fields = '__all__'


class RaceErrorSerializer(serializers.ModelSerializer):

    class Meta:
        model = RaceError
        fields = '__all__'