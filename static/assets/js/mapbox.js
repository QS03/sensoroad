mapboxgl.accessToken = 'pk.eyJ1Ijoid2ViZGV2MTAyOCIsImEiOiJjazJ5aHdrYWswODhrM2x0NDY5NmgyNmJhIn0.esJEdNvrfUWs1o8wcFiWvg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [-122.48383155304096, 37.82882682974591],
    zoom: 16
});

var pointsData = [
    {coordinate: [-122.4833858013153, 37.829607404976734], rate: 1, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.4830961227417, 37.82932776098012], rate: 3, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48339653015138, 37.83270036637107], rate: 2, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48356819152832, 37.832056363179625], rate: 5, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48404026031496, 37.83114119107971], rate: 6, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48404026031496, 37.83049717427869], rate: 7, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48348236083984, 37.829920943955045], rate: 10, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48356819152832, 37.82954808664175], rate: 4, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48507022857666, 37.82944639795659], rate: 7, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48610019683838, 37.82880236636284], rate: 9, image_url: "static/assets/img/test.jpg"},
    {coordinate: [-122.48695850372314, 37.82931081282506], rate: 9, image_url: "static/assets/img/test.jpg"}
];

var linesData = [
    {coordinates: [[-122.4833858013153, 37.829607404976734], [-122.4830961227417, 37.82932776098012]], rate: 2},
    {coordinates: [[-122.4830961227417, 37.82932776098012], [-122.48339653015138, 37.83270036637107]], rate: 3},
    {coordinates: [[-122.48339653015138, 37.83270036637107], [-122.48356819152832, 37.832056363179625]], rate: 5},
    {coordinates: [[-122.48356819152832, 37.832056363179625], [-122.48404026031496, 37.83114119107971]], rate: 1},
    {coordinates: [[-122.48404026031496, 37.83114119107971], [-122.48404026031496, 37.83049717427869]], rate: 8},
    {coordinates: [[-122.48404026031496, 37.83049717427869], [-122.48348236083984, 37.829920943955045]], rate: 9},
    {coordinates: [[-122.48348236083984, 37.829920943955045], [-122.48356819152832, 37.82954808664175]], rate: 4},
    {coordinates: [[-122.48356819152832, 37.82954808664175], [-122.48507022857666, 37.82944639795659]], rate: 10},
    {coordinates: [[-122.48507022857666, 37.82944639795659], [-122.48610019683838, 37.82880236636284]], rate: 7},
    {coordinates: [[-122.48610019683838, 37.82880236636284], [-122.48695850372314, 37.82931081282506]], rate: 6},
];

var colorRate = {
  1: '#880015', 2: '#ed1c24', 3: '#ffaec9', 4: '#ffc90e', 5: '#fff200', 
  6: '#efe4b0', 7: '#d7f187', 8: '#b4e61e', 9: '#22b14c', 10: '#0e471f'
};

map.on('load', function() {
    var mapPointsData = [];
    for(var i = 0; i < pointsData.length; i++)
    {
        var item = {type: "Feature", geometry: { coordinates: pointsData[i].coordinate, type: "Point"},
            properties: {RATE: pointsData[i].rate, LON: pointsData[i].coordinate[0], LAT: pointsData[i].coordinate[1],
            IMAGE_URL: pointsData[i].image_url}};
        mapPointsData.push(item);
    }

    console.log(mapPointsData);
    var mapLinesData = [];
    for(var i = 0; i < linesData.length; i++)
    {
        var item = {'type': 'Feature', 'properties': {RATE: linesData[i].rate},'geometry': {'type': 'LineString', 'coordinates':
            linesData[i].coordinates}};
        mapLinesData.push(item);
    }

  map.addSource('points', {
    type: "geojson",
    data: {
      "type": "FeatureCollection",
      "features": mapPointsData
    }
  });

  map.addSource('lines', {
      'type': 'geojson',
      'data': {
          'type': 'FeatureCollection',
          'features': mapLinesData
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

    var image = "<a href='" + e.features[0].properties.IMAGE_URL + "' data-lightbox='image'>"+
        "<img src='" + e.features[0].properties.IMAGE_URL + "' style='width:100%'/></a>";

    var rating = '<h3> Rating:' + rate + '</h3>';
    var position = "<table style='border: solid 1px gray'><tr><th>Langitude</th><td>" + lon + "</td></tr><tr><th>Longitude</th><td>" + lat + "</td></tr></table>";
            
    content = image + '<hr>' + rating + position;

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




