import pandas as pd
import pathlib
import re
import sys


class FuzzyImplicationTable:
    def __init__(self, p: dict, v: dict) -> None:
        self.columns = ["Ф(x,y)"] + list(v.keys())
        self.table = self.calculate(p, v)

    def calculate(self, p: dict, v: dict) -> pd.DataFrame:
        table = pd.DataFrame()
        for key, x in p.items():
            data = []
            for y in v.values():
                data.append(fuzzy_implication(x, y))

            table = pd.concat(
                [
                    table,
                    pd.DataFrame(
                        columns=self.columns,
                        data=[
                            [key] + data
                        ]
                    )
                ],
                ignore_index=True,
                axis=0
            )

        return table

    def __str__(self) -> str:
        return self.table.to_string(index=False)


class FuzzyDirectConclusionTable:
    def __init__(self, v: dict, b: dict, fuzzy_implication_table: pd.DataFrame) -> None:
        self.columns = ["Ф(x,y) ∧ B(x)"] + list(v.keys())
        self.table = self.calculate(b, fuzzy_implication_table)

    def calculate(self, b: dict, fuzzy_implication_table: pd.DataFrame) -> pd.DataFrame:
        table = pd.DataFrame()

        for index in range(len(b.values())):
            data = []

            for cell in fuzzy_implication_table.iloc[index][1:]:
                data.append(
                    triangular_norm(
                        list(b.values())[index],
                        cell
                    )
                )

            table = pd.concat(
                [
                    table,
                    pd.DataFrame(
                        columns=self.columns,
                        data=[
                            [list(b.keys())[index]] + data
                        ]
                    )
                ],
                ignore_index=True,
                axis=0
            )

        return table

    def get_max(self) -> str:
        result = "{"
        for column in self.table.columns[1:]:
            result += f"({column}, {self.table[column].max()})"
        return result + "}"

    def __str__(self) -> str:
        return self.table.to_string(index=False)


def triangular_norm(x: float, y: float, mode: str = "gentzen") -> float:
    if mode == "gentzen":
        return min(x, y)
    elif mode == "godel":
        return x * y
    elif mode == "lukasiewicz":
        return max((x + y - 1), 0)
    elif mode == "drastic":
        if x == 1:
            return y
        if y == 1:
            return x
        else:
            return 0
    else:
        print("Wrong mode")


def fuzzy_implication(x: float, y: float, mode: str = "gentzen") -> float:
    if mode == "gentzen":
        if y >= x:
            return 1
        else:
            return y
    elif mode == "godel":
        pass
    elif mode == "lukasiewicz":
        pass
    elif mode == "drastic":
        pass
    else:
        print("Wrong mode")


def validate(line: str) -> bool:
    pattern_1 = r"^\(?[a-z]+, [0|1]\)"
    pattern_2 = r"^\(?[a-z]+, 0\.[1-9]\)"

    if re.match(pattern_1, line) or re.match(pattern_2, line):
        return True


def count_dicts(read_path: pathlib.Path) -> int:
    with read_path.open() as file:
        return file.read().count("\n\n") + 1


def check_for_double_new_lines(read_path: pathlib.Path) -> None:
    with read_path.open() as file:
        try:
            index = file.read().index("\n\n\n")
            if index:
                raise SyntaxError(f"no more than one new line between sets")
        except ValueError:
            pass


def from_file(read_path: pathlib.Path) -> list[dict]:
    number_of_dicts = count_dicts(read_path)
    check_for_double_new_lines(read_path)
    memory = [{} for _ in range(number_of_dicts)]

    with read_path.open() as file:
        counter = 0
        for index, line in enumerate(file):
            line = line.replace("\n", "")
            if validate(line):
                key, value = line[1:-1].split(", ")
                memory[counter][key] = float(value)
            elif len(line) == 0:
                counter += 1
            else:
                raise SyntaxError(f"wrong syntax at line {index}: {line}")
    return memory


def to_file(write_path: pathlib.Path):
    sys.stdout = open(write_path, "w", encoding="utf-8")


if __name__ == "__main__":
    try:
        p_dict, v_dict, b_dict = from_file(pathlib.Path(sys.argv[1]))
        to_file(pathlib.Path(sys.argv[2]))
    except IndexError:
        p_dict, v_dict, b_dict = from_file(pathlib.Path("input2.txt"))
        to_file(pathlib.Path("output2.txt"))

    print(FuzzyImplicationTable(p_dict, v_dict), "\n")

    print(FuzzyDirectConclusionTable(v_dict, p_dict, FuzzyImplicationTable(p_dict, v_dict).table), "\n")
    print(FuzzyDirectConclusionTable(v_dict, p_dict, FuzzyImplicationTable(p_dict, v_dict).table).get_max(), "\n")

    print(FuzzyDirectConclusionTable(v_dict, b_dict, FuzzyImplicationTable(p_dict, v_dict).table), "\n")
    print(FuzzyDirectConclusionTable(v_dict, b_dict, FuzzyImplicationTable(p_dict, v_dict).table).get_max(), "\n")
