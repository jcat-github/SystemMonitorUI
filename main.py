import psutil
import cpuinfo
import customtkinter

def setup():
  global app
  app = customtkinter.CTk()
  app.geometry("400x240")
  app.title("CustomTkinter App")
setup()
# CPU information
cpu_info_label = customtkinter.CTkLabel(master=app, text=cpuinfo.get_cpu_info()["brand_raw"])
cpu_info_label.grid(column=0, row=0, padx=10, pady=5)
print(psutil.cpu_percent(interval=1, percpu=True))
app.mainloop()