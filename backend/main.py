from __future__ import annotations

import os
import sqlite3
from contextlib import asynccontextmanager, contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Iterator, Literal

from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR.parent / "data" / "tasks.db"))


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@contextmanager
def database() -> Iterator[sqlite3.Connection]:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialise_database() -> None:
    with database() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                description TEXT NOT NULL,
                cover_url TEXT NOT NULL DEFAULT '',
                publisher TEXT NOT NULL,
                publication_year INTEGER NOT NULL,
                age_rating TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1,
                favorite INTEGER NOT NULL DEFAULT 0,
                reserved INTEGER NOT NULL DEFAULT 0,
                collection_name TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        count = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if count == 0:
            now = utc_now()
            connection.executemany(
                """
                INSERT INTO books (
                    title, author, description, cover_url, publisher,
                    publication_year, age_rating, available, favorite,
                    reserved, collection_name, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        "Чапаев и Пустота",
                        "Виктор Пелевин",
                        "Фантасмагорический роман о поиске внутренней свободы.",
                        "https://placehold.co/480x680/143c3b/f5efdf?text=Чапаев+и+Пустота",
                        "Вагриус",
                        1996,
                        "18+",
                        1,
                        1,
                        0,
                        "Современная проза",
                        now,
                        now,
                    ),
                    (
                        "Анна Каренина",
                        "Лев Толстой",
                        "Роман о семье, выборе и противоречиях русского общества.",
                        "https://placehold.co/480x680/9b594a/fff8ec?text=Анна+Каренина",
                        "ЛитРес Классика",
                        1878,
                        "16+",
                        1,
                        0,
                        0,
                        "Русская классика",
                        now,
                        now,
                    ),
                    (
                        "Мастер и Маргарита",
                        "Михаил Булгаков",
                        "Мистический роман о любви, ответственности и творческой свободе.",
                        "https://placehold.co/480x680/2d3047/f4d35e?text=Мастер+и+Маргарита",
                        "АСТ",
                        1967,
                        "16+",
                        0,
                        1,
                        1,
                        "Русская классика",
                        now,
                        now,
                    ),
                    (
                        "Clean Code",
                        "Robert C. Martin",
                        "Практическое руководство по созданию понятного и поддерживаемого кода.",
                        "https://placehold.co/480x680/1b4965/cae9ff?text=Clean+Code",
                        "Prentice Hall",
                        2008,
                        "12+",
                        1,
                        0,
                        0,
                        "Профессиональное развитие",
                        now,
                        now,
                    ),
                ],
            )


AgeRating = Literal["0+", "6+", "12+", "16+", "18+"]


class BookBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=2, max_length=160)
    author: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=2000)
    cover_url: str = Field(default="", max_length=2_000_000)
    publisher: str = Field(min_length=2, max_length=120)
    publication_year: int = Field(ge=1450, le=datetime.now().year)
    age_rating: AgeRating
    available: bool = True
    favorite: bool = False
    reserved: bool = False
    collection_name: str = Field(default="", max_length=100)

    @field_validator("cover_url")
    @classmethod
    def validate_cover(cls, value: str) -> str:
        if value and not (value.startswith("https://") or value.startswith("data:image/jpeg;base64,")):
            raise ValueError("Обложка должна быть HTTPS-ссылкой или JPG-файлом")
        return value


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    created_at: str
    updated_at: str


class BookAction(BaseModel):
    value: bool


class CollectionUpdate(BaseModel):
    collection_name: str = Field(default="", max_length=100)


def row_to_book(row: sqlite3.Row) -> dict:
    book = dict(row)
    for key in ("available", "favorite", "reserved"):
        book[key] = bool(book[key])
    return book


def get_book_or_404(connection: sqlite3.Connection, book_id: int) -> sqlite3.Row:
    row = connection.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return row


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialise_database()
    yield


app = FastAPI(
    title="ElectoLibrary API",
    description="REST API итогового проекта по Vue 3",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "database": str(DATABASE_PATH)}


@app.get("/api/books", response_model=list[Book])
def list_books(
    availability: Annotated[Literal["all", "available", "unavailable"], Query()] = "all",
    favorite: bool | None = None,
) -> list[dict]:
    clauses: list[str] = []
    params: list[object] = []
    if availability != "all":
        clauses.append("available = ?")
        params.append(availability == "available")
    if favorite is not None:
        clauses.append("favorite = ?")
        params.append(favorite)
    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    with database() as connection:
        rows = connection.execute(f"SELECT * FROM books{where} ORDER BY created_at DESC", params).fetchall()
    return [row_to_book(row) for row in rows]


@app.get("/api/books/{book_id}", response_model=Book)
def get_book(book_id: int) -> dict:
    with database() as connection:
        return row_to_book(get_book_or_404(connection, book_id))


@app.post("/api/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate) -> dict:
    data = payload.model_dump()
    now = utc_now()
    fields = ", ".join(data)
    placeholders = ", ".join("?" for _ in data)
    with database() as connection:
        cursor = connection.execute(
            f"INSERT INTO books ({fields}, created_at, updated_at) VALUES ({placeholders}, ?, ?)",
            [*data.values(), now, now],
        )
        row = get_book_or_404(connection, cursor.lastrowid)
    return row_to_book(row)


@app.put("/api/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate) -> dict:
    data = payload.model_dump()
    assignments = ", ".join(f"{field} = ?" for field in data)
    with database() as connection:
        get_book_or_404(connection, book_id)
        connection.execute(
            f"UPDATE books SET {assignments}, updated_at = ? WHERE id = ?",
            [*data.values(), utc_now(), book_id],
        )
        row = get_book_or_404(connection, book_id)
    return row_to_book(row)


@app.delete("/api/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int) -> Response:
    with database() as connection:
        get_book_or_404(connection, book_id)
        connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update_boolean_field(book_id: int, field: str, payload: BookAction) -> dict:
    with database() as connection:
        get_book_or_404(connection, book_id)
        connection.execute(
            f"UPDATE books SET {field} = ?, updated_at = ? WHERE id = ?",
            (payload.value, utc_now(), book_id),
        )
        row = get_book_or_404(connection, book_id)
    return row_to_book(row)


@app.patch("/api/books/{book_id}/favorite", response_model=Book)
def set_favorite(book_id: int, payload: BookAction) -> dict:
    return update_boolean_field(book_id, "favorite", payload)


@app.patch("/api/books/{book_id}/reserve", response_model=Book)
def set_reserved(book_id: int, payload: BookAction) -> dict:
    with database() as connection:
        row = get_book_or_404(connection, book_id)
        if payload.value and not row["available"]:
            raise HTTPException(status_code=409, detail="Книга сейчас недоступна")
        connection.execute(
            "UPDATE books SET reserved = ?, available = ?, updated_at = ? WHERE id = ?",
            (payload.value, not payload.value, utc_now(), book_id),
        )
        updated = get_book_or_404(connection, book_id)
    return row_to_book(updated)


@app.patch("/api/books/{book_id}/availability", response_model=Book)
def set_availability(book_id: int, payload: BookAction) -> dict:
    return update_boolean_field(book_id, "available", payload)


@app.patch("/api/books/{book_id}/collection", response_model=Book)
def set_collection(book_id: int, payload: CollectionUpdate) -> dict:
    with database() as connection:
        get_book_or_404(connection, book_id)
        connection.execute(
            "UPDATE books SET collection_name = ?, updated_at = ? WHERE id = ?",
            (payload.collection_name.strip(), utc_now(), book_id),
        )
        row = get_book_or_404(connection, book_id)
    return row_to_book(row)


@app.get("/api/collections", response_model=list[str])
def list_collections() -> list[str]:
    with database() as connection:
        rows = connection.execute(
            "SELECT DISTINCT collection_name FROM books WHERE collection_name <> '' ORDER BY collection_name"
        ).fetchall()
    return [row[0] for row in rows]
