import unittest
from unittest.mock import MagicMock, call, patch

from Practice import *

class TestParties(unittest.TestCase):
    def test_base_party(self):
        self.assertEqual(Party("Альфа").get_name(), "Альфа")

    def test_representative(self):
        party = RepresentativeParty("Альфа", 10)
        self.assertEqual(party.get_name(), "Альфа")
        self.assertEqual(party.get_deputies_count(), 10)

    def test_budget(self):
        party = BudgetFundedParty("Бета", 5000)
        self.assertEqual(party.get_name(), "Бета")
        self.assertEqual(party.get_allocation_amount(), 5000)


class TestValidators(unittest.TestCase):
    def test_name(self):
        validator = PartyNameValidator()
        self.assertEqual(validator.validate("  Альфа  "), "Альфа")
        for value in ("", "  ", "1234"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validator.validate(value)

    def test_deputies(self):
        validator = DeputiesCountValidator()
        self.assertEqual(validator.validate(0), 0)
        self.assertEqual(validator.validate(10), 10)
        with self.assertRaises(ValueError):
            validator.validate(-1)

    def test_allocation(self):
        validator = AllocationAmountValidator()
        self.assertEqual(validator.validate(5000), 5000)
        for value in (0, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validator.validate(value)


class TestRegistry(unittest.TestCase):
    def test_add_and_get_copy(self):
        registry = PartyRegistry()
        first = Party("Альфа")
        second = Party("Бета")
        registry.add_party(first)
        registry.add_party(second)
        self.assertEqual(registry.get_parties(), [first, second])
        registry.get_parties().clear()
        self.assertEqual(registry.get_parties(), [first, second])

    def test_wrong_object(self):
        with self.assertRaises(TypeError):
            PartyRegistry().add_party("Альфа")


class TestCheckerAndFilter(unittest.TestCase):
    def test_checker(self):
        checker = RequiredFirstLetterChecker()
        for name in ("Альфа", "кедр", "Ёж"):
            with self.subTest(name=name):
                self.assertTrue(checker.check(Party(name)))
        for name in ("Лето", "Яблоко", "", "   "):
            with self.subTest(name=name):
                self.assertFalse(checker.check(Party(name)))

    def test_filter_mock(self):
        checker = MagicMock(spec=FirstLetterCheckerInterface)
        checker.check.side_effect = [True, False]
        first, second = Party("Альфа"), Party("Яблоко")
        result = PartyFilter(checker).filter([first, second])
        self.assertEqual(result, [first])
        checker.check.assert_has_calls([call(first), call(second)])

class TestInputs(unittest.TestCase):
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["неизвестная", " БЮДЖЕТНАЯ "])
    def test_party_type(self, mock_input, mock_print):
        self.assertEqual(PartyTypeInput().input(), "бюджетная")
        self.assertEqual(mock_input.call_count, 2)

    @patch("builtins.input", return_value="стоп")
    def test_stop(self, mock_input):
        with patch("builtins.print"):
            self.assertEqual(PartyTypeInput().input(), "стоп")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["неправильно", "Альфа"])
    def test_name_retry(self, mock_input, mock_print):
        validator = MagicMock(spec=PartyNameValidatorInterface)
        validator.validate.side_effect = [ValueError("Ошибка"), "Альфа"]
        self.assertEqual(PartyNameInput(validator).input(), "Альфа")
        self.assertEqual(validator.validate.call_count, 2)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["не число", "-1", "10"])
    def test_deputies_retry(self, mock_input, mock_print):
        validator = MagicMock(spec=CountValidatorInterface)
        validator.validate.side_effect = [ValueError("Отрицательно"), 10]
        self.assertEqual(DeputiesCountInput(validator).input(), 10)
        self.assertEqual(validator.validate.call_count, 2)
        validator.validate.assert_has_calls([call(-1), call(10)])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["10,5", "0", "5000"])
    def test_allocation_retry(self, mock_input, mock_print):
        validator = MagicMock(spec=CountValidatorInterface)
        validator.validate.side_effect = [ValueError("Ноль"), 5000]
        self.assertEqual(AllocationAmountInput(validator).input(), 5000)
        validator.validate.assert_has_calls([call(0), call(5000)])


class TestCreators(unittest.TestCase):
    def test_representative_creator(self):
        party = RepresentativePartyCreator().create("Альфа", 10)
        self.assertIsInstance(party, RepresentativeParty)
        self.assertEqual(party.get_deputies_count(), 10)

    def test_budget_creator(self):
        party = BudgetFundedPartyCreator().create("Бета", 5000)
        self.assertIsInstance(party, BudgetFundedParty)
        self.assertEqual(party.get_allocation_amount(), 5000)

    def test_representative_flow(self):
        inp = MagicMock(spec=DeputiesCountInputInterface)
        creator = MagicMock(spec=RepresentativeCreatorInterface)
        inp.input.return_value = 10
        party = RepresentativeParty("Альфа", 10)
        creator.create.return_value = party
        result = RepresentativePartyCreationFlow(inp, creator).create("Альфа")
        self.assertIs(result, party)
        creator.create.assert_called_once_with("Альфа", 10)

    def test_budget_flow(self):
        inp = MagicMock(spec=AllocationAmountInputInterface)
        creator = MagicMock(spec=BudgetCreatorInterface)
        inp.input.return_value = 5000
        party = BudgetFundedParty("Бета", 5000)
        creator.create.return_value = party
        result = BudgetFundedPartyCreationFlow(inp, creator).create("Бета")
        self.assertIs(result, party)
        creator.create.assert_called_once_with("Бета", 5000)


class TestFormatters(unittest.TestCase):
    def test_representative_formatter(self):
        formatter = RepresentativePartyFormatter()
        party = RepresentativeParty("Альфа", 10)
        self.assertTrue(formatter.supports(party))
        self.assertFalse(formatter.supports(BudgetFundedParty("Бета", 1)))
        self.assertEqual(formatter.format(party), 'Партия "Альфа", количество депутатов: 10')
        with self.assertRaises(TypeError):
            formatter.format(Party("Бета"))

    def test_budget_formatter(self):
        formatter = BudgetFundedPartyFormatter()
        party = BudgetFundedParty("Бета", 5000)
        self.assertTrue(formatter.supports(party))
        self.assertFalse(formatter.supports(RepresentativeParty("Альфа", 1)))
        self.assertEqual(formatter.format(party), 'Партия "Бета", ассигнование: 5000')
        with self.assertRaises(TypeError):
            formatter.format(Party("Альфа"))

    def test_aggregate_formatter(self):
        rep = MagicMock(spec=PartyTypeFormatterInterface)
        budget = MagicMock(spec=PartyTypeFormatterInterface)
        party = Party("Альфа")
        rep.supports.return_value = False
        budget.supports.return_value = True
        budget.format.return_value = "Готово"
        self.assertEqual(PartyFormatter([rep, budget]).format(party), "Готово")
        rep.format.assert_not_called()
        budget.format.assert_called_once_with(party)

    def test_no_formatter(self):
        with self.assertRaises(ValueError):
            PartyFormatter([]).format(Party("Альфа"))


class TestOutput(unittest.TestCase):
    @patch("builtins.print")
    def test_console(self, mock_print):
        ConsoleOutput().write("Привет")
        mock_print.assert_called_once_with("Привет")

    def test_printer(self):
        formatter = MagicMock(spec=FormatterInterface)
        output = MagicMock(spec=OutputInterface)
        party = Party("Альфа")
        formatter.format.return_value = "Партия Альфа"
        PartyPrinter(formatter, output).print([party])
        formatter.format.assert_called_once_with(party)
        output.write.assert_called_once_with("Партия Альфа")

    def test_printer_empty(self):
        formatter = MagicMock(spec=FormatterInterface)
        output = MagicMock(spec=OutputInterface)
        PartyPrinter(formatter, output).print([])
        formatter.format.assert_not_called()
        output.write.assert_called_once_with("Нет партий, удовлетворяющих условию.")


class TestScenarioAndTask(unittest.TestCase):
    def test_scenario(self):
        type_input = MagicMock(spec=PartyTypeInputInterface)
        name_input = MagicMock(spec=PartyNameInputInterface)
        registry = MagicMock(spec=PartyWriterInterface)
        rep_flow = MagicMock(spec=PartyCreationFlowInterface)
        budget_flow = MagicMock(spec=PartyCreationFlowInterface)
        type_input.input.side_effect = ["обычная", "бюджетная", "стоп"]
        name_input.input.side_effect = ["Альфа", "Бета"]
        rep = RepresentativeParty("Альфа", 10)
        budget = BudgetFundedParty("Бета", 5000)
        rep_flow.create.return_value = rep
        budget_flow.create.return_value = budget
        scenario = PartyInputScenario(
            type_input, name_input, {"обычная": rep_flow, "бюджетная": budget_flow}, registry
        )
        scenario.run()
        rep_flow.create.assert_called_once_with("Альфа")
        budget_flow.create.assert_called_once_with("Бета")
        registry.add_party.assert_has_calls([call(rep), call(budget)])
        self.assertEqual(registry.add_party.call_count, 2)

    def test_scenario_unknown(self):
        type_input = MagicMock(spec=PartyTypeInputInterface)
        type_input.input.return_value = "другой"
        name_input = MagicMock(spec=PartyNameInputInterface)
        registry = MagicMock(spec=PartyWriterInterface)
        with self.assertRaises(ValueError):
            PartyInputScenario(type_input, name_input, {}, registry).run()
        name_input.input.assert_not_called()

    def test_task(self):
        scenario = MagicMock(spec=PartyInputScenarioInterface)
        registry = MagicMock(spec=PartyReaderInterface)
        party_filter = MagicMock(spec=PartyFilterInterface)
        printer = MagicMock(spec=PrinterInterface)
        parties = [Party("Альфа"), Party("Молоко")]
        registry.get_parties.return_value = parties
        party_filter.filter.return_value = [parties[0]]
        Task(scenario, registry, party_filter, printer).run()
        scenario.run.assert_called_once_with()
        registry.get_parties.assert_called_once_with()
        party_filter.filter.assert_called_once_with(parties)
        printer.print.assert_called_once_with([parties[0]])


if __name__ == "__main__":
    unittest.main()
