mapboxgl.accessToken = mapboxToken;//'pk.eyJ1Ijoid2ViZGV2MTAyOCIsImEiOiJjazJ5aHdrYWswODhrM2x0NDY5NmgyNmJhIn0.esJEdNvrfUWs1o8wcFiWvg';


// var pointsData = [
//   {coordinate: [-122.4833858013153, 37.829607404976734], rate: 1, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.4830961227417, 37.82932776098012], rate: 3, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48339653015138, 37.83270036637107], rate: 2, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48356819152832, 37.832056363179625], rate: 5, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48404026031496, 37.83114119107971], rate: 6, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48404026031496, 37.83049717427869], rate: 7, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48348236083984, 37.829920943955045], rate: 10, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48356819152832, 37.82954808664175], rate: 4, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48507022857666, 37.82944639795659], rate: 7, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48610019683838, 37.82880236636284], rate: 9, image_url: "static/assets/img/test.jpg"},
//   {coordinate: [-122.48695850372314, 37.82931081282506], rate: 9, image_url: "static/assets/img/test.jpg"}
// ];
//
// var linesData = [
//   {coordinates: [[-122.4833858013153, 37.829607404976734], [-122.4830961227417, 37.82932776098012]], rate: 2},
//   {coordinates: [[-122.4830961227417, 37.82932776098012], [-122.48339653015138, 37.83270036637107]], rate: 3},
//   {coordinates: [[-122.48339653015138, 37.83270036637107], [-122.48356819152832, 37.832056363179625]], rate: 5},
//   {coordinates: [[-122.48356819152832, 37.832056363179625], [-122.48404026031496, 37.83114119107971]], rate: 1},
//   {coordinates: [[-122.48404026031496, 37.83114119107971], [-122.48404026031496, 37.83049717427869]], rate: 8},
//   {coordinates: [[-122.48404026031496, 37.83049717427869], [-122.48348236083984, 37.829920943955045]], rate: 9},
//   {coordinates: [[-122.48348236083984, 37.829920943955045], [-122.48356819152832, 37.82954808664175]], rate: 4},
//   {coordinates: [[-122.48356819152832, 37.82954808664175], [-122.48507022857666, 37.82944639795659]], rate: 10},
//   {coordinates: [[-122.48507022857666, 37.82944639795659], [-122.48610019683838, 37.82880236636284]], rate: 7},
//   {coordinates: [[-122.48610019683838, 37.82880236636284], [-122.48695850372314, 37.82931081282506]], rate: 6}
// ];

var pointsData = pointsData;
var linesData = linesData;

// console.log(pointsData);
// console.log(linesData);

var colorRate = {
  1: '#880015', 2: '#ed1c24', 3: '#ffaec9', 4: '#ffc90e', 5: '#fff200',
  6: '#efe4b0', 7: '#d7f187', 8: '#b4e61e', 9: '#22b14c', 10: '#0e471f'
};

var city = selectedCityState.split(',')[0];
var state = selectedCityState.split(',')[1];

// console.log(city, state);

var query = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + city + ".json?access_token=" + mapboxgl.accessToken;

$.ajax({
  method: 'GET',
  url: query
}).done(function(data) {

  mapCenter = data.features[0].center;

  // console.log(mapCenter);

  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [-122.4833858013153, 37.829607404976734], //mapCenter,
    zoom: 16,
    minZoom: 16,
  });

  map.on('load', function() {
    var mapPointsData = [];
    for(var i = 0; i < pointsData.length; i++)
    {
      var item = {type: "Feature", geometry: { coordinates: pointsData[i].coordinate, type: "Point"},
        properties: {RATE: pointsData[i].rate, LON: pointsData[i].coordinate[0], LAT: pointsData[i].coordinate[1],
          IMAGE_URL: pointsData[i].image_url}};
      mapPointsData.push(item);
    }

    map.addSource('points', {
      type: "geojson",
      data: {
        "type": "FeatureCollection",
        "features": mapPointsData
      }
    });

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

    var mapLinesData = {};
    for(i = 0; i < linesData.length; i++)
      mapLinesData[linesData[i].rate] = linesData[i].coordinates;

    for(i = 1; i <= 10; i++)
      updateRoute(mapLinesData[i], colorRate[i], 'line'+i.toString());
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

// Draw the Map Matching route as a new layer on the map
function addRoute(coords, lineColor, layerID) {
  map.addLayer({
    "id": layerID,
    "type": "line",
    "source": {
      "type": "geojson",
      "data": {
        "type": "Feature",
        "properties": {},
        "geometry": coords
      }
    },
    "layout": {
      "line-join": "round",
      "line-cap": "round",
      "visibility": "none"
    },
    "paint": {
      "line-color": lineColor,
      "line-width": 8,
      "line-opacity": 0.8
    }
  });
}

function updateRoute(coords, lineColor, layerID) {
  // Set the profile
  var profile = "driving";
  // Format the coordinates
  var newCoords = coords.join(';');
  // Set the radius for each coordinate pair to 25 meters
  var radius = [];
  coords.forEach(element => {
    radius.push(25);
  });
  getMatch(newCoords, radius, profile, lineColor, layerID);
}

// Make a Map Matching request
function getMatch(coordinates, radius, profile, lineColor, layerID) {
  // Separate the radiuses with semicolons
  var radiuses = radius.join(';')
  // Create the query
  var query = 'https://api.mapbox.com/matching/v5/mapbox/' + profile + '/' + coordinates + '?geometries=geojson&radiuses=' + radiuses + '&steps=true&access_token=' + mapboxgl.accessToken;

  $.ajax({
    method: 'GET',
    url: query
  }).done(function(data) {
    // Get the coordinates from the response
    var coords = data.matchings[0].geometry;
    // Draw the route on the map
    addRoute(coords, lineColor, layerID);
    // getInstructions(data.matchings[0]);
  });
}

var viewMode = 'point'

$('#layer1').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[1], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line1', 'visibility', 'visible');
  }
});

$('#layer2').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[2], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line2', 'visibility', 'visible');
  }
});

$('#layer3').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[3], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line3', 'visibility', 'visible');
  }
});


$('#layer4').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[4], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line4', 'visibility', 'visible');
  }
});


$('#layer5').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[5], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line5', 'visibility', 'visible');
  }
});


$('#layer6').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[6], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line6', 'visibility', 'visible');
  }
});


$('#layer7').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[7], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line7', 'visibility', 'visible');
  }
});


$('#layer8').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[8], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line8', 'visibility', 'visible');
  }
});


$('#layer9').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[9], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line9', 'visibility', 'visible');
  }
});

$('#layer10').click(function (data) {
  for(var i = 1; i <= 10; i++)
    $('#layer'+i.toString()).css({"border": "none"});
  $(this).css({"border": "1px solid "+colorRate[10], "border-radius": "20px"});
  if (viewMode === 'line') {
    for (var j = 1; j <= 10; j++)
      map.setLayoutProperty('line' + j.toString(), 'visibility', 'none');
    map.setLayoutProperty('points', 'visibility', 'none');
    map.setLayoutProperty('line10', 'visibility', 'visible');
  }
});

$('#toggleMode').click(function (data) {
  for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});

  var atLeastOneIsChecked = $('input[id="toggleMode"]:checked').length > 0;
  if (atLeastOneIsChecked) {
    viewMode = 'line';
    map.setLayoutProperty('points', 'visibility', 'none');
    for (var i = 1; i <= 10; i++)
      map.setLayoutProperty('line' + i.toString(), 'visibility', 'visible');
  }
  else {
    viewMode = 'point';
    map.setLayoutProperty('points', 'visibility', 'visible');
    for (var i = 1; i <= 10; i++)
      map.setLayoutProperty('line' + i.toString(), 'visibility', 'none');
  }
});






