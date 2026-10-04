from abc import ABC, abstractmethod
from accessify import private


# Принципы SOLID
# S - Single Responsibility principle
# O - Open/close principle
# L - Liskov substitution principle
# I - Interface segregarion principle
# D - Dependency inversion principle

# DRY

class Book(ABC):
    def __init__(self, name: str, pages_count: int):
        if len(name) < 1:
            raise ValueError("Имя не может быть пустым")
        if pages_count <= 0:
            raise ValueError("Количество страниц должно быть положительным")
        self.__name = name
        self.__pages_count = pages_count

    @property
    def name(self) -> str:
        return self.__name

    def __str__(self) -> str:
        return f"{self.name} {self.__pages_count}"

    @property
    def pages_count(self):
        return self.__pages_count


class Magazine(Book):

    def __init__(self, name: str, pages_count: int,
                 year: int, number: int
                 ):
        super.__init__(name, pages_count)
        self.__year = year
        self.__number = number

    def __str__(self):
        s = super.__str__()
        return f"{s} {self.__year} {self.__number}"

class IBookReceiver(ABC):

    @abstractmethod
    def add_book(self, book: Book):
        pass

class ILibrary(IBookReceiver):

    @abstractmethod
    def print_books_with_pages_count_more_than_10(self):
        pass


class Library(IBookPrinter, IBookReceiver):
    def __init__(self):
        self.__books = []

    def add_book(self, book: Book):
        pass

    def print_books_with_pages_count_more_than_10(self):
        for book in self.__books:
            if book.pages_count > 10:
                print(book)

    pass


class ClassicBook(Book):
    pass


class InputBooks:

    def input(self, library: IBookReceiver) -> None:
        # Ввод книг
        while True:
            type_of_book = input("Укажите тип книги: ")
            if type_of_book == "журнал":
                pass
            elif type_of_book == "книга":
                pass
            else:
                print("Неверный тип книги")
                continue


class Task:

    def __init__(self,library: ILibrary):
        self.__library__ = library

    def run(self):
        # тут все вместе делает
        library = self.__library__
        InputBooks().input(library)
        library.print_books_with_pages_count_more_than_10()
        pass


Task(Library()).run()
