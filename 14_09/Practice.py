from abc import ABC, abstractmethod


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


class RequiredFirstLetterChecker:
    def check(self, party: Party) -> bool:
        pass



class PartyFilter:
    def __init__(
        self,
        checker: RequiredFirstLetterChecker,
    ) -> None:
        pass

    def filter(
        self,
        parties: list[Party],
    ) -> list[Party]:
        pass

# class InputParties:
#     def input(self, registry: PartyRegistry) -> None:
#         while True:
#             print(
#                 'Для выбора обычной партии введите "обычная", '
#                 'для выбора бюджетной введите "бюджетная", '
#                 'для выхода напишите "стоп"'
#             )
#             type_of_party = input("\nВыберите тип партии: ").strip().lower()

#             if type_of_party == "стоп":
#                 break

#             try:
#                 name = input("Введите название партии: ")

#                 if type_of_party == "обычная":
#                     deputies_count = int(input("Введите количество депутатов: "))
#                     party = RepresentativeParty(name, deputies_count)
#                 elif type_of_party == "бюджетная":
#                     allocation_amount = float(input("Введите размер ассигнования: "))
#                     party = BudgetFundedParty(name, allocation_amount)
#                 else:
#                     print("Неверный тип партии")
#                     continue

#                 registry.add_party(party)
#             except ValueError as error:
#                 print(error)


class PartyNameValidator:
    def validate(self, name: str) -> str:
        pass


class DeputiesCountValidator:
    def validate(self, deputies_count: int) -> int:
        pass


class AllocationAmountValidator:
    def validate(self, allocation_amount: float) -> float:
        pass
    

class PartyTypeInput:
    def input(self) -> str:
        while True:
            print()
            print('Введите "обычная" для обычной партии')
            print('Введите "бюджетная" для бюджетной партии')
            print('Введите "стоп" для завершения')

            party_type = input(
                "Выберите тип партии: "
            ).strip().lower()

            if party_type in (
                "обычная",
                "бюджетная",
                "стоп",
            ):
                return party_type

            print("Неверный тип партии")


class PartyNameInput:
    def __init__(
        self,
        validator: PartyNameValidator,
    ) -> None:
        self.__validator = validator

    def input(self) -> str:
        while True:
            name = input(
                "Введите название партии: "
            )

            try:
                return self.__validator.validate(name)

            except ValueError as error:
                print(error)


class DeputiesCountInput:
    def __init__(
        self,
        validator: DeputiesCountValidator,
    ) -> None:
        self.__validator = validator

    def input(self) -> int:
        while True:
            try:
                value = int(
                    input(
                        "Введите количество депутатов: "
                    )
                )

                return self.__validator.validate(value)

            except ValueError as error:
                print(error)


class AllocationAmountInput:
    def __init__(
        self,validator
    ) -> None:
        self.__validator = validator

    def input(self) -> float:
        while True:
            try:
                value = input(
                    "Введите размер ассигнования: "
                ).strip()

                value = value.replace(",", ".")

                amount = float(value)

                return self.__validator.validate(amount)

            except ValueError as error:
                print(error)


class RepresentativePartyCreator:
    def create(
        self,
        name: str,
        deputies_count: int,
    ) -> RepresentativeParty:
        pass


class BudgetFundedPartyCreator:
    def create(
        self,
        name: str,
        allocation_amount: float,
    ) -> BudgetFundedParty:
        pass
    

class RequiredFirstLetterChecker:
    def check(self, party: Party) -> bool:
        pass


class PartyFilter:
    def __init__(
        self,
        checker: RequiredFirstLetterChecker,
    ) -> None:
        pass

    def filter(
        self,
        parties: list[Party],
    ) -> list[Party]:
        pass


# class Task:
#     def run(self) -> None:
#         registry = PartyRegistry()
#         input_parties = InputParties()
#         input_parties.input(registry)
#         print("Партии с названиями от А до К:")
#         registry.print_required_parties()


class PartyFormatter:
    def format(self, party: Party) -> str:
        pass

class ConsoleOutput:
    def write(self, message: str) -> None:
        pass


class PartyPrinter:
    def __init__(
        self,
        formatter: PartyFormatter,
        output: ConsoleOutput,
    ) -> None:
        pass

    def print(self, parties: list[Party]) -> None:
        pass


class PartyInputScenario:
    def __init__(
        self,
        party_type_input: PartyTypeInput,
        party_name_input: PartyNameInput,
        deputies_count_input: DeputiesCountInput,
        allocation_amount_input: AllocationAmountInput,
        representative_creator: RepresentativePartyCreator,
        budget_creator: BudgetFundedPartyCreator,
        registry: PartyRegistry,
        formatter: PartyFormatter,
        output: ConsoleOutput,
    ) -> None:
        pass

    def run(self) -> None:
        pass

# task = Task()
# task.run()
