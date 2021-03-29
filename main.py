# ---------------------------- PASSWORD GENERATOR ------------------------------- #
from tkinter.messagebox import askyesno
import string
import random
import json

generated_pass = None


def generate_pass():

    global generated_pass
    generated_pass = ""
    letters = list(string.ascii_letters)
    numbers = list(string.digits)
    symbols = ['_', '.', '-']
    for _ in range(10):
        var = random.randint(0,6)
        if var < 3:
            extra = random.choice(letters)
        elif var >3:
            extra = random.choice(numbers)
        else:
            extra = random.choice(symbols)
        generated_pass += extra
        pass_var.set(generated_pass)




# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():

    website = entry_site.get()
    website = website.lower()
    user_mail = entry_usermail.get()
    password = entry_password.get()

    final_entry = {
        website: {
            "email": user_mail,
            "password": password,
        }
    }

    if website == "" or user_mail == "" or password == "":
        messagebox.showwarning  (title="Falta informacion", message="No puedes dejar campos vacios")
    else:
        proceed = askyesno(title="Guardar?",
                           message=f"Revisa tus datos\n\nWebsite: {website.title()}\nUsuario: {user_mail}\nPassword: {password}")
        if proceed == True:
            try:
                with open("passwords.json", "r") as data_file:
                    data = json.load(data_file)
            except:
                with open("passwords.json", "w") as data_file:
                    json.dump(final_entry, data_file, indent=4)
            else:
                data.update(final_entry)

                with open("passwords.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                entry_site.delete(0,END)
                entry_usermail.delete(0,END)
                entry_password.delete(0,END)
                messagebox.showinfo(title="Finalizado", message="Tu contraseña ha sido guardada")

# ---------------------------- SHOW PASSWORDS ------------------------------- #

def search():

    website = entry_site.get()
    website =  website.lower()
    try:
        with open("passwords.json", "r") as data_file:
            data = json.load(data_file)

        if website in data:
            messagebox.showinfo(title=f"{website.title()}",
                                message=f"Usuario: {data[website]['email']}\nContraseña: {data[website]['password']}")
        else:
            messagebox.showinfo(title="Error", message="No has ingresado aun una contraseña de este sitio")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Aun no hay contraseñas")

# ---------------------------- UI SETUP ------------------------------- #
from tkinter import *

window = Tk()
window.config(padx=20, pady=30)
window.title("Password Saver")
window.resizable(0,0)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 99, image=lock_img)
canvas.grid(column=1, row=1)


pass_var = StringVar()

entry_site = Entry(width=36)
entry_site.grid(column=1,row=2, columnspan=1)
entry_usermail = Entry(width=51)
entry_usermail.grid(column=1,row=3, columnspan=2)
entry_password = Entry(width=36, textvariable= pass_var)
entry_password.grid(column=1,row=5)

label_site = Label(text="Sitio Web")
label_site.grid(column=0,row=2)
label_usermail = Label(text="User / Mail")
label_usermail.grid(column=0,row=3)
label_password = Label(text="Password")
label_password.grid(column=0,row=5)

button_generate = Button(text="Generate", width=11, command=generate_pass)
button_generate.grid(column=2, row=5, padx=0)

button_save = Button(text="Save password", command=save_pass, width=43)
button_save.grid(column=1, row=6, columnspan=2)

button_show = Button(text="Buscar", width=11, command=search)
button_show.grid(column=2, row=2, columnspan=1)

window.mainloop()

