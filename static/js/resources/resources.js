$(document).ready(function(){
	
	// lead form controls
	$("#appointmentCheck1" ).click(function() {
	  $( "#appointment1" ).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	});
	$("#appointmentCheck2" ).click(function() {
	  $( "#appointment2" ).animate({
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
	
	//shopping check 
	$("#shoppingCheck" ).click(function() {
		  $( "#shoppingTerms" ).animate({
			height: "toggle"
		  }, 300, function() {
		  });
	});	
	
	$("#addTask1" ).click(function() {		
	  //$( "#task2" ).fadeIn();
	  $( "#task2" ).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	  setTimeout(function() {
		  $( "#removeTask1" ).fadeIn();
		  }, 300); 
	});
	
	$("#removeTask1" ).click(function() {		
	  //$( "#task2" ).fadeOut();
	  $( "#task2" ).animate({
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
	
	// date picker
	$(function() {
		$( "#datepickerFrom, #datepickerTo" ).datepicker();
	});
  
  	// profile field disabled
	  $("#profileEdit").click(function(event){
	   event.preventDefault();
	   $('.profile-section.editable .non-edit').prop("disabled", false); // Element(s) are now enabled.
	   $('.profile-section.editable .form-control').removeClass("non-edit");
	   $('#profileEdit').hide();
	   $('#profileUpdate, #profileCancel').show();
	});
	$("#profileCancel").click(function(event){
	   $('.profile-section.editable .form-control').addClass("non-edit");
	   $('#profileEdit').show();
	   $('#profileUpdate, #profileCancel').hide();
	});
	
	// media query for profile
	$("#profileEdit").click(function(event){
	if ($(window).width() <= 767){	
		$(".profile-page .editable label").css('padding-left','0');
	}
	});
	$("#profileCancel").click(function(event){
		$(".profile-page .editable label").css('padding-left','15px');
	});
	
});



