$(document).ready(function() {
    // Form submission handler
    $('#prediction-form').on('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = {
            cylinders: $('#cylinders').val(),
            displacement: $('#displacement').val(),
            horsepower: $('#horsepower').val(),
            weight: $('#weight').val(),
            acceleration: $('#acceleration').val(),
            model_year: $('#model_year').val()
        };
        
        // Show loading state
        $('#result').removeClass('success error').html('Predicting...').show();
        
        // Make API call
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                if (response.success) {
                    $('#result')
                        .removeClass('error')
                        .addClass('success')
                        .html(`<strong>Predicted MPG:</strong> ${response.prediction.toFixed(2)} miles per gallon`);
                } else {
                    $('#result')
                        .removeClass('success')
                        .addClass('error')
                        .html(`Error: ${response.error}`);
                }
            },
            error: function() {
                $('#result')
                    .removeClass('success')
                    .addClass('error')
                    .html('Error: Could not connect to the server. Please try again.');
            }
        });
    });

    // Form validation
    $('input[type="number"]').on('input', function() {
        let value = $(this).val();
        if (this.id === 'model_year') {
            if (value < 70 || value > 82) {
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        }
    });
});