from equation_system import EquationSystem


class EquationSolver:
    """
    Класс для решения системы уравнений
    """

    @staticmethod
    def solve_system(equation_system_: EquationSystem) -> [list[str] | None]:
        left_side = []
        right_side = []

        for index, equation_ in enumerate(equation_system_.get_equations(), start=0):
            left_result, right_result = EquationSolver.solve_equation(equation_)
            if not left_result and not right_result:
                return None

            if left_result is None:
                left_result = [1.0, [right_result[0], right_result[0]]]
            if right_result is None:
                right_result = [1.0, [left_result[0], left_result[0]]]

            if not index:
                left_side = left_result
                right_side = right_result
            else:
                if left_result[0] == left_side[0] or left_result[1][1] == left_side[1][1]:
                    if left_result[0] < left_side[0]:
                        left_side = left_result
                else:
                    return None

                if right_result[0] == right_side[0] or right_result[1][1] == right_side[1][1]:
                    if right_result[0] < right_side[0]:
                        right_side = right_result
                else:
                    return None

        # Не тестировал, может испортить ответ
        # if left_side[0] < left_side[1][1]:
        #     left_side[1][0] = left_side[1][1]
        if right_side[0] >= right_side[1][1]:
            right_side[1][0] = right_side[1][1]

        return left_side, right_side

    @staticmethod
    def solve_equation(equation_: str):
        split = equation_.split(" ")

        left_constant = float(split[0])
        right_constant = float(split[4])
        answer = float(split[8])

        # Первая строка дерева
        print(f"{equation_:^120}")

        # Ответ есть. Хотя бы одна часть при умножении даст верный ответ
        if max(left_constant, right_constant) >= answer:
            # Если ответ делённый на константу в какой-либо
            # части уравнения > 1, то переменная в этой
            # части не влияет на ответ
            left_max = answer / left_constant
            right_max = answer / right_constant

            if left_max > 1:
                left_max = None

            if right_max > 1:
                right_max = None

            # Если переменная A(x1) влияет на ответ
            if left_max is not None:
                if right_max:
                    left_result = [left_max, [0.0, right_max]]
                else:
                    left_result = [left_max, [0.0, 1.0]]
            # Иначе
            else:
                left_result = None

            # Если переменная A(x2) влияет на ответ
            if right_max is not None:
                if left_max:
                    right_result = [right_max, [0.0, left_max]]
                else:
                    right_result = [right_max, [0.0, 1.0]]
            # Иначе
            else:
                right_result = None

            # Вторая строка дерева
            print(
                f"{'A(x1) = ' + str(left_max):^60}",
                f"{'A(x2) = ' + str(right_max):^60}"
            )

            # Третья строка дерева
            string = ''

            if left_result:
                string += f"{'A(x1) = ' + str(left_result[0]) + ', A(x2) = ' + str(left_result[1]):^60}"
            else:
                string += f"{' ':^60}"
            if right_result:
                string += f"{'A(x1) = ' + str(right_result[1]) + ', A(x2) = ' + str(right_result[0]):^60}"

            print(string)
            print()

            return left_result, right_result

        # Ответ не может быть получен. Максимум из левой части всегда будет меньше ответа
        else:
            # Вторая строка дерева
            print(f"{'A(x1) = None':^60} {'A(x2) = None':^60}")
            print()

            return None, None
