from typing import List

from src.domain.event.event import EventOut
from src.domain.event.output.public_event_repository import PublicEventRepository
from src.domain.utils.exceptions import ApplicationError
from src.infrastructure.adapters.output.components.http import HttpConsumer, HttpMethod
from src.infrastructure.adapters.output.remote import PUBLIC_EVENTS_URL
from src.infrastructure.adapters.output.remote.mapper.public_event_remote_mapper import PublicEventRemoteMapper


class RemotePublicEventRepository(PublicEventRepository):
    def list_public_events(self) -> List[EventOut]:
        url = f"{PUBLIC_EVENTS_URL}/events"
        response = HttpConsumer.consume(HttpMethod.GET, url)

        app_error = ApplicationError(response.status_code, 'An error occurred while obtaining public events.',
                                     response.data)
        if not response.is_success:
            raise app_error
        data = response.data
        if not isinstance(data, list):
            raise app_error

        return PublicEventRemoteMapper().remote_to_domain(data)
