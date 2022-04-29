from rest_framework import serializers

from realestate_app.models import (County, State,
                                   Race, RaceError, RaceEstimate,
                                   Income,IncomeError, IncomeEstimate,)


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
        fields = ['race_estimate_value', 'county_id', 'race_id']


class RaceErrorSerializer(serializers.ModelSerializer):

    class Meta:
        model = RaceError
        fields = ['race_error_value', 'county_id', 'race_id']


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ['income_id', 'income_name']


class IncomeEstimateSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeEstimate
        fields = ['income_estimate_value', 'county_id', 'income_id']


class IncomeErrorSerializer(serializers.ModelSerializer):

    class Meta:
        model = IncomeError
        fields = ['income_error_value', 'county_id', 'income_id']
