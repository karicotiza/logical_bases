import typing

from file import File


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
