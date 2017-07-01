# Carta Marina Córdoba 2017

Procesamiento de la Carta Marina Cordoba 2017

Se inicia el proceso con la [Carta Marina Cordoba 2017 publicada en PDF](LugaresDeVotacion-elecciones-2017.pdf).  

Como este PDF no permite una lectura correcta se usa el script _pdftotext_ que permite obtener el texto a secas del archivo PDF.  

```
pdftotext -layout LugaresDeVotacion-elecciones-2017.pdf carta-marina-cordoba-2017.txt
# notese el -layout, es clave
```
Luego este texto se convierte a CSV vía:  

```
python3 carta-marina-process.py
```
Este script esta adaptado de [uno similar hecho en 2015](https://github.com/OpenDataCordoba/elecciones2015/blob/master/resources/carta-marina/CartaMarinaProcess.py).  
La Carta Marina no es muy precisa en el orden de las escuelas y es posible.  
