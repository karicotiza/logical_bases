from equation_system import EquationSystem
from file import File
from equation_solver import EquationSolver

if __name__ == "__main__":
    file = File("data/input.txt")
    equation_system = EquationSystem(file)
    result = EquationSolver.solve_system(equation_system)

    if result:
        if (
                result[1][1][0] <= result[0][0] <= result[1][1][1]
        ) and (
                result[0][1][0] <= result[1][0] <= result[0][1][1]
        ):
            print(
                f"((A(x1) = {result[0][0]}) /\\ ({result[0][1][0]} <= A(x2) <= {result[0][1][1]}))"
            )
        else:
            print(
                f"((A(x1) = {result[0][0]}) /\\ ({result[0][1][0]} <= A(x2) <= {result[0][1][1]})"
                f" \\/ "
                f"({result[1][1][0]} <= A(x1) <= {result[1][1][1]}) /\\ (A(x2) = {result[1][0]}))"
            )
    else:
        print("Нет решения")

    # if result:
    #     result = "(" + str(" /\\ ").join(result) + ")"
    # else:
    #     result = "Нет верного ответа"
    # print(result)
