import typing


class File:
    """
    Класс для возможности проходить циклом
    по строкам файла с уравнением
    """

    __MODE = "r"
    __ENCODING = "utf-8"

    def __init__(self, path_: str = "data/input.txt") -> None:
        """
        Инициализация объекта

        :param path_: Путь к файлу в формате .txt
        """

        self.__path = path_

    def __iter__(self) -> typing.Generator[str, None, None]:
        """
        Функция для возможности итерации посредством ключевого
        слова for

        :return: Строку с уравнением в том виде,
        в котором она находится в файле
        """

        with open(
                self.__path,
                mode=self.__MODE,
                encoding=self.__ENCODING
        ) as file:
            for equation in file.read().splitlines():
                yield equation
