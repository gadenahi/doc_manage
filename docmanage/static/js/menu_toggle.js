$(document).ready( function() {
    $(".navbar-nav").on("click", function() {
        $(".navbar-collapse").toggleClass("toggled");
    })(jQuery);
} );


<script>
    (function($) {
        $(".menu-toggle").on("click", function() {
            $(".main-navigation").toggleClass("toggled");
        });
    })(jQuery);
</script>