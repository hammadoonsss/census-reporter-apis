from rest_framework import serializers

from realestate_education.models import Education

class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ['education_id', 'education_name']