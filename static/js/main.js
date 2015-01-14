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
	
	// Add Multiple Code Type/ Tasks
	$(".add" ).click(function() {	
	  $(this).fadeOut();
	  $(".remove").fadeOut();
	  id = $(this).attr('id');
	  indx = id.split('_')[1];
	  next_id = parseInt(indx) + 1;
	  $("#addTask_"+ next_id).fadeIn();
	  $( "#task_" + indx ).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	  setTimeout(function() {
		  $( "#removeTask_" + indx ).fadeIn();
		  }, 300); 
	});

	
	// Remove Code Type/ Tasks
	$(".remove" ).click(function() {
	  $(".add").fadeOut();
	  $(this).fadeOut();
	  id = $(this).attr('id');
	  indx = id.split('_')[1];
	  prev_id = parseInt(indx) - 1;
	  $("#addTask_" + indx).fadeIn();
	  $( "#task_" + indx).animate({
		height: "toggle"
	  }, 300, function() {
	  });
	  $( "#removeTask_" + indx ).hide();  
	  $( "#removeTask_" + prev_id ).fadeIn();
	});
	
});

