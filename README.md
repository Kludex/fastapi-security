# FastAPI Security Strategies

Each folder contains a different strategy to authenticate a user/client/application with FastAPI.

All the strategies are using a `dictionary` as database.

We have:

* [APIKey Header](api_key)
* [HTTP Basic](http_basic)
* [HTTP Bearer](https://github.com/tiangolo/fastapi/blob/master/tests/test_security_http_bearer.py)
* [OAuth2 Password Flow](oauth2_password)

Missing:

* HTTP Digest
    - https://github.com/tiangolo/fastapi/pull/3071
* OAuth2 Implicit Flow
    - https://blog.authlib.org/2020/fastapi-google-login
    - https://github.com/tiangolo/fastapi/issues/12
* OAuth2 Client Credentials Flow
    - https://github.com/tiangolo/fastapi/issues/774
* OAuth2 Authorization Code Flow
* OpenID Connect
