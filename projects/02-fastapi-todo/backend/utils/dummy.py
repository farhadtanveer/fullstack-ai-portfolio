from enum import Enum

dummy_todos = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Walk the dog", "completed": True},
    {"id": 3, "title": "Read a book", "completed": False},
    {"id": 4, "title": "Write code", "completed": True},
    {"id": 5, "title": "Cook dinner", "completed": False},
    {"id": 6, "title": "Exercise", "completed": True},
    {"id": 7, "title": "Call a friend", "completed": False},
    {"id": 8, "title": "Plan a trip", "completed": True},
    {"id": 9, "title": "Clean the house", "completed": False},
    {"id": 10, "title": "Pay bills", "completed": True},
]

class Order_by(str, Enum):
    asc = "asc"
    desc = "desc"