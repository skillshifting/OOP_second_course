from abc import ABC, abstractmethod


class PartyInterface(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

class Party(PartyInterface):
    def __init__(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name


class BudgetFundedPartyInterface(ABC):
    @abstractmethod
    def get_allocation_amount(self)-> int:
        pass

class BudgetFundedParty(Party,BudgetFundedPartyInterface):
    def __init__(self, name: str, allocation_amount: int) -> None:
        super().__init__(name)
        self.__allocation_amount = allocation_amount

    def get_allocation_amount(self) -> int:
        return self.__allocation_amount


class RepresentativePartyInterface(ABC):
    @abstractmethod
    def get_deputies_count(self)-> int:
        pass

class RepresentativeParty(Party,RepresentativePartyInterface):
    def __init__(self, name: str, deputies_count: int) -> None:
        super().__init__(name)
        self.__deputies_count = deputies_count

    def get_deputies_count(self) -> int:
        return self.__deputies_count


class PartyWriterInterface(ABC):
    @abstractmethod
    def add_party(self, party:PartyInterface):
        pass


class PartyReaderInterface(ABC):
    @abstractmethod
    def get_parties(self) -> list[PartyInterface]:
        pass


class PartyRegistry(PartyWriterInterface,PartyReaderInterface):
    def __init__(self) -> None:
        self.__parties: list[PartyInterface] = []

    def add_party(self, party: PartyInterface) -> None:
        if not isinstance(party, PartyInterface):
            raise TypeError(
                "Можно добавлять только объект класса Party"
            )

        self.__parties.append(party)

    def get_parties(self) -> list[PartyInterface]:
        return self.__parties.copy()


class FirstLetterCheckerInterface(ABC):
    @abstractmethod
    def check(self,party:PartyInterface) -> bool:
        pass

class RequiredFirstLetterChecker(FirstLetterCheckerInterface):
    def check(self, party: PartyInterface) -> bool:
        name = party.get_name().strip()

        return name[0].upper() in ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К']


class PartyFilterInterface(ABC):
    @abstractmethod
    def filter(self, parties: list[PartyInterface]) -> list[PartyInterface]:
        pass


class PartyFilter(PartyFilterInterface):
    def __init__(self, checker: FirstLetterCheckerInterface) -> None:
        self.__checker = checker

    def filter(self, parties: list[PartyInterface]) -> list[PartyInterface]:
        filtered_parties=[]
        for party in parties:
            if self.__checker.check(party):
                filtered_parties.append(party)
        return filtered_parties


class PartyNameValidatorInterface(ABC):

    @abstractmethod
    def validate(self,name:str) -> str:
        pass


class PartyNameValidator(PartyNameValidatorInterface):
    def validate(self, name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Имя не должно быть пустым")

        if not any(char.isalpha() for char in name):
            raise ValueError("Имя должно включать в себя буквы")
        return name

class CountValidatorInterface(ABC):
    @abstractmethod
    def validate(self, count_amount: int) -> int:
        pass

class DeputiesCountValidator(CountValidatorInterface):
    def validate(self, deputies_count: int) -> int:
        if deputies_count < 0:
            raise ValueError("Количество депутатов не может быть меньше нуля")
        return deputies_count

class AllocationAmountValidator(CountValidatorInterface):
    def validate(self, allocation_amount: int) -> int:
        if allocation_amount <= 0:
            raise ValueError("Ассигнование должно быть больше нуля")
        return allocation_amount

class PartyTypeInputInterface(ABC):
    @abstractmethod
    def input(self) -> str:
        pass


class PartyTypeInput(PartyTypeInputInterface):
    def input(self) -> str:
        while True:
            print()
            print('Введите "обычная" для обычной партии')
            print('Введите "бюджетная" для бюджетной партии')
            print('Введите "стоп" для завершения')

            party_type = input("Выберите тип партии: ").strip().lower()

            if party_type in ("обычная", "бюджетная", "стоп"):
                return party_type

            print("Неверный тип партии")


class PartyNameInputInterface(ABC):
    @abstractmethod
    def input(self) -> str:
        pass

class PartyNameInput(PartyNameInputInterface):
    def __init__(self, validator: PartyNameValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> str:
        while True:
            name = input("Введите название партии: ")

            try:
                return self.__validator.validate(name)
            except ValueError as error:
                print(error)


class DeputiesCountInputInterface(ABC):
    @abstractmethod
    def input(self) -> int:
        pass

class DeputiesCountInput(DeputiesCountInputInterface):
    def __init__(self, validator: CountValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> int:
        while True:
            try:
                value = int(input("Введите количество депутатов: "))
                return self.__validator.validate(value)
            except ValueError as error:
                print(error)

class AllocationAmountInputInterface(ABC):
    @abstractmethod
    def input(self) -> int:
        pass


class AllocationAmountInput(AllocationAmountInputInterface):
    def __init__(self, validator: CountValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> int:
        while True:
            try:
                value = input("Введите размер ассигнования: ")
                value = value.strip().replace(",", ".")
                amount = int(value)

                return self.__validator.validate(amount)
            except ValueError as error:
                print(error)


class RepresentativeCreatorInterface(ABC):
    @abstractmethod
    def create(self,name: str,deputies_count: int) -> RepresentativeParty:
        pass



class RepresentativePartyCreator(RepresentativeCreatorInterface):
    def create(self,name: str,deputies_count: int) -> RepresentativeParty:
        party = RepresentativeParty(name,deputies_count)
        return party


class BudgetCreatorInterface(ABC):
    @abstractmethod
    def create(self,name: str,allocation_amount: int) -> BudgetFundedParty:
        pass

class BudgetFundedPartyCreator(BudgetCreatorInterface):
    def create(self,name: str,allocation_amount: int) -> BudgetFundedParty:
        party = BudgetFundedParty(name, allocation_amount)
        return party

class FormatterInterface(ABC):
    @abstractmethod
    def format(self, party:Party) -> str|None:
        pass

class RepresentativePartyFormatter(FormatterInterface):
    def format(self,party:Repre)


class PartyFormatter(FormatterInterface):
    def format(self, party: Party) -> str|None:
        if isinstance(party,RepresentativeParty):
            return f'Партия "{party.get_name()}", количество депутатов: {party.deputies_count}'

        if isinstance(party,BudgetFundedParty):
            return f'Партия "{party.get_name()}", ассигнование: {party.allocation_amount}'
        return

class OutputInterface(ABC):
    @abstractmethod
    def write(self,message:str|None) -> None:
        pass


class ConsoleOutput(OutputInterface):
    def write(self, message: str|None) -> None:
        print(message)


class PrinterInterface(ABC):
    @abstractmethod
    def print(self, parties: list[Party]) -> None:
        pass

class PartyPrinter(PrinterInterface):
    def __init__(self,formatter: FormatterInterface,output: OutputInterface) -> None:
        self.__formatter = formatter
        self.__output = output

    def print(self, parties: list[Party]) -> None:
        for party in parties:
            format_party=self.__formatter.format(party)
            self.__output.write(format_party)

class PartyInputScenarioInterface(ABC):
    @abstractmethod
    def run(self) -> None:
        pass


class PartyInputScenario(PartyInputScenarioInterface):
    def __init__(self,
        party_type_input: PartyTypeInputInterface,
        party_name_input: PartyNameInputInterface,
        deputies_count_input: DeputiesCountInputInterface,
        allocation_amount_input: AllocationAmountInputInterface,
        representative_creator: RepresentativeCreatorInterface,
        budget_creator: BudgetCreatorInterface,
        registry: PartyWriterInterface) -> None:
        self.__party_type_input = party_type_input
        self.__party_name_input = party_name_input
        self.__deputies_count_input = deputies_count_input
        self.__allocation_amount_input = allocation_amount_input
        self.__representative_creator = representative_creator
        self.__budget_creator = budget_creator
        self.__registry = registry

    def run(self) -> None:

        while True:
            party_type = self.__party_type_input.input()
            if party_type =='стоп':
                break


            name = self.__party_name_input.input()

            if party_type =='обычная':
                deputies = self.__deputies_count_input.input()
                representative_party = self.__representative_creator.create(name=name,deputies_count=deputies)
                self.__registry.add_party(representative_party)


            if party_type =='бюджетная':
                allocation = self.__allocation_amount_input.input()
                budget_party = self.__budget_creator.create(name=name,allocation_amount=allocation)
                self.__registry.add_party(budget_party)


class TaskInterface(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

class Task(TaskInterface):
    def __init__(
        self,
        input_scenario: PartyInputScenarioInterface,
        registry: PartyReaderInterface,
        party_filter: PartyFilterInterface,
        printer: PrinterInterface,
    ):
        self.__input_scenario = input_scenario
        self.__registry = registry
        self.__party_filter = party_filter
        self.__printer = printer

    def run(self) -> None:
        self.__input_scenario.run()
        parties = self.__registry.get_parties()
        filtered_parties = self.__party_filter.filter(parties=parties)
        self.__printer.print(filtered_parties)

if __name__ == "__main__":

    name_validator = PartyNameValidator()
    deputies_validator = DeputiesCountValidator()
    allocation_validator = AllocationAmountValidator()

    letter_checker = RequiredFirstLetterChecker()
    formatter = PartyFormatter()
    output = ConsoleOutput()


    type_input = PartyTypeInput()
    name_input = PartyNameInput(validator=name_validator)
    deputies_input = DeputiesCountInput(validator=deputies_validator)
    allocation_input = AllocationAmountInput(validator=allocation_validator)


    rep_creator = RepresentativePartyCreator()
    budget_creator = BudgetFundedPartyCreator()

    registry = PartyRegistry()
    party_filter = PartyFilter(checker=letter_checker)
    printer = PartyPrinter(formatter=formatter, output=output)

    scenario = PartyInputScenario(
        party_type_input=type_input,
        party_name_input=name_input,
        deputies_count_input=deputies_input,
        allocation_amount_input=allocation_input,
        representative_creator=rep_creator,
        budget_creator=budget_creator,
        registry=registry
    )

    task = Task(
        input_scenario=scenario,
        registry=registry,
        party_filter=party_filter,
        printer=printer
    )

    task.run()
