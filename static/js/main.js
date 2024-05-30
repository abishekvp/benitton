(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 90) {
            $('.nav-bar').addClass('sticky-top shadow');
        } else {
            $('.nav-bar').removeClass('sticky-top shadow');
        }
    });
    
    
    // Dropdown on mouse hover
    const $dropdown = $(".dropdown");
    const $dropdownToggle = $(".dropdown-toggle");
    const $dropdownMenu = $(".dropdown-menu");
    const showClass = "show";
    
    $(window).on("load resize", function() {
        if (this.matchMedia("(min-width: 992px)").matches) {
            $dropdown.hover(
            function() {
                const $this = $(this);
                $this.addClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "true");
                $this.find($dropdownMenu).addClass(showClass);
            },
            function() {
                const $this = $(this);
                $this.removeClass(showClass);
                $this.find($dropdownToggle).attr("aria-expanded", "false");
                $this.find($dropdownMenu).removeClass(showClass);
            }
            );
        } else {
            $dropdown.off("mouseenter mouseleave");
        }
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });


    // Date and time picker
    $('.date').datetimepicker({
        format: 'L'
    });
    $('.time').datetimepicker({
        format: 'LT'
    });


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });


    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });


    // Service carousel
    $(".service-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        margin: 25,
        dots: true,
        loop: true,
        nav : false,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:2
            },
            1200:{
                items:3
            }
        }
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        center: true,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            768:{
                items:2
            },
            992:{
                items:3
            }
        }
    });
    
})(jQuery);


function search() {
    $(".search-result").css("display", "block");
    $(".search-result").empty();
    $(".search-result").append("<button type='button' onclick='close_result()' class='close-result'>Clear</button>")
    $(".search-result").append('<div id="loader" class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>')
    $.ajax({
        type: "POST",
        url: "/search",
        data: {
          search: $('#search-input').val(),
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function (response) {
            $("#loader").remove();
          for (i = 0; i < response["products"].length + 1; i++) {
            setTimeout(
              function (i) {
                $(".search-result").append(
                  "<a href='" +
                    response["products"][i]["url"] +
                    "'>" +
                    "<div class='search-result-product'>" +
                    "<img src='data:image/jpeg;base64," +
                    response["products"][i]["image"] +
                    "'/>" +
                    "<p>" +
                    response["products"][i]["name"] +
                    "</p>" +
                    "<br>" +
                    "</div>" +
                    "</a>"
                );
              },
              100 * i,
              i
            );
          }
        },
    });
}

function close_result() {
    $(".search-result").empty();
    $(".search-result").css("display", "none");
}

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

function open_enquiry_form(){
$(".float-enquiry-form").css("display", "block");
}
function close_enquiry_form(){
$(".float-enquiry-form").css("display", "none");
}
function submit_enquiry(){

$.ajax({
    type: "POST",
    url: "/enquiry",
    data: {
    user_name: $("#user_name").val(),
    user_contact: $("#user_contact").val(),
    product_name: $("#product_name").val(),
    product_code: $("#product_code").val(),
    user_city: $("#user_city").val(),
    user_state: $("#user_state").val(),
    user_message: $("#user_message").val(),
    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    },
    success: function(response){
    if(response['status']==200){
        alert('Enquiry has been Submitted Succesfully');
        close_enquiry_form();
    }
    }
});
}

$(".navbar-nav>li>a").on("click", function () {
$(".navbar-collapse").collapse("hide");
});