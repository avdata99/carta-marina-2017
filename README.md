# Carta Marina Córdoba 2017

Procesamiento de la Carta Marina Cordoba 2017

Se inicia el proceso con la [Carta Marina Cordoba 2017 publicada en PDF](LugaresDeVotacion-elecciones-2017.pdf).  

Como este PDF no permite una lectura correcta se usa el script _pdftotext_ que permite obtener el texto a secas del archivo PDF.  

```
pdftotext -layout LugaresDeVotacion-elecciones-2017.pdf carta-marina-cordoba-2017.txt
# notese el -layout, es clave
```

