# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

A widget management application: add, remove, rename, and remix widgets in a database. What is a widget? Only Claude knows.

## Commands

Setup (once):
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the API:
```
.venv/bin/uvicorn app.main:app --reload
```

Tests:
```
.venv/bin/pytest                            # full suite
.venv/bin/pytest tests/test_widgets.py::test_remix_links_parent   # single test
```

The test fixture points the app at a temp SQLite file via the `WIDGETS_DB` env var, so tests never touch `widgets.db`.

## Architecture

FastAPI + stdlib `sqlite3`, no ORM. Three modules under `app/`:

- `db.py` — owns the single-table schema and connection lifecycle. `get_conn()` is a context manager that commits on exit; `init_db()` runs `CREATE TABLE IF NOT EXISTS`. `DB_PATH` is read from `WIDGETS_DB` at import time. FastAPI's `lifespan` calls `init_db()` on startup.
- `models.py` — Pydantic request/response schemas (`WidgetCreate`, `WidgetUpdate`, `WidgetRemix`, `Widget`).
- `main.py` — route handlers. Each handler opens a connection via `get_conn()`, calls the private `_get()` helper (raises 404 if missing), and returns rows mapped through `_row_to_widget`.

Widget schema: `id`, `name`, `description`, `parent_id` (nullable, self-FK set to NULL on parent delete), `created_at`. **Remix** = insert a new row copying the source's description, setting `parent_id` to the source. A remix defaults its name to `"<source> (remix)"` unless one is provided.

Endpoints: `GET/POST /widgets`, `GET/PATCH/DELETE /widgets/{id}`, `POST /widgets/{id}/remix`.
