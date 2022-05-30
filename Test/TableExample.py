import tkinter as tk
import tkinter.ttk as ttk
from turtle import width


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"]=headings
        table["displaycolumns"]=headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, width=3, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


root = tk.Tk()
table = Table(root, headings=('Вопрос №', 'Выбранный ответ'), rows=[[1,2], [2,3],[3,2],[4,1],[5, "2,4"]])
table.pack(expand=tk.YES, fill=tk.BOTH)
root.mainloop()
