import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def conectar_bd():
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def adicionar_produto():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    preco = entry_preco.get()
    quantidade = entry_quantidade.get()
    
    if not nome or not preco or not quantidade:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
        return
    
    try:
        preco = float(preco)
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "Preço e quantidade devem ser numéricos!")
        return
    
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES (?, ?, ?, ?)",
                   (nome, descricao, preco, quantidade))
    conn.commit()
    conn.close()
    atualizar_lista()
    limpar_campos()
    

def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def excluir_produto():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um produto para excluir!")
        return
    
    item = tree.item(selecionado)
    produto_id = item["values"][0]
    
    conn = sqlite3.connect("produtos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()
    atualizar_lista()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)

# Criando a interface gráfica
root = tk.Tk()
root.title("Gerenciamento de Produtos")
root.geometry("600x400")

conectar_bd()

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

# Campos de entrada
labels = ["Nome:", "Descrição:", "Preço:", "Quantidade:"]
entries = []

for i, label in enumerate(labels):
    tk.Label(frame_form, text=label).grid(row=i, column=0, padx=5, pady=5)
    entry = tk.Entry(frame_form)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

entry_nome, entry_descricao, entry_preco, entry_quantidade = entries

# Botões
btn_adicionar = tk.Button(root, text="Adicionar Produto", command=adicionar_produto)
btn_adicionar.pack(pady=5)

btn_excluir = tk.Button(root, text="Excluir Produto", command=excluir_produto)
btn_excluir.pack(pady=5)

# Lista de produtos
columns = ("ID", "Nome", "Descrição", "Preço", "Quantidade")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(pady=10)

atualizar_lista()

root.mainloop()
