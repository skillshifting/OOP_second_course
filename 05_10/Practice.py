from abc import ABC, abstractmethod

class Party:
    def __init__(self, name: str) -> None:
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name


class BudgetFundedParty(Party):
    def __init__(self, name: str, allocation_amount: int) -> None:
        super().__init__(name)
        self.__allocation_amount = allocation_amount

    @property
    def allocation_amount(self) -> int:
        return self.__allocation_amount


class RepresentativeParty(Party):
    def __init__(self, name: str, deputies_count: int) -> None:
        super().__init__(name)
        self.__deputies_count = deputies_count

    @property
    def deputies_count(self) -> int:
        return self.__deputies_count


class PartyWriterInterface(ABC):
    @abstractmethod
    def add_party(self, party:Party):
        pass


class PartyReaderInterface(ABC):
    @abstractmethod
    def get_parties(self) -> list[Party]:
        pass


class PartyRegistry(PartyWriterInterface,PartyReaderInterface):
    def __init__(self) -> None:
        self.__parties: list[Party] = []

    def add_party(self, party: Party) -> None:
        if not isinstance(party, Party):
            raise TypeError(
                "Можно добавлять только объект класса Party"
            )

        self.__parties.append(party)

    def get_parties(self) -> list[Party]:
        return self.__parties.copy()


class FirstLetterCheckerInterface(ABC):
    @abstractmethod
    def check(self,party:Party) -> bool:
        pass

class RequiredFirstLetterChecker(FirstLetterCheckerInterface):
    def check(self, party: Party) -> bool:
        name = party.name

        return name[0].upper() in 'А Б В Г Д Е Ё Ж З И Й К'.split()


class PartyFilterInterface(ABC):
    @abstractmethod
    def filter(self, parties: list[Party]) -> list[Party]:
        pass


class PartyFilter(PartyFilterInterface):
    def __init__(self, checker: FirstLetterCheckerInterface) -> None:
        self.__checker = checker

    def filter(self, parties: list[Party]) -> list[Party]:
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

class InputStringInterface(ABC):
    @abstractmethod
    def input(self) -> str:
        pass


class PartyTypeInput(InputStringInterface):
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


class PartyNameInput(InputStringInterface):
    def __init__(self, validator: PartyNameValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> str:
        while True:
            name = input("Введите название партии: ")

            try:
                return self.__validator.validate(name)
            except ValueError as error:
                print(error)


class InputIntInterface(ABC):
    @abstractmethod
    def input(self) -> int:
        pass

class DeputiesCountInput(InputIntInterface):
    def __init__(self, validator: CountValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> int:
        while True:
            try:
                value = int(input("Введите количество депутатов: "))
                return self.__validator.validate(value)
            except ValueError as error:
                print(error)


class AllocationAmountInput(InputIntInterface):
    def __init__(self, validator: CountValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> input:
        while True:
            try:
                value = input("Введите размер ассигнования: ")
                value = value.strip().replace(",", ".")
                amount = int(value)

                return self.__validator.validate(amount)
            except ValueError as error:
                print(error)

class PartyCreatorInterface(ABC):
    @abstractmethod
    def create(self, name: str, count_amount:int) -> RepresentativeParty | BudgetFundedParty:
        pass


class RepresentativePartyCreator(PartyCreatorInterface):
    def create(self,name: str,deputies_count: int) -> RepresentativeParty:
        party = RepresentativeParty(name,deputies_count)
        return party


class BudgetFundedPartyCreator(PartyCreatorInterface):
    def create(self,name: str,allocation_amount: int) -> BudgetFundedParty:
        party = BudgetFundedParty(name, allocation_amount)
        return party

class FormatterInterface(ABC):
    @abstractmethod
    def format(self, party:Party) -> str:
        pass


class PartyFormatter(FormatterInterface):
    def format(self, party: Party) -> str:
        if isinstance(party,RepresentativeParty):
            return f'Партия "{party.name}", количество депутатов: {party.deputies_count}'
        
        if isinstance(party,BudgetFundedParty):
            return f'Партия "{party.name}", ассигнование: {party.allocation_amount}'


class OutputInterface(ABC):
    @abstractmethod
    def write(self,message:str) -> None:
        pass


class ConsoleOutput(OutputInterface):
    def write(self, message: str) -> None:
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


class PartyInputScenario:
    def __init__(self,party_type_input: InputStringInterface,party_name_input: InputStringInterface,deputies_count_input: InputIntInterface,allocation_amount_input: InputIntInterface,representative_creator: PartyCreatorInterface,budget_creator: PartyCreatorInterface,registry: PartyWriterInterface | PartyReaderInterface) -> None:
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


class Task:
    def __init__(
        self,
        input_scenario: PartyInputScenario,
        registry: PartyRegist,
        party_filter: PartyFilter,
        printer: PartyPrinter,
    ) -> None:
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
