$(document).ready(function () {
    var searches = [];
    function loadSearches() {
        $.getJSON('/searches', function (data, status, xhr) {
            for (var i = 0; i < data.length; i++) {
                searches.push(data[i].search);
            }
        });
    };
    loadSearches();

    $('#id_search').autocomplete({
        source: searches,
    }); 
}); 