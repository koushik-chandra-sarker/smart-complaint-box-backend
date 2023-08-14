from django.contrib.auth import password_validation, get_user_model

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from author.models import User
from author.models.user_model import EmailConfirmed, Designation


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class VarifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmed
        fields = ['activation_key', 'email_confirm']
