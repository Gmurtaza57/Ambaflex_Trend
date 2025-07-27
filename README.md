````markdown
# AmbaFlex Proximity Dashboard

This is a **Tkinter-based Python app** for viewing live proximity sensor trends from PLCs.  
It was designed to help technicians and engineers diagnose issues on AmbaFlex beds without needing PLC software.

---

## Features

- Live graph of two proximity sensors for any selected bed
- Pause button to freeze the graph and scroll back in time
- Simple PDF viewer to show a built-in help file
- Dark themed, easy-to-read interface

---

## Requirements

- Python 3.8+
- Install dependencies:
  ```bash
  pip install pycomm3 matplotlib pillow pymupdf
````

---

## How to Use

1. Set up the PLC IPs and bed tags in the `PLC_CONFIG` section of the code:

   ```python
   PLC_CONFIG = [
       ("Sorter A", "192.168.0.10", ["B1001", "B1002"]),
       ("Sorter B", "192.168.0.11", ["B2001", "B2002"])
   ]
   ```
2. Run the script:

   ```bash
   python main_file.py
   ```
3. Click a bed button to see its live proximity data.

---

## Building an EXE (Optional)

To create a standalone app:

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "readme.pdf;."main_file.py
```

---

## Notes

* Replace the placeholder IPs and bed tags with your own.
* The `resource_path()` function makes the app compatible with PyInstaller.
* A PDF named `readme.pdf` can be included to provide help within the app.

---

```
```
