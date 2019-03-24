//Displaysdropdown when page is loaded
$(document).ready(function () {
    populateDayDropdown()
    populate('#time')
    initMap();
});

$(document).on("submit", "#travel_now", function (e) { 
     var url = $("#travel_now").attr("predict-url"); 
    console.log(url);
    console.log($(this).serialize());
    alert(($("#travel_now").serialize()));
             $.ajax({    
                type:'POST',
                url: url,
                data: $("#travel_now").serialize(),
                success: function (data) {
                    $("#journeyRes").html(data); 
                }
             });
          e.preventDefault();
        });

$(document).on("submit", "#route_selector", function (e) { 
     var url = $("#route_selector").attr("predict-url"); 
    console.log(url)
             $.ajax({    
                type:'POST',
                url: url,
                data: $("#route_selector").serialize(),
                success: function (data) {
                    $("#prediction").html(data); 
                }
             });
          e.preventDefault();
        });

$(document).on("change","#Route", function () {
    var routeName = $(this).val(); 
    var csrf = $(this).attr('csrf-token');
    var url = $(this).attr("url");
    $.ajax({    
        type:'POST',
        url: url,                   
        data: {routeName: routeName,
               csrfmiddlewaretoken: csrf},
        success: function (data) { 
            $("#StartStop").html(data); 
            $("#EndStop").html(data);
        }
    });
});

//Populates BusLines Tab with stops serviced along selected route
$(document).on("click", "#Busline", function() {
var i;
var url = $("#Busline").attr("url"); 
var csrf = $(this).attr('csrf-token');
console.log(csrf)
    var busline = $(this).val();
    var panel = this.nextElementSibling;
    console.log(busline)
    this.classList.toggle("active");
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        panel.style.display = "block";
    }   
    $.ajax({    
      type:'POST',
      url: url,                   
      data: {busline: busline,
             csrfmiddlewaretoken: csrf},
    success: function (data) { 
        panel.innerHTML=data;
    }
  });     
});


//Populates the day dropdown list for prediction model using weekday/weekend value
function populateDayDropdown() {
        var d = new Date();
        var n = d.getDay();
        var date = d.getDate();
        var month = d.getMonth();
        var i = n;
		var option = document.getElementById('day'),
        days = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday']
        months =['January','February','March','April','May','June','July','August','September','October','November','December']
        var j = 1;
        while (j <= 5){
              if (month==3 || month==5 || month==8 || month==10){
            datelim=30;
        }
        else if (month==1){
            datelim=28;
        }
        else{
            datelim=31;
        }
        if (date>datelim){
            newDate=date-datelim;
            newMonth=months[month+1];
        }
        else{
            newDate=date;
            newMonth=month;
        }
            if (newDate==1 || newDate==2 || newDate==31){
                var suffix = 'st';
            }
            else if (newDate==2||newDate==22){
                var suffix = 'nd';
            }
            else if (newDate==3||newDate==23){
                var suffix = 'rd';
            }
            else{
                var suffix='th';
            }
            option[j] = new Option(days[i-1]+" "+ newDate+suffix+" "+months[newMonth], days[i-1]+" "+newDate++)
            if (i > 6){
                i -=6;
            }
            else{
                i++
            }
            j++
            date++
            }}

//Populates the dropdown menu with times
function populate(selector) {
    var select = $(selector);
    var hours, minutes, ampm;
    for (var i = 0; i <= 1450; i += 5) {
        hours = Math.floor(i / 60);
        minutes = i % 60;
        if (minutes < 10) {
            minutes = '0' + minutes; // adding leading zero to minutes portion
        }
        if (hours < 10) {
            hours = '0' + hours;
        }
        //add the value to dropdownlist
        select.append($('<option></option>')
        .attr('value', hours)
        .text(hours + ':' + minutes));
            }
        }

// Display the markers on the map when route is selected 
function displayMarkers() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 53.3498053,
            lng: -6.260309699999993
        },
        zoom: 13,
    });
}
    
    var route = $('#Route').val(); 
    var csrf = $(this).attr('csrf-token');
    var url = $(this).attr("url");
    
//    $.ajax({    
//        type:'POST',
//        url: url,                   
//        data: {route: route,
//               csrfmiddlewaretoken: csrf},
//        success: function (data) { 
//            $("#lat").html(data); // replace the contents of the city input with the data that came from the server
//            $("#lng").html(data);
//        }
//    });
//});
//

    

// Display the map
function initMap() {
    var myLatLng = {lat: 53.3498, lng: -6.2603};
    var mapCanvas = document.getElementById('map');
    var map = new google.maps.Map(mapCanvas, {
        zoom: 15,
        center: myLatLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
});            
// Autocomplete functionality 
function initialize_origin() {
    var options = {
        componentRestrictions: {country: "ie"}
    };
    var input = document.getElementById('searchOrigin');
    var autocomplete = new google.maps.places.Autocomplete(input, options);
                
    // Centre on selected location on map
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
    var place = autocomplete.getPlace();
    if (place.geometry.viewport) {
        map.fitBounds(place.geometry.viewport);
        }
    else {
        map.setCenter(place.geometry.location);
        map.setZoom(17); 
        }  
    });
}
function initialize_destination() {
    var options = {
        componentRestrictions: {country: "ie"}
     };
    
    var input = document.getElementById('searchDest');
    var autocomplete = new google.maps.places.Autocomplete(input, options);

    // Centre on selected location on map
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        var place = autocomplete.getPlace();
        //console.log(place);
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17); 
        }  
   });
}
initialize_origin(); 
initialize_destination();

}
