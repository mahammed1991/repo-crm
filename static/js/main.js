$(document).ready(function(){

	// lead form controls
	$("#appointmentCheck" ).click(function() {
	  $( "#appointment" ).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	});
	
	$("#webmasterCheck" ).click(function() {
	  $( "#webmaster" ).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	  $( "#web-dum1, #web-dum2" ).toggle(500);
	});
	
	$("#tagImplementation" ).click(function() {
	  $( "#tasks" ).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	  //$( "#tagImplementation .check-icon" ).toggle();
	  $( "#tagImplementation .check-icon" ).animate({
		opacity: "toggle"
	  }, 200, function() {
	  });
	});
	
	$("#shoppingSetup" ).click(function() {
	  $( "#shoppingInfo" ).animate({
		height: "toggle"
	  }, 300, function() { 
	  });
	  $( "#shoppingSetup .check-icon" ).animate({
		opacity: "toggle"
	  }, 200, function() {
	  });
	});
	
	$(".add" ).click(function() {	
	  $( ".add" ).fadeOut();
	  $( ".remove" ).fadeOut();
	  id = $(this).attr('id');
	  indx = id.split('_')[1];
	  next_id = parseInt(indx) + 1
	  $( "#task_" + indx ).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	  setTimeout(function() {
		  $( "#removeTask_" + indx).fadeIn();
	  }, 300); 
	  $("#addTask_" + next_id).fadeIn();

	});
	
	$(".remove" ).click(function() {		
	  $( ".add" ).fadeOut();
	  $( ".remove" ).fadeOut();
	  id = $(this).attr('id');
	  indx = id.split('_')[1];
	  next_id = parseInt(indx) + 1
	  prev_id = parseInt(indx) - 1
	  $( "#task_" + indx).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	  $( "#removeTask1" ).hide();  
	});
	
	// media query for team page
	if ($(window).width() <= 767){	
		$("div.team-slider").removeClass('slider1');
	}
	
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



