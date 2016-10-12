$(document).ready(function() {
    /**** Menu Scroll ****/
    $('.mainMenuLink:not(a[href=#])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                exact_s = target.offset().top - 55;
                $('html,body').animate({
                    scrollTop : exact_s
                }, 1000, function() {
                });
                return false;
            }
        }
    });
    /***** Scroller *****/
});
