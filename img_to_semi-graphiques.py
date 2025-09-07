#images maximum 80*69 en 8 niveaux de gris sur un écran monochrome
import greatfet

from PIL import Image, ImageFilter

pixel_block = {
    0: 0x20,

    2: 0x30,
    1: 0x60,
    3: 0x70,

    32: 0x21,
    34: 0x31,
    33: 0x61,
    35: 0x71,

    16: 0x22,
    18: 0x32,
    17: 0x62,
    19: 0x72,

    48: 0x23,
    50: 0x33,
    49: 0x63,
    51: 0x73,

    8: 0x24,
    10: 0x34,
    9: 0x64,
    11: 0x74,

    40: 0x25,
    42: 0x35,
    41: 0x65,
    43: 0x75,

    24: 0x26,
    26: 0x36,
    25: 0x66,
    27: 0x76,

    56: 0x27,
    58: 0x37,
    57: 0x67,
    59: 0x77,

    4: 0x28,
    6: 0x38,
    5: 0x68,
    7: 0x78,

    36: 0x29,
    38: 0x39,
    37: 0x69,
    39: 0x79,

    20: 0x2A,
    22: 0x3A,
    21: 0x6A,
    23: 0x7A,

    52: 0x2B,
    54: 0x3B,
    53: 0x6B,
    55: 0x7B,

    12: 0x2C,
    14: 0x3C,
    13: 0x6C,
    15: 0x7C,

    44: 0x2D,
    46: 0x3D,
    45: 0x6D,
    47: 0x7D,

    28: 0x2E,
    30: 0x3E,
    29: 0x6E,
    31: 0x7E,

    60: 0x2F,
    62: 0x3F,
    63: 0x5F,
    61: 0x6F

}

def even_byte(byte) :
    res = (byte.bit_count() % 2 != 0)
    return byte | (res << 7)



def convertir_image(image_path, output_path):
    # Ouvrir l'image
    image = Image.open(image_path)
    
    # Convertir l'image en niveaux de gris
    image = image.convert("L")

    
    # Redimensionner l'image en gardant les proportions
    image.thumbnail((80, 69))
    
    # Réduire l'image à 8 niveaux de gris
    #niveaux_de_gris = 2
    # Diviser chaque pixel par (256 / niveaux_de_gris) et le ramener entre 0 et 255
    #image = image.point(lambda x: int(x / (256 / niveaux_de_gris)) * (255 // (niveaux_de_gris - 1)))

        # Appliquer un seuil pour convertir en noir et blanc pur
    seuil = 128  # Vous pouvez ajuster cette valeur selon vos besoins
    image = image.point(lambda p: 255 if p > seuil else 0)
    image = image.convert("1")

    # Convertir l'image en couleur pour avoir #000000 et #FFFFFF
    image = image.convert("RGB")

    # Maintenant l'image a des pixels #000000 (noir) et #FFFFFF (blanc)
    # Vous pouvez enregistrer cette image binaire pur
    image.save("image_noir_et_blanc.bmp")

    # Afficher l'image pour vérifier
    #image.show()

    # Réduire le bruit avec un filtre de lissage
    #image = image.filter(ImageFilter.MedianFilter(size=3))  # Le filtre médian aide à réduire le bruit

    # Améliorer la netteté
    #image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # Sauvegarder l'image
    #image.save(output_path)
   # print(f"L'image a été convertie et enregistrée sous {output_path}")

    # Définir les dimensions de la découpe
    largeur_coupe, hauteur_coupe = 2, 3

    # Obtenir la largeur et la hauteur de l'image d'origine
    largeur_image, hauteur_image = image.size

    # Tableau pour stocker les images découpées avec leurs coordonnées
    images_decoupees = []

    # Parcourir l'image pour effectuer les découpes
    pos_y = -1
    for y in range(0, hauteur_image, hauteur_coupe):
        pos_y = pos_y + 1
        pos_x = -1
        for x in range(0, largeur_image, largeur_coupe):
            pos_x = pos_x + 1
            # Définir la zone de découpe (gauche, haut, droite, bas)
            zone = (x, y, x + largeur_coupe, y + hauteur_coupe)
            # Découper l'image
            decoupe = image.crop(zone)
            # Ajouter l'image découpée et ses coordonnées au tableau
            images_decoupees.append((decoupe, (pos_x, pos_y)))

    # Enregistrer les petites images ou les traiter
    octets_modifiables = bytearray([])
    octets_modifiables.append(even_byte(0x0C))
    octets_modifiables.append(even_byte(0xE))
    for i, (img, (x, y)) in enumerate(images_decoupees):
        #img.save(f"tmp_img/petite_image_{i}_x{x}_y{y}.bmp")
        #print(f"Image {i}: x={x}, y={y}")
        # Afficher les valeurs des pixels (en RGB)
        pixel_id : int = 0
        largeur, hauteur = img.size
        for yb in range(hauteur):
            for xb in range(largeur):
                pixel = img.getpixel((xb, yb))
                pixel_id = pixel_id << 1
                if(pixel[0] > 0) :
                    pixel_id = pixel_id | 1
                
                #print(f"Pixel ({yb},{xb}): {pixel}")
                #print(f"pixel_id: {pixel_id} - i : {i}")
                #i = i + 1 
        octets_modifiables.append(even_byte(pixel_block[pixel_id]))
        print(f"pixel_id: {pixel_id}")
        #octets_modifiables.append(pixel_block[pixel_id])
    return bytes(octets_modifiables)


# Créer une instance de GreatFET
device = greatfet.GreatFET()

# Initialiser l'UART
uart = device.uart


# Mettre à jour les paramètres si nécessaire (facultatif si déjà défini dans l'initialisation)
uart.update_parameters(baud=1200, data_bits=8, parity=uart.PARITY_NONE)


#uart.write(convertir_image("./shl2.jpg", "image_convertie.jpg"))
uart.write(convertir_image("./shl2.jpg", "image_convertie.jpg"))