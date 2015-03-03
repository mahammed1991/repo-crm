if(google.loader.ClientLocation)
  {
      visitor_lat = google.loader.ClientLocation.latitude;
      visitor_lon = google.loader.ClientLocation.longitude;
      visitor_city = google.loader.ClientLocation.address.city;
      visitor_region = google.loader.ClientLocation.address.region;
      visitor_country = google.loader.ClientLocation.address.country;
      visitor_countrycode = google.loader.ClientLocation.address.country_code;
      var currentLoc = visitor_city + ', ' + visitor_region + ', ' + visitor_country;
      document.getElementById('rep_location').value = currentLoc;
  }
  else
  {
      document.getElementById('rep_location').value = '';
  }