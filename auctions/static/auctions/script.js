
document.addEventListener('DOMContentLoaded', function() {
    update_totals();
    setInterval(update_totals, 3000);
});

function update_totals() {
    fetch(`api_listing_toatals`)
    .then(response => response.json())
    .then(data => {
        document.querySelector('#active_listings').innerHTML = data['total_active_listings'],
        document.querySelector('#total_watchlisted').innerHTML = data['total_watchlisted']
    })
    .catch(error => {
        console.log('There is an error with updating counters', error);
    });
}