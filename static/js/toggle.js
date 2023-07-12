
$(window).on("load", function () {
    $('body').addClass('loaded');
});

console.log("Home section is working")

$(document).ready(function () {
    $('.dropdown').hover(
        function () {
            $(this).find('i').removeClass('fa-chevron-down').addClass('fa-chevron-up');
        },
        function () {
            $(this).find('i').removeClass('fa-chevron-up').addClass('fa-chevron-down');
        }
    )
});
var hamburger = document.querySelector('.navbar-toggler');
var body = document.body;

hamburger.addEventListener('click', function() {
  body.classList.toggle('no-scroll');
});

