import pytest

from .common import create_tag


class Test01ApiTag:
    url_tags = '/api/tags/'
    url_one_tag = '/api/tags/1/'

    @pytest.mark.django_db(transaction=True)
    def test_get_tags__invalid_request(self, client, admin_client):
        url = self.url_tags
        request_types_allowed = ('GET', 'HEAD', 'OPTIONS',)
        response = client.get(url)
        expected_code = 200
        response_types = response.headers.get('Allow').replace(' ', '').split(
            ',')
        for request in response_types:
            assert request in request_types_allowed, (
                f'Убедитесь, что {url} принимает только {request_types_allowed} '
                f'запросы и возвращает код {expected_code}'
            )
        data = {
            'name': 'Новый тег',
            'color': '#ffffff',
            'slug': 'white',
        }
        response = admin_client.post(url, data=data)
        expected_code = 405
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} неавторизованным пользователем '
            f'возвращается код {expected_code}'
        )
        field = 'detail'
        assert field in response.json().keys(), (
            f'Убедитесь, что при запросе {url} неавторизованным пользователем, '
            f'в ответе возвращается код {expected_code} с ключом '
            f'{field}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_tag__invalid_request(self, client, admin_client):
        url = self.url_one_tag
        request_types_allowed = ('GET', 'HEAD', 'OPTIONS',)
        response = client.get(url)
        expected_code = 200
        response_types = response.headers.get('Allow').replace(' ', '').split(
            ',')
        for request in response_types:
            assert request in request_types_allowed, (
                f'Убедитесь, что {url} принимает только {request_types_allowed} '
                f'запросы и возвращает код {expected_code}'
            )
        data = {
            'name': 'Новый тег',
            'color': '#ffffff',
            'slug': 'white',
        }
        response = admin_client.post(url, data=data)
        expected_code = 405
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} неавторизованным пользователем '
            f'возвращается код {expected_code}'
        )
        field = 'detail'
        assert field in response.json().keys(), (
            f'Убедитесь, что при запросе {url} неавторизованным пользователем, '
            f'в ответе возвращается код {expected_code} с ключом '
            f'{field}.'
        )

    @pytest.mark.django_db
    def test_get_tags__valid_request(self, client):
        url = self.url_tags
        create_tag()
        response = client.get(url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} возвращается '
            f'код {expected_code}'
        )
        response_json = response.json()[0]
        fields_in_response = ('id', 'name', 'color', 'slug')
        for field in fields_in_response:
            assert field in response_json, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )

    @pytest.mark.django_db
    def test_get_tag__valid_request(self, client):
        url = self.url_one_tag
        create_tag()
        response = client.get(url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} '
            f'возвращается код {expected_code}'
        )
        response_json = response.json()
        fields_in_response = ('id', 'name', 'color', 'slug')
        for field in fields_in_response:
            assert field in response_json, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
