    function initMap() {
        var uluru = { lat: 53.109684, lng: 6.100173 };
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 18,
            center: uluru,
            
        });
        var marker = new google.maps.Marker({
            position: uluru,
            map: map,
            title: 'Experina sports prizes'
        });
    }