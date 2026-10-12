from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence



class PartyInterface(ABC):
    """Define access to a political party name."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the party name.

        Returns:
            The party name as a string.
        """
        pass


class RepresentativePartyInterface(ABC):
    """Define access to a party's deputy count."""

    @abstractmethod
    def get_deputies_count(self) -> int:
        """Return the number of deputies.

        Returns:
            The deputy count.
        """
        pass


class BudgetFundedPartyInterface(ABC):
    """Define access to a party's budget allocation."""

    @abstractmethod
    def get_allocation_amount(self) -> int:
        """Return the budget allocation amount.

        Returns:
            The allocation amount as an integer.
        """
        pass


class Party(PartyInterface):
    """Store the name of a political party."""

    def __init__(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        """Return the stored party name.

        Returns:
            The party name as provided to the constructor.
        """
        return self.__name


class RepresentativeParty(Party, RepresentativePartyInterface):
    """Store a representative party and its deputy count."""

    def __init__(self, name: str, deputies_count: int) -> None:
        super().__init__(name)
        self.__deputies_count = deputies_count

    def get_deputies_count(self) -> int:
        """Return the stored deputy count.

        Returns:
            The number of deputies.
        """
        return self.__deputies_count


class BudgetFundedParty(Party, BudgetFundedPartyInterface):
    """Store a budget-funded party and its allocation."""

    def __init__(self, name: str, allocation_amount: int) -> None:
        super().__init__(name)
        self.__allocation_amount = allocation_amount

    def get_allocation_amount(self) -> int:
        """Return the stored allocation amount.

        Returns:
            The budget allocation amount.
        """
        return self.__allocation_amount



class PartyWriterInterface(ABC):
    """Define the contract for adding parties to storage."""

    @abstractmethod
    def add_party(self, party: PartyInterface) -> None:
        """Add a party to storage.

        Args:
            party: The party to store.
        """
        pass


class PartyReaderInterface(ABC):
    """Define the contract for reading stored parties."""

    @abstractmethod
    def get_parties(self) -> list[PartyInterface]:
        """Return the stored parties.

        Returns:
            A list of stored parties.
        """
        pass


class PartyRegistry(PartyWriterInterface, PartyReaderInterface):
    """Store political parties in memory."""

    def __init__(self) -> None:
        self.__parties: list[PartyInterface] = []

    def add_party(self, party: PartyInterface) -> None:
        """Add a party to the registry.

        Args:
            party: The party object to add.

        Raises:
            TypeError: If the object does not implement PartyInterface.
        """
        if not isinstance(party, PartyInterface):
            raise TypeError("Можно добавлять только объекты PartyInterface")
        self.__parties.append(party)

    def get_parties(self) -> list[PartyInterface]:
        """Return all parties in the registry.

        Returns:
            A list containing the stored parties.

        Notes:
            A shallow copy of the internal list is returned.
        """
        return self.__parties.copy()



class FirstLetterCheckerInterface(ABC):
    """Define a rule for checking a party name."""

    @abstractmethod
    def check(self, party: PartyInterface) -> bool:
        """Check whether a party matches the initial-letter rule.

        Args:
            party: The party to check.

        Returns:
            True if the party matches; otherwise False.
        """
        pass


class RequiredFirstLetterChecker(FirstLetterCheckerInterface):
    """Check a party name against the allowed initial letters."""

    def check(self, party: PartyInterface) -> bool:
        """Check the first letter of a party name.

        Args:
            party: The party whose name is checked.

        Returns:
            True if the first letter is allowed; otherwise False.

        Notes:
            Allowed initials are Cyrillic letters from А through К, including Ё.
            Leading and trailing spaces are ignored; case does not matter.
            An empty or whitespace-only name returns False.
        """
        name = party.get_name().strip()
        return bool(name) and name[0].upper() in "АБВГДЕЁЖЗИЙК"


class PartyFilterInterface(ABC):
    """Define the contract for filtering parties."""

    @abstractmethod
    def filter(self, parties: list[PartyInterface]) -> list[PartyInterface]:
        """Filter a list of parties.

        Args:
            parties: The parties to evaluate.

        Returns:
            A list of parties satisfying the filter.
        """
        pass


class PartyFilter(PartyFilterInterface):
    """Select parties that satisfy an injected checker."""

    def __init__(self, checker: FirstLetterCheckerInterface) -> None:
        self.__checker = checker

    def filter(self, parties: list[PartyInterface]) -> list[PartyInterface]:
        """Select parties accepted by the configured checker.

        Args:
            parties: The parties to filter.

        Returns:
            A new list of accepted parties.

        Notes:
            The original order is preserved.
        """
        return [party for party in parties if self.__checker.check(party)]



class PartyNameValidatorInterface(ABC):
    """Define the contract for validating party names."""

    @abstractmethod
    def validate(self, name: str) -> str:
        """Validate a party name.

        Args:
            name: The name to validate.

        Returns:
            The validated name.
        """
        pass


class PartyNameValidator(PartyNameValidatorInterface):
    """Validate and normalize political party names."""

    def validate(self, name: str) -> str:
        """Validate and trim a party name.

        Args:
            name: The candidate party name.

        Returns:
            The name without surrounding whitespace.

        Raises:
            ValueError: If the name is empty or has no alphabetic characters.

        Notes:
            At least one alphabetic character is required.
        """
        name = name.strip()
        if not name:
            raise ValueError("Название партии не должно быть пустым")
        if not any(char.isalpha() for char in name):
            raise ValueError("Название партии должно содержать буквы")
        return name


class CountValidatorInterface(ABC):
    """Define the contract for validating integer amounts."""

    @abstractmethod
    def validate(self, count_amount: int) -> int:
        """Validate an integer value.

        Args:
            count_amount: The integer to validate.

        Returns:
            The validated integer.

        Notes:
            The accepted range depends on the implementation.
        """
        pass


class DeputiesCountValidator(CountValidatorInterface):
    """Validate the number of deputies in a party."""

    def validate(self, deputies_count: int) -> int:
        """Validate a deputy count.

        Args:
            deputies_count: The deputy count to validate.

        Returns:
            The validated deputy count.

        Raises:
            ValueError: If the count is negative.

        Notes:
            A count of zero is allowed.
        """
        if deputies_count < 0:
            raise ValueError("Количество депутатов не может быть меньше нуля")
        return deputies_count


class AllocationAmountValidator(CountValidatorInterface):
    """Validate a party's budget allocation amount."""

    def validate(self, allocation_amount: int) -> int:
        """Validate a budget allocation.

        Args:
            allocation_amount: The allocation amount to validate.

        Returns:
            The validated allocation amount.

        Raises:
            ValueError: If the amount is zero or negative.

        Notes:
            Only strictly positive integer amounts are accepted.
        """
        if allocation_amount <= 0:
            raise ValueError("Ассигнование должно быть больше нуля")
        return allocation_amount



class PartyTypeInputInterface(ABC):
    """Define the contract for reading a party type."""

    @abstractmethod
    def input(self) -> str:
        """Read a party type from the user.

        Returns:
            The selected party type or the stop command.

        Notes:
            The value "стоп" indicates that entry should end.
        """
        pass


class PartyTypeInput(PartyTypeInputInterface):
    """Prompt the user to select a party type."""

    def __init__(self, allowed_types: Sequence[str] = ("обычная", "бюджетная")) -> None:
        self.__allowed_types = tuple(allowed_types)

    def input(self) -> str:
        """Prompt until the user enters an allowed party type.

        Returns:
            The normalized party type or "стоп".

        Notes:
            Input is stripped of surrounding spaces and converted to lowercase.
            Allowed types are configured when the object is created.
            The command "стоп" ends data entry.
        """
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
    """Define the contract for reading a party name."""

    @abstractmethod
    def input(self) -> str:
        """Read a party name from the user.

        Returns:
            A validated party name.
        """
        pass


class PartyNameInput(PartyNameInputInterface):
    """Prompt the user for a validated party name."""

    def __init__(self, validator: PartyNameValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> str:
        """Read and validate a party name.

        Returns:
            A name accepted by the configured validator.

        Notes:
            The prompt is repeated after a ValueError from the validator.
        """
        while True:
            name = input("Введите название партии: ")
            try:
                return self.__validator.validate(name)
            except ValueError as error:
                print(error)


class DeputiesCountInputInterface(ABC):
    """Define the contract for reading a deputy count."""

    @abstractmethod
    def input(self) -> int:
        """Read a deputy count from the user.

        Returns:
            A validated integer deputy count.
        """
        pass


class DeputiesCountInput(DeputiesCountInputInterface):
    """Prompt the user for a validated deputy count."""

    def __init__(self, validator: CountValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> int:
        """Read and validate the number of deputies.

        Returns:
            An integer accepted by the configured validator.

        Notes:
            Invalid integers and validation errors trigger another prompt.
        """
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
    """Define the contract for reading a budget allocation."""

    @abstractmethod
    def input(self) -> int:
        """Read an allocation amount from the user.

        Returns:
            A validated integer allocation amount.
        """
        pass


class AllocationAmountInput(AllocationAmountInputInterface):
    """Prompt the user for a validated allocation amount."""

    def __init__(self, validator: CountValidatorInterface) -> None:
        self.__validator = validator

    def input(self) -> int:
        """Read and validate a budget allocation amount.

        Returns:
            An integer accepted by the configured validator.

        Notes:
            Only whole-number input is parsed; invalid input is requested again.
        """
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
    """Define the contract for creating representative parties."""

    @abstractmethod
    def create(self, name: str, deputies_count: int) -> RepresentativeParty:
        """Create a representative party.

        Args:
            name: The party name.
            deputies_count: The number of deputies.

        Returns:
            A newly created representative party.
        """
        pass


class RepresentativePartyCreator(RepresentativeCreatorInterface):
    """Create representative party objects."""

    def create(self, name: str, deputies_count: int) -> RepresentativeParty:
        """Construct a representative party.

        Args:
            name: The party name.
            deputies_count: The number of deputies.

        Returns:
            A new RepresentativeParty instance.
        """
        return RepresentativeParty(name, deputies_count)


class BudgetCreatorInterface(ABC):
    """Define the contract for creating budget-funded parties."""

    @abstractmethod
    def create(self, name: str, allocation_amount: int) -> BudgetFundedParty:
        """Create a budget-funded party.

        Args:
            name: The party name.
            allocation_amount: The budget allocation amount.

        Returns:
            A newly created budget-funded party.
        """
        pass


class BudgetFundedPartyCreator(BudgetCreatorInterface):
    """Create budget-funded party objects."""

    def create(self, name: str, allocation_amount: int) -> BudgetFundedParty:
        """Construct a budget-funded party.

        Args:
            name: The party name.
            allocation_amount: The budget allocation amount.

        Returns:
            A new BudgetFundedParty instance.
        """
        return BudgetFundedParty(name, allocation_amount)


class PartyCreationFlowInterface(ABC):
    """Define a workflow for creating a party."""

    @abstractmethod
    def create(self, name: str) -> PartyInterface:
        """Create a party using a configured workflow.

        Args:
            name: The party name.

        Returns:
            The created party.
        """
        pass


class RepresentativePartyCreationFlow(PartyCreationFlowInterface):
    """Coordinate creation of a representative party."""

    def __init__(
        self,
        deputies_input: DeputiesCountInputInterface,
        creator: RepresentativeCreatorInterface,
    ) -> None:
        self.__deputies_input = deputies_input
        self.__creator = creator

    def create(self, name: str) -> PartyInterface:
        """Read the deputy count and create a representative party.

        Args:
            name: The party name.

        Returns:
            The newly created representative party.
        """
        count = self.__deputies_input.input()
        return self.__creator.create(name, count)


class BudgetFundedPartyCreationFlow(PartyCreationFlowInterface):
    """Coordinate creation of a budget-funded party."""

    def __init__(
        self,
        allocation_input: AllocationAmountInputInterface,
        creator: BudgetCreatorInterface,
    ) -> None:
        self.__allocation_input = allocation_input
        self.__creator = creator

    def create(self, name: str) -> PartyInterface:
        """Read the allocation and create a budget-funded party.

        Args:
            name: The party name.

        Returns:
            The newly created budget-funded party.
        """
        amount = self.__allocation_input.input()
        return self.__creator.create(name, amount)



class FormatterInterface(ABC):
    """Define the contract for formatting a party as text."""

    @abstractmethod
    def format(self, party: PartyInterface) -> str:
        """Convert a party into display text.

        Args:
            party: The party to format.

        Returns:
            A formatted text description.
        """
        pass


class PartyTypeFormatterInterface(FormatterInterface):
    """Define a formatter that declares which parties it supports."""

    @abstractmethod
    def supports(self, party: PartyInterface) -> bool:
        """Check whether the formatter can handle a party.

        Args:
            party: The party to check.

        Returns:
            True if the formatter supports the party; otherwise False.
        """
        pass


class RepresentativePartyFormatter(PartyTypeFormatterInterface):
    """Format representative parties as text."""

    def supports(self, party: PartyInterface) -> bool:
        """Check whether this formatter supports a representative party.

        Args:
            party: The party to examine.

        Returns:
            True if the party implements RepresentativePartyInterface.
        """
        return isinstance(party, RepresentativePartyInterface)

    def format(self, party: PartyInterface) -> str:
        """Format the name and deputy count of a representative party.

        Args:
            party: The representative party to format.

        Returns:
            The formatted representative party description.

        Raises:
            TypeError: If the party does not implement RepresentativePartyInterface.
        """
        if not isinstance(party, RepresentativePartyInterface):
            raise TypeError("Форматтер ожидает представительную партию")
        return (
            f'Партия "{party.get_name()}", '
            f'количество депутатов: {party.get_deputies_count()}'
        )


class BudgetFundedPartyFormatter(PartyTypeFormatterInterface):
    """Format budget-funded parties as text."""

    def supports(self, party: PartyInterface) -> bool:
        """Check whether this formatter supports a budget-funded party.

        Args:
            party: The party to examine.

        Returns:
            True if the party implements BudgetFundedPartyInterface.
        """
        return isinstance(party, BudgetFundedPartyInterface)

    def format(self, party: PartyInterface) -> str:
        """Format the name and allocation of a budget-funded party.

        Args:
            party: The budget-funded party to format.

        Returns:
            The formatted budget-funded party description.

        Raises:
            TypeError: If the party does not implement BudgetFundedPartyInterface.
        """
        if not isinstance(party, BudgetFundedPartyInterface):
            raise TypeError("Форматтер ожидает бюджетную партию")
        return (
            f'Партия "{party.get_name()}", '
            f'ассигнование: {party.get_allocation_amount()}'
        )


class PartyFormatter(FormatterInterface):
    """Delegate party formatting to a compatible formatter."""

    def __init__(self, formatters: Sequence[PartyTypeFormatterInterface]) -> None:
        self.__formatters = tuple(formatters)

    def format(self, party: PartyInterface) -> str:
        """Format a party using the first compatible formatter.

        Args:
            party: The party to format.

        Returns:
            The formatted party description.

        Raises:
            ValueError: If no registered formatter supports the party.

        Notes:
            Formatters are evaluated in the order in which they were provided.
        """
        for formatter in self.__formatters:
            if formatter.supports(party):
                return formatter.format(party)
        raise ValueError(f'Нет форматтера для партии "{party.get_name()}"')


class OutputInterface(ABC):
    """Define the contract for writing a text message."""

    @abstractmethod
    def write(self, message: str) -> None:
        """Write a text message.

        Args:
            message: The text to write.
        """
        pass


class ConsoleOutput(OutputInterface):
    """Write text messages to standard output."""

    def write(self, message: str) -> None:
        """Print a text message to standard output.

        Args:
            message: The text to display.
        """
        print(message)


class PrinterInterface(ABC):
    """Define the contract for printing a collection of parties."""

    @abstractmethod
    def print(self, parties: list[PartyInterface]) -> None:
        """Print a collection of parties.

        Args:
            parties: The parties to print.
        """
        pass


class PartyPrinter(PrinterInterface):
    """Coordinate formatting and output of a collection of parties."""

    def __init__(self, formatter: FormatterInterface, output: OutputInterface) -> None:
        self.__formatter = formatter
        self.__output = output

    def print(self, parties: list[PartyInterface]) -> None:
        """Format and output each party in the collection.

        Args:
            parties: The parties to print.

        Notes:
            If the list is empty, a message is displayed instead.
        """
        if not parties:
            self.__output.write("Нет партий, удовлетворяющих условию.")
            return
        for party in parties:
            self.__output.write(self.__formatter.format(party))



class PartyInputScenarioInterface(ABC):
    """Define the contract for running party entry."""

    @abstractmethod
    def run(self) -> None:
        """Run the party entry process."""
        pass


class PartyInputScenario(PartyInputScenarioInterface):
    """Coordinate user input, party creation, and storage."""

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
        """Read party data and store the created parties.

        Raises:
            ValueError: If the selected party type has no registered creation flow.

        Notes:
            The command "стоп" ends the input loop.
        """
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
    """Define the contract for running the application task."""

    @abstractmethod
    def run(self) -> None:
        """Run the application task."""
        pass


class Task(TaskInterface):
    """Coordinate input, filtering, and printing of parties."""

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
        """Collect, filter, and print parties.

        Notes:
            Parties are printed only after the input scenario finishes.
        """
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
