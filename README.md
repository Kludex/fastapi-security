# FastAPI Security Strategies

Each folder contains a different strategy to authenticate a user/client/application with FastAPI.

All the strategies are using a `dictionary` as database.

We have:

* [APIKey Header](api_key)
* [HTTP Basic](http_basic)
* [HTTP Bearer](https://github.com/tiangolo/fastapi/blob/master/tests/test_security_http_bearer.py)

Missing:

* HTTP Digest (I'm working on it [here](https://github.com/tiangolo/fastapi/pull/3071))
* OAuth2 Implicit Flow
* OAuth2 Client Credentials Flow
* OAuth2 Authorization Code Flow
* OAuth2 Password Flow
* OpenID Connect
