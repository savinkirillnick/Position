import tkinter as tk
from os.path import exists
from tkinter import ttk
import json

ver = '1.0'


class MainWindow(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.qty = 0.0
        self.price = 0.0
        self.history = list()
        self.last_price = 0.0

        self.load()

        toolbar = tk.Frame(bg='#ffffff', bd=0, width=240, height=145)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        y = 5
        tk.Label(toolbar, bg='#ffffff', text='Position:', font='Arial 10 bold').place(x=10, y=y)

        y += 25
        tk.Label(toolbar, bg='#ffffff', text='Price', font='Arial 10 bold').place(x=10, y=y)
        self.label_price = tk.Label(toolbar, bg='#ffffff', text='0.0')
        self.label_price.place(x=60, y=y)

        tk.Label(toolbar, bg='#ffffff', text='Qty', font='Arial 10 bold').place(x=130, y=y)
        self.label_qty = tk.Label(toolbar, bg='#ffffff', text='0.0')
        self.label_qty.place(x=170, y=y)

        y += 25
        tk.Label(toolbar, bg='#ffffff', text='Price', font='Arial 10').place(x=10, y=y)
        self.entry_price = ttk.Entry(toolbar)
        self.entry_price.place(x=60, y=y, width=50)

        label_qty = tk.Label(toolbar, bg='#ffffff', text='Qty', font='Arial 10')
        label_qty.place(x=130, y=y)
        self.entry_qty = ttk.Entry(toolbar)
        self.entry_qty.place(x=170, y=y, width=50)

        y += 25
        self.label_delta = tk.Label(toolbar, bg='#ffffff', text='', font='Arial 8')
        self.label_delta.place(x=60, y=y)

        y += 20
        ttk.Button(toolbar, text='Check', command=self.check).place(x=10, y=95, width=50, height=25)
        ttk.Button(toolbar, text='Buy', command=self.buy).place(x=65, y=95, width=50, height=25)
        ttk.Button(toolbar, text='Sell', command=self.sell).place(x=120, y=95, width=50, height=25)
        ttk.Button(toolbar, text='Reset', command=self.reset).place(x=175, y=95, width=55, height=25)

        y += 25
        treebar = tk.Frame(bg='#ffffff', bd=0, width=240, height=255)
        treebar.pack(side=tk.TOP, fill=tk.X)

        self.tree = ttk.Treeview(treebar, columns=('side', 'price', 'qty'), height=20, show='headings')
        self.tree.column('side', width=40, anchor=tk.CENTER)
        self.tree.column('price', width=85, anchor=tk.CENTER)
        self.tree.column('qty', width=85, anchor=tk.CENTER)
        self.tree.heading('side', text='Side')
        self.tree.heading('price', text='Price')
        self.tree.heading('qty', text='Qty')

        scroll_bar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_bar.set)
        self.tree.place(width=240)
        self.tree.pack(fill=tk.X)

    def view(self):
        self.label_price.configure(text=f'{round(self.price, 8)}')
        self.label_qty.configure(text=f'{round(self.qty, 8)}')
        self.label_delta.configure(text='')
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i in range(len(self.history)):
            self.tree.insert('', 'end',
                             values=(self.history[i]['side'], self.history[i]['price'], self.history[i]['qty']))
            self.tree.yview_moveto(1)

    def check(self):
        if self.last_price:
            delta = round(float(self.entry_price.get()) / self.last_price * 100, 1)
            self.label_delta.configure(text=f'{str(delta)}%')

    def reset(self):
        self.last_price = 0.0
        self.qty = 0.0
        self.price = 0.0
        self.history = list()
        self.label_delta.configure(text='')
        self.view()
        self.save()

    def buy(self):
        price = float(self.entry_price.get())
        qty = float(self.entry_qty.get())
        lot = self.price * self.qty + price * qty
        self.qty += qty
        self.price = lot / self.qty
        self.history.append({'side': 'buy', 'price': price, 'qty': qty})
        self.last_price = price
        self.view()
        self.save()

    def sell(self):
        price = float(self.entry_price.get())
        qty = float(self.entry_qty.get())
        self.qty -= qty
        if round(self.qty, 8) <= 0:
            self.reset()
        self.history.append({'side': 'sell', 'price': price, 'qty': qty})
        self.last_price = price
        self.view()
        self.save()

    def save(self):
        data = dict()
        data['price'] = self.price
        data['qty'] = self.qty
        data['history'] = self.history
        data['last_price'] = self.last_price
        json_string = json.dumps(data)
        with open('pos_file.txt', 'w') as f:
            f.write(json_string)

    def load(self):
        if exists('pos_file.txt'):
            with open('pos_file.txt', 'r') as f:
                data = json.loads(f.read())
                self.price = data['price'] if 'price' in data else 0.0
                self.qty = data['qty'] if 'qty' in data else 0.0
                self.history = data['history'] if 'history' in data else list()
                self.last_price = data['last_price'] if 'last_price' in data else 0.0


if __name__ == '__main__':

    root = tk.Tk()
    app = MainWindow(root)

    # Вычисляем расширение экрана пользователя и задаем размеры окна программы
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app_width = 240
    app_height = 400

    root.title('Position ' + ver)

    root.geometry(
        f'{app_width}x{app_height}+{screen_width // 2 - app_width // 2}+{screen_height // 2 - app_height // 2}')
    root.resizable(False, False)
    root.mainloop()
