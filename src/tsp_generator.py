import random
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent / 'datasets'


def generate_tsp_file(n: int, filename: str) -> None:
    content = [
        f"NAME: custom{n}",
        "COMMENT: Randomly generated TSP problem",
        "TYPE: TSP",
        f"DIMENSION: {n}",
        "EDGE_WEIGHT_TYPE: EUC_2D",
        "NODE_COORD_SECTION"
    ]

    points = set()

    for i in range(1, n + 1):
        while True:
            x = random.randint(1, 1000)
            y = random.randint(1, 1000)
            if (x, y) not in points:
                break

        content.append(f"{i} {x}.0 {y}.0")
        points.add((x, y))

    content.append("EOF")
    content.append("")

    with open(base_path / filename, 'w') as f:
        f.write('\n'.join(content))

    print(f"Файл {filename} успешно создан с {n} вершинами.")


def main() -> None:
    for n in (10, 11, 20, 21, 50, 51, 100, 101):
        generate_tsp_file(n, f"custom{n}.tsp")


if __name__ == '__main__':
    main()
