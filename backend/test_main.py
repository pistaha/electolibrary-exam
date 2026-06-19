import os
from pathlib import Path

os.environ["DATABASE_PATH"] = str(Path(__file__).parent / "test_tasks.db")

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402


def setup_module() -> None:
    main.DATABASE_PATH.unlink(missing_ok=True)


def teardown_module() -> None:
    main.DATABASE_PATH.unlink(missing_ok=True)


def test_crud_and_library_actions() -> None:
    with TestClient(main.app) as client:
        initial = client.get("/api/books")
        assert initial.status_code == 200
        assert len(initial.json()) == 4

        payload = {
            "title": "Тестовая книга",
            "author": "Автор Теста",
            "description": "Описание тестовой книги достаточной длины.",
            "cover_url": "",
            "publisher": "Экзамен",
            "publication_year": 2026,
            "age_rating": "12+",
            "available": True,
            "favorite": False,
            "reserved": False,
            "collection_name": "Тесты",
        }
        created = client.post("/api/books", json=payload)
        assert created.status_code == 201
        book_id = created.json()["id"]

        payload["title"] = "Обновлённая книга"
        assert client.put(f"/api/books/{book_id}", json=payload).json()["title"] == payload["title"]
        assert client.patch(f"/api/books/{book_id}/favorite", json={"value": True}).json()["favorite"]
        reserved = client.patch(f"/api/books/{book_id}/reserve", json={"value": True})
        assert reserved.json()["reserved"] is True
        assert reserved.json()["available"] is False

        assert client.delete(f"/api/books/{book_id}").status_code == 204
        assert client.get(f"/api/books/{book_id}").status_code == 404

