from fastapi import FastAPI, Body, HTTPException

app = FastAPI()


BOOKS = [
    {"id": 1, "title": "My first book", "author": "author 1", "category": "science"},
    {"id": 2, "title": "My second book", "author": "author 2", "category": "art"},
    {"id": 3, "title": "My third book", "author": "author 3", "category": "science"},
    {"id": 4, "title": "My fourth book", "author": "author 4", "category": "art"},
    {"id": 5, "title": "My fifth book", "author": "author 5", "category": "technology"},
]

@app.get("/books")
async def read_all_books(category: str = "", search: str = "", author: str = ""):
    books_to_return = BOOKS
    if category:
        books_to_return = [
            book for book in books_to_return
            if book["category"].casefold() == category.casefold()
        ]
    if search:
        books_to_return = [
            book for book in books_to_return
            if search.casefold() in book["title"].casefold()
        ]
    if author:
        books_to_return = [
            book for book in books_to_return
            if book["author"].casefold() == author.casefold()
        ]
    return {"data": books_to_return}

@app.get("/books/{id}")
async def read_book(id: int):
    for book in BOOKS:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return {
        "data": new_book,
        "message": "Book created successfully"
    }

@app.put("/books/{id}")
async def update_book(id: int, new_book=Body()):
    for index, book in enumerate(BOOKS):
        if book["id"] == id:
            new_book["id"] = id
            BOOKS[index] = new_book
            return {"data": new_book, "message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{id}")
async def delete_book(id: int):
    for index, book in enumerate(BOOKS):
        if book["id"] == id:
            BOOKS.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
