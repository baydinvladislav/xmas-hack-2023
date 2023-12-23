import pandas as pd
import matplotlib.pyplot as plt


def show_three_intervals_diagram(file_path: str) -> None:
    data = pd.read_csv(file_path)

    plt.figure(figsize=(12, 6))
    plt.bar(data['week_number'], data['movement_count'], color='skyblue')
    plt.xlabel('Порядковый номер недели')
    plt.ylabel('Количество передвежений')
    plt.title('Вечерний час пик')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()


def show_top_loaded_hours_diagram(file_path: str) -> None:
    data = pd.read_csv(file_path)

    plt.figure(figsize=(12, 6))
    plt.bar(data['hour_of_day'], data['total_connections'], color='orange')
    plt.xlabel('Час в сутках')
    plt.ylabel('Количество перемещений')
    plt.title('Самые нагруженные часы в году')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(round(x)))))
    plt.show()
