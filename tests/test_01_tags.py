import pytest


class Test01ApiTag:
    url_tags = '/api/tags/'
    url_one_tag = '/api/tags/1/'

    @pytest.django.db.transaction(transaction=True)
    def test_get_tags__invalid_request(self, client):
        url = self.url_tags
        request_types = ('GET', 'HEAD', 'OPTIONS',)
        response = client.get(url)
        expected_code = 405
        response_types = response.accepted_types
        for request in request_types:
            assert request in response_types, (
                f'Убедитесь, что {url} принимает только {request_types} '
                f'запросы и возвращает статус код {expected_code}'
            )
        # TODO: Подумать над логикой этого теста, все ли корректно тут.
        #  Идея в том, чтобы проверить, что в заголовке могут быть только
        #  GET, HEAD, OPTIONS запросы

    # TODO: Проверить, что даже админ не может ничего менять через API
    # TODO: Написать аналогичные тесты и для одного тега

    @pytest.django.db.transaction(transaction=True)
    def test_get_tags__valid_request(self, client):
        url = self.url_tags
        response = client.get(url=url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} возвращается код {expected_code}'
        )
        response_json = response.json()
        fields_in_response = ('id', 'name', 'color', 'slug')
        for field in fields_in_response:
            assert field in response_json, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )

    @pytest.django.db.transaction(transaction=True)
    def test_get_tags__valid_request(self, client):
        url = self.url_one_tag
        response = client.get(url=url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} возвращается код {expected_code}'
        )
        response_json = response.json()
        fields_in_response = ('id', 'name', 'color', 'slug')
        for field in fields_in_response:
            assert field in response_json, (
                f'Убедитесь, что в ответе при правильном запросе есть '
                f'поле {field} и код ответа {expected_code}'
            )
