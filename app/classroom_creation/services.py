import uuid
from datetime import date
from typing import Any

from classroom_creation.exceptions import InvalidClassRoomException
from core.models import ClassRoom


class ClassRoomFactory:
    """Factory for creating class room objects"""

    _classrooms = ClassRoom.objects

    def make_classroom(self, **classroom_data: Any) -> ClassRoom:
        subject: str = classroom_data.pop("subject")

        if not subject:
            raise InvalidClassRoomException("A subject must be set")

        subject = subject.lower()
        subject = subject.strip()

        name_suffix = str(uuid.uuid4())
        name = f"{subject}_{name_suffix}"

        start = classroom_data.get("start")
        if not start:
            raise InvalidClassRoomException("A starting date must be set")

        deadline = classroom_data.get("deadline")
        if not deadline:
            raise InvalidClassRoomException("A deadline must be set")

        self._check_start_and_deadline(start, deadline)

        members = classroom_data.pop("members", [])

        new_classroom: ClassRoom = self._classrooms.create(
            name=name, subject=subject, **classroom_data
        )

        new_classroom.members.add(*members)

        return new_classroom

    def _check_start_and_deadline(self, start: date, deadline: date):
        if start > deadline:
            raise InvalidClassRoomException(
                "The starting date must happen before the deadline"
            )
