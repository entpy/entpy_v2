/*	
	Custom JS

	2. Fixed Top Menubar
	6. Project Counter
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


	/* ----------------------------------------------------------- */
	/*  6. Project Counter
	/* ----------------------------------------------------------- */
	(function($) {
		$.fn.countTo = function(options) {
			options = options || {};

			return $(this).each(function() {
				// set options for current element
				var settings = $.extend({}, $.fn.countTo.defaults, {
					from: $(this).data('from'),
					to: $(this).data('to'),
					speed: $(this).data('speed'),
					refreshInterval: $(this).data('refresh-interval'),
					decimals: $(this).data('decimals')
				}, options);

				// how many times to update the value, and how much to increment the value on each update
				var loops = Math.ceil(settings.speed / settings.refreshInterval),
					increment = (settings.to - settings.from) / loops;

				// references & variables that will change with each update
				var self = this,
					$self = $(this),
					loopCount = 0,
					value = settings.from,
					data = $self.data('countTo') || {};

				$self.data('countTo', data);

				// if an existing interval can be found, clear it first
				if (data.interval) {
					clearInterval(data.interval);
				}
				data.interval = setInterval(updateTimer, settings.refreshInterval);

				// initialize the element with the starting value
				render(value);

				function updateTimer() {
					value += increment;
					loopCount++;

					render(value);

					if (typeof(settings.onUpdate) == 'function') {
						settings.onUpdate.call(self, value);
					}

					if (loopCount >= loops) {
						// remove the interval
						$self.removeData('countTo');
						clearInterval(data.interval);
						value = settings.to;

						if (typeof(settings.onComplete) == 'function') {
							settings.onComplete.call(self, value);
						}
					}
				}

				function render(value) {
					var formattedValue = settings.formatter.call(self, value, settings);
					$self.html(formattedValue);
				}
			});
		};

		$.fn.countTo.defaults = {
			from: 0, // the number the element should start at
			to: 0, // the number the element should end at
			speed: 1000, // how long it should take to count between the target numbers
			refreshInterval: 100, // how often the element should be updated
			decimals: 0, // the number of decimal places to show
			formatter: formatter, // handler for formatting the value before rendering
			onUpdate: null, // callback method for every time the element is updated
			onComplete: null // callback method for when the element finishes updating
		};

		function formatter(value, settings) {
			return value.toFixed(settings.decimals);
		}
	}(jQuery));

	jQuery(function($) {
		// custom formatting example
		$('#count-number').data('countToOptions', {
			formatter: function(value, options) {
				return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
			}
		});

		$('#count-number2').data('countToOptions', {
			formatter: function(value, options) {
				return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
			}
		});

		$('#count-number3').data('countToOptions', {
			formatter: function(value, options) {
				return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
			}
		});

		$('#count-number4').data('countToOptions', {
			formatter: function(value, options) {
				return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
			}
		});

		// start all the timers
		$('.timer').each(count);

		function count(options) {
			var $this = $(this);
			options = $.extend({}, options || {}, $this.data('countToOptions') || {});
			$this.countTo(options);
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
