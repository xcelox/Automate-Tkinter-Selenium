import os
import re
import time
import threading
import requests
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

def iniciar_navegador(x=0, y=0, largura=800, altura=800):
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option('prefs', {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    nav = webdriver.Chrome(service=ChromeService(executable_path='chromedriver.exe'),
                           options=chrome_options)

    nav.set_window_position(x, y)
    nav.set_window_size(largura, altura)
    return nav

def verificar_conexao(url="https://cas.correios.com.br/login?service=https%3A%2F%2Fssii.correios.com.br%2Fpages%2Finicio.jsf", timeout=10):
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def ler_credenciais():
    try:
        with open("usuario.txt", "r", encoding="utf-8") as fu:
            usuario = fu.read().strip()
        with open("senha.txt", "r", encoding="utf-8") as fs:
            senha = fs.read().strip()
        return (usuario if usuario else None), (senha if senha else None)
    except Exception as e:
        print(f"Erro ao ler arquivos de credenciais: {e}")
        return None, None

def validar_codigo_objeto(codigo: str):
    """
    Formato Correios: 2 letras + 9 dígitos + 2 letras (ex.: LB123456789BR)
    """
    padrao = r'^[A-Z]{2}[0-9]{9}[A-Z]{2}$'
    return bool(re.match(padrao, codigo.upper()))

def wait_click(nav, by, sel, t=20):
    elem = WebDriverWait(nav, t).until(EC.element_to_be_clickable((by, sel)))
    elem.click()
    return elem

def wait_sendkeys(nav, by, sel, texto, t=20, clear_js=True):
    elem = WebDriverWait(nav, t).until(EC.element_to_be_clickable((by, sel)))
    if clear_js:
        try:
            elem.clear()
        except Exception:
            pass
        nav.execute_script("arguments[0].value = '';", elem)
    elem.click()
    elem.send_keys(texto)
    return elem

def get_js_value(nav, elem):
    return nav.execute_script("return arguments[0].value;", elem)

def iniciar_rastreamento(login, senha):
    """
    Abre e navega até a tela de Bloqueio/Segurança (como no DSBLQ original).
    """
    nav = iniciar_navegador()
    nav.get("https://cas.correios.com.br/login?service=https%3A%2F%2Fsmarti.correios.com.br%2Fvalidar")

    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(login)
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(senha)
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fm1"]/div/div[2]/button'))).click()

    # menu Segurança -> bloqueio encomenda
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-top"]/li[4]/a'))).click()
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-top"]/li[4]/ul/div/div[1]/ul/li[5]/a'))).click()
    
    return nav  

def processar_rastreamento(nav_rastreamento, codigo):
    """
    Preenche o campo do rastreamento com o código e envia ENTER.
    """
    try:
        campo = WebDriverWait(nav_rastreamento, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='objeto']"))
        )
        
        try:
            campo.clear()
        except:
            pass
        nav_rastreamento.execute_script("arguments[0].value='';", campo)

        campo.click()
        campo.send_keys(codigo)
        campo.send_keys(Keys.ENTER)  
        
    except Exception as e:
        print(f"Erro rastreamento: {e}")

X_ADMN = {
    "menu_go": '//*[@id="menuGestaoOperacional"]/a',
    "menu_trat": '//*[@id="menuPrincipal:menuAlterarTratamentoAdministrativo"]',
    "info_text": '//*[@id="formularioDaPagina:txtInformacaoFiscalizacao"]',
    "codigo": '//*[@id="formularioDaPagina:edtCodigoObjeto"]',
    #"btn_ler": '//*[@id="formularioDaPagina:btnLerObjeto"]',
    #"btn_fin": '//*[@id="formularioDaPagina:btnFinalizar"]',
    "btn_conf": '//*[@id="formularioDaPagina:btnModalConfirmacaoAlteracao"]',
} 

def iniciar_armazenar_smart(login, senha, informacoes=""):
    """
    Abre e navega até Gestão Operacional → Alterar Tratamento Administrativo.
    Prepara o campo de informações e a opção do combo (mantido option[4]).
    """
    nav = iniciar_navegador()
    nav.get("https://cas.correios.com.br/login?service=https%3A%2F%2Fssii.correios.com.br%2Fpages%2Finicio.jsf")

    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(login)
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(senha)
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fm1"]/div/div[2]/button'))).click()

    wait_click(nav, By.XPATH, X_ADMN["menu_go"], 20)
    wait_click(nav, By.XPATH, X_ADMN["menu_trat"], 20)

    try:
        if informacoes:
            campo = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, X_ADMN["info_text"])))
            atual = (get_js_value(nav, campo) or "").strip()
            if atual != informacoes.strip():
                nav.execute_script("arguments[0].value = '';", campo)
                time.sleep(0.1)
                campo.click()
                campo.send_keys(informacoes)
                time.sleep(0.1)
    except Exception:
        pass

    try:
        wait_click(nav, By.XPATH, X_ADMN["trat_opt4"], 10)
        time.sleep(0.1)
    except Exception:
        pass

    return nav 

def processar_armazenar_smart(nav_admn, codigo):
    """
    Preenche o campo 'edtCodigoObjeto', clica 'Ler Objeto' → 'Finalizar' → 'Confirmar' (se modal),
    e então limpa o campo para a próxima leitura.
    """
    try:
        print(f"\n[ArmazenarSmart] Processando: {codigo}")
        campo = WebDriverWait(nav_admn, 10).until(
            EC.element_to_be_clickable((By.XPATH, X_ADMN["codigo"]))
        )

        nav_admn.execute_script("arguments[0].value='';", campo)
        try:
            campo.clear()
        except Exception:
            pass
        campo.click()
        campo.send_keys(codigo)

        wait_click(nav_admn, By.XPATH, X_ADMN["btn_ler"], 10)
        time.sleep(0.3)
        wait_click(nav_admn, By.XPATH, X_ADMN["btn_fin"], 10)

        try:
            btn = WebDriverWait(nav_admn, 10).until(
                EC.element_to_be_clickable((By.XPATH, X_ADMN["btn_conf"]))
            )
            btn.click()
            time.sleep(0.2)
            print(f"[ArmazenarSmart] OK: {codigo} finalizado.")
        except TimeoutException:
            print("[ArmazenarSmart] Aviso: modal de confirmação não apareceu.")

        try:
            campo = WebDriverWait(nav_admn, 10).until(
                EC.element_to_be_clickable((By.XPATH, X_ADMN["codigo"]))
            )
            nav_admn.execute_script("""
                const c = arguments[0];
                c.value = '';
                c.dispatchEvent(new Event('input', {bubbles: true}));
                c.dispatchEvent(new Event('change', {bubbles: true}));
                c.dispatchEvent(new Event('blur', {bubbles: true}));
            """, campo)
            time.sleep(0.1)
            campo.click()
        except Exception:
            pass

    except Exception as e:
        print(f"[ArmazenarSmart] Erro: {e}")

def dividir_tela_meio(nav_esquerda, nav_direita):
    """
    Coloca os dois navegadores ocupando metade da tela cada.
    """
    root = tk.Tk(); root.withdraw()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.destroy()

    try:
        nav_esquerda.set_window_position(0, 0)
        nav_esquerda.set_window_size(sw // 2, sh)
    except Exception:
        pass

    try:
        nav_direita.set_window_position(sw // 2, 0)
        nav_direita.set_window_size(sw // 2, sh)
    except Exception:
        pass

def sincronizar_processos(objeto, nav_rastreamento, nav_admn):
    """
    Processa nas duas janelas:
      1) rastreamento (bloqueio/ativação)
      2) armazenar_smart (tratamento administrativo)
    """
    try:
        print(f"Iniciando processamento do objeto: {objeto}")
        processar_rastreamento(nav_rastreamento, objeto)
        time.sleep(0.6)
        processar_armazenar_smart(nav_admn, objeto)
        print(f"Objeto {objeto} processado nas duas janelas.")
    except Exception as e:
        print(f"Erro ao sincronizar processos: {e}")

def iniciar_dois_navegadores(login, senha, informacoes=""):
    """
    Inicializa e autentica:
      - nav_rastreamento  (esquerda)
      - nav_admn (armazenar_smart) (direita)
    """
    nav1 = nav2 = None
    try:
        nav1 = iniciar_rastreamento(login, senha)   
    except Exception as e:
        print(f"Erro ao iniciar navegador (rastreamento): {e}")

    try:
        nav2 = iniciar_armazenar_smart(login, senha, informacoes)  
    except Exception as e:
        print(f"Erro ao iniciar navegador (armazenar_smart): {e}")

    if nav1 and nav2:
        dividir_tela_meio(nav1, nav2)

    return nav1, nav2

def obter_dados_tkinter():
    
    def centralizar_janela(janela, largura, altura, posicao='centro_inferior'):
        janela.update_idletasks()
        screen_largura = janela.winfo_screenwidth()
        screen_altura = janela.winfo_screenheight()
        if posicao == 'centro_inferior':
            x = (screen_largura // 2) - (largura // 2)
            y = screen_altura - altura - 80
        else:
            x = (screen_largura // 2) - (largura // 2)
            y = (screen_altura // 2) - (altura // 2)
        janela.geometry(f'{largura}x{altura}+{x}+{y}')

    def iniciar_processo():
        login, senha = ler_credenciais()
        if not login or not senha:
            messagebox.showwarning("Erro", "Credenciais inválidas.")
            return

        try:
            with open("informacoes.txt", "r", encoding="utf-8") as fi:
                informacoes = fi.read().strip()
        except Exception:
            informacoes = ""

        root.destroy()
        threading.Thread(target=lambda: abrir_interface_objetos(login, senha, informacoes)).start()

    def abrir_interface_objetos(login, senha, informacoes):

        nav_rastreamento, nav_admn = iniciar_dois_navegadores(login, senha, informacoes)

        janela_obj = tk.Tk()
        janela_obj.title("Sistema de Desbloqueio Expedição e Triagem RFB") 
        janela_obj.configure(bg='#17234E')
        largura = 1400
        altura = 200
        janela_obj.geometry(f'{largura}x{altura}')
        janela_obj.resizable(False, False)

        tk.Label(
            janela_obj,
            text="Digite o código do objeto:",
            bg='#17234E',
            fg='white',
            font=("Arial", 16)
        ).pack(pady=15)

        entry_objeto = tk.Entry(janela_obj, bg='white', fg='black', font=("Arial", 18), width=30)
        entry_objeto.pack(pady=10)
        entry_objeto.focus()

        def enviar_objeto():
            objeto = entry_objeto.get().strip().upper()
            if not validar_codigo_objeto(objeto):
                messagebox.showwarning("Código inválido", "O código do objeto não está no formato correto.")
                return
            sincronizar_processos(objeto, nav_rastreamento, nav_admn)
            entry_objeto.delete(0, tk.END)

        def verificar_leitura():
            texto = entry_objeto.get().strip()
            if len(texto) == 13:
                enviar_objeto()
            janela_obj.after(500, verificar_leitura)

        verificar_leitura()

        botao_enviar = tk.Button(
            janela_obj,
            text="Enviar",
            command=enviar_objeto,
            bg="#468146",
            fg="white",
            font=("Arial", 16),
            width=10,
            height=1
        )
        botao_enviar.pack(pady=15)

        centralizar_janela(janela_obj, largura, altura, posicao='centro_inferior')
        janela_obj.mainloop()

    root = tk.Tk()
    root.title("SDEX_Objetos")
    root.configure(bg='#17234E')
    root.geometry('300x100')
    root.resizable(False, False)

    tk.Label(root, text="Clique para iniciar o processo",
             bg='#17234E', fg='white', font=("Arial", 12)).pack(pady=20)

    botao = tk.Button(root, text="Iniciar", command=iniciar_processo,
                      bg="#3078E2", fg="white", font=("Arial", 14))
    botao.pack(pady=10)

    centralizar_janela(root, 300, 150)
    root.mainloop()

if __name__ == "__main__":
    if not verificar_conexao():
        print("Sem conexão ou portal indisponível. Tente novamente.")
    else:
        obter_dados_tkinter()

