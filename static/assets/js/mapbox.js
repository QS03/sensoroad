mapboxgl.accessToken = 'pk.eyJ1Ijoid2ViZGV2MTAyOCIsImEiOiJjazJ5aHdrYWswODhrM2x0NDY5NmgyNmJhIn0.esJEdNvrfUWs1o8wcFiWvg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [-122.48383155304096, 37.82882682974591],
    zoom: 16
});

// var source = [{
//   'point1': [-122.4833858013153, 37.829607404976734],
//   'point2': [-122.4830961227417, 37.82932776098012],
//   'point-rate': 1,
//   'line-rate': 2
// }];

var colorRate = {
  1: '#880015', 2: '#ed1c24', 3: '#ffaec9', 4: '#ffc90e', 5: '#fff200', 
  6: '#efe4b0', 7: '#d7f187', 8: '#b4e61e', 9: '#22b14c', 10: '#0e471f'
}

map.on('load', function() {
  pointArray = [
    {type: "Feature", geometry: { coordinates: [-122.4833858013153, 37.829607404976734], type: "Point"}, 
    properties: {RATE: 3, LON: -122.4833858013153, LAT: 37.829607404976734, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.4830961227417, 37.82932776098012], type: "Point"}, 
    properties: {RATE: 4, LON: -122.4830961227417, LAT: 37.82932776098012, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48339653015138, 37.83270036637107], type: "Point"}, 
    properties: {RATE: 1, LON: -122.48339653015138, LAT: 37.83270036637107, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48356819152832, 37.832056363179625], type: "Point"}, 
    properties: {RATE: 6, LON: -122.48356819152832, LAT: 37.832056363179625, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48404026031496, 37.83114119107971], type: "Point"}, 
    properties: {RATE: 7, LON: -122.48404026031496, LAT: 37.83114119107971, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48404026031496, 37.83049717427869], type: "Point"}, 
    properties: {RATE: 8, LON: -122.48404026031496, LAT: 37.83049717427869, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48348236083984, 37.829920943955045], type: "Point"}, 
    properties: {RATE: 9, LON: -122.48348236083984, LAT: 37.829920943955045, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48356819152832, 37.82954808664175], type: "Point"}, 
    properties: {RATE: 2, LON: -122.48356819152832, LAT: 37.82954808664175, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48507022857666, 37.82944639795659], type: "Point"}, 
    properties: {RATE: 10, LON: -122.48507022857666, LAT: 37.82944639795659, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48610019683838, 37.82880236636284], type: "Point"}, 
    properties: {RATE: 5, LON: -122.48610019683838, LAT: 37.82880236636284, IMAGE_URL: "static/assets/img/test.jpg"}},
    {type: "Feature", geometry: { coordinates: [-122.48695850372314, 37.82931081282506], type: "Point"}, 
    properties: {RATE: 5, LON: -122.48695850372314, LAT: 37.82931081282506, IMAGE_URL: "static/assets/img/test.jpg"}},

  ]

  lineArray = [
    {'type': 'Feature', 'properties': {RATE: 1},'geometry': {'type': 'LineString', 'coordinates': 
      [[-122.4833858013153, 37.829607404976734], [-122.4830961227417, 37.82932776098012]]}},
    // {'type': 'Feature', 'properties': {RATE: 2},'geometry': {'type': 'LineString', 'coordinates': 
    //   [[-122.4830961227417, 37.82932776098012], [-122.48339653015138, 37.83270036637107]]}},
    {'type': 'Feature', 'properties': {RATE: 5},'geometry': {'type': 'LineString', 'coordinates': 
    [[-122.48339653015138, 37.83270036637107], [-122.48356819152832, 37.832056363179625]]}},
    {'type': 'Feature', 'properties': {RATE: 7},'geometry': {'type': 'LineString', 'coordinates': 
    [[-122.48356819152832, 37.832056363179625], [-122.48404026031496, 37.83114119107971]]}},
    {'type': 'Feature', 'properties': {RATE: 8},'geometry': {'type': 'LineString', 'coordinates': 
    [[-122.48404026031496, 37.83114119107971], [-122.48404026031496, 37.83049717427869]]}},
    {'type': 'Feature', 'properties': {RATE: 10},'geometry': {'type': 'LineString', 'coordinates': 
    [[-122.48404026031496, 37.83049717427869], [-122.48348236083984, 37.829920943955045]]}},
    {'type': 'Feature', 'properties': {RATE: 5},'geometry': {'type': 'LineString', 'coordinates': 
    [[-122.48348236083984, 37.829920943955045], [-122.48356819152832, 37.82954808664175]]}},
    {'type': 'Feature', 'properties': {RATE: 6},'geometry': {'type': 'LineString', 'coordinates': 
    [[-122.48356819152832, 37.82954808664175], [-122.48507022857666, 37.82944639795659]]}},
    {'type': 'Feature', 'properties': {RATE: 4},'geometry': {'type': 'LineString', 'coordinates': 
    [[-122.48507022857666, 37.82944639795659], [-122.48610019683838, 37.82880236636284]]}},
    {'type': 'Feature', 'properties': {RATE: 3},'geometry': {'type': 'LineString', 'coordinates': 
    [[-122.48610019683838, 37.82880236636284], [-122.48695850372314, 37.82931081282506]]}},

  ]

  map.addSource('points', {
    type: "geojson",
    data: {
      "type": "FeatureCollection",
      "features": pointArray
    }
  });

  map.addSource('lines', {
      'type': 'geojson',
      'data': {
          'type': 'FeatureCollection',
          'features': lineArray
      }
  })

  map.addLayer({
    id: "points",
    type: "circle",
    source: "points",
    layout:{
      visibility: 'visible'
    },
    paint: {
      "circle-stroke-color": "white",
      "circle-stroke-width": {
        stops: [
          [0, 0.1],
          [18, 3]
        ],
        base: 5
      },
      "circle-radius": {
        stops: [
          [12, 5],
          [22, 180]
        ],
        base: 5
      },
      "circle-color": [
        'match',
        ['get', 'RATE'],
        1, colorRate['1'],
        2, colorRate['2'],
        3, colorRate['3'],
        4, colorRate['4'],
        5, colorRate['5'],
        6, colorRate['6'],
        7, colorRate['7'],
        8, colorRate['8'],
        9, colorRate['9'],
        10, colorRate['10'],
        '#000000' // any other store type
      ]
    }
  });

  map.addLayer({
    id: 'lines',
    type: 'line',
    source: 'lines',
    layout:{
      visibility: 'none'
    },
    paint: {
      'line-width': 5,
      // Use a get expression (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-get)
      // to set the line-color to a feature property value.
      'line-color': ['match',
        ['get', 'RATE'],
        1, colorRate['1'],
        2, colorRate['2'],
        3, colorRate['3'],
        4, colorRate['4'],
        5, colorRate['5'],
        6, colorRate['6'],
        7, colorRate['7'],
        8, colorRate['8'],
        9, colorRate['9'],
        10, colorRate['10'],
        '#000000' // any other store type
      ]
    }
  });

  var popup = new mapboxgl.Popup;

  map.on('click', 'points', function(e) {
    map.getCanvas().style.cursor = 'pointer';
    var lon = e.features[0].properties.LON;
    var lat = e.features[0].properties.LAT;
    var rate = e.features[0].properties.RATE;
    var coordinates = new mapboxgl.LngLat(lon, lat);

    var image = "<img src='" + e.features[0].properties.IMAGE_URL + "' style='width:100%'/><hr>";
    var rating = '<h3> Rating:' + rate + '</h3>';
    var position = "<table style='border: solid 1px gray'><tr><th>Langitude</th><td>" + lon + "</td></tr><tr><th>Longitude</th><td>" + lat + "</td></tr></table>";
            
    content = image + rating + position;

    popup.setLngLat(coordinates)
       .setHTML(content)
       .addTo(map);
  })

  map.on('mouseenter', 'points', function(e) {
    map.getCanvas().style.cursor = 'pointer';
  })
  map.on('mouseleave', 'points', function() {
    map.getCanvas().style.cursor = '';
    // popup.remove();
  });
});

$('#toggleMode').click(function(data){
  var atLeastOneIsChecked = $('input[id="toggleMode"]:checked').length > 0;
  if(atLeastOneIsChecked)
  {
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('lines', 'visibility', 'visible');
  }
  else
  {
    map.setLayoutProperty('points', 'visibility', 'visible');
    map.setLayoutProperty('lines', 'visibility', 'none');
  }
});




