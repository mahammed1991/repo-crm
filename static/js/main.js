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
	
});

