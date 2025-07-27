# 📊 AmbaFlex Trend Dashboard

A **Python/Tkinter-based PLC dashboard** for live monitoring of proximity sensor signals from conveyors.  
This tool helps **Controls Engineers** and **Technicians** visualize sensor timing, troubleshoot issues faster, and reduce downtime.

---

## 🚀 Features
✅ **Live PLC Data Trending** – Plots proximity sensor values in real time using Matplotlib.  
✅ **Pause & Scrollback** – Freeze the live graph and scroll back up to 10 seconds.  
✅ **Multi-Sorter Support** – Add multiple PLCs and beds, switch between them dynamically.  
✅ **Built-in PDF Viewer** – Opens a “README Before Calling Controls” guide directly in the app.  
✅ **PyInstaller-Ready** – Easily package into an `.exe` for field deployment.  

---

## 📂 Project Structure

📁 Ambaflex_Trend/
├── main.py # Main application code
├── readme.pdf # (Optional) Help guide shown in-app
├── requirements.txt # Dependencies for installation
└── README.md # You are here


---

## ⚙️ Configuration

All PLC setup is handled in the `PLC_CONFIG` list in **main.py**:

```python
PLC_CONFIG = [
    ("Sorter A", "192.168.0.10", ["B1001", "B1002", "B1003"]),
    ("Sorter B", "192.168.0.11", ["B2001", "B2002", "B2003"]),
    ("Sorter C", "192.168.0.12", ["B3001", "B3002", "B3003"]),
]

    Sorter Name → Display label in the GUI

    IP Address → PLC’s IP address (replace with your site’s)

    Bed Tags → Tag prefixes for the beds you want to trend

👉 All values here are placeholders. Replace them with your own site’s PLC info.
🛠 Installation

1️⃣ Clone the repo

git clone https://github.com/YOURUSERNAME/Ambaflex_Trend.git
cd Ambaflex_Trend

2️⃣ Install dependencies

pip install -r requirements.txt

Dependencies include:

    tkinter (bundled with Python on Windows)

    pycomm3 (for PLC communications)

    matplotlib (for real-time plotting)

    PyMuPDF (to render PDFs)

    Pillow (for image support)

3️⃣ Run the app

python main.py

📊 How to Use

1️⃣ Select a bed tag from the panel on the left.
2️⃣ Watch the live proximity sensor graph update in real time.
3️⃣ Click Pause to freeze the trend and scroll back (0.1s or 0.5s increments).
4️⃣ Click README Before Calling Controls to open the PDF help guide.
📦 Build an Executable

This app is PyInstaller-compatible.
To create a .exe for deployment:

pyinstaller --onefile --noconsole main.py

The compiled file will appear in the dist folder.
🛡 Disclaimer

This is an open-source framework for Controls & Automation teams.

    🚫 No proprietary IPs, names, or credentials are included.

    ✅ Configure your own PLCs and bed tags before using in production.

👨‍💻 Credits

Developed by the Controls Engineering Team – shared for the automation community.
