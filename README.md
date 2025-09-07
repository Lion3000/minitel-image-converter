# Convertisseur d’images vers le format Minitel

Ce projet permet de convertir une image bitmap en caractères semi-graphiques exploitables sur un terminal **Minitel**.  
Il utilise **Python**, la bibliothèque **Pillow (PIL)** pour le traitement d’image, et **GreatFET** pour communiquer avec le périphérique via **UART**.

---

## 🎯 Fonctionnalités
- Conversion d’images en noir et blanc ou niveaux de gris adaptés au Minitel.
- Support de tous les formats pris en charge par **Pillow** : `.bmp`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.tif`, etc.
- Redimensionnement automatique aux dimensions maximales supportées par l’affichage (`80 x 69`).
- Découpage en blocs de `2x3 pixels` convertis en codes semi-graphiques Minitel.
- Transmission des données vers le Minitel via **GreatFET UART** (1200 bauds).

---

## 📦 Prérequis

- Python 3.9+
- [Pillow](https://pypi.org/project/pillow/)
- [GreatFET](https://github.com/greatscottgadgets/greatfet)

Installation des dépendances :

```bash
pip install pillow greatfet
