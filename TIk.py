import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
import bcrypt

conn=mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="2004",
    database="usedb"
)
cursor=conn.cursor()

def hash_password(password):
    salt=bcrypt.gensalt()
    hashed_password=bcrypt.hashpw(password.encode(),salt)
    return hashed_password


def save_data():
    email=entry_email.get()
    password=entry_password.get()
    role=role_var.get()
    
    if email and password and role:
        hashed_password=hash_password(password)
        try:
            if role=="doctor":
                sql="INSERT INTO doctors(email,password) VALUES (%s,%s)"
            elif role=="patient":
                sql="INSERT INTO pateints(email,password) VALUES(%s,%s)"
            else:
                messagebox.showerror("Error","Error")
                
            values=(email,hashed_password)
            cursor.execute(sql,values)
            conn.commit()
            messagebox.showinfo("Succes","the data has been saved")
            open_dash(role)
            app.withdraw()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error",f"Failed to insert data:{err}")
        
        entry_email.delete(0,ctk.END)
        entry_password.delete(0,ctk.END)
    else:
        messagebox.showerror("Error","Please fill all the felids!")
        
    
def open_dash(role):
    if role=="doctor":
        open_doctor_dashboard()
    else:
        open_patient_dashboard()
        
#doctor dashboard

def open_doctor_dashboard():
    doctor_dashboard=ctk.CTkToplevel(app)
    doctor_dashboard.geometry("400x400")
    doctor_dashboard.title("Doctor Dashboard")
    
    ctk.CTkLabel(doctor_dashboard,
                 text="Doctor's Dashboard").pack(pady=20)
    
    ctk.CTkButton(doctor_dashboard,
                  text="View Appointments",
                  command=lambda:messagebox.showinfo("Appointments","Showing ..."))
    
    ctk.CTkButton(doctor_dashboard,
                  text="Manage Patients",
                  command=lambda:messagebox.showeinfo("Managing patients")).pack(pady=20)
    
    ctk.CTkButton(doctor_dashboard,
                  text="LogOut",
                  command=lambda:logout(doctor_dashboard)).pack(pady=10)
        
#patient Dashboard
def open_patient_dashboard():
    patient_dashboard=ctk.CTkToplevel(app)
    patient_dashboard.geometry("400x400")
    patient_dashboard.title("Patient's Dashboard")
    
    ctk.CTkLabel(patient_dashboard,
                 text="Patient's Dashboard").pack(pady=20)
    
    ctk.CTkButton(patient_dashboard,
                  text="View Prescriptions",
                  command=lambda:messagebox.showinfo("Prescriptions","Showing prescriptions..,")).pack(pady=10)
    
    ctk.CTkButton(patient_dashboard,
                  text="Schedule Appointment",
                  command=lambda:messagebox.showinfo("Appointment","Scheduling appointment..."))
    
    ctk.CTkButton(patient_dashboard,
                  text="LogOut",
                  command=lambda:logout(patient_dashboard)).pack(pady=20)
    
    
def logout(dashboard):
    dashboard.destroy()
    app.deiconify()
    

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

app=ctk.CTk()
app.geometry("400x400")
app.title("User Form")

ctk.CTkLabel(app,
             text="Register Users:",
             font=("Verenda",20)).pack(pady=5)

ctk.CTkLabel(app,
             text="Email:").pack(pady=5)

entry_email=ctk.CTkEntry(app,
                         width=300,
                         placeholder_text="Enter Your Email:")

entry_email.pack(pady=5)

ctk.CTkLabel(app,
             text="Password:").pack(pady=5)


entry_password=ctk.CTkEntry(app,
                            width=300,
                            placeholder_text="Enter Your Password:",
                            show="*")

entry_password.pack(pady=5)
ctk.CTkLabel(app,
             text="Are You a :").pack(pady=5)
role_var=ctk.StringVar(value="Doctor")
role_drop=ctk.CTkOptionMenu(app,
                            variable=role_var,
                            values=["doctor","Patient"])
role_drop.pack(pady=5)

save_button=ctk.CTkButton(app,
                          text="Save",
                          command=save_data)
save_button.pack(pady=30)

app.mainloop()

cursor.close()
conn.close()