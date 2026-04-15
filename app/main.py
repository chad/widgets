from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from .db import get_conn, init_db
from .models import Widget, WidgetCreate, WidgetRemix, WidgetUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Widgets", lifespan=lifespan)


def _row_to_widget(row) -> Widget:
    return Widget(**dict(row))


def _get(conn, widget_id: int):
    row = conn.execute("SELECT * FROM widgets WHERE id = ?", (widget_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="widget not found")
    return row


@app.get("/widgets", response_model=list[Widget])
def list_widgets():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM widgets ORDER BY id").fetchall()
        return [_row_to_widget(r) for r in rows]


@app.get("/widgets/{widget_id}", response_model=Widget)
def get_widget(widget_id: int):
    with get_conn() as conn:
        return _row_to_widget(_get(conn, widget_id))


@app.post("/widgets", response_model=Widget, status_code=201)
def create_widget(body: WidgetCreate):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO widgets (name, description) VALUES (?, ?)",
            (body.name, body.description),
        )
        return _row_to_widget(_get(conn, cur.lastrowid))


@app.patch("/widgets/{widget_id}", response_model=Widget)
def update_widget(widget_id: int, body: WidgetUpdate):
    with get_conn() as conn:
        _get(conn, widget_id)
        fields, values = [], []
        if body.name is not None:
            fields.append("name = ?")
            values.append(body.name)
        if body.description is not None:
            fields.append("description = ?")
            values.append(body.description)
        if fields:
            values.append(widget_id)
            conn.execute(f"UPDATE widgets SET {', '.join(fields)} WHERE id = ?", values)
        return _row_to_widget(_get(conn, widget_id))


@app.delete("/widgets/{widget_id}", status_code=204)
def delete_widget(widget_id: int):
    with get_conn() as conn:
        _get(conn, widget_id)
        conn.execute("DELETE FROM widgets WHERE id = ?", (widget_id,))


@app.post("/widgets/{widget_id}/remix", response_model=Widget, status_code=201)
def remix_widget(widget_id: int, body: WidgetRemix | None = None):
    with get_conn() as conn:
        src = _get(conn, widget_id)
        new_name = (body.name if body else None) or f"{src['name']} (remix)"
        cur = conn.execute(
            "INSERT INTO widgets (name, description, parent_id) VALUES (?, ?, ?)",
            (new_name, src["description"], src["id"]),
        )
        return _row_to_widget(_get(conn, cur.lastrowid))
