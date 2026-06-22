from enum import Enum

dummy_todos = [
    {"id": 1, "title": "Buy groceries", "description": "Get milk, eggs, bread, and fresh vegetables.", "completed": False},
    {"id": 2, "title": "Walk the dog", "description": "Take Max to the park for his afternoon walk.", "completed": True},
    {"id": 3, "title": "Read a book", "description": "Read at least two chapters of my sci-fi novel.", "completed": False},
    {"id": 4, "title": "Write code", "description": "Finish implementing the CRUD endpoints for the backend.", "completed": True},
    {"id": 5, "title": "Cook dinner", "description": "Prepare a healthy chicken and rice meal.", "completed": False},
    {"id": 6, "title": "Exercise", "description": "Complete a 30-minute full-body workout.", "completed": True},
    {"id": 7, "title": "Call a friend", "description": "Catch up with Sarah to see how her week went.", "completed": False},
    {"id": 8, "title": "Plan a trip", "description": "Look up flight prices and hotels for the weekend getaway.", "completed": True},
    {"id": 9, "title": "Clean the house", "description": "Vacuum the living room and wipe down kitchen counters.", "completed": False},
    {"id": 10, "title": "Pay bills", "description": "Settle the electricity and internet utility bills.", "completed": True},
]

class Order_by(str, Enum):
    asc = "asc"
    desc = "desc"