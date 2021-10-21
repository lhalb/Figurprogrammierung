from PIL import Image
from numpy import asarray, cumsum

def show_tonal_values(file):
    try:
        # Bild oeffnen und in Helligkeitswerte konvertieren
        im = Image.open(file).convert('L')
        # Numpy array aufspannen
        data = asarray(im)

        erg = cumsum(data)[-1]

        # den letzten Wert der aufsummierten Helligkeiten zurückgeben
        print(f'Das Bild enthält {erg} Tonwerte.')
        return erg

    except FileNotFoundError:
        print('Bild wurde nicht gefunden')
        return None


if __name__ == '__main__':
    from sys import argv
    show_tonal_values(argv[1])