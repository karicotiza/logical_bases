import operator
import itertools

from equation_system import EquationSystem
from log_unit import LogUnit


class EquationSolver:
    """
    Класс для решения системы уравнений
    """

    log_unit = LogUnit

    @staticmethod
    def solve_system(equation_system_: EquationSystem) -> [list[str] | str]:
        """
        Основной метод класса,
        решает систему уравнений

        :param equation_system_: Система уравнений.
        :return: Если есть решение - возвращает список
        с допустимыми значениями переменных. Если
        решения нет возвращает строку со значением
        "Нет ответа"
        """

        equations = EquationSolver.__sort_equations(equation_system_)
        variables = {key: set() for key in equation_system_.get_variables()[1]}

        equation: dict
        for equation in equations:
            variables = EquationSolver.get_brute_force_range(equation, variables)
            variables = EquationSolver.adjust_range_based_on_solution_of_equation(equation, variables)
            if not variables:
                return "Нет ответа"

        return [
            f"({min(value)} <= {key} <= {max(value)})"
            for key, value
            in variables.items()
        ]

    @staticmethod
    def __sort_equations(equation_system_: EquationSystem) -> dict[str: int, str: int, str: str]:
        """
        Сортирует уравнения в порядке:
        1. Наименьшее количество переменных
        2. Требуется наименьшая точность

        :param equation_system_: система уравнений.
        :return: отсортированный список
        уравнений
        """
        equations = []

        for equation in equation_system_.get_as_python_code():
            equations.append(equation)

        return sorted(equations, key=operator.itemgetter('variables', 'precision'))

    @staticmethod
    def get_brute_force_range(equation_: dict, variables: dict[str: set]) -> dict[str: set[float]]:
        """
        Возвращает значения, которые нужно перебрать

        :param equation_: строка у уравнением.
        :param variables: все переменные и их
        диапазоны - проверенные и нет
        :return:
        """

        for variable in variables.keys():
            if variable in equation_["code"]:
                if not variables[variable]:
                    variables[variable] = set(
                        number / (10 ** equation_["precision"])
                        for number
                        in range(0, 11 ** equation_["precision"])
                    )

                else:
                    variables[variable] = set(
                        number / (10 ** equation_["precision"])
                        for number
                        in range(
                            int(min(variables[variable]) * 10 ** equation_["precision"]),
                            int(max(variables[variable]) * 10 ** equation_["precision"]) + 1,
                        )
                    )

        return variables

    @staticmethod
    def adjust_range_based_on_solution_of_equation(equation_: dict, variables: dict[str: set]):
        """
        Изменение диапазонов переменных.
        Изменение происходит за счёт проверки
        выполнения уравнения с подставленными
        значениями: решение истинно - диапазон
        остаётся; решение ложно - диапазон
        удаляется из множества диапазонов

        :param equation_: строка с уравнением.
        :param variables: все переменные и их
        диапазоны - проверенные и нет
        :return:
        """

        if equation_["variables"] == 1:
            memory = EquationSolver.solve_equation_with_one_variable(equation_, variables)
        else:
            variables_for_this_equation = {}
            for variable in variables.keys():
                if variable in equation_["code"]:
                    variables_for_this_equation[variable] = variables[variable]

            memory = EquationSolver.solve_equation_with_multiple_variables(equation_, variables_for_this_equation)

        answers = {}
        for element in memory:
            for key, value in element.items():
                if key not in answers:
                    answers[key] = {value}
                else:
                    answers[key].add(value)

        for key, value in variables.items():
            result = answers.get(key, None)
            if result:
                variables[key] = value & result

        if not answers:
            return False

        return variables

    @staticmethod
    def solve_equation_with_one_variable(equation_: dict, variables: dict):
        """
        Проверка диапазонов на уравнении
        с одной переменной

        :param equation_: строка с уравнением.
        :param variables: все переменные и их
        диапазоны - проверенные и нет.
        :return: множество верных диапазонов
        """

        memory = []

        for variable in variables.keys():
            if variable in equation_["code"]:
                code = equation_["code"]
                for value in variables[variable]:
                    code = code.replace(variable, "LogUnit(" + str(value) + ")")

                    if eval(code):
                        memory.append({variable: value})

        return memory

    @staticmethod
    def solve_equation_with_multiple_variables(equation_: dict, variables: dict):
        """
                Проверка диапазонов на уравнении
                с несколькими переменными

                :param equation_: строка с уравнением.
                :param variables: все переменные и их
                диапазоны - проверенные и нет.
                :return: множество верных диапазонов
                """

        memory = []

        keys, values = zip(*variables.items())
        all_combinations = [dict(zip(keys, value)) for value in itertools.product(*values)]
        for values in all_combinations:
            code = equation_["code"]
            for variable, value in values.items():
                code = code.replace(variable, "LogUnit(" + str(value) + ")")

            if eval(code):
                memory.append(values)

        return memory
