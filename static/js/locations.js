var placeSearch, autocomplete;
var componentForm = {
  street_number: 'short_name',
  route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  country: 'long_name',
  postal_code: 'short_name'
};

function initialize() {
  // Create the autocomplete object, restricting the search
  // to geographical location types.
  autocomplete = new google.maps.places.Autocomplete(
      /** @type {HTMLInputElement} */(document.getElementById('advertiser_location')),
      { types: ['geocode'] });
  // When the user selects an address from the dropdown,
  // populate the address fields in the form.
  google.maps.event.addListener(autocomplete, 'place_changed', function() {
    // fillInAddress();
  });
}

// [START region_geolocation]
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.

    var geocoder =  new google.maps.Geocoder();
    window.selected_location = 'India';
    geocoder.geocode( { 'address': window.selected_location}, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
            console.log("location : " + results[0].geometry.location.lat() + " " +results[0].geometry.location.lng());
            window.latitude = results[0].geometry.location.lat();
            window.longtitude = results[0].geometry.location.lng();
          } else {
            alert("Something got wrong " + status);
          }
        });

function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      if (window.latitude && window.longtitude){
          var geolocation = new google.maps.LatLng(window.latitude, window.longtitude);  
      }else{
          var geolocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);  
      }
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}