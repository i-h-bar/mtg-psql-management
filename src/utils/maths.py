from uuid import UUID


def increment_uuid(uuid: str) -> str:
    uuid = UUID(uuid)
    uuid_int = int(uuid) + 1

    return str(UUID(int=uuid_int))
