# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import schedule
import time
import json
import os
from urllib.parse import quote
from datetime import datetime
import random
import time
import threading
import re
import unicodedata

mes_actual = datetime.now().strftime("%Y-%m")
# ===========================
# CONFIG
# ===========================


URL_LINKEDIN = "https://www.linkedin.com/jobs/search/?currentJobId=4413503372&f_TPR=r86400&f_WT=2&geoId=91000011&keywords=data%20analyst&sortBy=DD"         
URL_ELEMPEO = "https://www.elempleo.com/co/ofertas-empleo/trabajo-datos?Salaries=4-45-millones:45-55-millones:55-6-millones:6-8-millones:8-10-millones:10-125-millones:125-15-millones:15-18-millones:18-21-millones:mas-21-millones:salario-confidencial&PublishDate=hoy"
URL_MAGNETO = "https://www.magneto365.com/co/trabajos/buscar/loc-bogota-d.c.-co/datos?order=desc_fecha-publicacion"
URL_INDEED = "https://co.indeed.com/jobs?q=data&l=Bogot%C3%A1%2C+Cundinamarca&sort=date&vjk=1732ecfd9a089776"
URL_MICHEL = "https://www.michaelpage.com.co/jobs/data?sort_by=most_recent"
URL_JOBGETHER = "https://jobs.lever.co/jobgether?location=Colombia&workplaceType=remote&commitment=Full-time"
URL_INFOJOBS = "https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=data&searchByType=country&referer=search-filtered&segmentId=&page=1&sortBy=RELEVANCE&onlyForeignCountry=false&countryIds=11&sinceDate=_24_HOURS"
URL_EPAM = "https://careers.epam.com/en/jobs?country=8150000000000001044&search=data%20analyst&seniority=lead,middle%20management,junior,middle&sort_by=relevance"
URL_COMPUTRABAJO = "https://co.computrabajo.com/trabajo-de-datos?pubdate=1&sal=7&by=publicationtime"
URL_MASTERCARD ="https://mastercard.wd1.myworkdayjobs.com/en-US/CorporateCareers?q=data&locations=60e8f8188b901000c330d5992aef0000&locations=5ce3d45a86824dcbb8736efbe3201cb1"
ARCHIVO_OFERTAS = "ofertas_enviadas.txt"

# ===========================
# BÚSQUEDAS LINKEDIN (ES + EN)
# ===========================

BUSQUEDAS_LINKEDIN = [

    # Perfil innovación

    "líder de innovación",
    "especialista en innovación",
    "coordinador de innovación",
    "líder de transformación digital",
    "líder de proyectos de innovación",
    "gestor de proyectos de innovación",
    "líder de laboratorio de innovación",
    "líder de innovación en ia",
    "innovation lead",
    "innovation specialist",
    "innovation coordinator",
    "digital transformation lead",
    "innovation project lead",
    "innovation project coordinator",
    "innovation lab lead",
    "ai innovation lead",

    # Perfil datos
    "data analyst",
    "analytics engineer",
    "business intelligence analyst",
    "data operations analyst",
    "NoSQL",
    "data",
    "Mongodb",
    "neo4j",

    # BUSINESS / PROCESS
    "business systems analyst",
    "financial systems analyst",
    "business process analyst",
    "operations analyst",
    "process automation analyst",
 

    # AUTOMATION / TOOLS
    "automation analyst",
    "power platform",
    "innovation analyst",
    "continuous improvement analyst",
    "digital transformation analyst",


    # DATOS Y ANALÍTICA
    "analista de datos",
    "ingeniero de analítica",
    "analista de inteligencia de negocios",
    "analista de operaciones de datos",
    "analista de reportes y automatización",
    "analista de calidad de datos",

    # NEGOCIO / SISTEMAS
    "analista de sistemas de negocio",
    "analista de sistemas financieros",
    "analista de procesos de negocio",
    "analista funcional ti",
    "analista de cumplimiento y datos",

    # AUTOMATIZACIÓN / INNOVACIÓN
    "analista de automatización",
    "analista de automatización de procesos",
    "especialista en power platform",
    "analista de mejora continua",
    "analista de innovación",
    "analista de transformación digital"

]

# ===========================
# KEYWORDS FILTRO FINAL
# ===========================

KEYWORDS = [
        # Perfil innovación
    "líder de innovación",
    "especialista en innovación",
    "coordinador de innovación",
    "líder de transformación digital",
    "líder de proyectos de innovación",
    "gestor de proyectos de innovación",
    "líder de laboratorio de innovación",
    "líder de innovación en ia",
    "innovation lead",
    "innovation specialist",
    "innovation coordinator",
    "digital transformation lead",
    "innovation project lead",
    "innovation project coordinator",
    "innovation lab lead",
    "ai innovation lead",
    "data", "analyst", "analytics", "business intelligence", "bi",
    "analítica", "datos", "etl", "pipelines", "mejora continua",
    "business analyst", "analista de negocio",
    "analista funcional", "business systems",
    "operations", "operaciones",
    "process", "procesos",
    "automation", "automatización",
    "workflow", "low code",
    "python", "sql", "power bi", "tableau", "sap", "power automate",
    "power apps", "powerapps", "power platform", "nosql", "json",
    "dax"
    "treasury", "finance", "financial", "audit"
]

# ===========================
# CHROME DRIVER
# ===========================

options = webdriver.ChromeOptions()


options.add_argument("--start-maximized")
options.add_argument("--log-level=3")
options.add_argument("--disable-webrtc")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)
#driver = webdriver.Chrome()

# ===========================
# CHROME DRIVER LOGIN
# ===========================

options_login = webdriver.ChromeOptions()

options_login.add_argument(r"--user-data-dir=C:\selenium_profile")
options_login.add_argument("--start-maximized")
options_login.add_argument("--log-level=3")
options_login.add_argument("--disable-webrtc")
options_login.add_argument("--disable-blink-features=AutomationControlled")

options_login.add_experimental_option(
    "excludeSwitches",
    ["enable-logging"]
)

driver_login = webdriver.Chrome(options=options_login)

wait_login = WebDriverWait(driver_login, 10)

# ===========================
# MEMORIA PERSISTENTE
# ===========================

if os.path.exists(ARCHIVO_OFERTAS):
    
    with open(ARCHIVO_OFERTAS, "r", encoding="utf-8") as f:
        ofertas_enviadas = set(f.read().splitlines())
else:
    ofertas_enviadas = set()

def guardar_oferta(clave):
    with open(ARCHIVO_OFERTAS, "a", encoding="utf-8") as f:
        f.write(clave + "\n")

# ===========================
# SCORE INTELIGENTE (BASE 3)
# ===========================

def calcular_score(titulo):
    t = titulo.lower()

    # Score base
    score = 3

    if "python" in t: score += 3
    if "líder de innovación" in t or "lider de innovacion" in t or "innovation lead" in t or "innovation lab lead" in t: score += 5

    if "especialista en innovación" in t or "especialista en innovacion" in t or "innovation specialist" in t or "coordinador de innovación" in t or "coordinador de innovacion" in t or "innovation coordinator" in t: score += 4

    if "líder de proyectos de innovación" in t or "lider de proyectos de innovacion" in t or "gestor de proyectos de innovación" in t or "gestor de proyectos de innovacion" in t or "innovation project lead" in t or "innovation project coordinator" in t: score += 4

    if "líder de transformación digital" in t or "lider de transformacion digital" in t or "digital transformation lead" in t: score += 3

    if "líder de innovación en ia" in t or "lider de innovacion en ia" in t or "ai innovation lead" in t: score += 3
    
    if "mongoDB" in t or "mongo bd" in t or "mongo" in t: score += 3
    if "low code" in t or "lowcode" in t: score += 3
    if "automation" in t or "automatización" in t: score += 3
    if "power bi" in t: score += 3
    if "tableau" in t: score += 2
    if "powerapps" in t or "power apps" in t: score += 3
    if "powerautomate" in t or "power automate" in t: score += 3
    if "powerplatform" in t or "power platform" in t: score += 3
    if "business analyst" in t or "analista de negocio" in t: score += 3
    if "data" in t or "datos" in t: score += 3
    if "analytics" in t or "analítica" in t: score += 3
    if "analyst" in t or "analista" in t: score += 3
    if "process" in t or "procesos" in t: score += 1
    if "operations" in t or "operaciones" in t: score += 1
    if "sql" in t: score += 3
    if "nosql" in t: score += 3
    if "ETL" in t or "ELT" in t: score += 3
    if "SAP" in t or "SAP HANA" in t: score += 3
    if "Excel" in t or "Macros" in t: score += 3
  

    return score

def pasa_filtro(titulo):
    t = titulo.lower()
    return any(k in t for k in KEYWORDS)

# ===========================
# TELEGRAM
# ===========================

# ===========================
# CONFIG
# ===========================

# Credenciales: se leen de variables de entorno (archivo .env), nunca del código.
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "TU_TOKEN_AQUI")        # bot perfil datos
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "TU_CHAT_ID_AQUI")

TELEGRAM_BOT_TOKEN2 = os.getenv("TELEGRAM_BOT_TOKEN2", "TU_TOKEN_AQUI")      # bot perfil innovación
TELEGRAM_CHAT_ID2 = os.getenv("TELEGRAM_CHAT_ID2", "TU_CHAT_ID_AQUI")

def enviar_telegram(mensaje, clave):
    if clave in ofertas_enviadas:
        #print(" oferta ya enviada", clave)
        return
    t_normalizado = "".join(
    c for c in unicodedata.normalize("NFD", clave.lower())
    if unicodedata.category(c) != "Mn"
    )

    if (
        "lider de innovacion" in t_normalizado
        or "especialista en innovacion" in t_normalizado
        or "proyectos de innovacion" in t_normalizado
        or "innovacion" in t_normalizado
        or "innovation specialist" in t_normalizado
        or "coordinador de innovacion" in t_normalizado
        or "innovation lead" in t_normalizado
        or "innovation specialist" in t_normalizado
        or "innovation coordinator" in t_normalizado
        or "innovation project lead" in t_normalizado
        or "innovation lab lead" in t_normalizado
        or "transformacion digital" in t_normalizado
        or "digital transformation lead" in t_normalizado
        or "innovacion en ia" in t_normalizado
        or "ai innovation lead" in t_normalizado
    ):
        token = TELEGRAM_BOT_TOKEN2
        chat_id = TELEGRAM_CHAT_ID2
    else:
        token = TELEGRAM_BOT_TOKEN
        chat_id = TELEGRAM_CHAT_ID
        
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    requests.post(url, data={
        "chat_id": chat_id,
        "text": mensaje
    })

    ofertas_enviadas.add(clave)
    guardar_oferta(clave)
    hora_envio = datetime.now().strftime("%H:%M:%S")
    print("✅ Enviado:", clave,'\n', mensaje)
    # 🔥 EXTRAER DESCRIPCIÓN
    #descripcion = obtener_descripcion_linkedin_debug(link)
    #print(descripcion[:4000])  # 👈 solo preview
    print(hora_envio,'\n\n')
    
    
# ===========================
# DESCRIPTION LINKEDIN
# ===========================

def obtener_descripcion_linkedin_debug(link):
    try:
        original_window = driver.current_window_handle
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        driver.get(link)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        

        descripcion = driver.find_element(
            By.CLASS_NAME, "show-more-less-html__markup"
        ).text

        driver.close()
        driver.switch_to.window(original_window)

        return descripcion

    except Exception as e:
        try:
            driver.switch_to.window(original_window)
        except:
            pass
        return f"Error: {str(e)}"

# ===========================
# LINKEDIN MULTI SEARCH
# ===========================
contador_url = 0  # variable global
def buscar_linkedin():
    print("🔎 Buscando en LinkedIn...",datetime.now().strftime("%H:%M:%S"))
    global contador_url
    LIMITE = random.randint(100, 170)

    for termino in BUSQUEDAS_LINKEDIN:
        
        # 🔀 Condicional de cambio de URL
        if contador_url >= LIMITE:
            url = (
                "https://www.linkedin.com/jobs/search?keywords=Data&location=Colombia&geoId=100876405&f_TPR=r86400&f_WT=2&position=1&pageNum=0"
            )
            print("🌐 Usando URL REMOTO")
            contador_url = 0  # 🔁 reinicia
        else:
            # 👉 URL original (Bogotá)

            url = (
                "https://www.linkedin.com/jobs/search?"
                #f"keywords={quote(termino)}&location=Colombia&f_TPR=r86400&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD"
                f"keywords={quote(termino)}&location=Bogotá%2C+Distrito+Capital%2C+Colombia&geoId=102361989&trk=public_jobs_jobs-search-bar_search-submit&f_TPR=r86400&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD"
            )
        contador_url += 1  # 🔢 suma al final
        driver.get(url)
        #print(driver.page_source)
        time.sleep(10)
            # 🔥 Espera inteligente a que carguen los resultados
        try:
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "base-card"))
            ) # PARA NO LOGEADO

        except:
            #print("⚠ LinkedIn no cargó resultados (posible login o bloqueo)")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        ofertas = soup.find_all("div", class_="base-card") #PARA NO LOGUEADOS

        for oferta in ofertas[:20]:
            try:
                titulo = oferta.find("h3").text.strip()
                empresa = oferta.find("h4").text.strip()
                link = oferta.find("a")["href"]
                tiempo = oferta.find("time").text.strip() if oferta.find("time") else "Sin tiempo"
                location = oferta.find("span").text.strip() 
                if not pasa_filtro(titulo):
                    continue

                score = calcular_score(titulo)

                if score < 5:
                    
                    continue

                
                clave = f"li-{titulo.lower().strip()}-{empresa.lower().strip()}-{mes_actual}"
                
                mensaje = (
                    f"💼 LinkedIn\n"
                    f"🔎 {termino}\n"
                    f"⭐ Score: {score}/15\n"
                    f"{titulo}\n"
                    f"🏢 {empresa}\n"
                    f"🏢 {location}\n"
                    f"⏱ {tiempo}\n"
                    f"🔗 {link}"
                    
                )

                enviar_telegram(mensaje, clave)#, link)

            except:
                continue
                
                
# ===========================
# LinkedIN
# ===========================                
                
def buscar_linkedin_Login():
    print("🔎 Buscando en LinkedIn REMOTO LATAM...",datetime.now().strftime("%H:%M:%S"))
    print("🌐 Usando URL REMOTO LATAM ---")
   
    driver_login.get(URL_LINKEDIN)
    time.sleep(10)
    
    
    
    
# Scroll para cargar lazy load
    for _ in range(30):
        driver_login.execute_script("window.scrollBy(0, 800);")
        time.sleep(0.7)
    time.sleep(3)

    datos = driver_login.execute_script("""
        const resultados = [];
        const vistos = new Set();
        const jobLinks = [...document.querySelectorAll('a[href*="/jobs/view/"]')];

        jobLinks.forEach(a => {
            try {
                const href = a.href || '';
                const match = href.match(/\\/jobs\\/view\\/(\\d+)/);
                if (!match) return;

                const jobId = match[1];
                if (vistos.has(jobId)) return;
                vistos.add(jobId);

                // Tomar solo la primera linea del texto del <a>
                const textoA = (a.innerText || '').trim();
                let titulo = textoA.split('\\n')[0].trim();
                titulo = titulo.replace(/\\s*with verification\\s*/gi, '').trim();
                titulo = titulo.replace(/\\s*empleo verificado\\s*/gi, '').trim();
                if (!titulo || titulo.length < 5) return;

                // Subir hasta contenedor con suficiente texto
                let container = a.parentElement;
                let lineas = [];
                for (let i = 0; i < 20; i++) {
                    if (!container) break;
                    const texto = container.innerText || '';
                    lineas = texto.split('\\n')
                        .map(l => l.trim())
                        .filter(l => l.length > 2);
                    // Necesitamos al menos titulo + empresa + ubicacion
                    if (lineas.length >= 4) break;
                    container = container.parentElement;
                }

                // Filtrar lineas que sean el titulo
                const lineasSinTitulo = lineas.filter(l => 
                    l !== titulo && 
                    !l.toLowerCase().includes(titulo.toLowerCase().substring(0, 25))
                );

                const empresa   = lineasSinTitulo[0] || 'Sin empresa';
                const ubicacion = lineasSinTitulo[1] || 'Sin ubicación';

                // Tiempo — buscar en lineas restantes
                let tiempo = 'Sin tiempo';
                for (const l of lineasSinTitulo) {
                    if (/ago|hour|day|week|month|minute/i.test(l) ||
                        /hace|hora|día|semana|mes|minuto/i.test(l)) {
                        tiempo = l;
                        break;
                    }
                }

                const link = `https://www.linkedin.com/jobs/view/${jobId}/`;
                resultados.push({ jobId, titulo, empresa, ubicacion, tiempo, link });

            } catch(e) {}
        });
        return resultados;
    """)

    if not datos:
        print("❌ No se encontraron ofertas")
        return

    print(f"📦 Ofertas encontradas: {len(datos)}")

    for oferta in datos:
        try:
            titulo    = oferta.get('titulo', '').strip()
            empresa   = oferta.get('empresa', 'Sin empresa').strip()
            ubicacion = oferta.get('ubicacion', 'Sin ubicación').strip()
            tiempo    = oferta.get('tiempo', 'Sin tiempo').strip()
            link      = oferta.get('link', '')

            if not titulo or not link:
                continue

            #print(f"📌 {titulo} | 🏢 {empresa} | 📍 {ubicacion} | ⏱ {tiempo}")

            if not pasa_filtro(titulo):
                continue

            score = calcular_score(titulo)
            if score < 5:
                continue

            clave = f"lilog-{titulo.lower().strip()}-{empresa.lower().strip()}-{mes_actual}"

            mensaje = (
                f"💼 LinkedIn LOGIN\n"
                f"⭐ Score: {score}/15\n"
                f"{titulo}\n"
                f"🏢 {empresa}\n"
                f"📍 {ubicacion}\n"
                f"⏱ {tiempo}\n"
                f"🔗 {link}"
            )

            enviar_telegram(mensaje, clave)

        except Exception as e:
            print("❌ ERROR:", e)
            continue
            
            
            
# ===========================
# ELEMPEO
# ===========================

def buscar_elempleo():
    print("🔎 Buscando en Elempleo...",datetime.now().strftime("%H:%M:%S"))

    driver.get(URL_ELEMPEO)
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    ofertas = soup.find_all("div", class_="result-item")
    #print(f"Ofertas encontradas: {len(ofertas)}")

    for oferta in ofertas[:20]:
        try:
            # Fuente primaria: data-ga4-offerdata
            data_attr = oferta.find("div", class_="js-area-bind")
            if not data_attr:
                continue

            raw = data_attr.get("data-ga4-offerdata", "").strip()

            if raw:
                # Oferta con JSON completo
                data_json = json.loads(raw)
                titulo  = data_json.get("title", "").strip()
                empresa = data_json.get("company", "").strip()
                link    = "https://www.elempleo.com" + data_attr.get("data-url", "")
            else:
                # Fallback: leer atributos del botón compartir
                share_btn = oferta.find(attrs={"data-offer-title": True})
                if not share_btn:
                    continue
                titulo  = share_btn.get("data-offer-title", "").strip()
                link    = share_btn.get("data-offer-url", "").strip()

                # Empresa desde el span visible
                empresa_tag = oferta.find("span", class_="info-company-name")
                empresa = empresa_tag.get_text(strip=True) if empresa_tag else "Confidencial"

            if not titulo:
                continue
            if not pasa_filtro(titulo):
                continue
            score = calcular_score(titulo)
            if score < 5:
                continue

            clave = f"El-{titulo.lower()}-{empresa.lower()}-{mes_actual}"
            mensaje = (
                f"💼 Elempleo\n"
                f"⭐ Score: {score}/15\n"
                f"{titulo}\n"
                f"🏢 {empresa}\n"
                f"🔗 {link}"
            )
            enviar_telegram(mensaje, clave)

        except Exception as e:
            print(f"Error procesando oferta: {e}")
            continue

# ===========================
# MAGNETO
# ===========================

def buscar_magneto():
    print("🔎 Buscando en Magneto...",datetime.now().strftime("%H:%M:%S"))

    driver.get(URL_MAGNETO)

    wait = WebDriverWait(driver, 10)

    # Esperar a que carguen las tarjetas de empleo
    ofertas = wait.until(EC.presence_of_all_elements_located(
        (By.TAG_NAME, "a")
    ))

    for oferta in ofertas:
        try:
            titulo = oferta.text.strip()
            link = oferta.get_attribute("href")
            #print("DEBUG:", titulo, link)
            if len(titulo) < 15:
                continue

            if not pasa_filtro(titulo):
                continue

            score = calcular_score(titulo)

            if score < 5:
                continue

            clave = f"mg-{titulo.lower().strip()}-{mes_actual}"

            mensaje = (
                f"💼 Magneto\n"
                f"⭐ Score: {score}/15\n"
                f"{titulo}\n"
                f"🔗 {link}"
            )

            enviar_telegram(mensaje, clave)

        except:
            continue
            
# ===========================
# Computrabajo
# ===========================          
def buscar_computrabajo():
    print("🔎 Buscando en Computrabajo...",datetime.now().strftime("%H:%M:%S"))

    try:
        driver.get(URL_COMPUTRABAJO)
        time.sleep(10)

        # Esperar a que carguen las ofertas
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        ofertas = soup.find_all("article")

        for oferta in ofertas[:30]:
            try:
                # 🔹 Título y link
                a_tag = oferta.find("a", href=True)
                if not a_tag:
                    continue

                titulo = a_tag.text.strip()
                link = a_tag["href"]

                if not link.startswith("http"):
                    link = "https://co.computrabajo.com" + link

                # 🔹 Empresa (correcto desde el DOM real)
                empresa = "Empresa no visible"

                contenedor_empresa = oferta.find("p", class_="dFlex vm_fx fs16 fc_base mt5")

                if contenedor_empresa:
                    # Caso 1: viene con <a> (empresa real)
                    a_tag = contenedor_empresa.find("a")
                    if a_tag:
                        empresa = a_tag.text.strip()
                    else:
                        # Caso 2: texto plano tipo "Empresa del sector"
                        empresa = contenedor_empresa.get_text(strip=True)

                # 🔹 Validación por keywords
                if not pasa_filtro(titulo):
                    continue

                score = calcular_score(titulo)

                if score < 5:
                    continue

                clave = f"ct-{titulo.lower().strip()}-{empresa.lower().strip()}-{mes_actual}"

                mensaje = (
                    f"💼 Computrabajo\n"
                    f"⭐ Score: {score}/15\n"
                    f"{titulo}\n"
                    f"🏢 {empresa}\n"
                    f"🔗 {link}"
                )

                enviar_telegram(mensaje, clave)

            except Exception as e:
                #print("Error en oferta Computrabajo:", e)
                continue

    except Exception as e:
        print("❌ Error general Computrabajo:", e)

# ===========================
# SCHEDULER
# ===========================
print("🚀 JOB HUNTER Agent Orchestator BOT  v4 iniciado...")

# ===========================
# LINKEDIN RANDOM CONTROLADO
# ===========================

def linkedin_job():
    buscar_linkedin()

    # 🎲 nuevo intervalo aleatorio
    nuevo_intervalo = random.randint(61, 91)
    print(f"⏳ Próximo LinkedIn en {nuevo_intervalo} segundos")

    # 🔄 modificar el MISMO job (sin crear otro)
    job.interval = nuevo_intervalo


# crear el job UNA sola vez
#job = schedule.every(65).seconds.do(linkedin_job) # ~61~91 min

schedule.every(61).seconds.do(buscar_linkedin)
time.sleep(2) # Pausa pequeña entre registros
schedule.every(13).minutes.do(buscar_linkedin_Login)
time.sleep(29) # Pausa pequeña entre registros
schedule.every(11).minutes.do(buscar_computrabajo) # ~13 min
time.sleep(157) # Pausa pequeña entre registros
schedule.every(8).minutes.do(buscar_elempleo)      # ~9 min
time.sleep(37) # Pausa pequeña entre registros
schedule.every(19).minutes.do(buscar_magneto)       # ~19 min
time.sleep(199) # Pausa pequeña entre registros





print(schedule.jobs)
while True:
    schedule.run_pending()
    time.sleep(1)