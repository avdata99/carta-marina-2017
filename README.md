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
La Carta Marina no es muy precisa en el orden de las escuelas y es posible que requiera toques a mano.  
Muchas direcciones tienen formas complicadas por lo que el retoque final a mano puede ser necesario. La detección de barrios (muchas veces metido entre la calle y el numero (?)) podría hacerce con expresiones regulares y simplificar este proceso.  
  

Dentro de google sheets se geolocalizaron las escuelas con [este script](https://github.com/ModernizacionMuniCBA/muni-google-util-app-scripts/tree/master/geolocalizar%20desde%20direccion) liberado desde la Municipalidad de Córdoba.  

Con esta geolocalización quedo disponible [un CSV](escuelas-elecciones-2017-cordoba-Geolocalizada.csv).  

Con esos datos junto a los de 2015 se armó una lista de variaciones de electores por sección (departamento) y por circuito (generalmente ciudades).  

[CSV variación por departamentos](Electores-2017-vs-2015-por-departamentos.csv).  
[CSV variación por circuitos](Electores-2017-vs-2015-por-Circuitos.csv).  


