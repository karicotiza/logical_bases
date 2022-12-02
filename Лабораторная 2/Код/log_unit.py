class LogUnit:
    """
    Класс для перезаписи методов "and" и "or" под
    нужды нечёткой логики
    """

    ROUND = 1

    def __init__(self, value_: int):
        """
        Инициализация объекта

        :param value_: значение числа
        """
        self.value = value_

    def __and__(self, other):
        """
        Операция "Нечёткое И"

        :param other: значение справа от знака |.
        :return: экземпляр класса LogUnit со
        значением результата операции
        """
        result = round((self.value * other.value), LogUnit.ROUND)
        return LogUnit(min(result, 1))

    def __or__(self, other):
        """
        Операция "Нечёткое ИЛИ"

        :param other: значение справа от знака &.
        :return: экземпляр класса LogUnit со
        значением результата операции
        """
        return LogUnit(max(self.value, other.value))

    def __eq__(self, other):
        """
        Операция сравнения

        :param other: значение справа от знака ==
        :return: Булева переменная (True или False)
        """
        if self.value == other.value:
            return True
        else:
            return False

    def __str__(self):
        """
        Вывод в виде строки

        :return: строку со значением
        """
        return str(self.value)
