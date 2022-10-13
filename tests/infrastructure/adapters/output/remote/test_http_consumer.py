from unittest.mock import Mock, MagicMock

import pytest
import requests
from pytest_mock import MockFixture

from src.infrastructure.adapters.output.components.http import HttpConsumer, HttpMethod


@pytest.fixture
def requests_patch(mocker: MockFixture) -> Mock:
    return mocker.patch('src.infrastructure.adapters.output.components.http.http_consumer.requests')


@pytest.fixture
def mock_response_200() -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        'id': 1, 'title': 'my title'
    }
    return response


@pytest.fixture
def mock_response_500() -> MagicMock:
    response = MagicMock()
    response.status_code = 500
    response.raise_for_status = Mock(side_effect=requests.HTTPError)
    return response


@pytest.fixture
def mock_response_404() -> MagicMock:
    response = MagicMock()
    response.status_code = 404
    response.raise_for_status = Mock(side_effect=requests.HTTPError)
    return response


@pytest.fixture
def mock_response_201() -> MagicMock:
    response = MagicMock()
    response.status_code = 201
    response.json.return_value = {
        'id': 1, 'title': 'my title'
    }
    return response


class TestHttpConsumer:

    def test_return_data_properly(self, requests_patch: Mock, mock_response_200: MagicMock) -> None:
        requests_patch.request.return_value = mock_response_200

        response = HttpConsumer.consume(HttpMethod.GET, 'http://ok-url/test', headers={'cookie': 'set-cookie'})

        assert response.status_code == 200
        assert response.is_success is True
        assert response.data is not None
        assert requests_patch.request.call_args.kwargs['headers'] == {
            'Content-Type': 'application/json',
            'charset': 'utf-8',
            'User-Agent': 'self-service-ms',
            'cookie': 'set-cookie'
        }

    def test_should_catch_internal_server_error(self, requests_patch: Mock, mock_response_500: MagicMock) -> None:
        requests_patch.request.return_value = mock_response_500

        response = HttpConsumer.consume(HttpMethod.GET, 'http://ok-url/test')

        assert response.status_code == 500
        assert response.is_success is False

    def test_should_catch_not_found_error(self, requests_patch: Mock, mock_response_404: MagicMock) -> None:
        requests_patch.request.return_value = mock_response_404

        response = HttpConsumer.consume(HttpMethod.GET, 'http://ok-url/test')

        assert response.status_code == 404
        assert response.is_success is False

    def test_should_return_status_201(self, requests_patch: Mock, mock_response_201: MagicMock) -> None:
        requests_patch.request.return_value = mock_response_201

        response = HttpConsumer.consume(HttpMethod.POST, 'http://ok-url/test', json_data={'title': 'my title'})

        assert response.status_code == 201
        assert response.is_success is True
        assert requests_patch.request.call_args.kwargs['json'] == {'title': 'my title'}
