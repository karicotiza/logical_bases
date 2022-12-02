from equation_system import EquationSystem
from file import File
from equation_solver import EquationSolver

if __name__ == "__main__":
    result = EquationSolver.solve_system(
        EquationSystem(
            File("data/input.txt")
        )
    )

    result = "(" + str(" /\\ ").join(result) + ")"

    print(result)
