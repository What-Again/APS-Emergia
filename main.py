import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

class EmergyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo de Emergia")
        self.root.geometry("600x600")

        self.transformities = {}
        self.inventory = []

        # Adicionar menu
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Importar CSV", command=self.import_csv)

    def create_widgets(self):
        # Seção de Transformidades
        transformity_frame = ttk.LabelFrame(self.root, text="Definir Transformidades", padding=(10, 10))
        transformity_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(transformity_frame, text="Fluxo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.flux_name_entry = ttk.Entry(transformity_frame, width=20)
        self.flux_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(transformity_frame, text="Transformidade (sej/unidade):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.transformity_entry = ttk.Entry(transformity_frame, width=20)
        self.transformity_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(transformity_frame, text="Adicionar Transformidade", command=self.add_transformity).grid(row=0, column=4, padx=5, pady=5)

        self.transformity_text = tk.Text(self.root, wrap="word", height=8, state="disabled")
        self.transformity_text.pack(fill="both", padx=10, pady=5)
        self.update_transformity_display()

        # Seção de Inventário
        inventory_frame = ttk.LabelFrame(self.root, text="Definir Inventário", padding=(10, 10))
        inventory_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(inventory_frame, text="Fluxo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.inventory_flux_entry = ttk.Entry(inventory_frame, width=20)
        self.inventory_flux_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(inventory_frame, text="Quantidade:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.inventory_quantity_entry = ttk.Entry(inventory_frame, width=20)
        self.inventory_quantity_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(inventory_frame, text="Adicionar ao Inventário", command=self.add_inventory_item).grid(row=0, column=4, padx=5, pady=5)

        self.inventory_text = tk.Text(self.root, wrap="word", height=8, state="disabled")
        self.inventory_text.pack(fill="both", padx=10, pady=5)
        self.update_inventory_display()

        # Botão de cálculo e resultados
        ttk.Button(self.root, text="Calcular Emergia", command=self.calculate_emergy).pack(pady=10)
        result_frame = ttk.LabelFrame(self.root, text="Resultados", padding=(10, 10))
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.result_text = tk.Text(result_frame, wrap="word", state="disabled", height=10)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)

    def import_csv(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")],
            title="Selecione um arquivo CSV"
        )
        if not filepath:
            return

        resposta = messagebox.askyesno(
            "Tipo de Dados",
            "Este arquivo contém Transformidades? (Sim para Transformidades, Não para Inventário)"
        )

        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler arquivo: {str(e)}")
            return

        if resposta:
            required = ['Fluxo', 'Transformidade']
            if not all(col in df.columns for col in required):
                messagebox.showerror("Erro", "CSV deve ter 'Fluxo' e 'Transformidade'")
                return
            success = 0
            for _, row in df.iterrows():
                flux = row['Fluxo']
                try:
                    trans = float(row['Transformidade'])
                    self.transformities[flux] = trans
                    success += 1
                except:
                    continue
            self.update_transformity_display()
            messagebox.showinfo("Sucesso", f"Importadas {success}/{len(df)} transformidades!")
        
        else:
            required = ['Fluxo', 'Quantidade']
            if not all(col in df.columns for col in required):
                messagebox.showerror("Erro", "CSV deve ter 'Fluxo' e 'Quantidade'")
                return
            success = 0
            for _, row in df.iterrows():
                flux = row['Fluxo']
                try:
                    quant = float(row['Quantidade'])
                    self.inventory.append({'Fluxo': flux, 'Quantidade': quant})
                    success += 1
                except:
                    continue
            self.update_inventory_display()
            messagebox.showinfo("Sucesso", f"Importados {success}/{len(df)} itens!")

    def update_transformity_display(self):
        self.transformity_text.config(state="normal")
        self.transformity_text.delete("1.0", tk.END)
        self.transformity_text.insert("1.0", "Transformidades adicionadas:\n")
        for flux, trans in self.transformities.items():
            self.transformity_text.insert(tk.END, f"{flux}: {trans} sej/unidade\n")
        self.transformity_text.config(state="disabled")

    def update_inventory_display(self):
        self.inventory_text.config(state="normal")
        self.inventory_text.delete("1.0", tk.END)
        self.inventory_text.insert("1.0", "Itens do inventário:\n")
        for item in self.inventory:
            self.inventory_text.insert(tk.END, f"{item['Fluxo']}: {item['Quantidade']} unidades\n")
        self.inventory_text.config(state="disabled")

    def add_transformity(self):
        flux = self.flux_name_entry.get()
        try:
            transformity = float(self.transformity_entry.get())
            if flux and transformity:
                self.transformities[flux] = transformity
                self.update_transformity_display()
                messagebox.showinfo("Sucesso", f"Transformidade de '{flux}' adicionada!")
            else:
                messagebox.showwarning("Erro", "Preencha todos os campos.")
        except ValueError:
            messagebox.showerror("Erro", "Transformidade deve ser um número.")
        self.flux_name_entry.delete(0, tk.END)
        self.transformity_entry.delete(0, tk.END)

    def add_inventory_item(self):
        flux = self.inventory_flux_entry.get()
        try:
            quantity = float(self.inventory_quantity_entry.get())
            if flux and quantity:
                self.inventory.append({'Fluxo': flux, 'Quantidade': quantity})
                self.update_inventory_display()
                messagebox.showinfo("Sucesso", f"Fluxo '{flux}' adicionado!")
            else:
                messagebox.showwarning("Erro", "Preencha todos os campos.")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número.")
        self.inventory_flux_entry.delete(0, tk.END)
        self.inventory_quantity_entry.delete(0, tk.END)

    def calculate_emergy(self):
        if not self.inventory:
            messagebox.showwarning("Erro", "Inventário vazio!")
            return
        if not self.transformities:
            messagebox.showwarning("Erro", "Transformidades não definidas!")
            return

        inventory_df = pd.DataFrame(self.inventory)
        inventory_df['Emergia (sej)'] = inventory_df.apply(
            lambda row: row['Quantidade'] * self.transformities.get(row['Fluxo'], 0), axis=1
        )

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, inventory_df.to_string(index=False))
        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmergyApp(root)
    root.mainloop()