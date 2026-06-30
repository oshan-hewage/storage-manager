import tkinter as tk
import os
import zipfile
from tkinter import filedialog
import time
import shutil
from tkinter import messagebox


path = ""
items = []
dates = []
count_of_items = []

def paste_item():
    run = 1
    def check_for_item():
        item = ""

        for c in char_list:
            if run == 1:
                if c == "{":
                    item = item.strip()
                    return item
                item = item + c
    def chek_date():
        date = ""

        for c in char_list:
            if c == "{":
                for _ in char_list[char_list.index("{")]:
                    if _ == "}":
                        return date
                    else:
                        date  = date + _
    def check_count():
        count = []

        
        for cu in char_list[-char_list.index(" ")]:
            count.insert(0, cu)
    
        
        try:
            return int(count) 
        except ValueError:
            return 1    


    clipboard_item = window.clipboard_get()
    
    char_list = list(clipboard_item)

    count = check_count()
    item = check_for_item()
    date = chek_date()
   
    
    if item in items:
        messagebox.showerror(title="item already exist",
                                 message="'" + item + "' already exist!",
                                 detail="can't paste the new item beacuse it already exist",
                                 icon="error")
    else:
        items.append(item)
        dates.append(date)
        count_of_items.append(count)
        item_list_box.insert("end", item)
    


def copy_item():
    selected_item = item_list_box.get("anchor")
    date_time = dates[items.index(selected_item)]
    count_number = count_of_items[items.index(selected_item)]
    window.clipboard_clear()
    window.clipboard_append([selected_item, date_time, count_number])


def mine_item():
    global count_of_items

    selected_item = item_list_box.get("anchor")
    if selected_item == "":
        pass
    else:
        index = items.index(selected_item)
    
        count_of_item = count_of_items[index]
        count_of_items[index] = count_of_items[index] - 1

        count_label.config(text=count_of_items[index])


def plus_count_of_items():
    global count_of_items

    selected_item = item_list_box.get("anchor")
    if selected_item == "":
        pass
    else:
        index = items.index(selected_item)
    
        count_of_item = count_of_items[index]
        count_of_items[index] = count_of_items[index] + 1

        count_label.config(text=count_of_items[index])
        


def save_as():

    file_type = [("suplie maneger data base", ".smdb")]
    open_window = filedialog.asksaveasfilename(title="Save data base", filetypes=file_type)
    path_for_archive = open_window.expandtabs()

    try:
        os.remove(path_for_archive)
    except FileNotFoundError:
        pass

    if path_for_archive == "":
        return

    date_data_file = open(os.path.join("dist", "data_and_time.data"), mode="w")
    item_file = open(os.path.join("dist", "item_data.data"), mode="w")
    count_item_file = open(os.path.join("dist", "item_count.data"), mode="w")

    for line in dates:
        date_data_file.write(line + "\n")

    for line in items:
        item_file.write(line + "\n")
    for line in count_of_items:
        count_item_file.write(str(line) + "\n")

    date_data_file.close()
    item_file.close()
    count_item_file.close()

    files_to_compress = [os.path.join("dist", "data_and_time.data"), os.path.join("dist", "item_data.data"), os.path.join("dist", "item_count.data")]
    zip_file = path_for_archive
    with zipfile.ZipFile(zip_file, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in files_to_compress:
            archive.write(file)


def save():

    date_data_file = open(os.path.join("dist", "data_and_time.data"), mode="w")
    item_file = open(os.path.join("dist", "item_data.data"), mode="w")
    count_item_file = open(os.path.join("dist", "item_count.data"), mode="w")

    try:
        os.remove(path)
    except FileNotFoundError:
        pass

    for line in dates:
        date_data_file.write(line + "\n")

    for line in items:
        item_file.write(line + "\n")

    for line in count_of_items:
        count_item_file.write(str(line) + "\n")


    date_data_file.close()
    item_file.close()
    count_item_file.close()
    

    files_to_compress = [os.path.join("dist", "data_and_time.data"), os.path.join("dist", "item_data.data"), os.path.join("dist", "item_count.data")]
    zip_file = path
    with zipfile.ZipFile(zip_file, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in files_to_compress:
            archive.write(file)


def rename_item():
    def rename():
        item = item_entry.get()
        past_item = item_list_box.get("anchor")
        
        if item in items:
            
            messagebox.showerror(title="item already exist",
                                 message="'" + item + "' already exist!",
                                 detail="can't rename the item beacuse it already exist",
                                 icon="error")

        else:
            created_day = dates[items.index(past_item)]
            past_count = count_of_items[items.index(past_item)]
            dates.remove(dates[items.index(past_item)])
            count_of_items.remove(count_of_items[items.index(past_item)])
            items.remove(past_item)
            item_list_box.delete("anchor")
            item_list_box.insert("end", item)
            items.append(item)
            dates.append(created_day)
            count_of_items.append(past_count)
            item_list_box.select_clear(0,tk.END)
            item_list_box.select_set(tk.END)

    rename_box = tk.Toplevel(master=window)
    selected_item = item_list_box.get("anchor")
    rename_icon1 = tk.PhotoImage(master=rename_box, file=os.path.join("assets", "rename_icon.png"))
    rename_box.geometry("300x200+" + str(int((window.winfo_screenwidth() - 300) / 2)) + "+" + str(int((window.winfo_screenheight() - 200) / 2)))
    rename_box.title("add item to the data base")
    rename_box.iconphoto(False, rename_icon1)

    item_entry = tk.Entry(rename_box, width=30)
    item_entry.insert("end", selected_item)
    tk.Label(rename_box, text="item: ").place(x=40, y=50)
    item_entry.place(x=80, y=50)
    add_button = tk.Button(rename_box, image=rename_icon, text="rename", compound="left", padx=5, pady=10, command=lambda: rename())
    add_button.place(x=110, y=90)

    
    rename_box.grab_set()
    #add_box.attributes("-toolwindow", True)
    rename_box.transient(window)
    rename_box.resizable(False, False)




def update_time_and_date(event):
    selected_item = item_list_box.get("anchor")
    #date.config(text=dates[items.index(selected_item)]) 
    if selected_item == "":
        pass
    else:
        index = items.index(selected_item)
        date.config(text=dates[index])
        plus_button.config(state="active")
        mine_button.config(state="active")
        count_label.config(text=str(count_of_items[index]))


def delete_something():
    selected_item = item_list_box.get("anchor")
    dates.remove(dates[items.index(selected_item)])
    count_of_items.remove(count_of_items[items.index(selected_item)])
    items.remove(selected_item)
    item_list_box.delete("anchor")
    

def add_something():
    def add():
        item = item_entry.get()
        if item in items:
            messagebox.showerror(title="item already exist",
                                 message="'" + item + "' already exist!",
                                 detail="can't add the new item beacuse it already exist",
                                 icon="error")
        else:
            items.append(item)
            count_of_items.append(1)
            item_list_box.insert("end", item)
            t = time.localtime(time.time())
            local_time = time.asctime(t)
            dates.append(local_time)


    add_box = tk.Toplevel(master=window)
    add_icon1 = tk.PhotoImage(master=add_box, file=os.path.join("assets", "add_icon.png"))
    add_box.geometry("300x200+" + str(int((window.winfo_screenwidth() - 300) / 2)) + "+" + str(int((window.winfo_screenheight() - 200) / 2)))
    add_box.title("add item to the data base")
    add_box.iconphoto(False, add_icon1)

    item_entry = tk.Entry(add_box, width=30)
    tk.Label(add_box, text="item: ").place(x=40, y=50)
    item_entry.place(x=80, y=50)
    add_button = tk.Button(add_box, image=add_icon, text="Add", compound="left", padx=5, pady=10, command=lambda: add())
    add_button.place(x=110, y=90)

    
    add_box.grab_set()
    #add_box.attributes("-toolwindow", True)
    add_box.transient(window)
    add_box.resizable(False, False)


def scroll_up(y, x):
    item_list_box.yview(y, x)
    

def update_explore():

    for clear in items:
        item_list_box.delete("end")
    items.clear()       
    dates.clear()
    
    try:
        date_file = open(os.path.join("dist", "data_and_time.data"))
        item_file = open(os.path.join("dist", "item_data.data"))
        item_count_file = open(os.path.join("dist", "item_count.data"))
    except FileNotFoundError:
        date_file = open(os.path.join("dist", "dist", "data_and_time.data"))
        item_file = open(os.path.join("dist", "dist", "item_data.data"))
        item_count_file = open(os.path.join("dist", "dist", "item_count.data"))



    for item in item_file:
        #item.strip()
        item_list_box.insert("end", item.strip())
        #(item.strip())
        items.append(item.strip())
    for dati in date_file:
        dati.strip()
        dates.append(dati.strip())
        #dates.append(dati.strip())
        #(dati.strip())
    for item in item_count_file:
        count_of_items.append(int(item.strip()))


    

    date_file.close()
    item_file.close()
    item_count_file.close()


def open_file():
    global path

    shutil.rmtree(os.path.join("dist"))
    os.makedirs("dist")

    file_type = [("suplie maneger data base", ".smdb")]
    open_window = filedialog.askopenfilename(title="Open data base", filetypes=file_type)
    path = open_window.expandtabs()

    if path == "":
        return
    
    data_base = zipfile.ZipFile(path, "r")
    data_base.extractall(os.path.join("dist"))
    data_base.close()

    update_explore()


def switch_windows():
    window.deiconify()
    splash_screen.destroy()
    window.geometry("800x600+0+0")
    window.state("zoom")


splash_screen = tk.Tk()
window = tk.Tk()
window.iconify()


splash_screen.geometry("300x200+" + str(int((splash_screen.winfo_screenwidth() - 300) / 2)) + "+" + str(int((splash_screen.winfo_screenheight() - 200) / 2)))
splash_screen.attributes('-alpha',1)
splash_screen.overrideredirect(True)

loading_image = tk.PhotoImage(master=splash_screen, file=os.path.join("assets", "loading_screen.png"))
loading_label = tk.Label(splash_screen, image=loading_image)
loading_label.place(x=0, y=0)


window.after(5000, lambda: switch_windows())

window.iconbitmap(os.path.join("assets", "icon_photo.ico"))
window.title("Suplie Maneger")

#images

open_file_icon = tk.PhotoImage(master=window, file=os.path.join("assets", "open_folder_icon.png"))
save_icon = tk.PhotoImage(master=window, file=os.path.join("assets", "save_icon.png"))
save_as_icon = tk.PhotoImage(master=window, file=os.path.join("assets", "save_as_icon.png"))
exit_icon = tk.PhotoImage(master=window, file=os.path.join("assets", "exit_icon.png"))
add_icon = tk.PhotoImage(master=window, file=os.path.join("assets", "add_icon.png"))
delete_icon  = tk.PhotoImage(master=window, file=os.path.join("assets", "delete_icon.png"))
copy_icon = tk.PhotoImage(master=window, file=os.path.join("assets", "copy_icon.png"))
paste_icon = tk.PhotoImage(master=window, file=os.path.join("assets", "paste_icon.png"))
rename_icon = tk.PhotoImage(master=window, file=os.path.join("assets", "rename_icon.png"))

#menu

menu = tk.Menu(window, tearoff=0)
window.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
edit_menu = tk.Menu(menu, tearoff=0)
item_menu = tk.Menu(menu, tearoff=0)

menu.add_cascade(menu=file_menu, label="File")
menu.add_cascade(menu=edit_menu, label="Edit")
menu.add_cascade(menu=item_menu, label="Item")

file_menu.add_command(label="Open File", image=open_file_icon, compound="left", command=lambda: open_file())
file_menu.add_command(label="Save", image=save_icon, compound="left", command=lambda: save())
file_menu.add_command(label="Save As", image=save_as_icon, compound="left", command=lambda: save_as())
file_menu.add_separator()
file_menu.add_command(label="Exit", image=exit_icon, compound="left", command=lambda: exit())

edit_menu.add_command(label="Add", image=add_icon, compound="left", command=lambda: add_something())
edit_menu.add_separator()
edit_menu.add_command(label="Copy", image=copy_icon, compound="left", command=lambda: copy_item())
edit_menu.add_command(label="Paste", image=paste_icon, compound="left", command=lambda: paste_item())

item_menu.add_command(label="Delete", image=delete_icon, compound="left", command=lambda: delete_something())
item_menu.add_command(label="Rename", image=rename_icon, compound="left", command=lambda: rename_item())

# tool bar 
tool_bar = tk.Frame(window, width=window.winfo_screenwidth(), height=60, bg="#E0E0E0")
tool_bar.place(x=0, y=0)

tool_bar.grid_propagate(False)

add_button = tk.Button(tool_bar, image=add_icon, command=lambda: add_something())
add_button.grid(column=0, row=0, pady=10, padx=5)

delete_button = tk.Button(tool_bar, image=delete_icon, command=lambda: delete_something())
delete_button.grid(column=1, row=0, pady=10, padx=5)

copy_button = tk.Button(tool_bar, image=copy_icon, command=lambda: copy_item())
copy_button.grid(column=2, row=0, pady=10, padx=5)

paste_button = tk.Button(tool_bar, image=paste_icon, command=lambda: paste_item())
paste_button.grid(column=3, row=0, pady=10, padx=5)

rename_button = tk.Button(tool_bar, image=rename_icon, command=lambda: rename_item())
rename_button.grid(column=4, row=0, pady=10, padx=5)

# body
working_frame_width = window.winfo_screenwidth()
working_frame_height = window.winfo_screenheight()

window.pack_propagate(False)


working_frame = tk.Frame(window, width=working_frame_width, height=working_frame_height, background="#CECECE")
working_frame.pack(padx=0, pady=65, side="left", fill="y")
working_frame.pack_propagate(False)
working_frame_scrollbar = tk.Scrollbar(master=working_frame, orient="vertical", command=scroll_up)
working_frame_scrollbar.pack(side="right", fill="y")
item_list_box = tk.Listbox(working_frame, yscrollcommand=working_frame_scrollbar.set, selectbackground="#2356FF", activestyle="dotbox", font=40)
item_list_box.place(width=working_frame_width - 20, height=working_frame_height - 220, y=0, x=0)

# state_bar

state_bar = tk.Frame(window, background="#BDBDBD", height=140, width=working_frame_width)
state_bar.place(y=working_frame_height - 140,x=0)

#state_bar.pack_propagate(False)

date_frame = tk.LabelFrame(state_bar, text="created date and time:", height=50, width=220, background="#BDBDBD")
date_frame.place(x=0, y=0)

date = tk.Label(date_frame, text="None", background="#BDBDBD", font=20)
date.place(x=5, y=2)

item_count_frame = tk.LabelFrame(state_bar, text="count of items:", height=50, width=220, background="#BDBDBD")
item_count_frame.place(x=225, y=0)
item_count_frame.pack_propagate(False)

plus_button = tk.Button(item_count_frame, text="+", state="disabled", command=lambda: plus_count_of_items())
plus_button.pack(padx=40, side="left")

count_label = tk.Label(item_count_frame, text="")
count_label.pack(padx=15, side="left")

mine_button = tk.Button(item_count_frame, text="-", state="disabled", command=lambda: mine_item())
mine_button.pack(padx=30, side="left")

item_list_box.bind("<<ListboxSelect>>", update_time_and_date)

window.mainloop()
splash_screen.mainloop()