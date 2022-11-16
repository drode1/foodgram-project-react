import pytest

from .common import create_recipe


class Test03ApiRecipe:
    url_recipes = '/api/recipes/'
    url_one_recipe = '/api/recipes/1/'

    @pytest.mark.django_db(transaction=True)
    def test_get_recipes__valid_request(self, client, auth_client):
        url = self.url_recipes
        create_recipe(auth_client)
        response = client.get(url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} возвращается '
            f'код {expected_code}'
        )
        response_json = response.json()
        fields_in_response = ('count', 'next', 'previous', 'results',)
        for field in fields_in_response:
            assert field in response_json, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
        response_json = response.json().get('results')
        fields_in_response = ('id', 'tags', 'author', 'ingredients',
                              'is_favorited', 'is_in_shopping_cart', 'name',
                              'image', 'text', 'cooking_time'
                              )
        for field in fields_in_response:
            assert field in response_json, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
        response_json_tags = response.json().get('tags')
        fields_in_response = ('id', 'name', 'color', 'slug',)
        for field in fields_in_response:
            assert field in response_json_tags, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
        response_json_author = response.json().get('author')
        fields_in_response = ('id', 'email', 'username', 'first_name',
                              'last_name', 'is_subscribed',
                              )
        for field in fields_in_response:
            assert field in response_json_author, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
        response_json_ingredients = response.json().get('ingredients')
        fields_in_response = ('id', 'name', 'measurement_unit', 'amount',)
        for field in fields_in_response:
            assert field in response_json_ingredients, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )

    def test_get_recipe__valid_request(self, client, auth_client):
        url = self.url_one_recipe
        create_recipe(auth_client)
        response = client.get(url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} возвращается '
            f'код {expected_code}'
        )
        response_json = response.json()
        fields_in_response = ('id', 'tags', 'author', 'ingredients',
                              'is_favorited', 'is_in_shopping_cart', 'name',
                              'image', 'text', 'cooking_time'
                              )
        for field in fields_in_response:
            assert field in response_json, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
        response_json_tags = response.json().get('tags')
        fields_in_response = ('id', 'name', 'color', 'slug',)
        for field in fields_in_response:
            assert field in response_json_tags, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
        response_json_author = response.json().get('author')
        fields_in_response = ('id', 'email', 'username', 'first_name',
                              'last_name', 'is_subscribed',
                              )
        for field in fields_in_response:
            assert field in response_json_author, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
        response_json_ingredients = response.json().get('ingredients')
        fields_in_response = ('id', 'name', 'measurement_unit', 'amount',)
        for field in fields_in_response:
            assert field in response_json_ingredients, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
