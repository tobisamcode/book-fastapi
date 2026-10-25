from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest (BaseModel):
    id: Optional[int] = Field(description="Book ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6 )
    published_date: int = Field(gt=1999, lt=2026)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A very nice book",
                "author": "codingwithtobi",
                "description": "A very good book",
                "rating": 3,
                "published_date": 2026,
            }
        }
    }

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Computer Science Pro",
                "author": "codingwithtobi",
                "description": "A very good book",
                "rating": 5,
                "published_date": 2024,
            }
        }
    }

class BooksResponse(BaseModel):
    books: list[BookResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "books": [
                    {
                        "id": 1,
                        "title": "Computer Science Pro",
                        "author": "codingwithtobi",
                        "description": "A very good book",
                        "rating": 5,
                        "published_date": 2024,
                    }
                ]
            }
        }
    }

BOOKS =[
    Book(1, "Computer Science Pro", "codingwithtobi", "A very good book", 1, 2026),
    Book(2, "Mathematics", "codingwithtobi", "A very nice book", 4, 2020),
    Book(3, "Computer Science Lite", "codingwithtobi", "A very awesome book", 1, 2021),
    Book(4, "MATH Science ", "codingwithtobi", "A very good book", 5, 2025),
    Book(5, "Biological Science Pro", "codingwithtobi", "A very good book", 3, 2026),
    Book(6, "APDE 1", "codingwithtobi", "A very good book", 5, 2024),
]

@app.get("/books", response_model=BooksResponse)
async def show_books(
    ratings: Optional[int] = Query(None, ge=1, le=5),
    published_date: Optional[int] = Query(None, gt=1999, lt=2026),
):
    books_to_return = BOOKS
    if ratings is not None:
        books_to_return = [book for book in BOOKS if book.rating == ratings]
    if published_date is not None:
        books_to_return = [book for book in BOOKS if book.published_date == published_date]
    return {"books": books_to_return}

@app.get("/books/{book_id}", response_model=BookResponse)
async def show_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return {"book": book}
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/create")
async def create_book(request: BookRequest):
    new_book = Book(**request.dict())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book created successfully", "data": new_book}

@app.put("/books/{book_id}")
async def update_book(book_id: int, request: BookRequest):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            updated_book = Book(**request.dict())
            updated_book.id = book_id
            BOOKS[index] = updated_book
            return {"message": "Book updated successfully", "data": updated_book}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return  book