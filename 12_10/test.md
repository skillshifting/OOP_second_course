**Unit-тест** — короткая автоматическая проверка одного поведения. В типовом тесте есть три этапа:

1. **Arrange (подготовка):** создать объект, входные данные и mock-зависимости.
2. **Act (действие):** вызвать проверяемый метод.
3. **Assert (проверка):** сравнить результат, проверить исключение или вызовы зависимостей.

Например, в `test_representative` подготовка — создание партии, действие — вызов методов `get_name()` и `get_deputies_count()`, проверка — две инструкции `assertEqual`.

### Понятия, которые встретятся ниже

| Термин | Объяснение |
|---|---|
| `unittest.TestCase` | Базовый класс, дающий тестовые утверждения `self.assert...` и запуск тестов через unittest. |
| `test_*` | Префикс названия метода; стандартный загрузчик тестов распознаёт эти методы. |
| `assert...` | Утверждение о поведении: если неверно, будет провал теста. |
| `MagicMock` | Подменный объект с управляемыми результатами и записью всех вызовов. |
| `spec=Интерфейс` | Не даёт обращаться к именам методов, которых нет у указанного интерфейса; **не** проверяет автоматически правильность типов/значений аргументов. |
| `return_value` | Значение, которое mock возвращает при вызове. |
| `side_effect` | Последовательные результаты, вызываемое действие или исключение при обращении к mock. |
| `patch` | Временно подменяет функцию или атрибут в тестовом контексте, затем восстанавливает оригинал. |
| `call(...)` | Объект-описание вызова, с которым сравнивают фактические обращения к mock. |
| `subTest(...)` | Разделяет входные случаи *внутри одного тестового метода*, помогая понять, какое значение провалилось. |

### Что важно не путать

- `MagicMock` нужен **для зависимостей** тестируемого класса. Сам объект, который тестируем, обычно должен быть **настоящим**.
- `assertEqual(a, b)` проверяет равенство; `assertIs(a, b)` — что это **один и тот же объект** в памяти.
- `assertRaises(ValueError)` не вызывает ошибку самостоятельно, а требует, чтобы она произошла при исполнении кода внутри блока.
- `@patch` в виде нескольких декораторов выдаёт mock-параметры **снизу вверх**.
- `assert_has_calls` проверяет наличие вызовов в нужном порядке, но **не исключает** дополнительных вызовов без отдельного `call_count`/`assert_called_once_with`.

## 1. Что это за файл и как он запускается

Это не программа, которая создаёт партии через консоль, а отдельный модуль проверки `test_practice.py`. Импорт `Practice` берёт классы из основного файла; блок `if __name__ == "__main__"` в основном файле при импорте не выполняется.

| Строка | Код | Что она означает |
|---:|---|---|
| 1 | `"""Модульные тесты практической работы; зависимости подменяются mock-объектами."""` | Это строка документации модуля (module docstring): описывает назначение тестового файла. Сам тест она не запускает. |
| 3 | `import unittest` | Подключает стандартный модуль `unittest`, который находит тестовые методы, запускает их и формирует отчёт. |
| 4 | `from unittest.mock import MagicMock, call, patch` | Подключает `MagicMock` (подмена объекта), `call` (описание ожидаемого вызова), `patch` (временная замена функции/атрибута). |
| 6 | `from Practice import (` | Начинает явный импорт имён из основного модуля `Practice`; круглые скобки позволяют продолжить импорт на следующих строках. |
| 7 | `AllocationAmountInput, AllocationAmountValidator, BudgetFundedParty,` | Импортирует ввод ассигнования, его валидатор и модель бюджетной партии для соответствующих тестов. |
| 8 | `BudgetFundedPartyCreationFlow, BudgetFundedPartyCreator, BudgetFundedPartyFormatter,` | Импортирует сценарий создания, создатель и форматтер бюджетной партии. |
| 9 | `BudgetCreatorInterface, ConsoleOutput, CountValidatorInterface,` | Импортирует интерфейс бюджетного создателя, вывод в консоль и общий интерфейс числового валидатора. |
| 10 | `DeputiesCountInput, DeputiesCountInputInterface, DeputiesCountValidator,` | Импортирует ввод числа депутатов, его интерфейс и проверяющий класс. |
| 11 | `FirstLetterCheckerInterface, FormatterInterface, OutputInterface, Party,` | Импортирует интерфейс checker, общий интерфейс форматтера, интерфейс вывода и базовый класс партии. |
| 12 | `PartyCreationFlowInterface, PartyFilter, PartyFilterInterface, PartyFormatter,` | Импортирует интерфейс сценария создания, фильтр, его интерфейс и агрегирующий форматтер. |
| 13 | `PartyInputScenario, PartyInputScenarioInterface, PartyNameInput,` | Импортирует сценарий пользовательского ввода, его интерфейс и ввод имени. |
| 14 | `PartyNameInputInterface, PartyNameValidator, PartyNameValidatorInterface,` | Импортирует интерфейс ввода имени, валидатор имени и интерфейс валидатора. |
| 15 | `PartyPrinter, PartyReaderInterface, PartyRegistry, PartyTypeFormatterInterface,` | Импортирует принтер, интерфейс чтения реестра, реестр и интерфейс форматтера отдельного типа партии. |
| 16 | `PartyTypeInput, PartyTypeInputInterface, PartyWriterInterface, PrinterInterface,` | Импортирует ввод типа партии, интерфейсы ввода и записи реестра, а также интерфейс принтера. |
| 17 | `RepresentativeCreatorInterface, RepresentativeParty,` | Импортирует интерфейс создателя представительной партии и сам класс представительной партии. |
| 18 | `RepresentativePartyCreationFlow, RepresentativePartyCreator,` | Импортирует сценарий создания и создатель представительной партии. |
| 19 | `RepresentativePartyFormatter, RequiredFirstLetterChecker, Task,` | Импортирует форматтер представительной партии, checker и общий координатор `Task`. |
| 20 | `AllocationAmountInputInterface,` | Импортирует интерфейс ввода ассигнования, используемый как `spec` в mock. |
| 21 | `)` | Закрывает многострочный список импортируемых имён; это часть синтаксиса, не отдельная операция. |

## 2. Сущности: TestParties

Три теста проверяют только хранение и выдачу значений. Ошибочные имена и отрицательные числа проверяют **отдельные валидаторы**, а не сущности: так устроен SRP в твоём проекте.

| Строка | Код | Что она означает |
|---:|---|---|
| 24 | `class TestParties(unittest.TestCase):` | Объявляет группу тестов моделей партий. Наследование от `unittest.TestCase` делает доступными `self.assert...` и автоматический запуск методов `test_*`. |
| 25 | `def test_base_party(self):` | Объявляет самостоятельный тест базового класса партии. Префикс `test_` обязателен для стандартного обнаружения тестов. |
| 26 | `self.assertEqual(Party("Альфа").get_name(), "Альфа")` | Создаёт `Party("Альфа")`, вызывает `get_name()` и проверяет, что вернулась ровно строка `"Альфа"`. |
| 28 | `def test_representative(self):` | Новый тест: представительная партия. |
| 29 | `party = RepresentativeParty("Альфа", 10)` | Создаёт партию с названием `"Альфа"` и десятью депутатами. |
| 30 | `self.assertEqual(party.get_name(), "Альфа")` | Проверяет, что унаследованный метод `get_name()` возвращает правильное имя. |
| 31 | `self.assertEqual(party.get_deputies_count(), 10)` | Проверяет собственный метод `get_deputies_count()` и сохранённое значение `10`. |
| 33 | `def test_budget(self):` | Новый тест: бюджетная партия. |
| 34 | `party = BudgetFundedParty("Бета", 5000)` | Создаёт объект с названием `"Бета"` и суммой `5000`. |
| 35 | `self.assertEqual(party.get_name(), "Бета")` | Проверяет имя через общий контракт `get_name()`. |
| 36 | `self.assertEqual(party.get_allocation_amount(), 5000)` | Проверяет специальное поле бюджетной партии через `get_allocation_amount()`. |

## 3. Валидаторы: TestValidators

Здесь мы проверяем как разрешённые значения, так и `ValueError`. Один метод с `subTest` проверяет сразу несколько входных значений, но считается одним тестовым методом `unittest`.

| Строка | Код | Что она означает |
|---:|---|---|
| 39 | `class TestValidators(unittest.TestCase):` | Открывает группу тестов валидаторов; здесь проверяются и успешные значения, и ожидаемые ошибки. |
| 40 | `def test_name(self):` | Метод тестирования названия партии. |
| 41 | `validator = PartyNameValidator()` | Создаёт настоящий валидатор имени (здесь mock не нужен: сам валидатор — проверяемый объект). |
| 42 | `self.assertEqual(validator.validate("  Альфа  "), "Альфа")` | Проверяет, что `validate()` удаляет пробелы с краёв и возвращает `"Альфа"`. |
| 43 | `for value in ("", "  ", "1234"):` | Перебирает три невалидных строки: пустую, только пробелы и только цифры. |
| 44 | `with self.subTest(value=value), self.assertRaises(ValueError):` | `subTest(value=value)` выделяет текущий пример в отчёте, а `assertRaises(ValueError)` требует появления `ValueError` внутри блока. |
| 45 | `validator.validate(value)` | Запускает валидацию текущего неправильного значения. Если исключение ожидаемого типа возникло, соответствующий подкейс успешен. |
| 47 | `def test_deputies(self):` | Метод тестирования числа депутатов. |
| 48 | `validator = DeputiesCountValidator()` | Создаёт настоящий `DeputiesCountValidator`. |
| 49 | `self.assertEqual(validator.validate(0), 0)` | Проверяет граничный разрешённый случай: ноль депутатов допустим. |
| 50 | `self.assertEqual(validator.validate(10), 10)` | Проверяет обычное положительное количество: `10` возвращается без изменения. |
| 51 | `with self.assertRaises(ValueError):` | Начинает блок ожидания ошибки `ValueError`. |
| 52 | `validator.validate(-1)` | Передаёт отрицательное число `-1`; именно эта строка должна вызвать ожидаемое исключение. |
| 54 | `def test_allocation(self):` | Метод тестирования суммы ассигнования. |
| 55 | `validator = AllocationAmountValidator()` | Создаёт настоящий `AllocationAmountValidator`. |
| 56 | `self.assertEqual(validator.validate(5000), 5000)` | Проверяет, что положительная сумма `5000` принимается. |
| 57 | `for value in (0, -1):` | Перебирает запрещённые суммы: `0` и `-1`. |
| 58 | `with self.subTest(value=value), self.assertRaises(ValueError):` | Для каждого значения заводит подкейс и ожидает `ValueError`. |
| 59 | `validator.validate(value)` | Передаёт неподходящее значение в валидатор. |

**Разбор записи через `with`:** `with self.assertRaises(ValueError):` — контекстный менеджер. Следующий блок должен выбросить ожидаемую ошибку; если ошибки нет, тест падает. Если выброшена ошибка другого типа, тест также не становится успешным.

## 4. Хранилище: TestRegistry

Проверяются добавление партий, порядок чтения, защищённость внутреннего списка и отказ принимать объект неправильного типа.

| Строка | Код | Что она означает |
|---:|---|---|
| 62 | `class TestRegistry(unittest.TestCase):` | Группа тестов хранилища `PartyRegistry`. |
| 63 | `def test_add_and_get_copy(self):` | Проверка добавления и важного свойства — возврата копии списка. |
| 64 | `registry = PartyRegistry()` | Создаёт пустой реестр. |
| 65 | `first = Party("Альфа")` | Создаёт первый объект партии. |
| 66 | `second = Party("Бета")` | Создаёт второй объект партии. |
| 67 | `registry.add_party(first)` | Добавляет первый объект в реестр. |
| 68 | `registry.add_party(second)` | Добавляет второй объект в реестр. |
| 69 | `self.assertEqual(registry.get_parties(), [first, second])` | Убеждается, что `get_parties()` вернул оба объекта в том же порядке. Сравнение списков учитывает порядок элементов. |
| 70 | `registry.get_parties().clear()` | Берёт *полученный* список и очищает его методом `clear()`; это не должно менять внутренний список реестра. |
| 71 | `self.assertEqual(registry.get_parties(), [first, second])` | Повторно читает реестр и убеждается, что две партии остались: значит, `get_parties()` не отдал наружу сам внутренний список. |
| 73 | `def test_wrong_object(self):` | Метод проверки добавления объекта неподходящего типа. |
| 74 | `with self.assertRaises(TypeError):` | Начинает контекст, в котором обязательно должен возникнуть `TypeError`. |
| 75 | `PartyRegistry().add_party("Альфа")` | Создаёт реестр и пытается добавить строку вместо объекта, удовлетворяющего `PartyInterface`. |

## 5. Checker и фильтр: TestCheckerAndFilter

Это пример **двух видов теста**: настоящий checker тестируем напрямую, а `PartyFilter` отдельно тестируем с `MagicMock` вместо checker.

| Строка | Код | Что она означает |
|---:|---|---|
| 78 | `class TestCheckerAndFilter(unittest.TestCase):` | Группа тестов проверки первой буквы и списка с фильтром. |
| 79 | `def test_checker(self):` | Проверка настоящего `RequiredFirstLetterChecker` без mock. |
| 80 | `checker = RequiredFirstLetterChecker()` | Создаёт экземпляр checker. |
| 81 | `for name in ("Альфа", "кедр", "Ёж"):` | Перебирает имена, которые должны пройти условие: А, к (в нижнем регистре), Ё. |
| 82 | `with self.subTest(name=name):` | Отдельно маркирует каждое имя для диагностики ошибок (`name=name`). |
| 83 | `self.assertTrue(checker.check(Party(name)))` | Создаёт партию с текущим именем и требует истинного результата `check()`. |
| 84 | `for name in ("Лето", "Яблоко", "", "   "):` | Перебирает названия, которые должны не пройти: буквы вне диапазона и пустые/пробельные названия. |
| 85 | `with self.subTest(name=name):` | Создаёт отдельный подкейс для каждого запрещённого названия. |
| 86 | `self.assertFalse(checker.check(Party(name)))` | Требует `False`; дополнительно проверяется безопасная обработка пустого имени checker'ом. |
| 88 | `def test_filter_mock(self):` | Отдельный тест `PartyFilter`, где настоящую зависимость checker подменяют, чтобы не тестировать две ответственности одновременно. |
| 89 | `checker = MagicMock(spec=FirstLetterCheckerInterface)` | Создаёт mock, ограниченный атрибутами `FirstLetterCheckerInterface`; доступны только заявленные в интерфейсе имена методов. |
| 90 | `checker.check.side_effect = [True, False]` | Настраивает *последовательные* ответы `check`: первый вызов вернёт `True`, второй — `False`. |
| 91 | `first, second = Party("Альфа"), Party("Яблоко")` | Одновременно создаёт две партии и присваивает их переменным `first` и `second`. |
| 92 | `result = PartyFilter(checker).filter([first, second])` | Передаёт mock в конструктор фильтра и вызывает `filter()` со списком двух партий. |
| 93 | `self.assertEqual(result, [first])` | Проверяет результат фильтрации: только первая партия, так как mock вернул `True` для неё. |
| 94 | `checker.check.assert_has_calls([call(first), call(second)])` | Проверяет наличие вызовов `check(first)` и затем `check(second)` в указанном порядке. Дополнительные вызовы эта проверка сама по себе не запрещает. |

**Проверка mock на трёх строках:**

```python
checker = MagicMock(spec=FirstLetterCheckerInterface)
checker.check.side_effect = [True, False]
result = PartyFilter(checker).filter([Party("Альфа"), Party("Яблоко")])
```

Первый вызов `check()` вернёт `True`, второй — `False`. Реальная проверка букв здесь **вообще не выполняется**. Именно поэтому этот тест изолированно проверяет алгоритм фильтра.

## 6. Консольный ввод: TestInputs

Главная идея: тесты должны обходиться без живого пользователя. `patch("builtins.input")` поставляет заранее известные строки, а `patch("builtins.print")` перехватывает печать.

| Строка | Код | Что она означает |
|---:|---|---|
| 97 | `class TestInputs(unittest.TestCase):` | Группа тестов классов ввода из консоли. `patch` позволяет запускать их без человека за клавиатурой. |
| 98 | `@patch("builtins.print")` | Верхний декоратор подменяет `builtins.print` на mock на время данного теста: сообщения не выводятся в настоящую консоль. |
| 99 | `@patch("builtins.input", side_effect=["неизвестная", " БЮДЖЕТНАЯ "])` | Нижний декоратор подменяет `builtins.input`: первый ввод `"неизвестная"`, второй — `" БЮДЖЕТНАЯ "`. |
| 100 | `def test_party_type(self, mock_input, mock_print):` | Тест получает два mock-параметра. Они передаются снизу вверх: сначала `mock_input` от нижнего декоратора, затем `mock_print` от верхнего. |
| 101 | `self.assertEqual(PartyTypeInput().input(), "бюджетная")` | Проверяет, что ввод повторится и будет возвращён нормализованный тип `"бюджетная"` (пробелы убраны, буквы переведены в нижний регистр). |
| 102 | `self.assertEqual(mock_input.call_count, 2)` | Проверяет, что было ровно два запроса к функции `input()`. |
| 104 | `@patch("builtins.input", return_value="стоп")` | Декоратор делает каждый вызов `input()` возвращающим строку `"стоп"`. |
| 105 | `def test_stop(self, mock_input):` | Отдельный тест команды остановки; `mock_input` передан декоратором, хотя внутри метода он не используется. |
| 106 | `with patch("builtins.print"):` | В пределах блока временно подменяет `print`; после выхода из `with` реальная функция автоматически восстанавливается. |
| 107 | `self.assertEqual(PartyTypeInput().input(), "стоп")` | Проверяет, что ввод типа партии распознаёт команду `"стоп"` и возвращает её. |
| 109 | `@patch("builtins.print")` | Подменяет консольный вывод на mock. |
| 110 | `@patch("builtins.input", side_effect=["неправильно", "Альфа"])` | Подменяет ввод двумя последовательными строками — тестирует попытку исправления названия. |
| 111 | `def test_name_retry(self, mock_input, mock_print):` | Тестовый метод с аргументами `mock_input`, `mock_print` от декораторов. |
| 112 | `validator = MagicMock(spec=PartyNameValidatorInterface)` | Создаёт фальшивый валидатор, соответствующий по названиям методов интерфейсу `PartyNameValidatorInterface`. |
| 113 | `validator.validate.side_effect = [ValueError("Ошибка"), "Альфа"]` | Первый вызов `validate()` выбрасывает `ValueError("Ошибка")`, второй возвращает `"Альфа"`. Важно: это запрограммированное поведение mock, а не реальная проверка текста. |
| 114 | `self.assertEqual(PartyNameInput(validator).input(), "Альфа")` | Проверяет, что `PartyNameInput` перехватывает первую ошибку, запрашивает ввод повторно и возвращает второй результат. |
| 115 | `self.assertEqual(validator.validate.call_count, 2)` | Убеждается, что проверка названия была запрошена два раза. |
| 117 | `@patch("builtins.print")` | Подменяет печать, чтобы вывод ошибок не засорял тесты. |
| 118 | `@patch("builtins.input", side_effect=["не число", "-1", "10"])` | Задаёт три ввода: нечисловой текст, `-1` и `10`. |
| 119 | `def test_deputies_retry(self, mock_input, mock_print):` | Тест метода ввода количества депутатов. |
| 120 | `validator = MagicMock(spec=CountValidatorInterface)` | Создаёт mock общего числового валидатора (`CountValidatorInterface` сохранён по требованию преподавателя). |
| 121 | `validator.validate.side_effect = [ValueError("Отрицательно"), 10]` | Первый вызов mock-валидатора выбросит `ValueError`, второй вернёт `10`. |
| 122 | `self.assertEqual(DeputiesCountInput(validator).input(), 10)` | Проверяет, что объект ввода в итоге возвращает `10`, не завершая работу после двух неудачных попыток. |
| 123 | `self.assertEqual(validator.validate.call_count, 2)` | Валидатор вызывался дважды: текст `"не число"` не преобразовался через `int()` и до валидатора не дошёл. |
| 124 | `validator.validate.assert_has_calls([call(-1), call(10)])` | Проверяет, что валидатор получил `-1`, затем `10` (именно `int`, а не исходные строки). |
| 126 | `@patch("builtins.print")` | Подменяет вывод сообщений о неверных значениях. |
| 127 | `@patch("builtins.input", side_effect=["10,5", "0", "5000"])` | Настраивает три последовательных ввода ассигнования: дробное `"10,5"`, ноль и `5000`. |
| 128 | `def test_allocation_retry(self, mock_input, mock_print):` | Тестирует повторный ввод ассигнования. |
| 129 | `validator = MagicMock(spec=CountValidatorInterface)` | Создаёт mock валидатора суммы через общий интерфейс. |
| 130 | `validator.validate.side_effect = [ValueError("Ноль"), 5000]` | Первый вызов `validate` генерирует `ValueError("Ноль")`, второй возвращает `5000`. |
| 131 | `self.assertEqual(AllocationAmountInput(validator).input(), 5000)` | Проверяет итог `5000` после двух неудачных вводов. Строка `"10,5"` не переводится в `int`, поэтому валидатор вызывается только для `0` и `5000`. |
| 132 | `validator.validate.assert_has_calls([call(0), call(5000)])` | Проверяет обращения `validate(0)` и `validate(5000)`. |

**Почему ввод и вызовы валидатора считаются отдельно?** В `test_deputies_retry` строка `"не число"` вызывает ошибку преобразования `int()` до вызова валидатора. Поэтому `input` вызывается 3 раза, а `validator.validate` — только 2 раза. То же с `"10,5"`: замена запятой на точку не превращает дробную строку в целое число.

**Порядок декораторов:**

```python
@patch("builtins.print")
@patch("builtins.input", side_effect=["неизвестная", "обычная"])
def test_example(self, mock_input, mock_print):
    ...
```

Нижний декоратор передаёт `mock_input` первым, верхний `mock_print` — вторым. Обе функции после теста восстанавливаются автоматически.

## 7. Создание партий: TestCreators

Creator превращает готовые значения в объект партии. CreationFlow получает недостающие значения от ввода и обращается к Creator. В тестах CreationFlow оба участника подменены mock.

| Строка | Код | Что она означает |
|---:|---|---|
| 135 | `class TestCreators(unittest.TestCase):` | Группа тестов создателей партий и более высокоуровневых CreationFlow. |
| 136 | `def test_representative_creator(self):` | Тест конкретного создателя представительной партии. |
| 137 | `party = RepresentativePartyCreator().create("Альфа", 10)` | Создаёт объект партии методом `create` из готовых данных `"Альфа"`, `10`. |
| 138 | `self.assertIsInstance(party, RepresentativeParty)` | Требует, чтобы результат был экземпляром `RepresentativeParty` (либо её подклассом). |
| 139 | `self.assertEqual(party.get_deputies_count(), 10)` | Проверяет сохранение количества депутатов. |
| 141 | `def test_budget_creator(self):` | Тест создателя бюджетной партии. |
| 142 | `party = BudgetFundedPartyCreator().create("Бета", 5000)` | Создаёт бюджетную партию со значениями `"Бета"`, `5000`. |
| 143 | `self.assertIsInstance(party, BudgetFundedParty)` | Проверяет тип полученного объекта. |
| 144 | `self.assertEqual(party.get_allocation_amount(), 5000)` | Проверяет сохранённую сумму ассигнования. |
| 146 | `def test_representative_flow(self):` | Тест сценария создания представительной партии с двумя заменёнными зависимостями. |
| 147 | `inp = MagicMock(spec=DeputiesCountInputInterface)` | Создаёт mock интерфейса получения числа депутатов. |
| 148 | `creator = MagicMock(spec=RepresentativeCreatorInterface)` | Создаёт mock интерфейса конструктора партии (Creator). |
| 149 | `inp.input.return_value = 10` | Говорит mock-вводу при вызове `input()` возвращать число `10`. |
| 150 | `party = RepresentativeParty("Альфа", 10)` | Создаёт заранее известный настоящий объект, который должен вернуться из сценария. |
| 151 | `creator.create.return_value = party` | Настраивает mock-Creator возвращать `party` при вызове `create()`. |
| 152 | `result = RepresentativePartyCreationFlow(inp, creator).create("Альфа")` | Создаёт `RepresentativePartyCreationFlow` с этими двумя mock и вызывает его `create("Альфа")`. |
| 153 | `self.assertIs(result, party)` | `assertIs` проверяет, что возвращена та же самая сущность *по идентичности*, а не лишь равный по значениям объект. |
| 154 | `creator.create.assert_called_once_with("Альфа", 10)` | Проверяет, что Creator вызван строго один раз с аргументами `"Альфа"` и `10`. |
| 156 | `def test_budget_flow(self):` | Аналогичный тест сценария создания бюджетной партии. |
| 157 | `inp = MagicMock(spec=AllocationAmountInputInterface)` | Создаёт mock интерфейса ввода ассигнования. |
| 158 | `creator = MagicMock(spec=BudgetCreatorInterface)` | Создаёт mock интерфейса бюджетного создателя. |
| 159 | `inp.input.return_value = 5000` | Устанавливает результат чтения ассигнования `5000`. |
| 160 | `party = BudgetFundedParty("Бета", 5000)` | Создаёт эталонную бюджетную партию. |
| 161 | `creator.create.return_value = party` | Настраивает mock-Creator возвращать заранее созданную партию. |
| 162 | `result = BudgetFundedPartyCreationFlow(inp, creator).create("Бета")` | Создаёт бюджетный flow и вызывает его `create("Бета")`. |
| 163 | `self.assertIs(result, party)` | Проверяет идентичность результата с `party`. |
| 164 | `creator.create.assert_called_once_with("Бета", 5000)` | Проверяет единственный вызов `creator.create("Бета", 5000)`. |

**Отличие `assertIs` от `assertEqual`:** `self.assertIs(result, party)` гарантирует, что CreationFlow вернул именно объект, который ему передал mock-Creator. Два разных объекта с одинаковым именем могли бы иметь равные поля, но не были бы идентичными.

## 8. Форматирование: TestFormatters

Проверяются `supports()`, итоговый текст, отказ от неподходящих объектов, делегирование подходящему форматтеру и отсутствие поддерживаемого форматтера.

| Строка | Код | Что она означает |
|---:|---|---|
| 167 | `class TestFormatters(unittest.TestCase):` | Группа тестов форматтеров (узкоспециализированных и выбирающего подходящий). |
| 168 | `def test_representative_formatter(self):` | Метод проверки `RepresentativePartyFormatter`. |
| 169 | `formatter = RepresentativePartyFormatter()` | Создаёт форматтер представительных партий. |
| 170 | `party = RepresentativeParty("Альфа", 10)` | Создаёт подходящую представительную партию для проверки. |
| 171 | `self.assertTrue(formatter.supports(party))` | `supports()` обязан возвращать `True` для поддерживаемой разновидности. |
| 172 | `self.assertFalse(formatter.supports(BudgetFundedParty("Бета", 1)))` | `supports()` обязан возвращать `False` для бюджетной партии. |
| 173 | `self.assertEqual(formatter.format(party), 'Партия "Альфа", количество депутатов: 10')` | Проверяет точную строку форматирования: имя и число депутатов, включая кавычки и знаки препинания. |
| 174 | `with self.assertRaises(TypeError):` | Начинает проверку ожидаемого `TypeError`. |
| 175 | `formatter.format(Party("Бета"))` | Передаёт неподходящую базовую `Party`: специальный форматтер должен отказаться от неё. |
| 177 | `def test_budget_formatter(self):` | Метод проверки `BudgetFundedPartyFormatter`. |
| 178 | `formatter = BudgetFundedPartyFormatter()` | Создаёт форматтер для бюджетных партий. |
| 179 | `party = BudgetFundedParty("Бета", 5000)` | Создаёт подходящую бюджетную партию. |
| 180 | `self.assertTrue(formatter.supports(party))` | Проверяет поддержку бюджетного типа. |
| 181 | `self.assertFalse(formatter.supports(RepresentativeParty("Альфа", 1)))` | Проверяет отсутствие поддержки представительной партии. |
| 182 | `self.assertEqual(formatter.format(party), 'Партия "Бета", ассигнование: 5000')` | Сравнивает результат `format()` с ожидаемой строкой о сумме ассигнования. |
| 183 | `with self.assertRaises(TypeError):` | Начинает блок ожидания `TypeError`. |
| 184 | `formatter.format(Party("Альфа"))` | Передаёт неподходящий базовый объект `Party`. |
| 186 | `def test_aggregate_formatter(self):` | Тест `PartyFormatter`, который делегирует работу одному из нескольких вложенных форматтеров. |
| 187 | `rep = MagicMock(spec=PartyTypeFormatterInterface)` | Создаёт первый mock формата с интерфейсом `PartyTypeFormatterInterface`. |
| 188 | `budget = MagicMock(spec=PartyTypeFormatterInterface)` | Создаёт второй mock такого же интерфейса. |
| 189 | `party = Party("Альфа")` | Создаёт партию, которую нужно форматировать. |
| 190 | `rep.supports.return_value = False` | Первый форматтер настроен сообщать `False` на вопрос о поддержке партии. |
| 191 | `budget.supports.return_value = True` | Второй форматтер сообщает `True`: он должен быть выбран. |
| 192 | `budget.format.return_value = "Готово"` | Устанавливает текст результата у второго mock-форматтера — `"Готово"`. |
| 193 | `self.assertEqual(PartyFormatter([rep, budget]).format(party), "Готово")` | Передаёт оба mock в агрегатор, форматирует партию и проверяет делегированный результат. |
| 194 | `rep.format.assert_not_called()` | Убеждается, что первый форматтер действительно *не форматировал* партию. |
| 195 | `budget.format.assert_called_once_with(party)` | Убеждается, что второй форматтер получил партию ровно один раз. |
| 197 | `def test_no_formatter(self):` | Отдельный тест ситуации без подходящего форматтера. |
| 198 | `with self.assertRaises(ValueError):` | Ожидает `ValueError` при попытке форматировать партию с пустым списком форматтеров. |
| 199 | `PartyFormatter([]).format(Party("Альфа"))` | Выполняет вызов с пустым списком форматтеров внутри `with`; из-за отсутствия подходящей реализации ожидается `ValueError`. |

**Связь с OCP:** общий `PartyFormatter` не решает через `isinstance` конкретных партий, какой формат выбрать. Он спрашивает `supports()` у форматтеров, а затем вызывает `format()` подходящего. Тест `test_aggregate_formatter` показывает это без настоящих форматтеров.

## 9. Вывод: TestOutput

`ConsoleOutput` должен вызвать печать. `PartyPrinter` должен запросить форматирование и передать готовый текст на вывод; подменяем оба участника.

| Строка | Код | Что она означает |
|---:|---|---|
| 202 | `class TestOutput(unittest.TestCase):` | Группа тестов классов вывода (низкоуровневый консольный вывод и принтер списка). |
| 203 | `@patch("builtins.print")` | Заменяет встроенный `print` на mock. |
| 204 | `def test_console(self, mock_print):` | Тест консольной реализации вывода. |
| 205 | `ConsoleOutput().write("Привет")` | Вызывает `ConsoleOutput().write("Привет")`; настоящая печать перехвачена mock. |
| 206 | `mock_print.assert_called_once_with("Привет")` | Проверяет, что `print("Привет")` вызван один раз и с ожидаемым текстом. |
| 208 | `def test_printer(self):` | Тест `PartyPrinter` с подменой двух зависимостей. |
| 209 | `formatter = MagicMock(spec=FormatterInterface)` | Создаёт mock общего интерфейса форматирования. |
| 210 | `output = MagicMock(spec=OutputInterface)` | Создаёт mock интерфейса отправки текста на вывод. |
| 211 | `party = Party("Альфа")` | Создаёт партию, которую нужно вывести. |
| 212 | `formatter.format.return_value = "Партия Альфа"` | Программирует mock форматтера возвращать строку `"Партия Альфа"`. |
| 213 | `PartyPrinter(formatter, output).print([party])` | Создаёт принтер с двумя mock, просит напечатать список из одной партии. |
| 214 | `formatter.format.assert_called_once_with(party)` | Проверяет, что `formatter.format` вызван один раз с нужной партией. |
| 215 | `output.write.assert_called_once_with("Партия Альфа")` | Проверяет, что `output.write` получил результат форматтера. |
| 217 | `def test_printer_empty(self):` | Тест поведения принтера при пустом списке партий. |
| 218 | `formatter = MagicMock(spec=FormatterInterface)` | Подменяет форматтер на mock. |
| 219 | `output = MagicMock(spec=OutputInterface)` | Подменяет вывод на mock. |
| 220 | `PartyPrinter(formatter, output).print([])` | Запускает печать пустого списка. |
| 221 | `formatter.format.assert_not_called()` | Проверяет, что форматтер не вызывался: форматировать нечего. |
| 222 | `output.write.assert_called_once_with("Нет партий, удовлетворяющих условию.")` | Проверяет, что вывод получил сообщение `"Нет партий, удовлетворяющих условию."`. |

## 10. Сценарий и Task: TestScenarioAndTask

Эти классы координируют многие другие, поэтому почти все их зависимости здесь являются `MagicMock`: тестируем последовательность взаимодействий, а не всю программу целиком.

| Строка | Код | Что она означает |
|---:|---|---|
| 225 | `class TestScenarioAndTask(unittest.TestCase):` | Группа тестов двух координирующих классов — сценария ввода и главного `Task`. |
| 226 | `def test_scenario(self):` | Тест полного сценария: обычная партия, бюджетная партия, затем остановка. |
| 227 | `type_input = MagicMock(spec=PartyTypeInputInterface)` | Подменяет чтение вида партии. |
| 228 | `name_input = MagicMock(spec=PartyNameInputInterface)` | Подменяет чтение её названия. |
| 229 | `registry = MagicMock(spec=PartyWriterInterface)` | Подменяет интерфейс добавления партии в реестр. |
| 230 | `rep_flow = MagicMock(spec=PartyCreationFlowInterface)` | Создаёт mock потока создания обычной партии. |
| 231 | `budget_flow = MagicMock(spec=PartyCreationFlowInterface)` | Создаёт mock потока создания бюджетной партии. |
| 232 | `type_input.input.side_effect = ["обычная", "бюджетная", "стоп"]` | Задаёт последовательность типов для трёх итераций цикла: обычная, бюджетная, `"стоп"`. |
| 233 | `name_input.input.side_effect = ["Альфа", "Бета"]` | Задаёт два названия, потому что на команде `"стоп"` название не запрашивается. |
| 234 | `rep = RepresentativeParty("Альфа", 10)` | Создаёт реальный объект ожидаемой обычной партии. |
| 235 | `budget = BudgetFundedParty("Бета", 5000)` | Создаёт реальный объект ожидаемой бюджетной партии. |
| 236 | `rep_flow.create.return_value = rep` | Программирует первый flow возвращать объект `rep`. |
| 237 | `budget_flow.create.return_value = budget` | Программирует второй flow возвращать объект `budget`. |
| 238 | `scenario = PartyInputScenario(` | Начинает многострочный вызов конструктора `PartyInputScenario`. |
| 239 | `type_input, name_input, {"обычная": rep_flow, "бюджетная": budget_flow}, registry` | Передаёт mock ввода типа, mock имени, словарь соответствия строк типам flow и mock хранилища. |
| 240 | `)` | Закрывает многострочный вызов конструктора — объект `scenario` создан. |
| 241 | `scenario.run()` | Вызывает `run()`: запускается ввод двух партий с остановкой на третьем типе. |
| 242 | `rep_flow.create.assert_called_once_with("Альфа")` | Проверяет, что обычный flow запускался единожды для имени `"Альфа"`. |
| 243 | `budget_flow.create.assert_called_once_with("Бета")` | Проверяет, что бюджетный flow запускался единожды для имени `"Бета"`. |
| 244 | `registry.add_party.assert_has_calls([call(rep), call(budget)])` | Проверяет, что в реестр вызвано добавление сначала `rep`, затем `budget`. |
| 245 | `self.assertEqual(registry.add_party.call_count, 2)` | Дополнительно проверяет ровно два вызова добавления (так как `assert_has_calls` может допускать дополнительные вызовы). |
| 247 | `def test_scenario_unknown(self):` | Тест обработки неизвестного типа партии. |
| 248 | `type_input = MagicMock(spec=PartyTypeInputInterface)` | Создаёт mock интерфейса ввода типа. |
| 249 | `type_input.input.return_value = "другой"` | Всегда возвращает строку `"другой"`, которой нет в карте сценариев. |
| 250 | `name_input = MagicMock(spec=PartyNameInputInterface)` | Создаёт mock ввода названия. |
| 251 | `registry = MagicMock(spec=PartyWriterInterface)` | Создаёт mock интерфейса записи в реестр. |
| 252 | `with self.assertRaises(ValueError):` | Открывает блок ожидания `ValueError`. |
| 253 | `PartyInputScenario(type_input, name_input, {}, registry).run()` | Конструирует сценарий с пустой картой типов и запускает; ожидается ошибка до чтения имени. |
| 254 | `name_input.input.assert_not_called()` | Проверяет, что после неизвестного типа метод ввода имени даже не был вызван. |
| 256 | `def test_task(self):` | Тест верхнеуровневого координатора `Task`. |
| 257 | `scenario = MagicMock(spec=PartyInputScenarioInterface)` | Подменяет сценарий ввода. |
| 258 | `registry = MagicMock(spec=PartyReaderInterface)` | Подменяет интерфейс чтения из реестра. |
| 259 | `party_filter = MagicMock(spec=PartyFilterInterface)` | Подменяет фильтр партий. |
| 260 | `printer = MagicMock(spec=PrinterInterface)` | Подменяет принтер результатов. |
| 261 | `parties = [Party("Альфа"), Party("Яблоко")]` | Создаёт список из двух партий: одна должна пройти фильтр, другая — нет. |
| 262 | `registry.get_parties.return_value = parties` | Настраивает mock реестра возвращать обе партии. |
| 263 | `party_filter.filter.return_value = [parties[0]]` | Настраивает mock фильтра возвращать список из одной первой партии. |
| 264 | `Task(scenario, registry, party_filter, printer).run()` | Собирает `Task` с четырьмя mock-зависимостями и вызывает `run()`. |
| 265 | `scenario.run.assert_called_once_with()` | Проверяет, что сценарий ввода запущен ровно один раз без аргументов. |
| 266 | `registry.get_parties.assert_called_once_with()` | Проверяет, что реестр прочитан ровно один раз без аргументов. |
| 267 | `party_filter.filter.assert_called_once_with(parties)` | Проверяет, что фильтр вызван с исходным полным списком партий. |
| 268 | `printer.print.assert_called_once_with([parties[0]])` | Проверяет, что принтер получил только отфильтрованную партию. |

**Последовательность работы `Task` в этом тесте:** `scenario.run()` → `registry.get_parties()` → `party_filter.filter(parties)` → `printer.print(filtered)`. Каждый вызов можно проверить изолированно, потому что зависимости подменены mock.

## 11. Точка входа

Последние две строки нужны для прямого запуска тестового файла.

| Строка | Код | Что она означает |
|---:|---|---|
| 271 | `if __name__ == "__main__":` | Условие, истинное при запуске файла напрямую (`python test_practice.py`), но ложное при импорте модуля. |
| 272 | `unittest.main()` | Запускает встроенный runner `unittest`, который найдёт и выполнит все методы `test_*`. |

## 12. Справочник всех использованных методов unittest и mock

| Метод / атрибут | Зачем | Особенность |
|---|---|---|
| `assertEqual(a, b)` | Сравнение значений. | Для списков сравнивает элементы и порядок; для объектов без своего `__eq__` обычно сравнивается идентичность. |
| `assertIs(a, b)` | Проверка, что это один и тот же объект. | Это сильнее, чем сравнивать значения. |
| `assertTrue(x)` | Проверка истинности. | Принимает любое значение с истинной логической интерпретацией, не только `True`. |
| `assertFalse(x)` | Проверка ложности. | Принимает ложные значения вроде `False`, `0`, пустой строки. |
| `assertIsInstance(obj, Class)` | Проверка принадлежности классу. | Подклассы тоже проходят. |
| `assertRaises(Error)` | Проверка ошибки указанного типа. | Удобен вместе с `with`. |
| `self.subTest(...)` | Метки для отдельных наборов входных данных. | Не создаёт отдельный метод `test_*`. |
| `MagicMock(spec=Interface)` | Подмена зависимого объекта. | Ограничивает набор доступных имён, но не является настоящим экземпляром интерфейса. |
| `patch("builtins.input")` | Подмена ввода пользователя. | Программа не ждёт реальную клавиатуру. |
| `patch("builtins.print")` | Перехват вывода. | Можно проверить содержимое через вызовы mock. |
| `return_value` | Один запрограммированный результат mock. | Обычно остаётся одинаковым при повторных вызовах. |
| `side_effect=[...]` | Серия результатов/исключений по вызовам. | Когда последовательность закончится, следующий вызов может породить `StopIteration`. |
| `mock.call_count` | Количество вызовов. | В отличие от `assert_has_calls`, помогает заметить лишние вызовы. |
| `mock.assert_called_once_with(...)` | Ровно один вызов с указанными аргументами. | Отличает позиционные и именованные аргументы. |
| `mock.assert_has_calls([...])` | Проверка набора вызовов в порядке. | По умолчанию порядок проверяется; это не гарантия отсутствия других вызовов. |
| `mock.assert_not_called()` | Требование отсутствия вызовов. | Полезно для веток, которые не должны вызывать зависимость. |
| `call(x)` | Описание вызова метода с `x`. | Служит элементом списка в `assert_has_calls`. |
| `unittest.main()` | Запуск обнаруженных тестов. | При прямом запуске файла. |

## 13. Какие тесты чему соответствуют

| Тестовый класс | Методов `test_*` | Что проверяет |
|---|---:|---|
| `TestParties` | 3 | Базовая и две специализированные сущности. |
| `TestValidators` | 3 | Три валидатора и неправильные аргументы. |
| `TestRegistry` | 2 | Хранение, копия списка, недопустимый объект. |
| `TestCheckerAndFilter` | 2 | Правило первой буквы, фильтр с mock. |
| `TestInputs` | 5 | Ввод, `patch`, повторные попытки, команда остановки. |
| `TestCreators` | 4 | Два Creator и два CreationFlow. |
| `TestFormatters` | 4 | Два специализированных форматтера, агрегатор, исключение. |
| `TestOutput` | 3 | Консольный вывод и два варианта печати. |
| `TestScenarioAndTask` | 3 | Обычный сценарий, ошибка неизвестного типа, главный Task. |
| **Итого** | **29** | Это 29 тестовых **методов**, а `subTest` добавляют варианты внутри некоторых методов. |

**Важно о полноте:** наличие 29 успешных тестов **не доказывает автоматически**, что все возможные входы и граничные ситуации проверены. Абстрактные интерфейсы здесь не создаются напрямую; их используют как контракты mock. Для строгого заявления «проверены все классы» нужно отдельно сопоставить список конкретных классов из `Practice.py` с тестами и при необходимости добавить граничные случаи.

## 14. Запуск в VS Code / терминале

Размести `Practice.py` и `test_practice.py` в одной папке:

```text
ООП/
├── Practice.py
└── test_practice.py
```

**Запуск с подробным списком тестов:**

```bash
python -m unittest -v test_practice.py
```

**Запуск файла напрямую:**

```bash
python test_practice.py
```

**Запуск одного конкретного метода:**

```bash
python -m unittest -v test_practice.TestInputs.test_deputies_retry
```

**Расшифровка итогового отчёта:**

```text
Ran 29 tests in ...s

OK
```

`Ran 29 tests` — найдено и выполнено 29 методов. `OK` — не было провалов и неожиданных исключений. Если увидишь `FAIL`, значит не выполнено проверочное утверждение; `ERROR` — тест столкнулся с неожиданной ошибкой (в том числе с ошибкой импорта). Время зависит от компьютера.

## 15. Типичные вопросы преподавателя и ответы

**Вопрос:** Зачем нужен unit-тест?  
**Ответ:** Чтобы автоматически проверять отдельное поведение класса и сразу замечать поломку после изменений.

**Вопрос:** Почему `unittest.TestCase`?  
**Ответ:** Он даёт механизм обнаружения тестовых методов и набор методов `assert...` для проверок.

**Вопрос:** Зачем начинать имена с `test_`?  
**Ответ:** Так тестовый загрузчик `unittest` распознаёт методы как проверки.

**Вопрос:** Для чего `MagicMock`?  
**Ответ:** Чтобы подменить зависимость и проверить только логику одного класса, не полагаясь на работу другого.

**Вопрос:** Что означает `spec=FirstLetterCheckerInterface`?  
**Ответ:** Mock разрешает обращаться только к именам атрибутов и методов, описанным данным интерфейсом; не гарантирует контроль всех аргументов.

**Вопрос:** Почему не всегда использовать реальные классы?  
**Ответ:** Иначе ошибка checker могла бы завалить тест фильтра, даже если сам фильтр корректен.

**Вопрос:** Почему `patch` для `input()`?  
**Ответ:** Чтобы тест не ждал человека, а получал управляемую последовательность строк.

**Вопрос:** Чем отличается `return_value` от `side_effect`?  
**Ответ:** Первое задаёт обычный результат вызова, второе позволяет задавать цепочку результатов, исключение или функцию.

**Вопрос:** Что означает `call_count == 2`?  
**Ответ:** Зависимый mock-метод вызывался ровно два раза.

**Вопрос:** Почему тест валидатора не использует MagicMock?  
**Ответ:** Потому что сам валидатор — объект испытания; при его подмене мы проверяли бы лишь собственные настройки mock.

**Вопрос:** Зачем тестируется список-копия у Registry?  
**Ответ:** Чтобы внешний код не мог уничтожить внутренний реестр, очистив полученный из `get_parties()` список.

**Вопрос:** Где проявляется DIP?  
**Ответ:** `Task`, `PartyFilter`, `PartyPrinter` и CreationFlow принимают зависимости через интерфейсы — их удобно заменить mock.

**Вопрос:** Какая разница между тестом Creator и CreationFlow?  
**Ответ:** Creator создаёт объект из уже готовых значений, а CreationFlow запрашивает данные через зависимость и передаёт их Creator.

**Вопрос:** Что происходит при неизвестном типе партии?  
**Ответ:** Тест требует `ValueError` и проверяет, что ненужный запрос названия не был выполнен.

**Вопрос:** Сколько тестов здесь?  
**Ответ:** 29 тестовых методов, плюс несколько дополнительных сценариев через `subTest` внутри них.

## 16. Что улучшить, если преподаватель попросит строгое покрытие

1. Проверить **каждый конкретный класс** из актуального `Practice.py`, а не ориентироваться на число методов тестирования.
2. Добавить кейс для реестра, когда список пустой, и для фильтра, когда список пуст.
3. Проверить, что при невалидном вводе не происходит некорректного добавления партии.
4. Для важных сценариев проверить не только набор, но и **число** вызовов и при необходимости строгий порядок вызовов (`mock_calls`).
5. Следить, чтобы `Practice.py` и тесты были одной версии: после изменений интерфейсов или сигнатур старые тесты придётся адаптировать.
