import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class GeneticAlgorithm:
    def __init__(self, pop_size, generations, lower_bound, upper_bound, mutation_rate):
        self.pop_size = pop_size
        self.generations = generations
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.mutation_rate = mutation_rate
        self.population = []

    def fitness(self, x):
        return x**2 - 5 * x + 6

    def initialize_population(self):
        self.population = [random.uniform(self.lower_bound, self.upper_bound) for _ in range(self.pop_size)]

    def select_parents(self):
        tournament_size = 3
        selected = random.sample(self.population, tournament_size)
        selected.sort(key=lambda x: self.fitness(x))
        return selected[0], selected[1]

    def crossover(self, parent1, parent2):
        alpha = random.uniform(0, 1)
        child1 = alpha * parent1 + (1 - alpha) * parent2
        child2 = (1 - alpha) * parent1 + alpha * parent2
        return child1, child2

    def mutate(self, child):
        if random.random() < self.mutation_rate:
            mutation = random.uniform(-1, 1)
            child += mutation
            child = max(min(child, self.upper_bound), self.lower_bound)
        return child

    def evolve(self):
        self.initialize_population()
        best_solution = None
        best_fitness_value = float('inf')
        results = []

        for generation in range(self.generations):
            self.population.sort(key=lambda x: self.fitness(x))
            new_population = [self.population[0]]

            while len(new_population) < self.pop_size:
                parent1, parent2 = self.select_parents()
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))

            self.population = new_population[:self.pop_size]

            current_best = min(self.population, key=lambda x: self.fitness(x))
            current_best_fitness = self.fitness(current_best)

            if current_best_fitness < best_fitness_value:
                best_solution = current_best
                best_fitness_value = current_best_fitness

            results.append((generation + 1, current_best, current_best_fitness))

        return best_solution, best_fitness_value, results


def run_ga():
    try:
        pop_size = int(pop_size_var.get())
        generations = int(generations_var.get())
        lower_bound = float(lower_bound_var.get())
        upper_bound = float(upper_bound_var.get())
        mutation_rate = float(mutation_rate_var.get())

        if not (0 <= mutation_rate <= 1):
            raise ValueError("Mutation rate must be between 0 and 1.")

        ga = GeneticAlgorithm(pop_size, generations, lower_bound, upper_bound, mutation_rate)
        best_solution, best_fitness, results = ga.evolve()

        # Display results in the result text area
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Optimal Solution Found:\n")
        result_text.insert(tk.END, f"Best Solution: {best_solution:.5f}\nFitness Value: {best_fitness:.5f}\n\n")
        result_text.insert(tk.END, f"Evolution Progress:\n")
        for gen, sol, fit in results:
            result_text.insert(tk.END, f"Generation {gen}: Best Solution = {sol:.5f}, Fitness = {fit:.5f}\n")

    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Error: {e}")


# GUI Setup
root = tk.Tk()
root.title("Professional Genetic Algorithm GUI")
root.geometry("800x600")
root.configure(bg="#2c3e50")

# Header Section
header = tk.Label(root, text="Genetic Algorithm Optimization", font=("Helvetica", 20, "bold"), bg="#34495e", fg="#ecf0f1")
header.pack(pady=20)

# Input Frame
input_frame = tk.Frame(root, bg="#2c3e50")
input_frame.pack(pady=10)

# Input Fields and Labels
fields = [
    ("Population Size:", "pop_size_var"),
    ("Number of Generations:", "generations_var"),
    ("Lower Bound:", "lower_bound_var"),
    ("Upper Bound:", "upper_bound_var"),
    ("Mutation Rate (0 to 1):", "mutation_rate_var"),
]

variables = {}
for i, (label_text, var_name) in enumerate(fields):
    tk.Label(input_frame, text=label_text, font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1").grid(row=i, column=0, padx=10, pady=5, sticky="w")
    variables[var_name] = tk.StringVar()
    ttk.Entry(input_frame, textvariable=variables[var_name], width=30).grid(row=i, column=1, padx=10, pady=5)

# Map variables
pop_size_var = variables["pop_size_var"]
generations_var = variables["generations_var"]
lower_bound_var = variables["lower_bound_var"]
upper_bound_var = variables["upper_bound_var"]
mutation_rate_var = variables["mutation_rate_var"]

# Button to Run Algorithm
run_button = ttk.Button(root, text="Run Genetic Algorithm", command=run_ga)
run_button.pack(pady=10)

# Results Frame
results_frame = tk.Frame(root, bg="#34495e", relief="ridge", bd=2)
results_frame.pack(padx=20, pady=20, fill="both", expand=True)

results_label = tk.Label(results_frame, text="Results", font=("Helvetica", 16, "bold"), bg="#34495e", fg="#ecf0f1")
results_label.pack(pady=10)

# Text Box for Results
result_text = tk.Text(results_frame, wrap="word", font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", height=15)
result_text.pack(padx=10, pady=10, fill="both", expand=True)

# Add a Scrollbar
scrollbar = ttk.Scrollbar(results_frame, command=result_text.yview)
result_text.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Start the GUI event loop
root.mainloop()
