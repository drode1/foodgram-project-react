import json

import pytest


class Test00ApiUser:
    url_login_token = '/api/auth/token/login/'
    url_logout_token = '/api/auth/token/logout/'
    url_users = '/api/users/'
    url_user_me = '/api/users/me/'
    url_user_profile = '/api/users/1/'
    url_user_profile_invalid = '/api/users/1000/'
    url_user_change_password = '/api/users/set_password/'

    @pytest.mark.django_db(transaction=True)
    def test_token_get__invalid_request_data(self, client, user):
        url = self.url_login_token
        response = client.post(url)
        expected_code = 400
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} без параметров, '
            f'возвращается код {expected_code}'
        )

        email_invalid = 'invalid@email.com'
        password_invalid = 'invalidpassword'
        invalid_data = {
            'username': email_invalid,
            'password': password_invalid
        }
        response = client.post(url, data=invalid_data)
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} без параметров, '
            f'возвращается код {expected_code}'
        )
        email_valid = user.email
        invalid_data = {
            'email': email_valid,
            'password': password_invalid
        }
        response = client.post(url, data=invalid_data)
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} без параметров, '
            f'возвращается код {expected_code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_token_get__valid_request_data(self, client, user):
        url = self.url_login_token
        valid_data = {
            'email': user.email,
            'password': '12345'
        }
        response = client.post(url, data=valid_data)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} с валидными данными, '
            f'возвращается код {expected_code}'
        )
        field = 'auth_token'
        assert field in response.json().keys(), (
            f'Убедитесь, что при запросе {url} с валидными данными, '
            f' в ответе возвращается код {expected_code} с ключом '
            f'{field}, где содержатся токен'
        )

    @pytest.mark.django_db(transaction=True)
    def test_token_logout__invalid_request_data(self, client):
        url = self.url_logout_token
        response = client.post(url)
        expected_code = 401
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} от неавторизованного '
            f'пользователя, возвращается код {expected_code}'
        )
        field = 'detail'
        assert field in response.json().keys(), (
            f'Убедитесь, что при запросе {url} с невалидными данными, '
            f'в ответе возвращается код {expected_code} с ключом '
            f'{field}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_token_logout__valid_request_data(self, auth_client):
        url = self.url_logout_token
        response = auth_client.post(url)
        expected_code = 204

        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} с валидными данными, '
            f'возвращается код {expected_code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_users__valid_request(self, client, user):
        url = self.url_users
        response = client.get(url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} возвращается '
            f'код {expected_code}'
        )

        response_json = response.json()
        fields_in_response = ('count', 'next', 'previous', 'results',)
        for field in fields_in_response:
            assert (field in response_json.keys()), (
                f'Проверьте, что при запросе {url} в ответе есть поле {field}'
            )
        response_results = json.dumps(response_json.get('results'))
        fields_in_results = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        for field in fields_in_results:
            assert (field in response_results), (
                f'Проверьте, что при запросе {url} в ответе есть поле {field}'
            )

    @pytest.mark.django_db(transaction=True)
    def test_get_me__invalid_request(self, client):
        url = self.url_user_me
        response = client.get(url)
        expected_code = 401
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
    def test_get_me__valid_request(self, auth_client):
        url = self.url_user_me
        response = auth_client.get(url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} авторизованным пользователем '
            f'возвращается код {expected_code}'
        )
        response_json = response.json()
        fields_in_response = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        for field in fields_in_response:
            assert (field in response_json.keys()), (
                f'Проверьте, что при запросе {url} в ответе есть поле {field}'
            )
        # TODO: Добавить тест, что при запросе /me/ возвращается id авторизованного пользователя

    @pytest.mark.django_db(transaction=True)
    def test_get_user_profile__invalid_request(self, client, auth_client):
        url = self.url_user_profile_invalid
        response = client.get(url)
        expected_code = 401
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} неавторизованным '
            f'пользователем возвращается код {expected_code}'
        )
        response = auth_client.get(url)
        expected_code = 404
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} авторизованным пользователем '
            f'возвращается код {expected_code}, т.к. объект не найден'
        )
        field = 'detail'
        assert field in response.json().keys(), (
            f'Убедитесь, что при запросе {url} авторизованным пользователем, '
            f'в ответе возвращается код {expected_code} с ключом {field}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_user_profile__valid_request(self, auth_client):
        url = self.url_user_profile
        response = auth_client.get(url)
        expected_code = 200
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} авторизованным пользователем '
            f'возвращается код {expected_code}'
        )
        response_json = response.json()
        fields_in_response = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )
        for field in fields_in_response:
            assert (field in response_json.keys()), (
                f'Проверьте, что при запросе {url} в ответе есть поле {field}'
            )

    @pytest.mark.django_db(transaction=True)
    def test_change_user_pass__invalid_request(self, client):
        url = self.url_user_change_password
        response = client.post(url)
        expected_code = 401
        assert response.status_code == expected_code, (
            f'Проверьте, что при запросе {url} неавторизованным '
            f'пользователем возвращается ошибка {expected_code}'
        )
        field = 'detail'
        assert field in response.json().keys(), (
            f'Убедитесь, что при запросе {url} неавторизованным пользователем, '
            f'в ответе возвращается код {expected_code} с ключом '
            f'{field}.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_change_user_pass__invalid_data_request(self, auth_client):
        url = self.url_user_change_password
        response = auth_client.post(url)
        expected_code = 400
        assert response.status_code == expected_code, (
            f'Убедитесь, что при запросе {url} с пустым телом запроса '
            f'возвращается код {expected_code}'
        )
        response_json = response.json()
        fields_in_response = ('new_password', 'current_password',)
        for field in fields_in_response:
            assert (field in response_json.keys()), (
                f'Проверьте, что при запросе {url} в ответе есть информация '
                f'о том, что поле {field} обязательно для заполнения'
            )
        invalid_data = {
            'current_password': 'current_password'
        }
        response = auth_client.post(url, data=invalid_data)
        response_json = response.json()
        assert response.status_code == expected_code
        field_in_response = 'new_password'
        assert field_in_response in response_json.keys(), (
            f'Убедитесь, что при отправке запроса с неполными данные '
            f'возвращается ошибка с кодом {expected_code} и полем '
            f'{field_in_response}'
        )
        invalid_data = {
            'new_password': 'new_password'
        }
        response = auth_client.post(url, data=invalid_data)
        response_json = response.json()
        assert response.status_code == expected_code
        field_in_response = 'current_password'
        assert field_in_response in response_json.keys(), (
            f'Убедитесь, что при отправке запроса с неполными данные '
            f'возвращается ошибка с кодом {expected_code} и полем '
            f'{field_in_response}'
        )
        new_password_invalid = 1234567
        current_password = 12345
        invalid_data = {
            'new_password': new_password_invalid,
            'current_password': current_password
        }
        response = auth_client.post(url, data=invalid_data)
        response_json = response.json()
        assert response.status_code == expected_code
        field_in_response = 'new_password'
        assert field_in_response in response_json.keys(), (
            f'Убедитесь, что при длине пароля меньше 8 символов возвращается '
            f'ошибка с кодом {expected_code} и полем {field_in_response}'
        )
        new_password_invalid = 12345678
        invalid_data = {
            'new_password': new_password_invalid,
            'current_password': current_password
        }
        response = auth_client.post(url, data=invalid_data)
        response_json = response.json()
        assert response.status_code == expected_code
        field_in_response = 'new_password'
        assert field_in_response in response_json.keys(), (
            f'Убедитесь, что при отправке пароля длиной 8 символов '
            f'и состоящий только из цифр возвращается ошибка с кодом '
            f'{expected_code} и полем {field_in_response}'
        )
        new_password_invalid = 'qwerty123'
        invalid_data = {
            'new_password': new_password_invalid,
            'current_password': current_password
        }
        response = auth_client.post(url, data=invalid_data)
        response_json = response.json()
        assert response.status_code == expected_code
        field_in_response = 'new_password'
        assert field_in_response in response_json.keys(), (
            f'Убедитесь, что при отправке простого пароля возвращается '
            f'ошибка с кодом {expected_code} и полем {field_in_response}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_change_user_pass__valid_data_request(self, auth_client):
        url = self.url_user_change_password
        new_password_valid = '!superHardPassword321!'
        current_password = 12345
        valid_data = {
            'new_password': new_password_valid,
            'current_password': current_password
        }
        expected_code = 204
        response = auth_client.post(url, data=valid_data)
        assert response.status_code == expected_code, (
            f'Убедитесь, что при отправке корректных данных возвращается ответ'
            f' с кодом {expected_code}'
        )

    # TODO: Написать тест на регистрацию пользователей

    def test_register_user__invalid_data_request(self, client):
        url = self.url_users
        response = client.get(url=url)
        expected_code = 400
        response_json = response.json()
        fields_in_response = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password',)
        for field in fields_in_response:
            assert (field in response_json.keys()), (
                f'Проверьте, что при пустом запросе {url} в ответе '
                f'есть поле {field} и код ошибки {expected_code}'
            )
        # TODO: Написать доп юз кейсы

    def test_register_user__valid_data_request(self, client):
        url = self.url_users
        valid_email = 'fakeuser@email.ru'
        valid_data = {
            'first_name': 'Fake',
            'last_name': 'User',
            'username': 'FakeUser',
            'email': valid_email,
            'password': '!qwer321ty123!'
        }

        response = client.get(url=url, data=valid_data)
        expected_code = 204
        response_json = response.json()
        fields_in_response = (
            'email', 'id', 'username', 'first_name', 'last_name',)
        for field in fields_in_response:
            assert (field in response_json.keys()), (
                f'Проверьте, что при пустом запросе {url} в ответе '
                f'есть поле {field} и код ошибки {expected_code}'
            )
