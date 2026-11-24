from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Sessao


class SessaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sessao
        fields = '__all__'

    def validate(self, attrs):
        # Aplica as mesmas regras de negócio dos formulários (clean() do model)
        instance = self.instance or Sessao()
        for campo, valor in attrs.items():
            setattr(instance, campo, valor)
        try:
            instance.clean()
        except DjangoValidationError as erro:
            raise serializers.ValidationError(erro.messages)
        return attrs
