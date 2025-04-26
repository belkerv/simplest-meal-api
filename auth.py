from base64 import b64encode

import httpx


class FatSecretAuth(httpx.Auth):
    requires_response_body = True
    invalid_token = 13

    def __init__(self, token_url, client_id, client_secret):
        self.token_url = token_url
        self.basic_header = self.build_basic_header(client_id, client_secret)
        self.access_token = None

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        response = yield request

        data = response.json()
        if 'error' in data and data['error']['code'] == FatSecretAuth.invalid_token:
            token_response = yield self.build_token_request()
            self.access_token = token_response.json()['access_token']

            request.headers["Authorization"] = f"Bearer {self.access_token}"
            yield request

    def build_token_request(self):
        # Build a request for obtaining a new access token.
        return httpx.Request(
            "POST",
            self.token_url,
            headers={ "Authorization": self.basic_header },
            data={ "grant_type": "client_credentials" }
        )

    def build_basic_header(self, username, password):
        userpass = f"{username}:{password}"
        return f"Basic {b64encode(userpass.encode()).decode()}"