# Widget Management Application — Plan

## Stack
- Python 3 + FastAPI (JSON API)
- SQLite via stdlib `sqlite3` (single file DB, no extra deps)
- pytest for tests
- `requirements.txt` for deps

## Domain
A **widget** has: `id`, `name`, `description`, `parent_id` (nullable — points at the widget it was remixed from), `created_at`.

## Operations (from CLAUDE.md)
- **Add**: `POST /widgets` — create with name + description
- **Remove**: `DELETE /widgets/{id}`
- **Rename**: `PATCH /widgets/{id}` — update name and/or description
- **Remix**: `POST /widgets/{id}/remix` — create a new widget derived from the source, linked via `parent_id`
- Plus: `GET /widgets`, `GET /widgets/{id}`

## Layout
```
app/
  __init__.py
  main.py       # FastAPI app, route handlers
  db.py         # connection + schema init
  models.py     # Pydantic request/response schemas
tests/
  test_widgets.py
requirements.txt
```

## Steps
- [x] Plan written
- [x] Create app package, db, models, routes
- [x] Write tests covering add/rename/remove/remix/list
- [x] Verify tests pass with `python3 -m pytest`
- [x] Update CLAUDE.md with real commands + architecture
- [x] git commit
