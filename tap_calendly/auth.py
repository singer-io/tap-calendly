"""calendly Authentication."""


from singer_sdk.authenticators import SimpleAuthenticator


class CalendlyAuthenticator(SimpleAuthenticator):
    """Authenticator class for calendly."""

    @classmethod
    def create_for_stream(cls, stream) -> "CalendlyAuthenticator":
        return cls(
            stream=stream,
            auth_headers={
                "Authorization": "Bearer " + stream.config.get("calendly_api_token")
            }
        )
