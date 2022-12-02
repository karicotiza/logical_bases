import typing

from file import File
from log_unit import LogUnit


class EquationSystem:
    """
    Класс для хранения и обработки всей системы уравнений
    полученной из файла
    """

    def __init__(self, file_: File = File()) -> None:
        """
        Инициализация объекта

        :param file_: Экземпляр объекта File
        """
        self.__equations = self.__normalize_spaces(equation for equation in file_)
        self.__multiplier = self.__get_round_value()
        LogUnit.ROUND = self.__multiplier

    def get_equations(self) -> typing.Generator[str, None, None]:
        """
        Функция для возврата уравнений в том
        виде, в котором они поступили в объект
        класс

        :return: генератор уравнений,
        уравнения имеют тип строка
        """

        for equation in self.__equations:
            yield equation

    def __get_round_value(self) -> int:
        """
        Функция для поиска значения, до которого будут
        округляться числа с плавающей запятой

        :return: значение до которого будут округляться
        числа. Значение имеет целочисленный тип
        """

        memory = 0

        for equation in self.get_equations():
            multiplier = max(
                len(number)
                for number
                in equation.replace(".", "").split(" ")
                if number.isalnum()
            )
            if multiplier > memory:
                memory = multiplier

        return memory

    @staticmethod
    def __normalize_spaces(equations_: typing.Generator[str, None, None]) -> list[str]:
        """
        Функция для нормализации количества пробелов.
        Убирает лишние, добавляет отсутствующие.
        Программа чувствительна к количеству пробелов.

        :return: генератор уравнений, с типом строка
        """

        substitutions = {
            "/~\\": " /~\\ ",
            "\\~/": " \\~/ ",
            "=": " = ",
        }

        memory = []

        for equation in equations_:
            equation = equation.replace(" ", "")
            for key, value in substitutions.items():
                equation = equation.replace(key, value)
            memory.append(equation)

        return memory

    @staticmethod
    def __convert_floats_to_log_ints(
            equation_: str
    ) -> str:
        """
        Функция для обёртки чисел с плавающей запятой
        в строке с уравнением, в экземпляр класс LogUnit

        :param equation_: строка с уравнением.
        :return: строка с уравнением, в котором
        числа с плавающей обёрнуты как экземпляр
        класс LogUnit
        """
        memory = []

        for element in equation_.split(" "):
            try:
                element = "LogUnit(" + str(float(element)) + ")"
            except ValueError:
                pass
            memory.append(element)
        equation = str(" ").join(memory)

        return equation

    @staticmethod
    def __normalize_operators(equation_: str) -> str:
        """
        Функция для замены логических операторов
        из стандарта синтаксиса нечёткой логики
        в стандарт синтаксиса python

        :param equation_: строка с уравнением.
        :return: строка с уравнением, в котором
        заменены логические операторы
        """
        substitutions = {
            "/~\\": "&",
            "\\~/": "|",
            "=": "==",
        }

        for key, value in substitutions.items():
            equation_ = equation_.replace(key, value)
        return equation_

    def get_as_python_code(self) -> typing.Generator[str, None, None]:
        """
        Функция для перевода строки с
        уравнением в код, который может
        быть выполнен языком python.
        Нужно, потому, что я не успеваю
        сделать обратную польскую нотацию
        для решения уравнений.

        :return:
        """
        for equation in self.get_equations():
            split = equation.split(" ")

            memory = {
                "variables": len([element for element in split if element[0].isalpha()]),
                "precision": len(split[-1]) - 2
            }

            equation = self.__convert_floats_to_log_ints(equation)
            equation = self.__normalize_operators(equation)

            memory["code"] = equation

            yield memory

    def get_variables(self) -> tuple[int, list[str]]:
        """
        Функция для возврата количества
        переменных и самих переменных во
        всей системе

        :return: целочисленное значение равное
        количеству переменных в системе и список
        с переменными в виде строк
        """
        number_of_variables, variables = 0, []

        for equation in self.get_equations():
            for element in equation.split(" "):
                if element[0].isalpha():
                    if element not in variables:
                        variables.append(element)
                        number_of_variables += 1

        return number_of_variables, variables
