from typing import Optional

from fastapi import  FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest (BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6 )

BOOKS =[
    Book(1, "Computer Science Pro", "codingwithtobi", "A very good book", 1),
    Book(2, "Mathematics", "codingwithtobi", "A very nice book", 4),
    Book(3, "Computer Science Lite", "codingwithtobi", "A very awesome book", 1),
    Book(4, "MATH Science ", "codingwithtobi", "A very good book", 5),
    Book(5, "Biological Science Pro", "codingwithtobi", "A very good book", 3),
    Book(6, "APDE 1", "codingwithtobi", "A very good book", 5),
]

@app.get("/books")
async def show_books():
    return {"books": BOOKS}

@app.post("/books/create")
async def create_book(request: BookRequest):
    new_book = Book(**request.dict())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book created successfully", "data": new_book}


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return  book