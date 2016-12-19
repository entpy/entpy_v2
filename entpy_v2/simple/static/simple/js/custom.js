/*	
	Custom JS

	2. Fixed Top Menubar
	13. PRELOADER 
	15. MOBILE MENU CLOSE 	
*/
jQuery(function($) {
	/* ----------------------------------------------------------- */
	/*  2. Fixed Top Menubar
	/* ----------------------------------------------------------- */
	// For fixed top bar
	$(window).scroll(function() {
		if ($(window).scrollTop() > 100 /*or $(window).height()*/ ) {
			$(".navbar-fixed-top").addClass('past-main');
		} else {
			$(".navbar-fixed-top").removeClass('past-main');
		}
	});

	//Check to see if the window is top if not then display button
	$(window).scroll(function() {
		if ($(this).scrollTop() > 300) {
			$('.scrollToTop').fadeIn();
		} else {
			$('.scrollToTop').fadeOut();
		}
	});

	//Click event to scroll to top
	$('.scrollToTop').click(function() {
		$('html, body').animate({scrollTop: 0}, 800);
		return false;
	});


	/* ----------------------------------------------------------- */
	/*  13. PRELOADER 
	/* ----------------------------------------------------------- */
	jQuery(window).load(function() { // makes sure the whole site is loaded
		$('#status').fadeOut(); // will first fade out the loading animation
		$('#preloader').delay(100).fadeOut('slow'); // will fade out the white DIV that covers the website.
		$('body').delay(100).css({'overflow': 'visible'});
	});

	/* ----------------------------------------------------------- */
	/*  15. MOBILE MENU ACTIVE CLOSE 
	/* ----------------------------------------------------------- */
	$('.navbar-nav').on('click', 'li a', function() {
		$('.navbar-collapse').collapse('hide');
	});
});
