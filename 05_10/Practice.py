
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence


class PartyInterface(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass


class RepresentativePartyInterface(ABC):

    @abstractmethod
    def get_deputies_count(self) -> int:
        pass


class BudgetFundedPartyInterface(ABC):

    @abstractmethod
    def get_allocation_amount(self) -> int:
        pass


class Party(PartyInterface):

    def __init__(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name


class RepresentativeParty(Party, RepresentativePartyInterface):

    def __init__(self, name: str, deputies_count: int) -> None:
        super().__init__(name)
        self.__deputies_count = deputies_count

    def get_deputies_count(self) -> int:
        return self.__deputies_count


class BudgetFundedParty(Party, BudgetFundedPartyInterface):

    def __init__(self, name: str, allocation_amount: int) -> None:
        super().__init__(name)
        self.__allocation_amount = allocation_amount

    def get_allocation_amount(self) -> int:
        return self.__allocation_amount


class PartyWriterInterface(ABC):

    @abstractmethod
    def add_party(self, party: PartyInterface) -> None:
        pass


class PartyReaderInterface(ABC):

    @abstractmethod
    def get_parties(self) -> list[PartyInterface]:
        pass


class PartyRegistry(PartyWriterInterface, PartyReaderInterface):

    def __init__(self) -> None:
        self.__parties: list[PartyInterface] = []

    def add_party(self, party: PartyInterface) -> None:
        if not isinstance(party, PartyInterface):
            raise TypeError("Можно добавлять только объекты PartyInterface")
        self.__parties.append(party)

    def get_parties(self) -> list[PartyInterface]:
        return self.__parties.copy()


class FirstLetterCheckerInterface(ABC):

    @abstractmethod
    def check(self, party: PartyInterface) -> bool:
        pass


class RequiredFirstLetterChecker(FirstLetterCheckerInterface):

    def check(self, party: PartyInterface) -> bool:
        name = party.get_name().strip()
        return bool(name) and name[0].upper() in "АБВГДЕЁЖЗИЙК"


class PartyFilterInterface(ABC):

    @abstractmethod
    def filter(self, parties: list[PartyInterface]) -> list[PartyInterface]:
        pass


class PartyFilter(PartyFilterInterface):

    def __init__(self, checker: FirstLetterCheckerInterface) -> None:
        self.__checker = checker

    def filter(self, parties: list[PartyInterface]) -> list[PartyInterface]:
        return [party for party in parties if self.__checker.check(party)]


class PartyNameValidatorInterface(ABC):

    @abstractmethod
    def validate(self, name: str) -> str:
        pass


class PartyNameValidator(PartyNameValidatorInterface):

    def validate(self, name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Название партии не должно быть пустым")
        if not any(char.isalpha() for char in name):
            raise ValueError("Название партии должно содержать буквы")
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

    def __init__(self, allowed_types: Sequence[str] = ("обычная", "бюджетная")) -> None:
        self.__allowed_types = tuple(allowed_types)

    def input(self) -> str:
        while True:
            print()
            for party_type in self.__allowed_types:
                print(f'Введите "{party_type}" для добавления партии этого типа')
            print('Введите "стоп" для завершения')
            party_type = input("Выберите тип партии: ").strip().lower()
            if party_type == "стоп" or party_type in self.__allowed_types:
                return party_type
            print("Неверный тип партии. Повторите ввод.")


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
                count = int(input("Введите количество депутатов: ").strip())
            except ValueError:
                print("Введите целое число.")
                continue
            try:
                return self.__validator.validate(count)
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
                amount = int(input("Введите размер ассигнования: ").strip())
            except ValueError:
                print("Введите целое число.")
                continue
            try:
                return self.__validator.validate(amount)
            except ValueError as error:
                print(error)



class RepresentativeCreatorInterface(ABC):

    @abstractmethod
    def create(self, name: str, deputies_count: int) -> RepresentativeParty:
        pass


class RepresentativePartyCreator(RepresentativeCreatorInterface):

    def create(self, name: str, deputies_count: int) -> RepresentativeParty:
        return RepresentativeParty(name, deputies_count)


class BudgetCreatorInterface(ABC):

    @abstractmethod
    def create(self, name: str, allocation_amount: int) -> BudgetFundedParty:
        pass


class BudgetFundedPartyCreator(BudgetCreatorInterface):

    def create(self, name: str, allocation_amount: int) -> BudgetFundedParty:
        return BudgetFundedParty(name, allocation_amount)


class PartyCreationFlowInterface(ABC):

    @abstractmethod
    def create(self, name: str) -> PartyInterface:
        pass


class RepresentativePartyCreationFlow(PartyCreationFlowInterface):

    def __init__(
        self,
        deputies_input: DeputiesCountInputInterface,
        creator: RepresentativeCreatorInterface,
    ) -> None:
        self.__deputies_input = deputies_input
        self.__creator = creator

    def create(self, name: str) -> PartyInterface:
        count = self.__deputies_input.input()
        return self.__creator.create(name, count)


class BudgetFundedPartyCreationFlow(PartyCreationFlowInterface):

    def __init__(
        self,
        allocation_input: AllocationAmountInputInterface,
        creator: BudgetCreatorInterface,
    ) -> None:
        self.__allocation_input = allocation_input
        self.__creator = creator

    def create(self, name: str) -> PartyInterface:
        amount = self.__allocation_input.input()
        return self.__creator.create(name, amount)



class FormatterInterface(ABC):

    @abstractmethod
    def format(self, party: PartyInterface) -> str:
        pass


class PartyTypeFormatterInterface(FormatterInterface):

    @abstractmethod
    def supports(self, party: PartyInterface) -> bool:
        pass


class RepresentativePartyFormatter(PartyTypeFormatterInterface):

    def supports(self, party: PartyInterface) -> bool:
        return isinstance(party, RepresentativePartyInterface)

    def format(self, party: PartyInterface) -> str:
        if not isinstance(party, RepresentativePartyInterface):
            raise TypeError("Форматтер ожидает представительную партию")
        return (
            f'Партия "{party.get_name()}", '
            f'количество депутатов: {party.get_deputies_count()}'
        )


class BudgetFundedPartyFormatter(PartyTypeFormatterInterface):

    def supports(self, party: PartyInterface) -> bool:
        return isinstance(party, BudgetFundedPartyInterface)

    def format(self, party: PartyInterface) -> str:
        if not isinstance(party, BudgetFundedPartyInterface):
            raise TypeError("Форматтер ожидает бюджетную партию")
        return (
            f'Партия "{party.get_name()}", '
            f'ассигнование: {party.get_allocation_amount()}'
        )


class PartyFormatter(FormatterInterface):

    def __init__(self, formatters: Sequence[PartyTypeFormatterInterface]) -> None:
        self.__formatters = tuple(formatters)

    def format(self, party: PartyInterface) -> str:
        for formatter in self.__formatters:
            if formatter.supports(party):
                return formatter.format(party)
        raise ValueError(f'Нет форматтера для партии "{party.get_name()}"')


class OutputInterface(ABC):

    @abstractmethod
    def write(self, message: str) -> None:
        pass


class ConsoleOutput(OutputInterface):

    def write(self, message: str) -> None:
        print(message)


class PrinterInterface(ABC):

    @abstractmethod
    def print(self, parties: list[PartyInterface]) -> None:
        pass


class PartyPrinter(PrinterInterface):

    def __init__(self, formatter: FormatterInterface, output: OutputInterface) -> None:
        self.__formatter = formatter
        self.__output = output

    def print(self, parties: list[PartyInterface]) -> None:
        if not parties:
            self.__output.write("Нет партий, удовлетворяющих условию.")
            return
        for party in parties:
            self.__output.write(self.__formatter.format(party))


class PartyInputScenarioInterface(ABC):

    @abstractmethod
    def run(self) -> None:
        pass


class PartyInputScenario(PartyInputScenarioInterface):

    def __init__(
        self,
        party_type_input: PartyTypeInputInterface,
        party_name_input: PartyNameInputInterface,
        creation_flows: Mapping[str, PartyCreationFlowInterface],
        registry: PartyWriterInterface,
    ) -> None:
        self.__party_type_input = party_type_input
        self.__party_name_input = party_name_input
        self.__creation_flows = dict(creation_flows)
        self.__registry = registry

    def run(self) -> None:
        while True:
            party_type = self.__party_type_input.input()
            if party_type == "стоп":
                return
            creation_flow = self.__creation_flows.get(party_type)
            if creation_flow is None:
                raise ValueError(f"Неизвестный тип партии: {party_type}")
            name = self.__party_name_input.input()
            party = creation_flow.create(name)
            self.__registry.add_party(party)


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
    ) -> None:
        self.__input_scenario = input_scenario
        self.__registry = registry
        self.__party_filter = party_filter
        self.__printer = printer

    def run(self) -> None:
        self.__input_scenario.run()
        parties = self.__registry.get_parties()
        filtered_parties = self.__party_filter.filter(parties)
        self.__printer.print(filtered_parties)


if __name__ == "__main__":
    name_validator = PartyNameValidator()
    deputies_validator = DeputiesCountValidator()
    allocation_validator = AllocationAmountValidator()

    type_input = PartyTypeInput(("обычная", "бюджетная"))
    name_input = PartyNameInput(name_validator)
    deputies_input = DeputiesCountInput(deputies_validator)
    allocation_input = AllocationAmountInput(allocation_validator)

    representative_flow = RepresentativePartyCreationFlow(
        deputies_input, RepresentativePartyCreator()
    )
    budget_flow = BudgetFundedPartyCreationFlow(
        allocation_input, BudgetFundedPartyCreator()
    )

    registry = PartyRegistry()
    scenario = PartyInputScenario(
        party_type_input=type_input,
        party_name_input=name_input,
        creation_flows={
            "обычная": representative_flow,
            "бюджетная": budget_flow,
        },
        registry=registry,
    )

    formatter = PartyFormatter([
        RepresentativePartyFormatter(),
        BudgetFundedPartyFormatter(),
    ])
    printer = PartyPrinter(formatter, ConsoleOutput())
    party_filter = PartyFilter(RequiredFirstLetterChecker())
    task = Task(scenario, registry, party_filter, printer)
    task.run()
