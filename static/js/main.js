$(document).ready(function(){

	// table accordian
    $(".clickable" ).click(function() {
      $(this).find( ".row-expand, .row-collapse" ).toggle();
    });
    

	$(document).on('click', '.live-transfer-location', function(e) { 
		phone_no = $(this).attr('data-phone');
		flag_url = $(this).attr('data-url');
		$("#loc_img").attr('src', flag_url);
        $(".location_number").text(phone_no);
	});

	// Get All Inbound Locations 
	$.ajax({
          url: "/main/get-inbound-locations",
          dataType: "json",
          type: 'GET',
          data: {},
          success: function(data) {
              console.log(data);
              displayLocations(data['location']);
              showUserLoc(data['user_loc']);
          },
          error: function(errorThrown) {
              console.log('failure');
          }
        }); 


	function displayLocations(locations){
		elem = "";
		for(i=0; i<locations.length; i++){
			elem = '<li><a href="#" data-phone="'+ locations[i]['phone'] +'" id="loc_'+ locations[i]['id'] +'" class="live-transfer-location" data-url="'+ locations[i]['url'] +'">'+
					'<img src="'+ locations[i]['url'] +'"/>'+ locations[i]['name'] +'</a>'+
					'</li>'
			$("#loc_list").append(elem);
		}
		
	}

	function showUserLoc(user_loc){
		if(user_loc['loc_phone']){
			$("#loc_img").attr("src", user_loc['loc_flag'])
			$(".location_number").text(user_loc['loc_phone'])	
		}
	}

	// Get Notifications
	$.ajax({
          url: "/main/get-notifications",
          dataType: "json",
          type: 'GET',
          data: {},
          success: function(notifications) {
              console.log(notifications);
              setNotifications(notifications);
          },
          error: function(errorThrown) {
              console.log('failure');
          }
        }); 


	function setNotifications(notifications){
		$("#notifications_count").text(notifications.length);
		elem = "";
		for(i=0; i<notifications.length; i++){
			elem = '<li><a href="#">'+ notifications[i]['text'] +'</a></li>'
			$("#notifications").append(elem);
		}
		
	}

});



