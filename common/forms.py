from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, CharField, PasswordInput


class RegisterForm(UserCreationForm):
    password1 = CharField(label='Password', widget=PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = CharField(label='Confirm Password', widget=PasswordInput(attrs={'autocomplete': 'new-password'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {
            'username': ''
        }

class LoginForm(Form):
    login = CharField(max_length=150)
    password = CharField(max_length=150, widget=PasswordInput)

class RecipeForm(Form):
    title = CharField(max_length=150)
    description = CharField(max_length=150)
    cooking_time = CharField(max_length=150)
    
class IngredientForm(Form):
    name = CharField(max_length=150)
