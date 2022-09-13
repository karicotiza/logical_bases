import pandas as pd


class FuzzyImplicationTable:
    def __init__(self, p: dict, v: dict) -> None:
        self.columns = ["Ф(x,y)"] + list(v.keys())
        self.table = self.calculate(p)

    def calculate(self, p: dict) -> pd.DataFrame:
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


if __name__ == "__main__":
    p = {}
    v = {}
    b = {}

    print(
        "Заполнение множества P, вводите пары значений через запятую, по одной паре на строку.\n"
        "Для завершения введите пустую строку"
    )

    while True:
        user_input = str(input("Ввод: ")).replace(" ", "").split(",")
        if len(user_input) == 2:
            if 0 <= float(user_input[1]) <= 1:
                if user_input[0] in p.keys():
                    print("Значение перезаписано")
                p[user_input[0]] = float(user_input[1])
            else:
                print("Ввод не соответствует правилам")
        elif len(user_input) == 1 and user_input[0] == "":
            print("Множество заполнено\n")
            break
        else:
            print("Ввод не соответствует правилам")

    print(
        "Заполнение множества V, вводите пары значений через запятую, по одной паре на строку.\n"
        "Для завершения введите пустую строку"
    )

    while True:
        user_input = str(input("Ввод: ")).replace(" ", "").split(",")
        if len(user_input) == 2:
            if 0 <= float(user_input[1]) <= 1:
                if user_input[0] in p.keys():
                    print("Эта пара уже находится в множестве P")
                else:
                    if user_input[0] in v.keys():
                        print("Значение перезаписано")
                    v[user_input[0]] = float(user_input[1])
            else:
                print("Ввод не соответствует правилам")
        elif len(user_input) == 1 and user_input[0] == "":
            print("Множество заполнено\n")
            break
        else:
            print("Ввод не соответствует правилам")

    print(
        "Заполнение множества B, заполните пары."
    )

    for key, value in p.items():
        while True:
            try:
                user_input = float(input(f"Ввод: {key}, "))
                if 0 <= user_input <= 1:
                    b[key] = user_input
                    break
                else:
                    print("Ввод не соответствует правилам")
            except ValueError:
                print("Ввод не соответствует правилам")
    print("Множество заполнено\n")

    print(FuzzyImplicationTable(p, v), "\n")

    print(FuzzyDirectConclusionTable(v, p, FuzzyImplicationTable(p, v).table), "\n")
    print(FuzzyDirectConclusionTable(v, p, FuzzyImplicationTable(p, v).table).get_max(), "\n")

    print(FuzzyDirectConclusionTable(v, b, FuzzyImplicationTable(p, v).table), "\n")
    print(FuzzyDirectConclusionTable(v, b, FuzzyImplicationTable(p, v).table).get_max(), "\n")
