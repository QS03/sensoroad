mapboxgl.accessToken = mapboxToken;

//var pointsData = [
//  {"coordinate":[-94.521963,39.071519],"rate":4,"image_url":"assets/img/test.jpg"},
//  {"coordinate":[-94.574257,39.068776],"rate":5,"image_url":"assets/img/test.jpg"},
//  {"coordinate":[-94.566779,39.068563],"rate":4,"image_url":"assets/img/test.jpg"},
//  {"coordinate":[-94.559686,39.068402],"rate":10,"image_url":"assets/img/test.jpg"},
//  {"coordinate":[-94.560659,39.073765],"rate":4,"image_url":"assets/img/test.jpg"},
//  {"coordinate":[-94.563512,39.080578],"rate":4,"image_url":"assets/img/test.jpg"},
//  {"coordinate":[-94.569889,39.08537],"rate":5,"image_url":"assets/img/test.jpg"}
//];
//var linesData = [
//  {"coordinates":[[-94.521963,39.071519],[-94.53609,39.074396]],"rate":4, "matching": "{'type': 'Feature', 'geometry': {'coordinates': [[-122.483616, 37.832074], [-122.483576, 37.832141], [-122.483406, 37.83245], [-122.483357, 37.832631], [-122.483365, 37.832702]], 'type': 'LineString'}, 'properties': {'confidence': 0.9769701603591643, 'distance': 74.2, 'duration': 11.1, 'matchedPoints': [[-122.483616, 37.832074], [-122.483365, 37.832702]], 'indices': [0, 1]}}"},
//  // {"coordinates":[[-94.574257,39.068776],[-94.574257,39.068776]],"rate":5},
//  // {"coordinates":[[-94.566779,39.068563],[-94.574257,39.068776]],"rate":4},
//  // {"coordinates":[[-94.559686,39.068402],[-94.566779,39.068563]],"rate":7},
//  // {"coordinates":[[-94.560659,39.073765],[-94.559686,39.068402]],"rate":7},
//  // {"coordinates":[[-94.563512,39.080578],[-94.560659,39.073765]],"rate":4},
//  // {"coordinates":[[-94.569889,39.08537],[-94.563512,39.080578]],"rate":4},
//  // {"coordinates":[[-94.571882,39.093435],[-94.569889,39.08537]],"rate":4},
//  // {"coordinates":[[-94.572502,39.101514],[-94.571882,39.093435]],"rate":2}
//];

var colorRate = {
  1: '#880015', 2: '#ed1c24', 3: '#ffaec9', 4: '#ffc90e', 5: '#fff200',
  6: '#efe4b0', 7: '#d7f187', 8: '#b4e61e', 9: '#22b14c', 10: '#0e471f'
};

var city = selectedCityState.split(',')[0];
var state = selectedCityState.split(',')[1];

if(!city)
  city = 'Kansas City';

var query = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+city+".json?access_token="+mapboxgl.accessToken;

$.ajax({
  method: 'GET',
  url: query
}).done(function(data) {

  mapCenter = data.features[0].center;

  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: mapCenter, //[-122.4833858013153, 37.829607404976734]
    zoom: 12,
    minZoom: 12,
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

    var mapLinesData = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[]};
    for(i = 0; i < linesData.length; i++)
    {
      matching = JSON.parse(linesData[i].matching.replace(/'/g, '"'));
      console.log(matching);
      addRoute(matching, linesData[i].rate);
    }
  });

  var popup = new mapboxgl.Popup;

  map.on('click', 'points', function(e) {
    map.getCanvas().style.cursor = 'pointer';

    var lon = e.features[0].properties.LON;
    var lat = e.features[0].properties.LAT;
    var rate = e.features[0].properties.RATE;
    var coordinates = new mapboxgl.LngLat(lon, lat);

    var image = "<a href='"+e.features[0].properties.IMAGE_URL+"' data-lightbox='image'>"+
      "<img src='"+e.features[0].properties.IMAGE_URL+"' style='width:100%'/></a>";

    var rating = '<h3> Rating:'+rate+'</h3>';
    var position = "<table style='border: solid 1px gray'><tr><th>Langitude</th><td>"+lon+"</td></tr><tr><th>Longitude</th><td>"+lat+"</td></tr></table>";

    content = image+'<hr>'+rating+position;

    popup.setLngLat(coordinates)
     .setHTML(content)
     .addTo(map);
  })

  map.on('mouseenter', 'points', function(e) {
    map.getCanvas().style.cursor = 'pointer';
  })
  map.on('mouseleave', 'points', function() {
    map.getCanvas().style.cursor = '';
  });
});

var layerSegCnt = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0};

// Draw the Map Matching route as a new layer on the map
function addRoute(geometry, rate) {
  map.addLayer({
    "id": 'line' + rate.toString() + layerSegCnt[rate].toString(),
    "type": "line",
    "source": {
      "type": "geojson",
      "data": {
        "type": "Feature",
        "properties": {},
        "geometry": geometry
      }
    },
    "layout": {
      "line-join": "round",
      "line-cap": "round",
      "visibility": "none"
    },
    "paint": {
      "line-color": colorRate[rate],
      "line-width": 8,
      "line-opacity": 0.8
    }
  });
  layerSegCnt[rate] += 1;
}

// function updateRoute(coords, lineColor, layerID) {
//   // Set the profile
//   var profile = "driving";
//   // Format the coordinates
//   var newCoords = coords.join(';');
//   // Set the radius for each coordinate pair to 25 meters
//   var radius = [];
//   coords.forEach(element => {
//     radius.push(25);
//   });
//   getMatch(newCoords, radius, profile, lineColor, layerID);
// }

// Make a Map Matching request

// function getMatch(coordinates, radius, profile, lineColor, layerID) {
//   // Separate the radiuses with semicolons
//   var radiuses = radius.join(';');
//   // Create the query
//
//   var query = 'https://api.mapbox.com/matching/v5/mapbox/'+profile+'/'+coordinates+'?geometries=geojson&radiuses='+radiuses+'&steps=true&access_token='+mapboxgl.accessToken;
//
//   $.ajax({
//     method: 'GET',
//     url: query,
//     async: false
//   }).done(function(data) {
//     if(data.matchings.length > 0){
//       // Get the coordinates from the response
//       var coords = data.matchings[0].geometry;
//       addRoute(coords, lineColor, layerID.toString());
//     }
//   });
// }

var viewMode = 'point'

$('#layer1').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[1], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===1?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer2').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[2], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===2?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer3').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[3], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===3?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer4').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[4], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===4?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer5').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[5], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===5?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer6').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[6], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===6?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer7').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[7], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===7?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer8').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[8], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===8?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer9').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[9], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===9?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layer10').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[10], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', j===10?'visible':'none');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#layerAll').click(function (data) {
  if (viewMode === 'line') {
    for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
    $('#layerAll').css({"border": "none"});
    $(this).css({"border": "1px solid "+colorRate[1], "border-radius": "20px"});
    for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', 'visible');
      }
    }
    if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', 'none');
  }
});

$('#toggleMode').click(function (data) {
  for(var i = 1; i <= 10; i++)
      $('#layer'+i.toString()).css({"border": "none"});
  var atLeastOneIsChecked = $('input[id="toggleMode"]:checked').length > 0;
  viewMode = atLeastOneIsChecked ? 'line' : 'point';


  if(map.getLayer('points'))
      map.setLayoutProperty('points', 'visibility', atLeastOneIsChecked ? 'none' : 'visible');
   for (var j = 1; j <= 10; j++)
    {
      for(var k = 0; k <= layerSegCnt[j.toString()]; k++)
      {
        layerID = 'line'+j.toString()+k.toString();
        if(map.getLayer(layerID))
          map.setLayoutProperty(layerID, 'visibility', atLeastOneIsChecked ? 'visible' : 'none');
      }
    }
});





