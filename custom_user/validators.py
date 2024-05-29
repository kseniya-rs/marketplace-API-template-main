from rest_framework.validators import ValidationError


class PasswordValidation:

    def __call__(self, data: dict):
        password_confirmation = data.pop('password_confirmation', None)
        checking_password = data.get('password')

        if password_confirmation is None:
            raise ValidationError("Поле 'password_confirmation' обязательно")

        if checking_password != password_confirmation:
            raise ValidationError("Пароль и его подтверждение не совпадают")
