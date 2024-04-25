import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import os
from scipy import stats


class DiceRoll:
    def __init__(self, filename="numbers.txt"):
        self.filename = filename
        self.ani = None
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.fig = plt.figure(figsize=(10, 8))

        self.ax_hist = self.fig.add_subplot(2, 3, 1)
        self.ax_qq = self.fig.add_subplot(2, 3, 2)
        self.ax_stats = self.fig.add_subplot(2, 3, 4)
        self.ax_trial_count = self.fig.add_subplot(2, 3, 5)
        self.ax_original_dist = self.fig.add_subplot(2, 3, (3, 6))

        self.trial_count = 0

    def generate_and_append_numbers(self):
        numbers = [random.randint(1, 6) for _ in range(7)]
        with open(self.filename, "a") as file:
            file.write(' '.join(map(str, numbers)) + '\n')
        self.trial_count += 1

    def read_numbers_from_file(self):
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
            return [list(map(int, line.strip().split())) for line in lines]
        except FileNotFoundError:
            return []

    def update_plots(self, frame):
        self.generate_and_append_numbers()
        lines = self.read_numbers_from_file()
        means = [np.mean(line) for line in lines if line]
        all_rolls = [roll for line in lines for roll in line]
        counts = [all_rolls.count(i) for i in range(1, 7)]

        self.ax_hist.clear()
        self.ax_hist.hist(means, bins=range(1, 7), edgecolor='black', color='blue', alpha=0.75)
        self.ax_hist.set_title('distribution of means')

        self.ax_qq.clear()
        stats.probplot(means, dist="norm", plot=self.ax_qq)
        self.ax_qq.set_title('Probability Plot')
        self.ax_qq.set_xlabel('Theoretical quantiles')
        self.ax_qq.set_ylabel('Ordered Values')

        _, p_value = stats.shapiro(lines[len(lines) - 1])

        self.ax_stats.clear()
        self.ax_stats.set_title("normality test p-value")
        self.ax_stats.text(0.5, 0.5, f'p-value: {p_value}', fontsize=10, ha='center', va='center')
        self.ax_stats.axis('off')

        self.ax_trial_count.clear()
        self.ax_trial_count.text(0.5, 0.5, f'{self.trial_count}', fontsize=50, ha='center', va='center')
        self.ax_trial_count.axis('off')

        self.ax_original_dist.clear()
        self.ax_original_dist.bar(np.arange(1, 7), counts, color='blue', edgecolor='black', width=1.0, alpha=0.75)
        self.ax_original_dist.set_title('distribution of outputs')

        self.fig.canvas.draw()

    def start_animation(self):
        self.ani = FuncAnimation(self.fig, self.update_plots, interval=500)
        plt.tight_layout()
        plt.show()


dice_roll_simulator = DiceRoll()
dice_roll_simulator.start_animation()
