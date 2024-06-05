from tkinter import Tk, Frame, Label, Entry, Button, Text, Scrollbar, messagebox, Toplevel
from fractions import Fraction
from sympy import Matrix

#CODE BY SWAT
class CramerSolver:
    def __init__(self):
        self.n = 0
        self.coeff_entries = []
        self.b_entries = []
        self.root = Tk()
        self.root.title("Resolución de Sistema de Ecuaciones por Cramer by SWAT")
        self.root.geometry("500x400")  # Tamaño específico de la ventana principal
        self.coeff_frame = Frame(self.root)
        self.coeff_frame.pack(fill="both", expand=True)

        # Textos de pantalla
        self.eq_label = Label(self.coeff_frame, text="Dimension de la matriz:")
        self.eq_label.grid(row=0, column=0, padx=5, pady=5)

        self.eq_entry = Entry(self.coeff_frame, width=6)
        self.eq_entry.grid(row=0, column=1, padx=5, pady=5)

        self.create_button = Button(self.coeff_frame, text="Establecer matriz", command=self.crear_casillas)
        self.create_button.grid(row=0, column=2, padx=5, pady=5)

        self.solve_button = Button(self.coeff_frame, text="Resolver", command=self.resolver_sistema)
        self.solve_button.grid(row=0, column=3, padx=5, pady=5)

        self.centrar_ventana()  # Centrar la ventana en la pantalla

    def crear_casillas(self):
        try:
            self.n = int(self.eq_entry.get())
            if self.n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero positivo.")
            return

        # Eliminar las casillas existentes, si las hay
        for entry_row in self.coeff_entries:
            for entry in entry_row:
                entry.destroy()

        # Eliminar las casillas del vector b existentes, si las hay
        for entry in self.b_entries:
            entry.destroy()

        # Crear las nuevas casillas de entrada
        self.coeff_entries.clear()
        for i in range(self.n):
            row_entries = []
            for j in range(self.n):
                entry = Entry(self.coeff_frame, width=10)
                entry.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")
                row_entries.append(entry)
            self.coeff_entries.append(row_entries)

        self.b_entries.clear()
        for i in range(self.n):
            entry = Entry(self.coeff_frame, width=10)
            entry.grid(row=i + 1, column=self.n, padx=5, pady=5, sticky="nsew")
            self.b_entries.append(entry)

        # Actualizar la geometría de la ventana para ajustarse a las nuevas casillas
        self.root.update()

    def resolver_sistema(self):
        # Obtener los coeficientes de las ecuaciones de las casillas de entrada
        coeficientes = []
        for row_entries in self.coeff_entries:
            fila = []
            for entry in row_entries:
                try:
                    valor = Fraction(entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido.")
                    return
                fila.append(valor)
            coeficientes.append(fila)

        # Obtener los valores del vector b
        b_values = []
        for entry in self.b_entries:
            try:
                valor = Fraction(entry.get())
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido para el vector b.")
                return
            b_values.append(valor)

        try:
            steps, solution = self.cramer(coeficientes, b_values)
            self.mostrar_resultados(steps, solution)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cramer(self, matrix, b):
        n = len(matrix)
        A = Matrix(matrix)
        B = Matrix(b)

        determinant = A.det()

        if determinant == 0:
            raise ValueError("La matriz es singular, no se puede resolver el sistema.")

        steps = []
        solution = []
        for i in range(n):
            A_i = A.copy()
            A_i[:, i] = B
            step = f"Paso {i + 1}:\n\n"
            step += f"Matriz A:\n{A_i}\n\n"
            step += f"Vector b:\n{B}\n\n"
            step += f"Determinante de A: {determinant}\n\n"
            determinant_i = A_i.det()
            step += f"Determinante de A{i + 1}: {Fraction(determinant_i).limit_denominator()}\n\n"
            solution_i = determinant_i / determinant
            step += f"Solución x{i + 1}: {Fraction(solution_i).limit_denominator()}\n\n"
            steps.append(step)
            solution.append(solution_i)

        return steps, solution

    def mostrar_resultados(self, steps, solution):
        # Crear la ventana de resultados
        results_window = Toplevel(self.root)
        results_window.title("Resultados")
        results_window.geometry("600x400")

        # Centrar la ventana en la pantalla
        self.centrar_ventana(results_window)

        results_frame = Frame(results_window)
        results_frame.pack(fill="both", expand=True)

        output_text = Text(results_frame)
        output_text.pack(fill="both", expand=True)

        scrollbar = Scrollbar(output_text)
        scrollbar.pack(side="right", fill="y")
        output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=output_text.yview)

        # Mostrar los pasos de resolución
        output_text.insert("end", "Pasos:\n\n")
        for step in steps:
            output_text.insert("end", step)

        # Mostrar la solución
        output_text.insert("end", "Solución:\n\n")
        for i, sol in enumerate(solution):
            output_text.insert("end", f"x{i + 1} = {Fraction(sol).limit_denominator()}\n")

        output_text.config(state="disabled")

    def centrar_ventana(self, ventana=None):
        if not ventana:
            ventana = self.root
        ventana.update_idletasks()
        ventana_width = ventana.winfo_width()
        ventana_height = ventana.winfo_height()
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        x = (screen_width // 2) - (ventana_width // 2)
        y = (screen_height // 2) - (ventana_height // 2)
        ventana.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")

solver = CramerSolver()
solver.root.mainloop()
        #SWAT


         

      
