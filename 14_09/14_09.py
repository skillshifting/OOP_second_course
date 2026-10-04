from abc import ABC
from accessify import private

class Book(ABC):
    def __init__(self, name: str, pages_count: int):
        if len(name)<1: 
            raise ValueError("имя не может быть пустым")
        if pages_count <=0:
            raise ValueError("количество страниц должно быть больше нуля")
        self.__name = name
        self.__pages_count = pages_count

    @property
    def name(self):
        return self.__name
    
    def __str__(self) -> str:
        return f"{self.name} {self.__pages_count}"

class Magazine(Book):
    def __init__(self, name: str, pages_count: int,
                year: int, number: int):
        super.__init__(name, pages_count)
        self.__year = year
        self.__number = number
        
    def __str__(self) -> str:
        s = super.__str__()
        return f"{s} {self.__year} {self.__number}"
    pass

# class ClassicBook(Book):
#     pass

class Library:
    def __init__(self):
        self.__books = []
        
    def add_book(self, book: ...):...

    def print_books_with_pages_count_more_than_10(self):
        # перебор и вывод
        for book in self.__books:
            if book.pages.count>10:
                print(book)
        pass

class InputBooks:

    def input(self) -> None:
        while True:
            # ввод книг 
            type_of_book = input("Укажите тип книги:")
            if type_of_book == "журнал":
                pass
            elif type_of_book == "книга":
                pass
            else: 
                print("Неверный тип книги")
                continue

class Task:
    def run(self):
        # тут все вместе делает 
        library = Library
        InputBooks = library
        library.print_books_with_pages_count_more_than_10
        pass
    
    