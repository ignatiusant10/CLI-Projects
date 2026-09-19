from dataclasses import dataclass

@dataclass

class Customer:
    def __init__(self, name, email,phone):
        self.name = name
        self.email =email
        self.phone =phone

    def __repr__(self):
        return f"Customer(name={self.name},email={self.email},phone={self.phone})"

