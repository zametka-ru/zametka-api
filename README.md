<p align="center">
<img height="200" width="200" src="https://github.com/lubaskinc0de/yourscript/assets/100635212/e9393d8b-e3b5-4990-8796-bdadf986e3c4"></img>
</p>

<h1 align="center" style="color: #92b4a7">your<span style="color: #81667a">script</span></h1>
<h2 align="center" style="color: #777da7">Инновационное решение в области написания <span style="color: #d5573b">
сценариев</span></h2>

------------------------
### *API*

API для приложения написания сценариев - **yourscript**.

*Чистая архитектура, безопасная аутентификация*.

---------------------

### *Эндпоинты*

#### Auth

#### POST /v1/auth/sign-up/

```bash
curl -X "POST" \
  "http://127.0.0.1:8000/v1/auth/sign-up/" \
  -d '{
      "email": "string",
      "password": "string",
      "password2": "string",
      "first_name": "string",
      "last_name": "string",
      "is_superuser": false,
      "is_active": false
  }'
```

```json
{
    "first_name": "string"
}
```

#### POST /v1/auth/sign-in/

```bash
curl -X "POST" \
  "http://127.0.0.1:8000/v1/auth/sign-in/" \
  -d '{
      "email": "string",
      "password": "string"
  }'
```

```json
{
  "access": "string",
  "refresh": "string"
}
```

#### GET /v1/auth/{token}/
```bash
curl -X "GET" "http://127.0.0.1:8000/v1/auth/{token}"
```
```json
{
  "email": "string"
}
```

#### POST /v1/auth/refresh/

```bash
curl -X "POST" --header "X-CSRF-Token: <csrf_refresh_token>" "http://127.0.0.1:8000/v1/auth/refresh/"
```

```json
{
  "access": "string",
  "refresh": "string"
}
```


#### Scripts

#### POST /v1/scripts/

```bash
curl -X "POST" \
  "http://127.0.0.1:8000/v1/scripts/" \
  -d '{
      "title": "string",
      "text": "string"
  }'
```

```json
{
    "script": {
        "title": "string",
        "text": "string",
        "created_at": "2023-11-20T08:39:01.841Z",
        "author_id": 0
    }
}
```

#### GET /v1/scripts/{script_id}/
```bash
curl -X "GET" "http://127.0.0.1:8000/v1/scripts/{script_id}/"
```
```json
{
    "script": {
        "title": "string",
        "text": "string",
        "created_at": "2023-11-20T08:39:56.439Z",
        "author_id": 0
    }
}
```

#### PUT /v1/scripts/{script_id}/

```bash
curl -X "PUT" \
  "http://127.0.0.1:8000/v1/scripts/{script_id}/" \
  -d '{
      "title": "string",
      "text": "string"
  }'
```

```json
{
    "script": {
        "title": "string",
        "text": "string",
        "created_at": "2023-11-20T08:39:01.841Z",
        "author_id": 0
    }
}
```

#### DELETE /v1/scripts/{script_id}/

```bash
curl -X "DELETE" \
  "http://127.0.0.1:8000/v1/scripts/{script_id}/"
```

```json
{}
```

#### GET /v1/scripts/

Possible query parameters:

```plain
page: integer (query)
Default value : 1

search: string (query)
```

```bash
curl -X "GET" "http://127.0.0.1:8000/v1/scripts/"
```
```json
{
  "scripts": [
    {
      "title": "string",
      "text": "string",
      "created_at": "2023-11-20T08:44:10.739Z",
      "author_id": 0
    }
  ]
}
```

---------------------

### Стeк технологий backend

- FastAPI
- SQLAlchemy (asyncpg)
- Pydantic
- JWT Auth
- Docker
- PostgreSQL
- Alembic

### Лицензия

Проект распространяется под лицензией GPLv3