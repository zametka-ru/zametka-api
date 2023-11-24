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
  "user_id": 1
}
```


#### GET /v1/auth/verify/{token}/
```bash
curl -X "GET" "http://127.0.0.1:8000/v1/auth/verify/{token}"
```
```json
{
  "email": "string"
}
```


#### Scripts

#### POST /v1/notes/

```bash
curl -X "POST" \
  "http://127.0.0.1:8000/v1/notes/" \
  -d '{
      "title": "string",
      "text": "string"
  }'
```

```json
{
    "note": {
        "title": "string",
        "text": "string",
        "created_at": "2023-11-20T08:39:01.841Z",
        "author_id": 0
    }
}
```

#### GET /v1/notes/{note_id}/
```bash
curl -X "GET" "http://127.0.0.1:8000/v1/notes/{note_id}/"
```
```json
{
    "note": {
        "title": "string",
        "text": "string",
        "created_at": "2023-11-20T08:39:56.439Z",
        "author_id": 0
    }
}
```

#### PUT /v1/notes/{note_id}/

```bash
curl -X "PUT" \
  "http://127.0.0.1:8000/v1/notes/{note_id}/" \
  -d '{
      "title": "string",
      "text": "string"
  }'
```

```json
{
    "note": {
        "title": "string",
        "text": "string",
        "created_at": "2023-11-20T08:39:01.841Z",
        "author_id": 0
    }
}
```

#### DELETE /v1/notes/{note_id}/

```bash
curl -X "DELETE" \
  "http://127.0.0.1:8000/v1/notes/{note_id}/"
```

```json
{}
```

#### GET /v1/notes/

Possible query parameters:

```plain
page: integer (query)
Default value : 1

search: string (query)
```

```bash
curl -X "GET" "http://127.0.0.1:8000/v1/notes/"
```
```json
{
  "notes": [
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