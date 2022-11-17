import requests

APPLICATION_JSON = "application/json"


class HTTPResponse:
    status: str
    httpCode: int
    data: any
    contentType: str

    def process_response(self, response) -> "HTTPResponse":
        self.httpCode = response.status_code
        if 200 <= self.httpCode < 300:
            self.status = "success"
        else:
            self.status = "error"
        self.set_data(response)
        return self

    def set_data(self, response):
        response.encoding = 'utf-8'
        self.contentType = response.headers["Content-Type"]
        if self.contentType and self.contentType.lower().startswith(APPLICATION_JSON):
            self.data = response.json()
        else:
            self.data = response.text

    @staticmethod
    def get_response(response) -> "HTTPResponse":
        http_response = HTTPResponse()
        http_response.process_response(response)
        return http_response


class PWebRequests:
    headers: dict = {}
    baseUrl: str

    def _get_url(self, url):
        return self.baseUrl + url

    def set_base(self, url) -> 'PWebRequests':
        self.baseUrl = url
        return self

    def get(self, url: str, params: dict = None) -> HTTPResponse:
        url = self._get_url(url)
        response = requests.get(url, headers=self.headers, params=params)
        return HTTPResponse.get_response(response)

    def post(self, url: str, json_dict: dict = None, data: dict = None, file: dict = None) -> HTTPResponse:
        url = self._get_url(url)
        response = requests.post(url, headers=self.headers, json=json_dict, data=data, files=file)
        return HTTPResponse.get_response(response)

    def delete(self, url: str, params: dict = None) -> HTTPResponse:
        url = self._get_url(url)
        response = requests.delete(url, headers=self.headers, params=params)
        return HTTPResponse.get_response(response)

    def add_header(self, key: str, value) -> 'PWebRequests':
        self.headers[key] = value
        return self

    def add_bearer(self, token) -> 'PWebRequests':
        self.add_header("Authorization", "Bearer " + str(token))
        return self

    def add_content_type(self, content_type) -> 'PWebRequests':
        self.add_header("Content-Type", str(content_type))
        return self
