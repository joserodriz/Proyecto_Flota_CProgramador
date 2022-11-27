import io
import base64

import matplotlib
matplotlib.use('Agg')   # Para multi-thread, non-interactive backend (avoid run in main loop)
import matplotlib.pyplot as plt
# Para convertir matplotlib a imagen y luego a datos binarios
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.image as mpimg


def graficar(x, y, ex, ey, tit):
    ''' 
        Crear el grafico que se desea mostrar en HTML
    '''
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.bar(x, y)
    plt.xlabel(ex)
    plt.ylabel(ey)
    plt.title(tit)

    # Convertir ese grafico en una imagen para enviar por HTTP
    # y mostrar en el HTML
    image_html = io.BytesIO()
    FigureCanvas(fig).print_png(image_html)
    plt.close(fig)  # Cerramos la imagen para que no consuma memoria del sistema
    return image_html