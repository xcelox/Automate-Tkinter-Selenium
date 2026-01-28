<h1>📘 SADM — SMART Activation & Storage System</h1> 

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
|------------------- |---------------------------------------------------|
| `SADM.py`          | Main automation script                            |
| `chromedriver.exe` | Selenium Chrome driver                            |
| `usuario.txt`      | CAS username                                      |
| `senha.txt`        | CAS password                                      |
| `informacoes.txt` *(optional)* | Text for the info field in ADMN       |

---

## ## 🚀Technologies

- Python 3.8 or newer  
- Google Chrome installed and updated  
- Selenium  
  ```bash
  pip install selenium


<div>
   
   <img src="https://img.shields.io/badge/Python-F7DF1E?style=for-the-badge&logo=python&logoColor=yelow">
   <img src="https://img.shields.io/badge/TKinter-17234E?style=for-the-badge&logo=Tkinter&logoColor=red">
   <img src="https://img.shields.io/badge/Selenium-239120?style=for-the-badge&logo=selenium&logoColor=withe">
  
</div>

</div>

## 👨‍💻Developer

[<img loading="lazy" src="https://avatars.githubusercontent.com/u/101431653?v=4" width=115><br><sub>| Marcelo Lourenço |</sub>](https://github.com/xcelox)
</div>
