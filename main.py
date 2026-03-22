import psutil
import cpuinfo
import customtkinter as ctk

def setup():
  global app
  app = ctk.CTk()
  app.geometry("400x240")
  app.title("CustomTkinter App")
setup()

# get CPU cores
cpucores = psutil.cpu_count(logical=True)
# CPU information
cpu_info_label = ctk.CTkLabel(master=app, text=cpuinfo.get_cpu_info()["brand_raw"])
cpu_info_label.grid(column=0, row=0, padx=10, pady=5, columnspan=cpucores)

# add CPU usage bars and grid
cpu_usage = []
for i in range(cpucores):
    app.grid_columnconfigure(i, weight=1)
    bar = ctk.CTkProgressBar(master=app, orientation="vertical", height=100, width=20, corner_radius=0)
    bar.grid(column=i, row=1, padx=10, pady=5)
    cpu_usage.append(bar)

# Update CPU Usage
def upd_cpu_usage():
    for i,s in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_usage[i].set(s/100)
    app.after(500, upd_cpu_usage)

# Functions
upd_cpu_usage()

app.mainloop()