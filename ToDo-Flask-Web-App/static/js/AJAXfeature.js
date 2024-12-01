$(document).ready(function() {
    $('.like-btn').click(function() {
        var productId = $(this).data('product-id');
        var button = $(this);
        
        $.ajax({
            url: '/like',
            type: 'POST',
            data: {product_id: productId},
            success: function(response) {
                if (response.success) {
                    button.toggleClass('btn-outline-primary btn-primary');
                    button.find('i').toggleClass('fas far');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error liking product:', error);
            }
        });
    });
});