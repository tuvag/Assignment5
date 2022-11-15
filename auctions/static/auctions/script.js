
document.addEventListener('DOMContentLoaded', function() {
    update_totals();
    setInterval(update_totals, 3000);
    initialize_watchlist_icons();
});

function update_totals() {
    fetch(`/api_listing_toatals`)
    .then(response => response.json())
    .then(data => {
        document.querySelector('#active_listings').innerHTML = data['total_active_listings'],
        document.querySelector('#total_watchlisted').innerHTML = data['total_watchlisted']
    })
    .catch(error => {
        console.log('There is an error with updating counters', error);
    });
}

function watchlist_toggle(listing_id) {
    fetch(`/api_toggle_watchlist/${listing_id}`)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        update_icon(data, listing_id);
    });
}

function initialize_watchlist_icons() {
    // called after doc loaded to make a javascript call back to the server
    // for each toggler, to find the correct currrent state.
    document.querySelectorAll(".toggler").forEach(img => {
        const listing_id = img.id.split("_")[1];
        fetch(`/api_watchlist_state/${listing_id}`)
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            update_icon(data, listing_id);
        });
    })
}

function update_icon(data, id) {
    newstate = data.curr_value;
    filename = `/media/images/${newstate}.png`;
    document.querySelector("#toggler_"+id).src = filename;
}
  
