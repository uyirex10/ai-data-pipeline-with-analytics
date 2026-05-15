import uuid
from datetime import datetime


def generate_batch_identifier(
    source_name: str
) -> str:
    """
    Generates unique batch identifier.
    """

    timestamp = datetime.utcnow().strftime(
        "%Y%m%d%H%M%S"
    )

    random_id = uuid.uuid4().hex[:8]

    return (
        f"{source_name}_{timestamp}_{random_id}"
    )