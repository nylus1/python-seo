#---------------------------------------------------------------#
#  Script SEO                                                   #
#  Autor: Ignacio Sánchez Gómez                                 #
#  DPTO: BirdCom                                                #
#  Fecha Inicio: 31/05/2023                                     #
#  Versión 1.0                                                  #
#---------------------------------------------------------------#


import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def analyze_speed_load(url):
    # Iniciar el temporizador
    start_time = time.time()
    # Enviar la solicitud GET al URL
    response = requests.get(url)
    # Detener el temporizador
    end_time = time.time()
    # Calcular el tiempo de carga
    load_time = end_time - start_time
    # Devolver el tiempo de carga
    return load_time

def get_size(url):
    # Descargar el recurso y devolver su tamaño
    response = requests.get(url, stream=True)
    # Devolver tamaño en kilobytes
    return len(response.content) / 1024 

def analyze_heaviest_elements(url, top=10):
    print("Analizando url, por favor mantengase a la espera.")
    # Enviar la solicitud GET al URL
    response = requests.get(url)
    # Analiza el contenido HTML de la respuesta utilizando BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Encuentra el elemento 'body' en el contenido HTML
    body = soup.find('body')
    # Encuentra todos los elementos 'img' y 'video' dentro del cuerpo
    elements = body.find_all(['img', 'video'])
    # Lista para almacenar los tamaños de los elementos
    sizes = []
    # Itera sobre los elementos encontrados
    for element in elements:
        if 'src' in element.attrs:
            # Obtiene la URL completa de la imagen o el video
            src = urljoin(url, element['src'])
            # Verifica si la URL tiene el mismo dominio que la URL original
            if urlparse(url).netloc == urlparse(src).netloc:  
                try:
                    # Obtiene el tamaño del archivo utilizando la función 'get_size'
                    size = get_size(src)
                    # Agrega el nombre del elemento, el tamaño y el nombre de archivo a la lista
                    sizes.append((element.name, size, src.split('/')[-1]))
                except Exception as e:
                    print(f"Error al descargar {src}: {e}")

    # Ordena la lista de tamaños en orden descendente basado en el tamaño
    sizes.sort(key=lambda x: x[1], reverse=True)
    # Retorna los 'top' elementos más pesados
    return sizes[:top]

if __name__ == "__main__":
    url = input("Por favor, introduzca un URL de sitio web: ")
    print(f"Tiempo de carga de {url}: {analyze_speed_load(url)} segundos")
    heaviest_elements = analyze_heaviest_elements(url)
    if heaviest_elements:
        print("Los 10 elementos más pesados en " + url + " son:")
        for element, size, filename in heaviest_elements:
            print(f"{element} ({filename}): {size} KB")
    else:
        print("No se encontraron elementos de img o video en el cuerpo de la página.")