import operator
import itertools

from equation_system import EquationSystem
from log_unit import LogUnit


class EquationSolver:
    log_unit = LogUnit

    @staticmethod
    def solve_system(equation_system_: EquationSystem):
        equations = EquationSolver.sort_equations(equation_system_)
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
    def sort_equations(equation_system_: EquationSystem) -> dict[str: int, str: int, str: str]:
        equations = []

        for equation in equation_system_.get_as_python_code():
            equations.append(equation)

        return sorted(equations, key=operator.itemgetter('variables', 'precision'))

    @staticmethod
    def get_brute_force_range(equation_: dict, variables: dict[str: set]):

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
