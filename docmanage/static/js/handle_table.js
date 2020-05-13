$(document).ready( function() {
    $('.myTable').DataTable({
    'rowCallback': function(row, data, index) {
    if (data[0].indexOf('Draft') != -1) {
        $(row).find('td').css('background-color', '#ffffc0');
    }
    }
    });
} );