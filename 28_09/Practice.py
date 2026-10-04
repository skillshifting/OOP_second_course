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
        base_info = super().__str__()
        return (
            f"{base_info}, "
            f"ассигнование: {self.__allocation_amount}"
        )


class RepresentativeParty(Party):
    def __init__(self, name: str, deputies_count: int) -> None:
        super().__init__(name)

        if deputies_count < 0:
            raise ValueError(
                "Количество депутатов не может быть меньше нуля"
            )

        self.__deputies_count = deputies_count

    @property
    def deputies_count(self) -> int:
        return self.__deputies_count

    def __str__(self) -> str:
        base_info = super().__str__()
        return (
            f"{base_info}, "
            f"количество депутатов: {self.__deputies_count}"
        )


class PartyRegistry:
    def __init__(self) -> None:
        self.__parties: list[Party] = []

    def add_party(self, party: Party) -> None:
        if not isinstance(party, Party):
            raise TypeError(
                "Можно добавлять только объекты класса Party"
            )

        self.__parties.append(party)

    def __has_required_first_letter(self, party: Party) -> bool:
        first_letter = party.name[0].upper()

        return first_letter in "АБВГДЕЁЖЗИЙК"

    def print_required_parties(self) -> None:
        found = False

        for party in self.__parties:
            if self.__has_required_first_letter(party):
                print(party)
                found = True

        if not found:
            print("Подходящих партий нет.")


class InputParties:
    def input_party_type(self) -> str:
        while True:
            print()
            print("Выберите тип партии:")
            print('  "обычная"   — партия с депутатами')
            print('  "бюджетная" — партия с ассигнованием')
            print('  "стоп"       — закончить ввод')

            party_type = input(
                "Ваш выбор: "
            ).strip().lower()

            if party_type in (
                "обычная",
                "бюджетная",
                "стоп",
            ):
                return party_type

            print(
                "Неверный тип партии. "
                "Введите «обычная», «бюджетная» или «стоп»."
            )

    def input_party_name(self) -> str:
        while True:
            name = input(
                "Введите название партии: "
            ).strip()

            if not name:
                print(
                    "Имя не должно быть пустым. "
                    "Попробуйте ещё раз."
                )
                continue

            if not any(char.isalpha() for char in name):
                print(
                    "Имя должно включать в себя буквы. "
                    "Попробуйте ещё раз."
                )
                continue

            return name

    def input_deputies_count(self) -> int:
        while True:
            try:
                deputies_count = int(
                    input(
                        "Введите количество депутатов: "
                    )
                )

                if deputies_count < 0:
                    print(
                        "Количество депутатов "
                        "не может быть меньше нуля."
                    )
                    continue

                return deputies_count

            except ValueError:
                print(
                    "Необходимо ввести целое число. "
                    "Попробуйте ещё раз."
                )

    def input_allocation_amount(self) -> float:
        while True:
            try:
                value = input(
                    "Введите размер ассигнования: "
                ).strip()

                value = value.replace(",", ".")

                allocation_amount = float(value)

                if allocation_amount <= 0:
                    print(
                        "Ассигнование должно быть больше нуля."
                    )
                    continue

                return allocation_amount

            except ValueError:
                print(
                    "Необходимо ввести число. "
                    "Попробуйте ещё раз."
                )

    def input(self, registry: PartyRegistry) -> None:
        print("Добавление партий")

        while True:
            type_of_party = self.input_party_type()

            if type_of_party == "стоп":
                print()
                print("Ввод партий завершён.")
                break

            name = self.input_party_name()

            if type_of_party == "обычная":
                deputies_count = self.input_deputies_count()

                party = RepresentativeParty(
                    name,
                    deputies_count,
                )

            elif type_of_party == "бюджетная":
                allocation_amount = (
                    self.input_allocation_amount()
                )

                party = BudgetFundedParty(
                    name,
                    allocation_amount,
                )

            registry.add_party(party)

            print()
            print("Партия успешно добавлена:")
            print(party)
            print('')

class Task:
    def run(self) -> None:
        registry = PartyRegistry()
        input_parties = InputParties()

        input_parties.input(registry)

        print()

        print("Партии с названиями от А до К:")

        registry.print_required_parties()


task = Task()
task.run()

