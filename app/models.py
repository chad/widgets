from pydantic import BaseModel, Field


class WidgetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = ""


class WidgetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None


class WidgetRemix(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)


class Widget(BaseModel):
    id: int
    name: str
    description: str
    parent_id: int | None
    created_at: str
