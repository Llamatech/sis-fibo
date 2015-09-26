jQuery(function($) {
    'use strict',

    //#main-slider
    $(function() {
        $('#main-slider.carousel').carousel({
            interval: 8000
        });
    });


    // accordian
    $('.accordion-toggle').on('click', function() {
        $(this).closest('.panel-group').children().each(function() {
            $(this).find('>.panel-heading').removeClass('active');
        });

        $(this).closest('.panel-heading').toggleClass('active');
    });

    //Initiat WOW JS
    new WOW().init();

    // portfolio filter
    $(window).load(function() {
        'use strict';
        var $portfolio_selectors = $('.portfolio-filter >li>a');
        var $portfolio = $('.portfolio-items');
        $portfolio.isotope({
            itemSelector: '.portfolio-item',
            layoutMode: 'fitRows'
        });

        $portfolio_selectors.on('click', function() {
            $portfolio_selectors.removeClass('active');
            $(this).addClass('active');
            var selector = $(this).attr('data-filter');
            $portfolio.isotope({
                filter: selector
            });
            return false;
        });
    });

    // Contact form
    // var form = $('#main-contact-form');
    // form.submit(function(event){
    // 	event.preventDefault();
    // 	var form_status = $('<div class="form_status"></div>');
    // 	$.ajax({
    // 		url: $(this).attr('action'),

    // 		beforeSend: function(){
    // 			form.prepend( form_status.html('<p><i class="fa fa-spinner fa-spin"></i> Email is sending...</p>').fadeIn() );
    // 		}
    // 	}).done(function(data){
    // 		form_status.html('<p class="text-success">' + data.message + '</p>').delay(3000).fadeOut();
    // 	});
    // });


    //goto top
    $('.gototop').click(function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $("body").offset().top
        }, 500);
    });

    //Pretty Photo
    $("a[rel^='prettyPhoto']").prettyPhoto({
        social_tools: false
    });

    $("#admin_employee").click(
        function(event) {
            $("#admin_info1").show();
            $("#admin_info1").collapse("show");
            $("#admin_info2").hide();
            $("#admin_info3").hide();
            $.smoothScroll({
                // scrollElement: $('div.scrollme'),
                scrollTarget: '#admin_info1',
                offset: -100
            });
            /* Act on the event */
        });

    $("#admin_pa").click(
        function(event) {
            $("#admin_info1").hide();
            $("#admin_info2").show();
            $("#admin_info2").collapse("show");
            $("#admin_info3").hide();
            $.smoothScroll({
                // scrollElement: $('div.scrollme'),
                scrollTarget: '#admin_info2',
                offset: -100
            });
            /* Act on the event */
        });

    $("#admin_offices").click(
        function(event) {
            $("#admin_info1").hide();
            $("#admin_info2").hide();
            $("#admin_info3").show();
            $("#admin_info3").collapse("show");
            $.smoothScroll({
                // scrollElement: $('div.scrollme'),
                scrollTarget: '#admin_info3',
                offset: -100
            });
            /* Act on the event */
        });

    $("#ggeneral_misc").click(
        function(event) {
            // $("#admin_info1").hide();
            // $("#admin_info2").hide();
            // $("#admin_info3").show();
            $("#ggeneral_info3").collapse("show");
            $.smoothScroll({
                // scrollElement: $('div.scrollme'),
                scrollTarget: '#ggeneral_info3',
                offset: -100
            });
            /* Act on the event */
        });

    $('#b_date .input-group.date').datepicker({
        format: "dd/mm/yyyy",
        startDate: "01/01/1950",
        endDate: "31/12/1996",
        startView: 2,
        language: "es"
    });

    $('#fromD').datepicker({
        format: "dd/mm/yyyy",
        startDate: "01/01/2015",
        endDate: "today",
        startView: 2,
        language: "es"
    });

    $('#cuota_input').datepicker({
        format: "dd/mm/yyyy",
        startDate: "today",
        startView: 2,
        language: "es"
    });

    $('#toD').datepicker({
        format: "dd/mm/yyyy",
        startDate: "01/01/2015",
        endDate: "today",
        startView: 2,
        language: "es"
    });

    $('#toMD').datepicker({
        format: "dd/mm/yyyy",
        startDate: "01/01/2015",
        endDate: "today",
        startView: 2,
        language: "es"
    });
    $('#fromMD').datepicker({
        format: "dd/mm/yyyy",
        startDate: "01/01/2015",
        endDate: "today",
        startView: 2,
        language: "es"
    });

    $('#back_btn').click(function() {
        parent.history.back();
        return false;
    });

});