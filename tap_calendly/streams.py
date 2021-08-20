"""Stream type classes for tap-calendly."""
from typing import Any, Dict, Optional, List

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_calendly.client import CalendlyStream


# rearrange for targets like BigQuery
def rearrange_schema(schema: dict):
    props = schema.get('properties', schema)
    for k, v in props.items():
        if 'type' in v:
            if isinstance(v['type'], list):
                temp = v['type'][0]
                v['type'][0] = v['type'][1]
                v['type'][1] = temp
        if 'properties' in v:
            v['properties'] = rearrange_schema(v['properties'])
        if 'items' in v:
            v['items'] = rearrange_schema(v['items'])
    return schema


def parse_id(uri):
    # https://api.calendly.com/organizations/HAHAZEHOQ7RURZ5V
    return uri.split('/')[-1]
    # return re.findall(r'/([A-Z0-9]{15,})', uri)[0]


class EventsStream(CalendlyStream):
    """Define custom stream."""
    name = "events"
    path = "/scheduled_events"
    primary_keys = ["uri"]
    replication_key = "updated_at"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = rearrange_schema(th.PropertiesList(
        th.Property("uri", th.StringType),
        th.Property("name", th.StringType),
        th.Property("status", th.StringType),
        th.Property("start_time", th.DateTimeType),
        th.Property("end_time", th.DateTimeType),
        th.Property("event_type", th.StringType),
        # th.Property("invitees_counter", th.IntegerType),
        th.Property("location",
                    th.ObjectType(th.Property("type", th.StringType), th.Property("location", th.StringType))),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("event_memberships", th.ArrayType(th.ObjectType(th.Property("user", th.StringType)))),
        th.Property("event_guests", th.ArrayType(th.ObjectType(th.Property("email", th.StringType),
                                                               th.Property("created_at", th.DateTimeType),
                                                               th.Property("update_at", th.DateTimeType)))),
    ).to_dict())

    # @property
    # def metadata(self) -> List[dict]:
    #     return []

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        return {'event_id': parse_id(record['uri'])}

    def get_url_params(
            self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params['sort'] = 'start_time:asc'
        params['min_start_time'] = self.config.get('start_date', None)
        return params


class EventInviteesStream(CalendlyStream):
    """Define custom stream."""
    name = "event_invitees"
    path = "/scheduled_events/{event_id}/invitees"
    parent_stream_type = EventsStream
    ignore_parent_replication_keys = True
    primary_keys = ["uri"]
    replication_key = "updated_at"

    schema = rearrange_schema(th.PropertiesList(
        th.Property("cancel_url", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("email", th.StringType),
        th.Property("event", th.StringType),
        th.Property("name", th.StringType),
        th.Property("first_name", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property("event_id", th.StringType),
        th.Property("new_invitee", th.StringType),
        th.Property("old_invitee", th.StringType),
        th.Property("questions_and_answers", th.ArrayType(
            th.ObjectType(th.Property("answer", th.StringType), th.Property("position", th.IntegerType),
                          th.Property("question", th.StringType)))),
        th.Property("reschedule_url", th.StringType),
        th.Property("rescheduled", th.BooleanType),
        th.Property("status", th.StringType),
        th.Property("text_reminder_number", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property("tracking", th.ObjectType(th.Property("utm_campaign", th.StringType),
                                              th.Property("utm_source", th.StringType),
                                              th.Property("utm_medium", th.StringType),
                                              th.Property("utm_content", th.StringType),
                                              th.Property("utm_term", th.StringType),
                                              th.Property("salesforce_uuid", th.StringType))),
        th.Property("updated_at", th.DateTimeType),
        th.Property("uri", th.StringType),
        th.Property("canceled", th.BooleanType),
        th.Property("payment", th.ObjectType(th.Property("external_id", th.StringType),
                                             th.Property("provider", th.StringType),
                                             th.Property("amount", th.NumberType),
                                             th.Property("currency", th.StringType),
                                             th.Property("terms", th.StringType),
                                             th.Property("successful", th.BooleanType))),
    ).to_dict())

    # @property
    # def metadata(self) -> List[dict]:
    #     return []


class EventTypesStream(CalendlyStream):
    """Define custom stream."""
    name = "event_types"
    path = "/event_types"
    primary_keys = ["uri"]
    replication_key = "updated_at"

    schema = rearrange_schema(th.PropertiesList(
        th.Property("uri", th.StringType),
        th.Property("name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("slug", th.StringType),
        th.Property("scheduling_url", th.StringType),
        th.Property("duration", th.IntegerType),
        th.Property("kind", th.StringType),
        th.Property("pooling_type", th.StringType),
        th.Property("type", th.StringType),
        th.Property("color", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("description_plain", th.StringType),
        th.Property("description_html", th.StringType),
        th.Property("profile", th.ObjectType(th.Property("type", th.StringType),
                                             th.Property("name", th.StringType),
                                             th.Property("owner", th.StringType))),
        th.Property("secret", th.BooleanType),
        th.Property("custom_questions", th.ArrayType(th.ObjectType(th.Property("name", th.StringType),
                                                                   th.Property("type", th.StringType),
                                                                   th.Property("position", th.IntegerType),
                                                                   th.Property("enabled", th.BooleanType),
                                                                   th.Property("required", th.BooleanType),
                                                                   th.Property("answer_choices",
                                                                               th.ArrayType(th.StringType)),
                                                                   th.Property("include_other", th.BooleanType)))),

    ).to_dict())

    # @property
    # def metadata(self) -> List[dict]:
    #     return []


class OrganizationMembershipsStream(CalendlyStream):
    """Define custom stream."""
    name = "organization_memberships"
    path = "/organization_memberships"
    primary_keys = ["uri"]
    replication_key = "updated_at"

    schema = rearrange_schema(th.PropertiesList(
        th.Property("uri", th.StringType),
        th.Property("role", th.StringType),
        th.Property("user", th.ObjectType(th.Property("uri", th.StringType),
                                          th.Property("name", th.StringType),
                                          th.Property("slug", th.StringType),
                                          th.Property("email", th.StringType),
                                          th.Property("scheduling_url", th.StringType),
                                          th.Property("timezone", th.StringType),
                                          th.Property("avatar_url", th.StringType),
                                          th.Property("created_at", th.DateTimeType),
                                          th.Property("updated_at", th.DateTimeType))),
        th.Property("organization", th.StringType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("created_at", th.DateTimeType),
    ).to_dict())

    # @property
    # def metadata(self) -> List[dict]:
    #     return []


class OrganizationInvitationsStream(CalendlyStream):
    """Define custom stream."""
    name = "organization_invitations"
    primary_keys = ["uri"]
    replication_key = "updated_at"

    schema = rearrange_schema(th.PropertiesList(
        th.Property("uri", th.StringType),
        th.Property("organization", th.StringType),
        th.Property("email", th.StringType),
        th.Property("role", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("last_sent_at", th.DateTimeType),
        th.Property("user", th.StringType),
    ).to_dict())

    def __init__(self, tap):
        super().__init__(tap)
        self.path = f"/organizations/{parse_id(self.user['current_organization'])}/invitations"

    # @property
    # def metadata(self) -> List[dict]:
    #     return []
