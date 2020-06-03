$(document).ready( function() {
    $('.reportTable').DataTable({
    'rowCallback': function(row, data, index) {
    if (data[0].indexOf('Draft') != -1) {
        $(row).find('td').css('background-color', '#ffffc0');
    }
    },
    "order": [[ 2, "desc"]]
    });

    $('.analyticsTable').DataTable({
    "order": [[ 0, "desc"]]
    });

    $('.ordersTable').DataTable({
    "order": [[ 0, "desc"]]
    });

    $('.ordersbyTable').DataTable({
    "order": [[ 0, "desc"]]
    });
} );