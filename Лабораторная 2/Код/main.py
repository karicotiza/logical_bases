from equation_system import EquationSystem
from file import File
from equation_solver import EquationSolver

eq_solver = EquationSolver.solve_system(
    EquationSystem(
        File("data/input.txt")
    )
)

print("(" + str("/\\").join(eq_solver) + ")")
