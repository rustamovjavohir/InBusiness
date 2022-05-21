from rest_framework import serializers
from .models import Projects


class ProjectsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'
        extra_kwargs = {'is_delete': {'write_only': True},
                        'created_by': {'read_only': True}
                        }
