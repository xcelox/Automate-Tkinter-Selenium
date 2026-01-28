# 🟦 **GitHub Badges (Prontos para colar no README)**

Você pode colocar estes no topo do README para deixar profissional:

```markdown
<p align="left">
  https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white
  https://img.shields.io/badge/Selenium-Automation-green?logo=selenium&logoColor=white
  https://img.shields.io/badge/Tkinter-GUI-orange
  https://img.shields.io/badge/Platform-Correios-yellow
  https://img.shields.io/badge/Status-Operational-success
</p>

# 📘 SADM — SMART Activation & Storage System

**SADM.py** is an automation tool built using **Python, Selenium, and Tkinter**.  
It accelerates and synchronizes two different internal Correios workflows:

1. **Object Tracking / Activation (SMArTi platform)**
2. **SMART Storage — Administrative Treatment (SSII platform)**

The system opens **two Chrome windows side-by-side** and processes every object code entered through the Tkinter interface, automatically executing all required actions in both platforms.

---

## 🚀 Main Features

### ✔ 1. Tracking Browser (Left Side)
- Automatic login to SMArTi  
- Navigates to **Security → Block/Activate Object**  
- Types the object code and submits using **ENTER**  
- Runs the internal activation flow automatically  

### ✔ 2. SMART Storage Browser (Right Side)
- Automatic login to SSII  
- Navigates to **Operational Management → Administrative Treatment**  
- Automatically fills the “information” field (from `informacoes.txt`, if present)  
- Automatically selects **option[4]** in the combo box  
- Reads → Finalizes → Confirms object treatment  
- Clears the field and prepares for the next entry  

### ✔ 3. Tkinter Operator Interface
- Clean and compact interface  
- Detects automatically when a **13‑character SRO code** is entered  
- Validates the Correios pattern (**AA123456789BB**)  
- Sends the value to both browser windows simultaneously  
- Automatically clears and waits for the next code  

### ✔ 4. Auto Split‑Screen Mode
The two Chrome browsers are automatically resized to occupy **half of the screen each**.

---

## 🗂 Required Files

Place these files in the same folder:

| File               | Description                                       |
|-------------------|----------------------------------------------------|
| `SADM.py`         | Main automation script                             |
| `chromedriver.exe` | Selenium Chrome driver                            |
| `usuario.txt`     | CAS username                                       |
| `senha.txt`       | CAS password                                       |
| `informacoes.txt` *(optional)* | Text for the info field in ADMN       |

---

## 🔧 Requirements

- Python 3.8 or newer  
- Google Chrome installed and updated  
- Selenium  
  ```bash
  pip install selenium