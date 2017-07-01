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
  

Dentro de google sheets se geolocalizaron las escuelas con este script (basado en otro de internet)

```
var ui = SpreadsheetApp.getUi();
var addressColumn = 1;
var latColumn = 2;
var lngColumn = 3;
var foundAddressColumn = 4;
var qualityColumn = 5;
var sourceColumn = 6;

googleGeocoder = Maps.newGeocoder().setRegion(
  PropertiesService.getDocumentProperties().getProperty('GEOCODING_REGION') || 'ar'
);

function geocode(source) {
  var sheet = SpreadsheetApp.getActiveSheet();
  var cells = sheet.getActiveRange();

  if (cells.getNumColumns() != 6) {
    ui.alert(
      'Error',
      'Tenes que pintar 6 columnas en total para los campos: Ubicación (uno tuyo con direccion, ciudad, estado, pais) y otros 5 que carga este script: Latitud, Longitud, Encontrado, Calidad, Origen',
      ui.ButtonSet.OK
    );
    return;
  }

  var nAll = 0;
  var nIgnores = 0;
  var nFailure = 0;
  var quality;
  var printComplete = true;

  for (addressRow = 1; addressRow <= cells.getNumRows(); addressRow++) {
    var address = cells.getCell(addressRow, addressColumn).getValue();

    if (!address)
        {continue}
    
    // ignorar los que ya están
    var lat = cells.getCell(addressRow, latColumn).getValue();
    if (lat !== '') {
          nIgnores++;
          continue;}
    
    nAll++;
    
    if (source == 'US Census') {
      nFailure += withUSCensus(cells, addressRow, address);
    } else {
      nFailure += withGoogle(cells, addressRow, address);
      Utilities.sleep(1100);
    }
  }

  if (printComplete) {
    ui.alert('Completado!', 'Geocodificados: ' + (nAll - nFailure)
    + '\nFallados: ' + nFailure + ' Ignorados: ' + nIgnores, ui.ButtonSet.OK);
  }

}

/**
 * Geocode address with Google Apps https://developers.google.com/apps-script/reference/maps/geocoder
 */
function withGoogle(cells, row, address) {
  Logger.log('Geolocalizando %s', address);
  try {
      location = googleGeocoder.geocode(address);
      } 
  catch (e) {
    msg = e.message;
    Logger.log('Error Google %s', msg);
    location = {'status': 'SCRIPT ERROR'};
  }
  
  if (location.status == 'SCRIPT ERROR') {
    insertDataIntoSheet(cells, row, [
      [foundAddressColumn, ''], [latColumn, ''], [lngColumn, ''], [qualityColumn, 'FAILED SCRIPT: ' + msg], [sourceColumn, 'Google']
    ]);

    return 1;
  }
  
  if (location.status !== 'OK') {
    insertDataIntoSheet(cells, row, [
      [foundAddressColumn, ''], [latColumn, ''], [lngColumn, ''], [qualityColumn, 'No Match'], [sourceColumn, 'Google']
    ]);

    return 1;
  }

  lat = location['results'][0]['geometry']['location']['lat'];
  lng = location['results'][0]['geometry']['location']['lng'];
  foundAddress = location['results'][0]['formatted_address'];

  var quality;
  if (location['results'][0]['partial_match']) {
    quality = 'Partial Match';
  } else {
    quality = 'Match';
  }

  insertDataIntoSheet(cells, row, [
    [foundAddressColumn, foundAddress],
    [latColumn, lat],
    [lngColumn, lng],
    [qualityColumn, quality],
    [sourceColumn, 'Google']
  ]);

  return 0;
}

/**
 * Geocoding with US Census Geocoder https://geocoding.geo.census.gov/geocoder/
 */
function withUSCensus(cells, row, address) {
  var url = 'https://geocoding.geo.census.gov/'
          + 'geocoder/locations/onelineaddress?address='
          + encodeURIComponent(address)
          + '&benchmark=Public_AR_Current&format=json';

  var response = JSON.parse(UrlFetchApp.fetch(url));
  var matches = (response.result.addressMatches.length > 0) ? 'Match' : 'No Match';

  if (matches !== 'Match') {
    insertDataIntoSheet(cells, row, [
      [foundAddressColumn, ''],
      [latColumn, ''],
      [lngColumn, ''],
      [qualityColumn, 'No Match'],
      [sourceColumn, 'US Census']
    ]);
    return 1;
  }

  var z = response.result.addressMatches[0];

  var quality;
  if (address.toLowerCase().replace(/[,\']/g, '') ==
      z.matchedAddress.toLowerCase().replace(/[,\']/g, '')) {
        quality = 'Exact';
  } else {
    quality = 'Match';
  }

  insertDataIntoSheet(cells, row, [
    [foundAddressColumn, z.matchedAddress],
    [latColumn, z.coordinates.y],
    [lngColumn, z.coordinates.x],
    [qualityColumn, quality],
    [sourceColumn, 'US Census']
  ]);

  return 0;
}


/**
 * Sets cells from a 'row' to values in data
 */
function insertDataIntoSheet(cells, row, data) {
  for (d in data) {
    cells.getCell(row, data[d][0]).setValue(data[d][1]);
  }
}

function censusAddressToPosition() {
  geocode('US Census');
}

function googleAddressToPosition() {
  geocode('Google');
}

function onOpen() {
  ui.createMenu('Geocoder')
   .addItem('with US Census', 'censusAddressToPosition')
   .addItem('with Google (limit 1000 per day)', 'googleAddressToPosition')
   .addToUi();
}

```

Con esta geolocalización quedo disponible [un CSV](escuelas-elecciones-2017-cordoba-Geolocalizada.csv).  

Con esos datos junto a los de 2015 se armó una lista de variaciones de electores por sección (departamento) y por circuito (generalmente ciudades).  

[CSV variación por departamentos](Electores-2017-vs-2015-por-departamentos.csv).  
[CSV variación por circuitos](Electores-2017-vs-2015-por-Circuitos.csv).  


