$(document).ready(function(){
	$('.nav-link').on('click', function() {
		$('.active-link').removeClass('active-link');
		$(this).addClass('active-link');
	});
	$("div.hamburger").click(function(){
		// $("div.overlay").fadeToggle();
	 //    $("#listVSV").fadeToggle();
	    if ( $('#hamburgerVivek').hasClass("is-active") ) {
	    	$('#listVSV').css("transform", "translateY(0%)");
	    	$('#overlayImage').css("transform", "translateX(0%)");
	    }
	    else {
	    	$('#listVSV').css("transform", "translateY(-125%)");
	    	$('#overlayImage').css("transform", "translateX(-200%)");	
	    }

	 });
});