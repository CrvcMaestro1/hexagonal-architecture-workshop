from typing import List

import inject
from fastapi import APIRouter
from starlette import status

from src.domain.event.event import EventIn, EventOut, EventWithOutRoom
from src.domain.event.input.event_service import EventService


@inject.autoparams()
def event_router(
        event_service: EventService
) -> APIRouter:
    router = APIRouter(tags=["event"])

    @router.get('/events', response_model=List[EventOut], status_code=status.HTTP_200_OK)
    async def event_list() -> List[EventOut]:
        return event_service.list()

    @router.get('/events/public', response_model=List[EventOut], status_code=status.HTTP_200_OK)
    async def event_public_list() -> List[EventOut]:
        return event_service.list_public_events()

    @router.get('/events/{event_id}', response_model=EventOut, status_code=status.HTTP_200_OK)
    async def get_event(event_id: int) -> EventOut:
        event = event_service.get(event_id)
        return event

    @router.post('/events', response_model=EventWithOutRoom, status_code=status.HTTP_201_CREATED)
    async def event_create(event: EventIn) -> EventWithOutRoom:
        event_created = event_service.create(event)
        return event_created

    @router.put('/events/{event_id}', response_model=EventWithOutRoom, status_code=status.HTTP_200_OK)
    async def event_update(event_id: int, event: EventIn) -> EventWithOutRoom:
        event_updated = event_service.update(event_id, event)
        return event_updated

    @router.delete('/events/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def event_delete(event_id: int) -> None:
        event_service.delete(event_id)

    return router
