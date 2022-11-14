from django.contrib.auth import get_user_model


def create_users_api(auth_client):
    data = {
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
        'username': 'TestUserNew',
        'email': 'testuser@yamdb.fake'
    }
    auth_client.post('/api/users/', data=data)
    user = get_user_model().objects.get(username=data['username'])
    return user


def create_tag():
    from recipes.models import Tag
    Tag.objects.create(
        name='Tag_name',
        color='#ffffff',
        slug='slug',
    )
    return


def create_ingredient():
    from recipes.models import Ingredient
    Ingredient.objects.create(
        name='Капуста',
        measurement_unit='кг',
    )
    return
