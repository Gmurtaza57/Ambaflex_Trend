import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pycomm3 import LogixDriver
from datetime import datetime
import time
import fitz
from PIL import Image, ImageTk
import io
import sys
import os

# For PyInstaller compatibility
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Equipment + Bed config
PLC_CONFIG = [
    ("Sorter A", "192.168.0.10", ["B1001", "B1002", "B1003"]),
    ("Sorter B", "192.168.0.11", ["B2001", "B2002", "B2003"]),
    ("Sorter C", "192.168.0.12", ["B3001", "B3002", "B3003"]),
]


class LivePLCGraph:
    def __init__(self, parent, plc_ip, bed_tag):
        self.prox1_tag = f"{bed_tag}_PRX_OL1"
        self.prox2_tag = f"{bed_tag}_PRX_OL2"
        self.paused = False

        try:
            self.plc = LogixDriver(plc_ip)
            self.plc.open()
        except Exception as e:
            messagebox.showerror("PLC Error", f"Failed to connect to PLC: {e}")
            self.plc = None

        self.fig = Figure(figsize=(10, 3.5), facecolor="#121212")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#121212")
        self.ax.set_ylim(-0.5, 1.5)
        self.ax.set_xlim(0, 10)
        self.ax.set_yticks([0, 1])
        self.ax.set_yticklabels(['0', '1'], color='white')
        self.ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
        self.ax.tick_params(colors='white', labelsize=8)
        self.ax.get_xaxis().set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)

        title_label = tk.Label(parent, text=f"Live Trend for Bed: {bed_tag}", font=("Arial", 12),
                               fg="white", bg="#121212", pady=5)
        title_label.pack()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.line1, = self.ax.plot([], [], color='deepskyblue', drawstyle='steps-post', label='Prox1')
        self.line2, = self.ax.plot([], [], color='lime', drawstyle='steps-post', label='Prox2')
        self.ax.legend(loc="upper right", fontsize=8, facecolor="#121212", edgecolor="gray", labelcolor='white')

        self.window = 1  # show last 10 seconds
        self.sample_interval = 0.001  # 50 ms
        self.max_samples = int(self.window / self.sample_interval) + 10
        self.start_time = time.time()
        self.times, self.prox1_data, self.prox2_data = [], [], []
        self.view_index = -1
        self.paused_time = 0
        self.time_label = None  # Will be set later

        self.update_plot()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.paused_time = time.time() - self.start_time
            self.view_index = -1
            self.update_paused_plot()

    def update_paused_plot(self):
        if not self.paused:
            return

        index_offset = self.view_index
        if abs(index_offset) >= len(self.times):
            index_offset = -len(self.times) + 1

        view_time = self.times[index_offset]
        self.line1.set_data(self.times, self.prox1_data)
        self.line2.set_data(self.times, self.prox2_data)
        self.ax.set_xlim(view_time - self.window, view_time)
        self.canvas.draw_idle()

        if self.time_label:
            self.time_label.config(text=f"⏸ Paused at: {self.paused_time:.2f}s | Viewing: {view_time:.2f}s")

    def read_proximity_values(self):
        try:
            prox1 = self.plc.read(self.prox1_tag).value
            prox2 = self.plc.read(self.prox2_tag).value
            return int(bool(prox1)), int(bool(prox2))
        except:
            return 0, 0

    def update_plot(self):
        if self.paused:
            self.canvas.get_tk_widget().after(int(self.sample_interval * 1000), self.update_plot)
            return

        t = time.time() - self.start_time
        p1, p2 = self.read_proximity_values()

        if self.times:
            self.times.append(t - 0.0001)
            self.prox1_data.append(self.prox1_data[-1])
            self.prox2_data.append(self.prox2_data[-1])

        self.times.append(t)
        self.prox1_data.append(p1)
        self.prox2_data.append(p2)

        self.times = self.times[-self.max_samples * 2:]
        self.prox1_data = self.prox1_data[-self.max_samples * 2:]
        self.prox2_data = self.prox2_data[-self.max_samples * 2:]

        self.line1.set_data(self.times, self.prox1_data)
        self.line2.set_data(self.times, self.prox2_data)
        self.ax.set_xlim(max(0, t - self.window), t)
        self.canvas.draw_idle()
        self.canvas.get_tk_widget().after(int(self.sample_interval * 1000), self.update_plot)

def open_pdf_viewer():
    try:
        pdf_path = resource_path("readme.pdf")
        doc = fitz.open(pdf_path)
        viewer = tk.Toplevel(root)
        viewer.title("README - Before Calling Controls")
        viewer.geometry("800x600")
        viewer.configure(bg="#1e1e1e")

        canvas = tk.Canvas(viewer, bg="#1e1e1e")
        scrollbar = tk.Scrollbar(viewer, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#1e1e1e")

        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.open(io.BytesIO(pix.tobytes("ppm")))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(scroll_frame, image=img_tk, bg="#1e1e1e")
            lbl.image = img_tk
            lbl.pack(pady=10)

        scroll_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    except Exception as e:
        messagebox.showerror("PDF Error", f"Could not load README PDF:\n{e}")
def shift_view(seconds):
    if current_graph and current_graph.paused:
        samples_to_shift = int(seconds / current_graph.sample_interval)
        max_index = len(current_graph.times) - 1

        # Move index but clamp it to avoid empty graph
        current_graph.view_index = max(-max_index, min(-1, current_graph.view_index - samples_to_shift))

        current_graph.update_paused_plot()


# -- UI Setup --
root = tk.Tk()
root.title("AmbaFlex Proximity Dashboard - Powered by Ghulam Murtaza")
root.geometry("1100x700")
root.configure(bg="#121212")

top = tk.Frame(root, bg="#121212")
top.pack(pady=5, fill="x")
timeline_frame = tk.Frame(top, bg="#121212")
timeline_frame.pack(side="left", padx=10)

back5_btn = tk.Button(timeline_frame, text="⏪ -0.5s", bg="gray", fg="white",
                      command=lambda: shift_view(-0.5))
back1_btn = tk.Button(timeline_frame, text="⬅️ -0.1s", bg="gray", fg="white",
                      command=lambda: shift_view(-0.1))
forward1_btn = tk.Button(timeline_frame, text="➡️ +0.1s", bg="gray", fg="white",
                         command=lambda: shift_view(0.1))


back5_btn.pack(side="left", padx=2)
back1_btn.pack(side="left", padx=2)
forward1_btn.pack(side="left", padx=2)

time_label = tk.Label(timeline_frame, text="⏸ Paused at: 0s", font=("Arial", 9),
                      bg="#121212", fg="white")
time_label.pack(side="left", padx=10)

# Placeholder for global pause button access
pause_btn = tk.Button(top, text="Pause", font=("Arial", 10), bg="darkorange", fg="black")
pause_btn.pack(side="right", padx=10)

menu_btn = tk.Button(top, text="README Before Calling Controls", command=open_pdf_viewer,
                     font=("Arial", 10), bg="darkred", fg="white")
menu_btn.pack(side="right", padx=10)

bed_panel = tk.Frame(root, bg="#121212")
bed_panel.pack(pady=10)

graph_frame = tk.Frame(root, bg="#121212")
graph_frame.pack(fill="both", expand=True)

current_graph = None

def load_bed_graph(ip, tag):
    global current_graph
    for widget in graph_frame.winfo_children():
        widget.destroy()
    current_graph = LivePLCGraph(graph_frame, ip, tag)
    pause_btn.config(command=current_graph.toggle_pause)
    current_graph.time_label = time_label  # Link label


for sorter, ip, beds in PLC_CONFIG:
    lbl = tk.Label(bed_panel, text=sorter, font=("Arial", 13, 'bold'), bg="#121212", fg="lightblue")
    lbl.pack(anchor="w", padx=10, pady=(10, 2))

    row_frame = tk.Frame(bed_panel, bg="#121212")
    row_frame.pack(anchor="w", padx=20)

    for i, tag in enumerate(beds):
        btn = tk.Button(row_frame, text=tag, width=12,
                        command=lambda ip=ip, tag=tag: load_bed_graph(ip, tag),
                        bg="gray", fg="white", font=("Arial", 10))
        btn.grid(row=i // 4, column=i % 4, padx=5, pady=3)

footer = tk.Label(root, text="Powered by Ghulam Murtaza",
                  font=("Arial", 10), bg="#121212", fg="white")
footer.pack(side="bottom", pady=5)

root.mainloop()
