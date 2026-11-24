from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Sala


class SalaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sala
        fields = '__all__'

    def validate(self, attrs):
        # Aplica as mesmas regras de negócio dos formulários (clean() do model)
        instance = self.instance or Sala()
        for campo, valor in attrs.items():
            setattr(instance, campo, valor)
        try:
            instance.clean()
        except DjangoValidationError as erro:
            raise serializers.ValidationError(erro.messages)
        return attrs
