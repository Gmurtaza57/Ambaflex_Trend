# AmbaFlex Trend Dashboard

A Python/Tkinter-based PLC dashboard for live monitoring of proximity sensor signals from conveyors.  
This tool helps Controls Engineers and Technicians visualize sensor timing, troubleshoot issues faster, and reduce downtime.

---

## Features

- Live PLC data trending using Matplotlib  
- Pause and scrollback up to 10 seconds  
- Multi-sorter support (configure multiple PLCs and beds)  
- Built-in PDF viewer for quick reference documentation  
- Compatible with PyInstaller for `.exe` packaging  

---

## Project Structure

Ambaflex_Trend/
├── main.py # Main application code
├── readme.pdf # (Optional) Help guide shown in-app
├── requirements.txt # Python dependencies
└── README.md # This file


---

## Configuration

PLC setup is defined in the `PLC_CONFIG` list in `main.py`:

```python
PLC_CONFIG = [
    ("Sorter A", "192.168.0.10", ["B1001", "B1002", "B1003"]),
    ("Sorter B", "192.168.0.11", ["B2001", "B2002", "B2003"]),
    ("Sorter C", "192.168.0.12", ["B3001", "B3002", "B3003"]),
]

    Sorter Name – Label shown in the interface

    IP Address – PLC IP address (replace with your own)

    Bed Tags – Tag prefixes for the beds you want to trend

Installation

    Clone the repository:

git clone https://github.com/YOURUSERNAME/Ambaflex_Trend.git
cd Ambaflex_Trend

Install dependencies:

pip install -r requirements.txt

Run the application:

    python main.py

Usage

    Select a bed tag from the panel on the left.

    View live proximity sensor signals on the graph.

    Use the Pause button to stop updates and scroll back in time.

    Open the built-in PDF viewer for the "README Before Calling Controls" guide.

Building an Executable

To create a standalone .exe file using PyInstaller:

pyinstaller --onefile --noconsole main.py

The executable will be in the dist folder.
Disclaimer

This is an open-source framework for Controls and Automation teams.
No proprietary IPs or site-specific data are included. Configure your own PLCs and bed tags before using in production.
Credits

Developed by the Controls Engineering Team and shared for the automation community.
