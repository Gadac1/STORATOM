import tkinter as tk
from tkinter import ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

def save_values():
    global eta, system_max_power, reactor_init_load_factor, reac_T_out, reac_T_in, T_stock_hot, T_stock_cold, storage_init_level, season, rate, study, reactor_power, storage_duration
    eta = float(eta_entry.get())
    system_max_power = float(sys_max_entry.get())
    reac_T_out = float(reac_T_out_entry.get())
    reac_T_in = float(reac_T_in_entry.get())
    T_stock_hot = float(T_hot_entry.get())
    T_stock_cold = float(T_cold_entry.get())
    storage_init_level = float(storage_level_entry.get())
    rate = int(rate_var.get())
    season = str(season_var.get())
    study = str(study_var.get())
    
    if study_var.get() == "Single system":
        reactor_power = float(reactor_power_entry.get())
        storage_duration = float(storage_duration_entry.get())


    root.destroy()

def on_study_select(*args):
    if study_var.get() == "Single system":
        reactor_power_label.grid(row=4, column=3)
        reactor_power_entry.grid(row=4, column=4)
        storage_duration_label.grid(row=5, column=3)
        storage_duration_entry.grid(row=5, column=4)
    else:
        reactor_power_label.grid_forget()
        reactor_power_entry.grid_forget()
        storage_duration_label.grid_forget()
        storage_duration_entry.grid_forget()

root = tk.Tk()
root.title("Simulation parameters")
font_option = ('Calibri', 14)

# title_label = tk.Label(root, text="Simulation parameters", font=('Calibri', 24))
# title_label.grid(row=0, column=1, columnspan=1, pady=10,padx=40)

eta_label = tk.Label(root, text="   Thermoelectrical conversion efficiency  ", font=font_option)
eta_label.grid(row=1, column=0)
eta_entry = tk.Entry(root)
eta_entry.grid(row=1, column=1)
eta_entry.insert(0, "0.33")

sys_max_label = tk.Label(root, text="System max power (MWe)", font=font_option)
sys_max_label.grid(row=2, column=0)
sys_max_entry = tk.Entry(root)
sys_max_entry.grid(row=2, column=1)
sys_max_entry.insert(0, "500")


reac_T_out_label = tk.Label(root, text="Reactor outlet temperature (°C)", font=font_option)
reac_T_out_label.grid(row=3, column=0)
reac_T_out_entry = tk.Entry(root)
reac_T_out_entry.grid(row=3, column=1)
reac_T_out_entry.insert(0, "550")

reac_T_in_label = tk.Label(root, text="Reactor inlet temperature (°C)", font=font_option)
reac_T_in_label.grid(row=4, column=0)
reac_T_in_entry = tk.Entry(root)
reac_T_in_entry.grid(row=4, column=1)
reac_T_in_entry.insert(0, "400")


T_hot_label = tk.Label(root, text="Hot storage temperature (°C)", font=font_option)
T_hot_label.grid(row=5, column=0)
T_hot_entry = tk.Entry(root)
T_hot_entry.grid(row=5, column=1)
T_hot_entry.insert(0, "500")


T_cold_label = tk.Label(root, text="Cold storage temperature (°C)", font=font_option)
T_cold_label.grid(row=6, column=0)
T_cold_entry = tk.Entry(root)
T_cold_entry.grid(row=6, column=1)
T_cold_entry.insert(0, "290")

storage_level_label = tk.Label(root, text="Storage Initial Level (0-1)", font=font_option)
storage_level_label.grid(row=7, column=0)
storage_level_entry = tk.Entry(root)
storage_level_entry.grid(row=7, column=1)
storage_level_entry.insert(0, "1")

# Create Combobox for season selection
rate_label = tk.Label(root, text="  VRE penetration rate  ", font=font_option)
rate_label.grid(row=1, column=3)
rate_var = tk.StringVar()
rate_combobox = ttk.Combobox(root, textvariable=rate_var, state='readonly')
rate_combobox['values'] = ('50', '80', '90')
rate_combobox.grid(row=1, column=4,padx=20)

season_label = tk.Label(root, text="    Season  ", font=font_option)
season_label.grid(row=2, column=3)
season_var = tk.StringVar()
season_combobox = ttk.Combobox(root, textvariable=season_var, state='readonly')
season_combobox['values'] = ('Winter week', 'Winter', 'Summer week', 'Summer')
season_combobox.grid(row=2, column=4)

study_label = tk.Label(root, text="    Type of study  ", font=font_option)
study_label.grid(row=3, column=3)
study_var = tk.StringVar()
study_combobox = ttk.Combobox(root, textvariable=study_var, state='readonly')
study_combobox['values'] = ('Single system', 'Parametric')
study_combobox.grid(row=3, column=4)

# Create Entry for reactor_power
reactor_power_label = tk.Label(root, text="Reactor Power", font=font_option)
reactor_power_entry = tk.Entry(root)

storage_duration_label = tk.Label(root, text="Storage Duration", font=font_option)
storage_duration_entry = tk.Entry(root)

study_var.trace("w", on_study_select)


save_button = tk.Button(root, text="Simulate", command=save_values)
save_button.grid(row=10, column=0, columnspan=8, pady=10, padx=10, ipadx=100)

ttk.Separator(root, orient='vertical').grid(column=2, row=1, rowspan=8, sticky='ns',padx=20)


root.mainloop()