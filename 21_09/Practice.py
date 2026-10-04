from abc import ABC, abstractmethod
import unittest

class Party(ABC):
    def __init__(self, name: str) -> None:
        name = name.strip()

        if not name:
            raise ValueError("Имя не должно быть пустым")

        if not any(char.isalpha() for char in name):
            raise ValueError("Имя должно включать в себя буквы")

        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @abstractmethod
    def __str__(self) -> str:
        return f'Партия "{self.__name}"'


class BudgetFundedParty(Party):
    def __init__(self, name: str, allocation_amount: float) -> None:
        super().__init__(name)

        if allocation_amount <= 0:
            raise ValueError("Ассигнование должно быть больше нуля")

        self.__allocation_amount = allocation_amount

    @property
    def allocation_amount(self) -> float:
        return self.__allocation_amount

    def __str__(self) -> str:
        s = super().__str__()
        return f"{s}, ассигнование: {self.__allocation_amount}"


class RepresentativeParty(Party):
    def __init__(self, name: str, deputies_count: int) -> None:
        super().__init__(name)

        if deputies_count < 0:
            raise ValueError("Количество депутатов не может быть меньше нуля")

        self.__deputies_count = deputies_count

    @property
    def deputies_count(self) -> int:
        return self.__deputies_count

    def __str__(self) -> str:
        s = super().__str__()
        return f"{s}, количество депутатов: {self.__deputies_count}"


class PartyRegistry:
    def __init__(self) -> None:
        self.__parties: list[Party] = []

    def add_party(self, party: Party) -> None:
        if not isinstance(party, Party):
            raise TypeError("Можно добавлять только объект класса Party")

        self.__parties.append(party)

    def __has_required_first_letter(self, party: Party) -> bool:
        first_letter = party.name[0].upper()
        return first_letter in "АБВГДЕЁЖЗИЙК"

    def print_required_parties(self) -> None:
        for party in self.__parties:
            if self.__has_required_first_letter(party):
                print(party)


class InputParties:
    def input(self, registry: PartyRegistry) -> None:
        while True:
            print(
                'Для выбора обычной партии введите "обычная", '
                'для выбора бюджетной введите "бюджетная", '
                'для выхода напишите "стоп"'
            )
            type_of_party = input("\nВыберите тип партии: ").strip().lower()

            if type_of_party == "стоп":
                break

            try:
                name = input("Введите название партии: ")

                if type_of_party == "обычная":
                    deputies_count = int(input("Введите количество депутатов: "))
                    party = RepresentativeParty(name, deputies_count)
                elif type_of_party == "бюджетная":
                    allocation_amount = float(input("Введите размер ассигнования: "))
                    party = BudgetFundedParty(name, allocation_amount)
                else:
                    print("Неверный тип партии")
                    continue

                registry.add_party(party)
            except ValueError as error:
                print(error)


class Task:
    def run(self) -> None:
        registry = PartyRegistry()
        input_parties = InputParties()
        input_parties.input(registry)
        print("Партии с названиями от А до К:")
        registry.print_required_parties()

class TestParty(unittest.TestCase):
    def test_representative_party(self):
        party = RepresentativeParty("Альфа",10)
        self.assertEqual(party.name, "Альфа")
        self.assertEqual(party.deputies)

    def test_budget_party(self):
        party = BudgetFundedParty("Бета",5000)
        self.assertEqual(party.name, "Бета")
        self.assertEqual(party.allocation_amount,5000)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            RepresentativeParty("",10)
    
    def test_name_without_letters(self):
        with self.assertRaises(ValueError):
            RepresentativeParty("1234",10)
    
    def test_negative_deputies(self):
        with self.assertRaises(ValueError):
            RepresentativeParty("Бета",-1)
    
    def test_zero_allocation(self):
        with self.assertRaises(ValueError):
            BudgetFundedParty("Альфа", 0)
    
    def test_add_wrong_object(self):
        registry = PartyRegistry()
        
        with self.assertRaises(TypeError):
            registry.add_party("Альфа")
    
if __name__ =='__main__':
    task = Task()
    task.run()
