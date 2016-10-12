var hash_scroll = function(e) {
 	if (window.location.pathname == '/main/home'){
 		e && e.preventDefault();

 		var elem_id = this.hash || window.location.hash;

	    var target = $(elem_id);
	    var scroll_pos = target.offset().top - 80;
	    if (elem_id != '#forms') {
	    	scroll_pos += 30;
	    }
	    $('html,body').animate({
		     scrollTop : scroll_pos
		}, 1000);
	}
}

$( window ).load(function() {
	if (window.location.hash) {
		hash_scroll();
	}
});

$(document).ready(function() {
	/**** Menu Scroll ****/
	 $('.mainMenuLink').click(hash_scroll);
	 /**** End Menu Scroll ****/
	$(document).on('click', ".board_mem", function(e) {
		e.preventDefault();
		$(".popupbackground").show();
		$(".board_members").show();
	});
	$(document).on('click', ".close", function(e) {
		e.preventDefault();
		$(".popupbackground").hide();
		$(".board_members").hide();
	});

	/* Sudo Slider Animation on mouse enter and mouse leave starts here */
	var auto = true;
   	var autostopped = false;

   	/* Slider 1 starts */
   	var sudoSlider1 = $("#slider1").sudoSlider({
		prevNext : true,
		speed: 100,
		effect: "fade",
	    auto:true,
	    resumePause:5000
	})
   	.mouseenter(function() {
      auto = sudoSlider1.getValue('autoAnimation');
      if (auto) {
         sudoSlider1.stopAuto();
      } else {
         autostopped = true;
      }
   	}).mouseleave(function() {
      if (!autostopped) {
         sudoSlider1.startAuto();
      }
   	});
   	/* Slider 1 ends */

   	/* Slider 2 starts */
   	var sudoSlider2 = $("#slider2").sudoSlider({
		prevNext : true,
		speed: 100,
		effect: "fade",
	    auto:true,
	    resumePause:5000
	})
   	.mouseenter(function() {
      auto = sudoSlider2.getValue('autoAnimation');
      if (auto) {
         sudoSlider2.stopAuto();
      } else {
         autostopped = true;
      }
   	}).mouseleave(function() {
      if (!autostopped) {
         sudoSlider2.startAuto();
      }
   	});
   	/* Slider 2 ends */

   	/* Slider 3 starts */
   	var sudoSlider3 = $("#slider3").sudoSlider({
		prevNext : true,
		speed: 100,
		effect: "fade",
	    auto:true,
	    resumePause:5000
	})
   	.mouseenter(function() {
      auto = sudoSlider3.getValue('autoAnimation');
      if (auto) {
         sudoSlider3.stopAuto();
      } else {
         autostopped = true;
      }
   	}).mouseleave(function() {
      if (!autostopped) {
         sudoSlider3.startAuto();
      }
   	});
   	/* Slider 3 ends */
	/* Sudo Slider Animation on mouse enter and mouse leave ends here */	

	$("#slider4").sudoSlider({
		prevNext : true,
		autoHeight: false,
		prevHtml : '<a href="#" class="prevBtnBig">  </a>',
		nextHtml : '<a href="#" class="nextBtnBig">  </a>',
	});
	
	//Menu Slide
	$('ul.tabs').each(function(){
		var $active, $content, $links = $(this).find('a');

		$active = $($links.filter('[href="'+location.hash+'"]')[0] || $links[0]);
		$active.addClass('active');

		$content = $($active[0].hash);

		$links.not($active).each(function () {
			$(this.hash).hide();
		});

		$(this).on('click', 'a', function(e){
			$active.removeClass('active');
			$content.hide();

			$active = $(this);
			$content = $(this.hash);

			$active.addClass('active');
			$content.show();

			e.preventDefault();
		});
	});
	 /***** Scroller *****/

 $(".management_scroll").slimScroll({
  height : "100%",
  width : "auto",
  disableFadeOut : true
 });
 $(".customer_scroll").slimScroll({
  height : "100%",
  width : "auto",
  disableFadeOut : true
 });

 /***** Scroller *****/
 $("#inbound_contacts").colorbox({inline:true, width:'30%'});
 $("#inbound_contacts").click(function(){
 	$('.icon_flag').qtip('hide');
 });
});

$('.date_time').each(function(){
	var new_date = moment($(this).attr('value'), 'MM DD YYYY, HH:mm').toDate();
	var offset = new_date.getTimezoneOffset();
	var browser_date = moment(new_date).add('minutes', -offset).format('ddd, MMM DD YYYY, h:mm A')
	$(this).text(browser_date)
});