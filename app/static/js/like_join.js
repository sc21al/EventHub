// Sends an AJAX POST request to like an event and updates the UI accordingly.
function likeEvent(buttonElement) {
    // Retrieve the event ID from the button's data attribute.
    var eventId = buttonElement.getAttribute('data-event-id');
    // Make the AJAX call to the server.
    $.ajax({
        url: '/like-event/' + eventId, // Server endpoint for liking an event.
        type: 'POST', // Method type.
        success: function(response) { // Callback for successful response.
            // Update like count on the UI.
            var likesElement = $('#likes-' + eventId);
            likesElement.text(response.likes);
            // Update button text based on like status.
            var buttonText = response.liked ? "Liked" : "Like";
            $(buttonElement).text(buttonText);
            // Toggle button class based on like status for styling.
            if (response.liked) {
                $(buttonElement).removeClass('btn-like-custom').addClass('btn-purple');
            } else {
                $(buttonElement).removeClass('btn-purple').addClass('btn-like-custom');
            }
        },
        error: function(error) { // Callback for errors.
            console.log('Error liking event:', error); // Log errors to console.
        }
    });
}

// Sends an AJAX POST request to join an event and updates the UI accordingly.
function joinEvent(buttonElement) {
    // Retrieve the event ID from the button's data attribute.
    var eventId = buttonElement.getAttribute('data-event-id');
    // Make the AJAX call to the server.
    $.ajax({
        url: '/join-event/' + eventId, // Server endpoint for joining an event.
        type: 'POST', // Method type.
        success: function(response) { // Callback for successful response.
            // Update participant count on the UI.
            var participantsElement = $('#participants-' + eventId);
            participantsElement.text(response.participants);
            // Update button text based on join status.
            var buttonText = response.joined ? "Unjoin" : "Join";
            $(buttonElement).text(buttonText);
            // Toggle button class based on join status for styling.
            if (response.joined) {
                $(buttonElement).removeClass('btn-warning').addClass('btn-join-custom');
            } else {
                $(buttonElement).removeClass('btn-join-custom').addClass('btn-warning');
            }
        },
        error: function(error) { // Callback for errors.
            console.log('Error joining event:', error); // Log errors to console.
        }
    });
}
