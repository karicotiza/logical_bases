from equation_system import EquationSystem
from file import File
from equation_solver import EquationSolver

if __name__ == "__main__":
    file = File("data/input.txt")
    equation_system = EquationSystem(file)
    result = EquationSolver.solve_system(equation_system)

    if result:
        result = "(" + str(" /\\ ").join(result) + ")"
    else:
        result = "Нет верного ответа"
    print(result)
