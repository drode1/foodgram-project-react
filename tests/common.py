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
    result = []
    Tag.objects.create(
        name='Обед',
        color='#ffffff',
        slug='slug',
    )
    data = {
        'id': 1,
        'name': 'Обед',
        'color': '#ffffff',
        'slug': 'lunch'
    }
    result.append(data)
    return result


def create_ingredient():
    from recipes.models import Ingredient
    result = []
    Ingredient.objects.create(
        name='Капуста',
        measurement_unit='кг',
    )
    data = {
        'id': 1,
        'name': 'Капуста',
        'measurement_unit': 'кг'
    }
    result.append(data)
    return result


def create_recipe(auth_client):
    tag = create_tag()
    ingredient = create_ingredient()
    result = []
    data = {
        "ingredients": [
            {
                "id": ingredient[0].get('id'),
                "amount": 2
            }
        ],
        "tags": [
            tag[0].get('id')
        ],
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
        "name": "string",
        "text": "string",
        "cooking_time": 1
    }
    auth_client.post('/api/recipes/', data=data)
    result.append(data)
    return result, tag, ingredient
