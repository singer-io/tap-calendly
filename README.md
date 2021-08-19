# tap-calendly

## Connecting

### Requirements

To set up tap-calendly in Stitch, you need:


-  **Calendly API Token** - API token belonging to the account to be used by the tap

### Setup

To obtain API token, login to calendly.com and visit the [API Webhooks](https://calendly.com/integrations/api_webhooks) page. Click "Generate New Token", and copy the token. Paste in config.json "calendly_api_token" field.

---

## Replication

As the Calendly API does not support sorting by replication key ("updated_at"), bookmarking and sync resume is not supported.

---

##  Streams/Endpoints

- [events](https://calendly.stoplight.io/docs/api-docs/reference/calendly-api/openapi.yaml/paths/~1scheduled_events/get)
- [event_invitees](https://calendly.stoplight.io/docs/api-docs/reference/calendly-api/openapi.yaml/paths/~1scheduled_events~1%7Buuid%7D~1invitees/get)
- [event_types](https://calendly.stoplight.io/docs/api-docs/reference/calendly-api/openapi.yaml/paths/~1event_types/get)
- [organization_memberships](https://calendly.stoplight.io/docs/api-docs/reference/calendly-api/openapi.yaml/paths/~1organization_memberships/get)
- [organization_invitations](https://calendly.stoplight.io/docs/api-docs/reference/calendly-api/openapi.yaml/paths/~1organizations~1%7Buuid%7D~1invitations/get)

Primary key of every stream/endpoint is "uri", and all endpoints are replicated fully (not incrementally)

---

## More Information
- "user" mode vs. "org" mode
  - In config.json file, specify "mode": "org" or "mode": "user".  This specifies whether the tap will fetch records pertaining to the current user only, or records pertaining to the user organization. For example, events that are scheduled by the user vs. every event scheduled by throughout the entire organization.
