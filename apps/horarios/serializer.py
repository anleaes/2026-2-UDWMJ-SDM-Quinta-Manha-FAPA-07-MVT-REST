from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Horario


class HorarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Horario
        fields = '__all__'

    def validate(self, attrs):
        # Aplica as mesmas regras de negócio dos formulários (clean() do model)
        instance = self.instance or Horario()
        for campo, valor in attrs.items():
            setattr(instance, campo, valor)
        try:
            instance.clean()
        except DjangoValidationError as erro:
            raise serializers.ValidationError(erro.messages)
        return attrs
