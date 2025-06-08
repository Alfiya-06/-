class Stack:
    """Простой стек с базовыми операциями push, pop и проверкой пустоты."""

    def __init__(self):
        """Инициализирует пустой стек."""
        self._items = []

    def push(self, item):
        """Добавляет элемент в стек.

        Args:
            item: Элемент, который нужно добавить.
        """
        self._items.append(item)

    def pop(self):
        """Удаляет и возвращает верхний элемент стека.

        Returns:
            Верхний элемент стека.

        Raises:
            IndexError: Если стек пуст.
        """
        if self._items:
            return self._items.pop()
        raise IndexError("Ошибка: попытка извлечь элемент из пустого стека")

    def peek(self):
        """Возвращает верхний элемент стека без удаления.

        Returns:
            Верхний элемент стека или None, если стек пуст.
        """
        return self._items[-1] if self._items else None

    def is_empty(self):
        """Проверяет, пуст ли стек.

        Returns:
            True, если стек пуст, иначе False.
        """
        return len(self._items) == 0


class MiniMaxParser:
    """Вычислитель выражений с операциями m и M."""

    ALLOWED_CHARS = set("0123456789mM(),-.")

    def __init__(self, expression: str):
        """Инициализация парсера.

        Args:
            expression (str): Входное выражение для вычисления.
        """
        self.expression = expression
        self._stack = Stack()

    def _validate_expression(self):
        """Проверяет корректность входного выражения.

        Raises:
            ValueError: Если выражение содержит ошибки синтаксиса или недопустимые символы.
        """
        if not self.expression:
            raise ValueError("Ошибка: пустое выражение")

        for ch in self.expression:
            if ch not in self.ALLOWED_CHARS:
                raise ValueError(f"Ошибка: недопустимый символ '{ch}'")

        balance = 0
        for ch in self.expression:
            if ch == '(':
                balance += 1
            elif ch == ')':
                balance -= 1
                if balance < 0:
                    raise ValueError("Ошибка: закрывающая скобка без соответствующей открывающей")
        if balance != 0:
            raise ValueError("Ошибка: несбалансированные скобки")

        if 'm' not in self.expression and 'M' not in self.expression:
            raise ValueError("Ошибка: должно быть хотя бы одно m или M")

    def evaluate(self) -> int:
        """Вычисляет значение выражения с использованием стека.

        Returns:
            int: Результат вычисления.

        Raises:
            ValueError: При нарушении структуры выражения.
        """
        self._validate_expression()

        def _read_number(start_idx: int) -> tuple[int, int]:
            """Считывает число из выражения, начиная с позиции.

            Args:
                start_idx (int): Начальная позиция.

            Returns:
                tuple[int, int]: Считанное число и позиция после него.
            """
            num = 0
            i = start_idx
            while i < len(self.expression) and self.expression[i].isdigit():
                num = num * 10 + int(self.expression[i])
                i += 1
            return num, i

        i = 0
        while i < len(self.expression):
            char = self.expression[i]

            if char == '-' and i + 1 < len(self.expression) and self.expression[i + 1].isdigit():
                raise ValueError("Ошибка: числа должны быть положительными")

            if char == '.' or (char.isdigit() and i + 1 < len(self.expression) and self.expression[i + 1] == '.'):
                raise ValueError("Ошибка: допустимы только целые положительные")

            if char.isdigit():
                number, i = _read_number(i)
                self._stack.push(number)
                continue

            elif char in ['m', 'M']:
                self._stack.push(char)

            elif char == ')':
                try:
                    b = self._stack.pop()
                    a = self._stack.pop()
                    operator = self._stack.pop()
                except IndexError:
                    raise ValueError("Ошибка: недостаточно аргументов для операции")

                if not isinstance(a, int) or not isinstance(b, int):
                    raise ValueError("Ошибка: аргументы операции должны быть целыми числами")

                if operator not in ('m', 'M'):
                    raise ValueError("Ошибка: лишние аргументы в операции или неверный формат")

                if operator == 'm':
                    self._stack.push(min(a, b))
                else:
                    self._stack.push(max(a, b))

            elif char in ['(', ',']:
                pass
            else:
                raise ValueError(f"Ошибка: неожиданный символ '{char}'")

            i += 1

        if self._stack.is_empty():
            raise ValueError("Ошибка: выражение не дало результата")

        result = self._stack.pop()

        if not self._stack.is_empty():
            raise ValueError("Ошибка: в выражении лишние аргументы или неполные операции")

        return result



class MiniMaxConsole:
    """Интерфейс командной строки для ввода и расчета выражения."""

    def run(self):
        """Запускает калькулятор минимума и максимума."""
        print("Калькулятор минимума и максимума")
        print("Введите выражение, например: M(15,m(16,8))")
        print("Числа для ввода должны быть положительными и без пробелов.")

        while True:
            expr = input("Введите выражение: ").strip()

            if not expr:
                print("Ошибка: пустая строка. Попробуйте снова.")
                continue

            parser = MiniMaxParser(expr)

            try:
                result = parser.evaluate()
                print(f"Результат: {result}")
                break
            except ValueError as e:
                print(e)
                print("Попробуйте ввести выражение снова.")


if __name__ == "__main__":
    MiniMaxConsole().run()


