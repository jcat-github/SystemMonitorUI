import psutil
import cpuinfo
import nvitop
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Setup window
global app
app = ctk.CTk()
app.geometry("400x1000")
app.title("System Resource Manager")

def pack(element):
    element.pack(side="top", fill="x", expand=True)
    return None

# get CPU cores
cpucores = psutil.cpu_count(logical=True)

# CPU information
cpu_info_label = ctk.CTkLabel(master=app, text=cpuinfo.get_cpu_info()["brand_raw"])
pack(cpu_info_label)

cpu_frame = ctk.CTkFrame(master=app)
pack(cpu_frame)
# add CPU usage bars and grid
cpu_usage = []
cpu_perc = []
for i in range(cpucores):
    cpu_frame.grid_columnconfigure(i, weight=1)
    bar = ctk.CTkProgressBar(master=cpu_frame, orientation="vertical", height=100, width=20, corner_radius=0)
    bar.grid(column=i, row=0, padx=10, pady=5)
    text = ctk.CTkLabel(master=cpu_frame)
    text.grid(column=i, row=1, padx=5, pady=5)
    cpu_usage.append(bar)
    cpu_perc.append(text)

# Ram percent
ram_info_label = ctk.CTkLabel(master=app)
pack(ram_info_label)

# Set up RAM usage chart
RAM_history = [0]*15
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
RAM_canva = FigureCanvasTkAgg(fig, master=app)
RAM_widget = RAM_canva.get_tk_widget()
pack(RAM_widget)

# GPU 
GPU_devices = nvitop.Device.all()
GPU_name = ctk.CTkLabel(master=app)
GPU_usage = ctk.CTkLabel(master=app)
GPU_mem = ctk.CTkLabel(master=app)
GPU_temp = ctk.CTkLabel(master=app)
GPU_fanspeed = ctk.CTkLabel(master=app)
pack(GPU_name)
pack(GPU_mem)
pack(GPU_usage)
pack(GPU_temp)
pack(GPU_fanspeed)
# Update CPU Usage
def upd_usage():
    # CPU
    for i,s in enumerate(psutil.cpu_percent(percpu=True, interval=0.5)):
        cpu_usage[i].set(s/100)
        cpu_perc[i].configure(text=f"{s}%")
    
    # RAM
    mem = psutil.virtual_memory()
    RAM_percent = mem.percent
    ram_info_label.configure(text=f"RAM used: {mem.percent}%")

    # RAM chart
    RAM_history.pop(0)
    RAM_history.append(mem.used/1024/1024/1024)
    ax.clear()
    ax.fill_between(range(len(RAM_history)), RAM_history, color="skyblue", alpha=0.5)
    ax.set_ylim(0, mem.total/1024/1024/1024+1)
    RAM_canva.draw()
    
    # GPU
    GPU_name.configure(text=f"GPU: {GPU_devices[0].name()}")
    GPU_usage.configure(text=f"GPU Utilization: {GPU_devices[0].gpu_utilization()}%")
    GPU_mem.configure(text=f"GPU Memory: {GPU_devices[0].memory_used_human()}")
    GPU_temp.configure(text=f"GPU Temperature: {GPU_devices[0].temperature()}°C")
    GPU_fanspeed.configure(text=f"GPU Fan Speed: {GPU_devices[0].fan_speed()}%")


    app.after(500, upd_usage)

# Functions
upd_usage()
RAM_canva.draw()
app.mainloop()