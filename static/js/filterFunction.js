$(document).ready(function() {
    $('#price-filter-form').on('submit', function(e) {
        e.preventDefault();
        var minPrice = $('#min-price').val();
        var maxPrice = $('#max-price').val();

        $.ajax({
            url: '/filter_products',
            type: 'GET',
            data: {
                min_price: minPrice,
                max_price: maxPrice
            },
            success: function(response) {
                $('.row').html(response);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});