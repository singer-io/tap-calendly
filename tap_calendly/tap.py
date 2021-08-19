"""Calendly tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_calendly.streams import (
    EventsStream,
    EventInviteesStream,
    EventTypesStream,
    OrganizationInvitationsStream,
    OrganizationMembershipsStream,
)

STREAM_TYPES = [
    EventsStream,
    EventInviteesStream,
    EventTypesStream,
    OrganizationInvitationsStream,
    OrganizationMembershipsStream
]


class TapCalendly(Tap):
    """Calendly tap class."""
    name = "tap-calendly"

    config_jsonschema = th.PropertiesList(
        th.Property("calendly_api_token", th.StringType, required=True),
        th.Property("start_date", th.DateTimeType),
        th.Property("api_url", th.StringType, default="https://api.calendly.com"),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

