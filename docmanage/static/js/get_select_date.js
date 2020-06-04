$(document).ready(function() {
    var select_date = $('.select-filter')

    select_date.on('change', function(){
//        getUpdateSettings();
        $("#submit_form").submit();
        // added to reload the png data
        window.onload = reload;
    });

    function reload() {
        location.reload()
    }

    // send the data of select box to analytics.html as filter_date
//    function getUpdateSettings() {
//        var send = {
//            filter_date: select_date.val()
//        };
//        console.log("send", send)
//        $.getJSON('./analytics', send, function(response) {
//            console.log("response", response)
//        })
//    }



} );