# processing.py
import cv2
import numpy as np
import math


#Encontrar plano mejorado por si tiene inclinacion
def homografia(img):
    # Paso 1: Puntos en la imagen original (elegidos manualmente o con detección)
    # Ejemplo: esquinas de un cuadrado inclinado
    src_points = np.float32([
        [40, 24],  # esquina sup izq
        [154, 10],  # esquina sup der
        [154, 168],
        [40, 176]   # esquina inf izq
    ])


    # Paso 2: Definir el rectángulo destino
    width, height = 200, 200
    dst_points = np.float32([
        [0, 0],
        [width-1, 0],
        [width-1, height-1],
        [0, height-1]
    ])

    # Paso 3: Calcular homografía
    H, _ = cv2.findHomography(src_points, dst_points)

    # Paso 4: Aplicar la transformación
    warped = cv2.warpPerspective(img, H, (width, height))
    return warped


def cut_circle(img):
    # Crear máscara completamente blanca
    mask = np.ones_like(img, dtype=np.uint8) * 0
    circle=cv2.circle(mask, (108, 110), 80, (255, 255, 255), -1)
    img = cv2.bitwise_and(img, circle)
    return img


ORIGIN_X = 108
ORIGIN_Y = 113

def angle_calculation(x, y, origin_x=ORIGIN_X, origin_y=ORIGIN_Y, invert_y_for_image_coords=True):
    """
    Devuelve el ángulo en grados en [0, 360) medido desde el eje +X (derecha),
    en sentido antihorario, tomando como origen (origin_x, origin_y).

    Si invert_y_for_image_coords=True, se asume sistema de coordenadas de imagen
    (y crece hacia abajo) y se invierte dy para que 90° = arriba.
    """
    dx = x - origin_x
    dy = y - origin_y

    if invert_y_for_image_coords:
        dy = -dy  # convierte coordenadas de imagen a coordenadas matemáticas

    ang = math.degrees(math.atan2(dy, dx))  # rango (-180, 180]
    ang = (ang + 360) % 360  # normalizar a [0, 360)
    return ang


def hugh_line_open(edges, img_gray):
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=40, maxLineGap=5)

    if lines is not None:
        line=lines[0]
        x1, y1, x2, y2 = line[0]
        #cv2.line(img_gray, (x1,y1), (x2,y2), (0,255,255), 2, cv2.LINE_AA)
        angulo=(angle_calculation(x1, y1, x2, y2))

        valor=-3.1939*angulo+758.06
        
        texto=str(round(valor, 1))+ "bar"
        posicion = (50, 20)  # Coordenadas (x, y)
        fuente = cv2.FONT_HERSHEY_SIMPLEX
        escala = 0.7
        color = (255, 255, 255)  # Blanco en BGR
        grosor = 1
        cv2.putText(img_gray, texto, posicion, fuente, escala, color, grosor, cv2.LINE_AA)

        return valor
 


def preprocesing(img):
    img = cv2.resize(img, (200,200), dst=None, fx=None, fy=None, interpolation=cv2.INTER_LINEAR)
    img =homografia(img)
    img=cut_circle(img)

    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(grayscale, 3)
    edges_2 = cv2.Canny(img_blur, 220, 255)

    return hugh_line_open(edges_2, img)


def process_image(img):

    valor=preprocesing(img)

    result = {
        "valor_calculado": valor
    }

    return result
