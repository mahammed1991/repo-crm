function getLocation(rep_location) {
  window.rep_location = rep_location
    if (Modernizr.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    getResult(position.coords.latitude, position.coords.longitude);
}

function getResult(latitude, longitude){
   $.ajax({
        url: "http://maps.googleapis.com/maps/api/geocode/json?latlng="+latitude+","+longitude+"&sensor=false",
        type: 'GET',
        dataType: "json",
        success: function(data) {
          console.log(data);
          var start = data['results'].length - 3
          var end = data['results'].length - 2
          var repLocObject = data['results'].slice(start, end);
          var repLoc = repLocObject[0];
          document.getElementById(window.rep_location).value = repLoc['formatted_address'];
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('failure');
        }

});
}