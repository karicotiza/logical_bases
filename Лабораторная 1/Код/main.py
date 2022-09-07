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

            # noinspection PyTypeChecker
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


class FuzzyDirectConclusion:
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
            # print(column, self.table[column].max())
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
        pass
    else:
        raise ValueError("Wrong mode")


def fuzzy_implication(x: float, y: float) -> float:
    if y >= x:
        return 1
    else:
        return y


if __name__ == "__main__":
    p = {"a": 0, "b": 0.3, "c": 1}
    v = {"f": 1, "d": 0.5, "t": 0}
    b = {"a": 0.8, "b": 0.3, "c": 0.9}

    print(FuzzyImplicationTable(p, v), "\n")

    print(FuzzyDirectConclusion(v, p, FuzzyImplicationTable(p, v).table), "\n")
    print(FuzzyDirectConclusion(v, p, FuzzyImplicationTable(p, v).table).get_max(), "\n")

    print(FuzzyDirectConclusion(v, b, FuzzyImplicationTable(p, v).table), "\n")
    print(FuzzyDirectConclusion(v, b, FuzzyImplicationTable(p, v).table).get_max(), "\n")
