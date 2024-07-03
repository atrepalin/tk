import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
import os
import tempfile
from PIL import Image, ImageTk 

storage_path = os.path.join(tempfile.gettempdir(), 'historyComputing.txt')
def close_window():
    if mb.askyesno("Выход", "Вы действительно хотите выйти из приложения?"):
        window.destroy()

def program_description():
    mb.showinfo("O Программе","Составить программу табулирования функции в диапазоне x0 (hx) xn и вычислить необходимое значение \
                (максимум, минимум, среднее) в соответствии с положением переключателя.")

def about_show():
    about = tk.Toplevel()
    about.title("Автор")
    about.geometry('250x200')
    about.resizable(False, False)
    myimage = ImageTk.PhotoImage(Image.open('homyak.png'))
    label_image = tk.Label(about, image=myimage)
    label_image.place(width=250, height=450)
    # Делаем дочернее окно модальным
    about.grab_set() # перехват событий, происходящих в приложении
    about.focus_set() # захват и удержание фокуса
    about.wait_window()

def read_file_history():
    if not os.path.exists(storage_path):
        mb.showinfo(title="Информация", message="Нет истории вычислений.")
    else:
        text.delete(1.0, tk.END)
    with open(storage_path, 'r') as f:
        text.insert(1.0, f.read())
        text.focus_set()

def save_file_history():
    if not os.path.exists(storage_path):
        f = open(storage_path, "w")
        f.close()
    with open(storage_path, 'a') as f:
        letter = label_text['text'] + '\n ' + label_window['text'] + '\n'  
        f.writelines(letter)
    
def popup(event):
    popupmenu.post(event.x_window, event.y_window)

def history_clear():
    answer = mb.askyesno(title="Подтверждение действия", message="Очистить историю?")
    if answer == True:
        text.delete(1.0, tk.END)
def clear(_):
    label_window["text"] = ""
    label_text['text'] = ""

    entry_x0.bind("<KeyRelease>", clear)
    entry_xn.bind("<KeyRelease>", clear)
    entry_hx.bind("<KeyRelease>", clear)


def data_clear():
    entry_x0.delete(0, tk.END)
    entry_xn.delete(0, tk.END)
    entry_hx.delete(0, tk.END)
    label_window['text'] = ''
    label_text['text'] = ''
    button_save['state'] = 'disable'
    button_clear['state'] = 'disable'

def run_solution():
    try:
        x0 = float(entry_x0.get())
        xn = float(entry_xn.get())
        hx = float(entry_hx.get())
    except ValueError:
        mb.showerror('Ошибка!', 'Неправильные значения!')
    except Exception:
        mb.showerror('Ошибка!', 'Непонятная ошибка.')
    label_text['text'] = "Функция на отрезке [{0},{1}] с шагом {2}" .format(entry_x0.get(), entry_xn.get(), entry_hx.get())
    d = equation_solution(x0, xn, hx)    
    if rb_var.get() == 0:
        label_window['text'] = f"Минимальное значение : {d}"
    elif rb_var.get() == 1:
       label_window['text'] = f"Максимальное значение : {d}"
    elif rb_var.get() == 2:
        label_window['text'] = f"Среднее арифмитическое значение : {d}"
    button_save['state'] = 'active'
   # button_clear['state'] = 'active'

    


def equation_solution(x0, xn, hx):
    x = x0
    lst = []
    if x < xn and hx < xn :
        while x <= xn + hx / 2:
            # Вычисление значения функции
            y = (x + 3) ** 2

            xs = round(x, 3)
            ys = round(y, 3)


            lst.append(ys)
            x += hx
    else:
        mb.showerror('Ошибка!', 'Неправильные значения!')

    if rb_var.get() == 0:
        lst = min(lst)
    elif rb_var.get() == 1:
        lst = max(lst)
    elif rb_var.get() == 2:
        lst = sum(lst)/len(lst)
        lst = round(lst,2)

    return lst



# Настройка окна
window = tk.Tk()
window.title("Решение уравнений")
window.geometry('500x270')
window.resizable(False, False)
# Настройка главного меню
mainmenu = tk.Menu(window)
window.config(menu=mainmenu)
# Создание выпадающих списков команд
filemenu = tk.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть", command=read_file_history)
filemenu.add_separator()
filemenu.add_command(label="Выход", command=close_window)
helpmenu = tk.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="О программе", command=program_description)
helpmenu.add_command(label="Об авторе", command=about_show)
# Подвязыванием экземпляры меню к главному меню
mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)
# Создание вкладок
nb = ttk.Notebook(window)
nb.pack(fill='both', expand='yes')
frame1 = tk.Frame(window)
frame2 = tk.Frame(window)
nb.add(frame1, text='Решение уравнения')
nb.add(frame2, text='Просмотр истории')
# Размещение виждетов на вкладке "Решение уравнения"
frame_koef = tk.LabelFrame(frame1)
frame_koef.grid(row=0, column=0, columnspan=2, padx=50, pady=5)
frame_type = tk.LabelFrame(frame1, text="Действие",)
frame_type.grid(row=0, column=2, padx=50, pady=5)
frame_result = tk.Frame(frame1)
frame_result.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
frame_button = tk.Frame(frame1)
frame_button.grid(row=1, column=2, padx=5, pady=5)
tk.Label(frame_koef, text="x0 = ", font=("Comic Sans MS", 11, "bold"),fg='#1B1BB3').grid(row=0, column=0, padx=5, pady=5,)
tk.Label(frame_koef, text="xn = ", font=("Comic Sans MS", 11, "bold"), fg='#1B1BB3').grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame_koef, text="hx = ", font=("Comic Sans MS", 11, "bold"), fg='#1B1BB3').grid(row=2, column=0, padx=5, pady=5)
entry_x0 = tk.Entry(frame_koef, width=10)
entry_x0.grid(row=0, column=1, padx=5, pady=10)
entry_xn = tk.Entry(frame_koef, width=10)
entry_xn.grid(row=1, column=1, padx=5, pady=5)
entry_hx = tk.Entry(frame_koef, width=10)
entry_hx.grid(row=2, column=1, padx=5, pady=10)
rb_var = tk.IntVar()
rb_var.set(0)
rb_min = tk.Radiobutton(frame_type, variable=rb_var, text='MIN', value=0)
rb_min.grid(row=0, column=0, padx=3, pady=4, sticky='nw')
rb_max = tk.Radiobutton(frame_type, variable=rb_var, text='MAX', value=1)
rb_max.grid(row=1, column=0, padx=3, pady=4, sticky='nw')
rb_sr = tk.Radiobutton(frame_type, variable=rb_var, text='средн. арифм', value=2)
rb_sr.grid(row=2, column=0, padx=3, pady=4, sticky='nw')
label_text = tk.Label(frame_result)
label_text.grid(row=0, column=0)
label_window = tk.Label(frame_result)
label_window.grid(row=1, column=0)
button_res = tk.Button(frame_button, width=12, text="Вычислить", command=run_solution)
button_res.grid(row=0, column=0, padx=5, pady=2, )
button_clear = tk.Button(frame_button, state='disabled', width=12, text="Очистить", command=clear)
button_clear.grid(row=1, column=0, padx=5, pady=2)
button_save = tk.Button(frame_button, state='disabled', width=12, text="Сохранить", command=save_file_history)
button_save.grid(row=2, column=0, padx=5, pady=2)
# Размещение виждетов на вкладке "Просмотр истории"
# Многострочное текстовое поле с полосой прокрутки
text = tk.Text(frame2, wrap=tk.WORD)
scroll = tk.Scrollbar(frame2, command=text.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=scroll.set)
text.pack(side=tk.LEFT)
# Контекстное меню
popupmenu = tk.Menu(tearoff=0)
popupmenu.add_command(label="Очистить", command=history_clear)
popupmenu.add_command(label="Показать историю", command=read_file_history)
text.bind('<Button-3>', popup)
window.mainloop()