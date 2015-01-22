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
	
	
	
	$(".live-transfer-location").click(function(){
        phone_no = $(this).attr('data-phone');
        $(".location_number").text(phone_no);
    });
});



