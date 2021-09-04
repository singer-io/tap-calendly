"""REST client handling, including calendlyStream base class."""
from pathlib import Path
from typing import Any, Dict, Optional, Iterable
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_calendly.auth import CalendlyAuthenticator

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class CalendlyStream(RESTStream):
    """calendly stream class."""

    url_base = "https://api.calendly.com"

    records_jsonpath = "$.collection[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.pagination.next_page"  # Or override `get_next_page_token`.

    def __init__(self, tap):
        super().__init__(tap)
        self.user = self.get_user()

    def get_user(self):
        r = self.requests_session.get(urljoin(self.url_base, '/users/me'),
                                      headers={'Authorization': 'Bearer ' + self.config.get('calendly_api_token')})
        r.raise_for_status()
        return r.json()['resource']

    @property
    def authenticator(self) -> CalendlyAuthenticator:
        """Return a new authenticator object."""
        return CalendlyAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def get_next_page_token(
            self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            if first_match:
                parsed = urlparse(first_match)
                qs = parse_qs(parsed.query)
                next_page_token = qs['page_token'][0]
            else:
                next_page_token = None
        else:
            next_page_token = response.headers.get("X-Next-Page", None)

        return next_page_token

    def get_url_params(
            self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["page_token"] = next_page_token
        # if self.replication_key:
            # params["sort"] = self.replication_key + ":asc"
            # params["order_by"] = self.replication_key
        params['count'] = 100
        if self.config.get('mode', 'org') == 'org':
            params['organization'] = self.user['current_organization']
        else:
            params['user'] = self.user['uri']
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
