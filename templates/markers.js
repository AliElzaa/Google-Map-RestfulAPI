function initMap() {
        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer;
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 13,
          center: {lat: 51.5388666, lng: -0.1685793}
        });
        directionsDisplay.setMap(map);

        document.getElementById('submit').addEventListener('click', function() {
          calculateAndDisplayRoute(directionsService, directionsDisplay);
        });
      

      function calculateAndDisplayRoute(directionsService, directionsDisplay) {
        var waypts = [];
        var checkboxArray = document.getElementById('waypoints');
        for (var i = 0; i < checkboxArray.length; i++) {
          if (checkboxArray.options[i].selected) {
            waypts.push({
              location: checkboxArray[i].value,
              stopover: true
            });
          }
        }

	//var orderboxArray = document.getElementById('orderlocations');
	//for (var i = 0; i < orderboxArray.length; i++) {
          //if (orderboxArray.options[i].selected) {
            //waypts.push({
		//location: orderboxArray[i].value,
		//stopover: true
		//});
	//}
    //}
	

        directionsService.route({
          origin: document.getElementById('start').value,
          destination: document.getElementById('end').value,
          waypoints: waypts,
          optimizeWaypoints: true,
          travelMode: 'DRIVING'
        }, function(response, status) {
          if (status === 'OK') {
            directionsDisplay.setDirections(response);
            var route = response.routes[0];
            var summaryPanel = document.getElementById('directions-panel');
            summaryPanel.innerHTML = '';
            // For each route, display summary information.
            for (var i = 0; i < route.legs.length; i++) {
              var routeSegment = i + 1;
              summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +
                  '</b><br>';
              summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
	      summaryPanel.innerHTML += route.legs[i].duration.text + '<br><br>';
            }
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
      }


        var icons = {
          supermarket: {
            icon: 'https://img.icons8.com/ios/50/000000/shopping-cart-filled.png'
          },
           house: {
          icon:  'https://img.icons8.com/office/40/000000/bungalow.png'
          },
        
        };

var features = [
{% for orders in form %}

{ position: new google.maps.LatLng({{orders.lat}}, {{ orders.lng }}),
  type: 'house'
  
}, 

{% endfor %}
 
  { position: new google.maps.LatLng(51.5388666, -0.1685793),
  type: 'supermarket'
},

{ position: new google.maps.LatLng(51.568151, -0.218803),
  type: 'supermarket'
},
{ position: new google.maps.LatLng(51.591676, -0.226486),
  type: 'supermarket'
},

{ position: new google.maps.LatLng(51.584525, -0.235139),
  type: 'supermarket'
}



 ];      
for (var i = 0; i < features.length; i++) {
          var marker = new google.maps.Marker({
            position: features[i].position,
            icon: icons[features[i].type].icon,
           map: map
          });
        };


      }

