import unittest
from unittest.mock import MagicMock, patch, call

from Practice import *


class TestParty(unittest.TestCase):

    def test_party_name(self):
        party = Party("Альфа")

        self.assertEqual(party.get_name(), "Альфа")

    def test_representative_party(self):
        party = RepresentativeParty("Альфа", 10)

        self.assertEqual(party.get_name(), "Альфа")
        self.assertEqual(party.deputies_count, 10)

    def test_budget_party(self):
        party = BudgetFundedParty("Бета", 5000)

        self.assertEqual(party.get_name(), "Бета")
        self.assertEqual(party.allocation_amount, 5000)


class TestPartyNameValidator(unittest.TestCase):

    def test_valid_name(self):
        validator = PartyNameValidator()

        result = validator.validate("Альфа")

        self.assertEqual(result, "Альфа")

    def test_empty_name(self):
        validator = PartyNameValidator()

        with self.assertRaises(ValueError):
            validator.validate("")

    def test_name_without_letters(self):
        validator = PartyNameValidator()

        with self.assertRaises(ValueError):
            validator.validate("1234")

    def test_name_strips_spaces(self):
        validator = PartyNameValidator()

        result = validator.validate("  Альфа  ")

        self.assertEqual(result, "Альфа")


class TestDeputiesCountValidator(unittest.TestCase):

    def test_valid_deputies(self):
        validator = DeputiesCountValidator()

        result = validator.validate(10)

        self.assertEqual(result, 10)

    def test_zero_deputies(self):
        validator = DeputiesCountValidator()

        result = validator.validate(0)

        self.assertEqual(result, 0)

    def test_negative_deputies(self):
        validator = DeputiesCountValidator()

        with self.assertRaises(ValueError):
            validator.validate(-1)


class TestAllocationAmountValidator(unittest.TestCase):

    def test_valid_allocation(self):
        validator = AllocationAmountValidator()

        result = validator.validate(5000)

        self.assertEqual(result, 5000)

    def test_zero_allocation(self):
        validator = AllocationAmountValidator()

        with self.assertRaises(ValueError):
            validator.validate(0)

    def test_negative_allocation(self):
        validator = AllocationAmountValidator()

        with self.assertRaises(ValueError):
            validator.validate(-100)


class TestPartyRegistry(unittest.TestCase):

    def test_add_party(self):
        registry = PartyRegistry()
        party = RepresentativeParty("Альфа", 10)

        registry.add_party(party)

        self.assertEqual(registry.get_parties(), [party])

    def test_add_several_parties(self):
        registry = PartyRegistry()

        party1 = RepresentativeParty("Альфа", 10)
        party2 = BudgetFundedParty("Бета", 5000)

        registry.add_party(party1)
        registry.add_party(party2)

        self.assertEqual(
            registry.get_parties(),
            [party1, party2]
        )

    def test_add_wrong_object(self):
        registry = PartyRegistry()

        with self.assertRaises(TypeError):
            registry.add_party("Альфа")

    def test_empty_registry(self):
        registry = PartyRegistry()

        self.assertEqual(registry.get_parties(), [])


class TestRequiredFirstLetterChecker(unittest.TestCase):

    def test_required_letter(self):
        checker = RequiredFirstLetterChecker()
        party = Party("Альфа")

        result = checker.check(party)

        self.assertTrue(result)

    def test_wrong_letter(self):
        checker = RequiredFirstLetterChecker()
        party = Party("Яблоко")

        result = checker.check(party)

        self.assertFalse(result)

    def test_lowercase_letter(self):
        checker = RequiredFirstLetterChecker()
        party = Party("бета")

        result = checker.check(party)

        self.assertTrue(result)


class TestPartyFilter(unittest.TestCase):

    def test_filter(self):
        checker = MagicMock(spec=FirstLetterCheckerInterface)

        party1 = Party("Альфа")
        party2 = Party("Яблоко")

        checker.check.side_effect = [True, False]

        party_filter = PartyFilter(checker)

        result = party_filter.filter([party1, party2])

        self.assertEqual(result, [party1])

        checker.check.assert_has_calls([
            call(party1),
            call(party2)
        ])


class TestPartyTypeInput(unittest.TestCase):

    @patch("builtins.input")
    def test_correct_party_type(self, mock_input):
        mock_input.return_value = "обычная"

        party_input = PartyTypeInput()

        result = party_input.input()

        self.assertEqual(result, "обычная")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_wrong_then_correct_party_type(
        self,
        mock_print,
        mock_input
    ):
        mock_input.side_effect = [
            "неправильно",
            "бюджетная"
        ]

        party_input = PartyTypeInput()

        result = party_input.input()

        self.assertEqual(result, "бюджетная")


class TestPartyNameInput(unittest.TestCase):

    @patch("builtins.input")
    def test_name_input(self, mock_input):
        validator = MagicMock(
            spec=PartyNameValidatorInterface
        )

        validator.validate.return_value = "Альфа"
        mock_input.return_value = "Альфа"

        party_input = PartyNameInput(validator)

        result = party_input.input()

        self.assertEqual(result, "Альфа")
        validator.validate.assert_called_once_with("Альфа")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_wrong_then_correct_name(
        self,
        mock_print,
        mock_input
    ):
        validator = MagicMock(
            spec=PartyNameValidatorInterface
        )

        mock_input.side_effect = ["123", "Альфа"]

        validator.validate.side_effect = [
            ValueError("Ошибка"),
            "Альфа"
        ]

        party_input = PartyNameInput(validator)

        result = party_input.input()

        self.assertEqual(result, "Альфа")
        self.assertEqual(
            validator.validate.call_count,
            2
        )


class TestDeputiesCountInput(unittest.TestCase):

    @patch("builtins.input")
    def test_deputies_input(self, mock_input):
        validator = MagicMock(
            spec=CountValidatorInterface
        )

        validator.validate.return_value = 10
        mock_input.return_value = "10"

        deputies_input = DeputiesCountInput(
            validator
        )

        result = deputies_input.input()

        self.assertEqual(result, 10)
        validator.validate.assert_called_once_with(10)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_wrong_then_correct_deputies(
        self,
        mock_print,
        mock_input
    ):
        validator = MagicMock(
            spec=CountValidatorInterface
        )

        mock_input.side_effect = ["abc", "10"]
        validator.validate.return_value = 10

        deputies_input = DeputiesCountInput(
            validator
        )

        result = deputies_input.input()

        self.assertEqual(result, 10)
        validator.validate.assert_called_once_with(10)


class TestAllocationAmountInput(unittest.TestCase):

    @patch("builtins.input")
    def test_allocation_input(self, mock_input):
        validator = MagicMock(
            spec=CountValidatorInterface
        )

        mock_input.return_value = "5000"
        validator.validate.return_value = 5000

        allocation_input = AllocationAmountInput(
            validator
        )

        result = allocation_input.input()

        self.assertEqual(result, 5000)
        validator.validate.assert_called_once_with(5000)


class TestRepresentativePartyCreator(unittest.TestCase):

    def test_create(self):
        creator = RepresentativePartyCreator()

        party = creator.create("Альфа", 10)

        self.assertIsInstance(
            party,
            RepresentativeParty
        )
        self.assertEqual(
            party.get_name(),
            "Альфа"
        )
        self.assertEqual(
            party.deputies_count,
            10
        )


class TestBudgetFundedPartyCreator(unittest.TestCase):

    def test_create(self):
        creator = BudgetFundedPartyCreator()

        party = creator.create("Бета", 5000)

        self.assertIsInstance(
            party,
            BudgetFundedParty
        )
        self.assertEqual(
            party.get_name(),
            "Бета"
        )
        self.assertEqual(
            party.allocation_amount,
            5000
        )


class TestPartyFormatter(unittest.TestCase):

    def test_representative_format(self):
        formatter = PartyFormatter()
        party = RepresentativeParty(
            "Альфа",
            10
        )

        result = formatter.format(party)

        self.assertEqual(
            result,
            'Партия "Альфа", количество депутатов: 10'
        )

    def test_budget_format(self):
        formatter = PartyFormatter()
        party = BudgetFundedParty(
            "Бета",
            5000
        )

        result = formatter.format(party)

        self.assertEqual(
            result,
            'Партия "Бета", ассигнование: 5000'
        )


class TestConsoleOutput(unittest.TestCase):

    @patch("builtins.print")
    def test_write(self, mock_print):
        output = ConsoleOutput()

        output.write("Привет")

        mock_print.assert_called_once_with(
            "Привет"
        )


class TestPartyPrinter(unittest.TestCase):

    def test_print(self):
        formatter = MagicMock(
            spec=FormatterInterface
        )
        output = MagicMock(
            spec=OutputInterface
        )

        party1 = Party("Альфа")
        party2 = Party("Бета")

        formatter.format.side_effect = [
            "Партия Альфа",
            "Партия Бета"
        ]

        printer = PartyPrinter(
            formatter,
            output
        )

        printer.print([party1, party2])

        formatter.format.assert_has_calls([
            call(party1),
            call(party2)
        ])

        output.write.assert_has_calls([
            call("Партия Альфа"),
            call("Партия Бета")
        ])


class TestPartyInputScenario(unittest.TestCase):

    def test_representative_party_input(self):
        type_input = MagicMock(
            spec=PartyTypeInputInterface
        )
        name_input = MagicMock(
            spec=PartyNameInputInterface
        )
        deputies_input = MagicMock(
            spec=DeputiesCountInputInterface
        )
        allocation_input = MagicMock(
            spec=AllocationAmountInputInterface
        )

        representative_creator = MagicMock(
            spec=RepresentativeCreatorInterface
        )
        budget_creator = MagicMock(
            spec=BudgetCreatorInterface
        )
        registry = MagicMock(
            spec=PartyWriterInterface
        )

        type_input.input.side_effect = [
            "обычная",
            "стоп"
        ]
        name_input.input.return_value = "Альфа"
        deputies_input.input.return_value = 10

        party = RepresentativeParty(
            "Альфа",
            10
        )

        representative_creator.create.return_value = party

        scenario = PartyInputScenario(
            type_input,
            name_input,
            deputies_input,
            allocation_input,
            representative_creator,
            budget_creator,
            registry
        )

        scenario.run()

        representative_creator.create.assert_called_once_with(
            name="Альфа",
            deputies_count=10
        )

        registry.add_party.assert_called_once_with(
            party
        )


class TestTask(unittest.TestCase):

    def test_run(self):
        scenario = MagicMock(
            spec=PartyInputScenarioInterface
        )
        registry = MagicMock(
            spec=PartyReaderInterface
        )
        party_filter = MagicMock(
            spec=PartyFilterInterface
        )
        printer = MagicMock(
            spec=PrinterInterface
        )

        parties = [
            Party("Альфа"),
            Party("Яблоко")
        ]

        filtered = [
            parties[0]
        ]

        registry.get_parties.return_value = parties
        party_filter.filter.return_value = filtered

        task = Task(
            scenario,
            registry,
            party_filter,
            printer
        )

        task.run()

        scenario.run.assert_called_once()
        registry.get_parties.assert_called_once()

        party_filter.filter.assert_called_once_with(
            parties=parties
        )

        printer.print.assert_called_once_with(
            filtered
        )


if __name__ == "__main__":
    unittest.main()