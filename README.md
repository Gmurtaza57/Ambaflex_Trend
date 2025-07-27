# AmbaFlex Proximity Dashboard

A **Tkinter-based real-time monitoring dashboard** for AmbaFlex beds that connects to Rockwell PLCs using `pycomm3`.  
This tool plots **live proximity sensor trends** for selected beds, helping technicians and engineers quickly diagnose issues without needing PLC software access.

---

## 🚀 Features

- 📊 **Live Graphing** of two proximity sensors (`PRX_OL1` and `PRX_OL2`) per bed  
- ⏸ **Pause & Scroll Timeline** — freeze live updates and scroll back through data  
- 📂 **Built-in PDF Viewer** — opens a `README` or support guide directly in the app  
- 🖥 **Clean, Dark-Themed UI** for control rooms and industrial environments  
- 🛠 **PLC Connectivity via pycomm3** for real-time data collection  
- ⚠ **Lockout Timer** (optional) — can disable app after a set date for version control

---

## 🗂 Project Structure

📁 AmbaFlex-Proximity-Dashboard
├── main.py # Main application code
├── readme.pdf # PDF shown in the in-app viewer
├── requirements.txt # Python dependencies
├── README.md # You are reading this file
└── (optional) config.json # External config for PLC IPs and beds (future-friendly)


---

## ⚙️ Requirements

- **Python 3.8+**
- The following Python packages (install via pip):
  ```bash
  pip install pycomm3 matplotlib pillow pymupdf

    A reachable Rockwell PLC (ControlLogix or CompactLogix)

    Configured PLC tags matching the naming convention:

    <BED_TAG>_PRX_OL1
    <BED_TAG>_PRX_OL2

🏗 How It Works

    Select a Sorter and Bed Tag from the buttons on the left panel.

    The dashboard connects to the PLC and streams live proximity values.

    Two lines are drawn on the graph:

        Blue → PRX_OL1

        Green → PRX_OL2

    You can pause the graph and scroll back in time using the timeline controls.

📖 App Layout

    Header Controls:

        ⏸ Pause Button → stops live updates and allows scrollback

        📄 README Button → opens an embedded PDF viewer for instructions/support

    Bed Selection Panel:

        Displays Sorter Names (e.g., “Sorter A”, “Sorter B”)

        Each sorter has buttons for configured Bed Tags

    Main Graph Area:

        Shows real-time proximity sensor trends

    Footer:

        Customizable branding message (e.g., Powered by Controls Team)

📝 Configuration

Inside the code, there’s a PLC_CONFIG list:

PLC_CONFIG = [
    ("Sorter A", "192.168.0.10", ["B1001", "B1002", "B1003"]),
    ("Sorter B", "192.168.0.11", ["B2001", "B2002", "B2003"]),
    ("Sorter C", "192.168.0.12", ["B3001", "B3002", "B3003"]),
]

    Sorter Name → Label shown in the UI

    PLC IP → The IP of the PLC for that sorter

    Bed Tags → List of beds (prefixes for sensor tags)

🔧 Tip: In a future version, this will move to a config.json file for easier editing.
🔒 Lockout Feature

The script includes a date-based lockout:

if datetime.now() >= datetime(2025, 12, 30):
    # Shows a lock screen and exits

    Change or remove this section if you don’t want the lockout behavior.

▶ How to Run

python main.py

📦 Building into an EXE (Optional)

Use PyInstaller if you want a standalone .exe:

pip install pyinstaller
pyinstaller --onefile --noconsole main.py

✅ The resource_path() helper is already included for PyInstaller compatibility.
⚠ Notes & Disclaimer

    No proprietary IPs or site-specific names are included.

    Replace placeholder IPs and Bed Tags with your own.

    This tool is intended for educational and troubleshooting purposes — use responsibly on production systems.

📜 License

MIT License — Free to use, modify, and distribute.
