//Displaysdropdown when page is loaded
$(document).ready(function() {
    startTime();
    $('#picker2').dateTimePicker();
    $('#picker').dateTimePicker();
    $("#picker").hide();
    $("#picker2").hide();
    $("#leapBalance").hide();
    displayMap();
});

//  Function to show the user's current location on the map 
function getLocation() {
    // Error handler for geolocation 
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(showPosition, showError);
    }
}

function showPosition(position) {
    //https://developers.google.com/maps/documentation/javascript/examples/geocoding-reverse

    // Function to show marker for user's current location on the map on page load
    var geocoder = new google.maps.Geocoder;
    var infowindow = new google.maps.InfoWindow;
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    var myLatLng = {
        lat: lat,
        lng: lon
    };
    geocoder.geocode({
        'location': myLatLng
    }, function(results) {
        console.log(results);
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(myLatLng),
            map: map,
            animation: google.maps.Animation.DROP,
        });
        map.setCenter(marker.getPosition());
        map.setZoom(13);
        google.maps.event.addListener(marker, 'click', (function(marker) {
            return function() {
                // Info window for current location marker on click 
                infowindow.setContent(results[0].formatted_address);
                infowindow.open(map, marker);
            }
        })(marker));
        var searchbox = document.getElementById("searchOrigin");
        console.log(results[0].formatted_address)
        searchbox.name = results[0].place_id;
        searchbox.value = results[0].formatted_address;
    });

}

function showError(error) {
    // Error messages to display when geolocation does not work or is denied by the user
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

// Function to allow the user to swap between hidden and visible password 
function PasswordToggle() {
    var x = document.getElementById("leapPass");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}


$(document).on("submit", "#leapForm", function(e) {
    // AJAX call to pass the leap card login credentials to the Python view functions leapForm
    $("#leapBalance").show();
    var url = $("#leapForm").attr("url");
    var username = document.getElementById('leapUsername').value;
    var password = $("#leapPass").val();
    var csrf = $("#leapPass").attr("csrf-token");
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            username: username,
            password: password,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#journeyRes").hide()
            $("#prediction").hide();
            $("#leapBalance").show();
            $("#leapBalance").html(data);
        }
    });
    e.preventDefault();
});

$(document).on("submit", "#travel_now", function(e) {
    // AJAX call to pass the values from the search by address tab to the predictNow function 
    // Gets value for origin, destination and leave time 
    var url = $("#travel_now").attr("predict-url");
    var startPlace = document.getElementById('searchOrigin').value;
    var startId = $('#searchOrigin').attr("name");
    var endPlace = document.getElementById('searchDest').value;
    var endId = $('#searchDest').attr("name");
    var csrf = $(this).attr('csrf-token');
    var value = $("#leaveTime").val();
    var dateTime;
    if (value == 1 || value == 2) {
        dateTime = $('#datetime').val();
        var DayTime = dateTime.split(" ");
        var dates = DayTime[0].split("/");
        var times = DayTime[1].split(":");
        var d = new Date(dates[2], dates[1] - 1, dates[0], times[0], times[1])
        var timeInSeconds = (d / 1000);
    } else {
        dateTime = "0";
        timeInSeconds = "0";
    }
    console.log(timeInSeconds);
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            startPlace: startPlace,
            startId: startId,
            endPlace: endPlace,
            endId: endId,
            csrfmiddlewaretoken: csrf,
            value: value,
            timeInSeconds: timeInSeconds,
            dateTime: dateTime,
        },
        success: function(data) {
            $("#leapBalance").hide();
            $("#prediction").hide();
            $("#journeyRes").show();
            $("#journeyRes").html(data);
        }
    });
    e.preventDefault();
});

$(document).on("submit", "#route_selector", function(e) {
    // AJAX call to pass all values taken from the search by route field back to the prediction Python view 
    // Gets value for route, direction, startStop, endStop and leaveTime 
    if ($.trim($("#routeStopSearch").val()) === "" || $.trim($("#Direction").val()) === "" || $.trim($("#StartStop").val()) === "" || $.trim($("#EndStop").val()) === "") {
        alert("You did not fill out one of the fields");
        return false;
    } else {
        var url = $("#route_selector").attr("predict-url");
        var value = $("#leaveTimeStop").val();
        var Route = $("#routeStopSearch").val();
        var Direction = $("#Direction").val();
        var StartStop = $("#StartStop").val();
        var EndStop = $("#EndStop").val();
        var csrf = $("#route_selector").attr('csrf-token');
        var dateTime;
        if (value == 1 || value == 2) {
            dateTime = $('#datetimeStop').val();
            console.log(dateTime);
        } else {
            dateTime = "0";
        }
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                Route: Route,
                Direction: Direction,
                StartStop: StartStop,
                EndStop: EndStop,
                value: value,
                dateTime: dateTime,
                csrfmiddlewaretoken: csrf
            },
            success: function(data) {
                $("#leapBalance").hide();
                $("#journeyRes").hide();
                $("#prediction").show();
                $("#prediction").html(data);
            }
        });
        e.preventDefault();
    }
});
$(document).on("change", "#routeStopSearch", function() {
    // AJAX call to pass the route typed by the user to the Python view get_routes_stops (autocomplete search) 
    // Passes value to load_direction view to populate the direction dropdown with the relevant information
    var routeName = $(this).val();
    document.getElementById("Direction").innerHTML = "";
    var csrf = $(this).attr('csrf-token');
    var url = $(this).attr("url");
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            routeName: routeName,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#Direction").html(data);
        }
    });
});

$(document).on("change", "#Direction", function() {
    // AJAX call to pass the value of the direction selected by the user to the Python load_busStops view 
    // Populates the Start Stop and End Stop dropdown with the relevent stops based on direction selected 
    var routeName = $("#routeStopSearch").val();
    var direction = $(this).val();
    var csrf = $(this).attr('csrf-token');
    var url = $(this).attr("url");
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            routeName: routeName,
            direction: direction,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            $("#StartStop").html(data);
            $("#EndStop").html(data);
        }
    });
    var sideNav = document.getElementById("mySidenav");
    if (sideNav.style.width == "100%") {
        $(document).ready(function() {
            $('[data-toggle="popover"]').popover();
        });
    }
});

$(document).on("change", "#StartStop", function() {
    // Function to disable the options based on the previously selected option
    // Stops up to and including the start stop will not be available for selection in the end stop dropdown
    var id = $(this).val();
    var routeName = $("#routeStopSearch").val();
    var direction = $("#Direction").val();
    var csrf = $("#Direction").attr('csrf-token');
    $.ajax({
        type: 'POST',
        url: "selectedStartStationInfo/",
        data: {
            routeName: routeName,
            direction: direction,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            var newID = parseInt(id);
            var start = data.indexOf(newID);
            for (i = 0; i < start + 1; i++) {
                //https://stackoverflow.com/questions/24909907/disable-options-based-on-previous-selects
                $("#EndStop").find("option[value='" + data[i] + "']").prop("disabled", true);
            }
        }
    });
});

$(document).on("change", "#EndStop", function() {
    // Function to disable the options based on the previously selected option
    // Stops after and including the end stop will not be available for selection in the start stop dropdown
    var id = $(this).val();
    var routeName = $("#routeStopSearch").val();
    var direction = $("#Direction").val();
    var csrf = $("#Direction").attr('csrf-token');
    $.ajax({
        type: 'POST',
        url: "selectedEndStationInfo/",
        data: {
            routeName: routeName,
            direction: direction,
            csrfmiddlewaretoken: csrf
        },
        success: function(data) {
            var newID = parseInt(id);
            var end = data.indexOf(newID);
            for (i = end; i < data.length; i++) {
                //https://stackoverflow.com/questions/24909907/disable-options-based-on-previous-selects
                $("#StartStop").find("option[value='" + data[i] + "']").prop("disabled", true);
            }
        }
    });
});

$(document).on("change", "#leaveTime", function() {
    // AJAX call to pass the value for the leave time to the prediction 
    var value = $("#leaveTime").val();
    var d = new Date();
    var today = d.toLocaleDateString();
    d.setDate(d.getDate() + 5);
    var Fivedays = d.toLocaleDateString();
    console.log(value);
    if (value == 1 || value == 2) {
        $('#picker').show();
    } else if (value == 0 || value == 3) {
        $('#picker').hide();
    }
});
$(document).on("change", "#leaveTimeStop", function() {
    var value = $("#leaveTimeStop").val();
    var d = new Date();
    var today = d.toLocaleDateString();
    d.setDate(d.getDate() + 5);
    var Fivedays = d.toLocaleDateString();
    if (value == 1 || value == 2) {
        $('#picker2').show();
    } else if (value == 0 || value == 3) {
        $('#picker2').hide();
    }
});

// Function to open the sidebar nav when the menu button is clicked 
function openNav() {
    var sideNav = document.getElementById("mySidenav");
    var main = document.getElementById("main");
    var map = document.getElementById('map');
    if (sideNav.style.width == "27%" || sideNav.style.width == "100%") {
        sideNav.style.width = "0";
        sideNav.style.padding = "0";
        main.style.marginLeft = "0";
        main.style.paddingLeft = "0"
        map.style.marginLeft = "0";
    } else if (window.innerWidth <= 1000 && window.innerHeight <= 900) {
        sideNav.style.width = "100%";
    } else {
        sideNav.style.width = "27%";
        main.style.marginLeft = "27%";
        main.style.paddingLeft = "2%"
        map.style.marginLeft = "27%";
    }
}


// Displays a simple map of Dublin with no markers
function displayMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 53.3498053,
            lng: -6.260309699999993
        },
        zoom: 13
    });

    // Autocomplete functionality for starting destination in search by address tab 
    function initialize_origin() {

        var circle = new google.maps.Circle({
                center: {
            lat: 53.3498053,
            lng: -6.260309699999993
        },
                radius: 3000
        });
        var input = document.getElementById('searchOrigin');
        var autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.setBounds(circle.getBounds());

        // Centre on selected location on map
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();
            console.log(place);
            if (place == undefined) {
                alert("Oops! Place not found. Please try again.");
            }
            document.getElementById('searchOrigin').value = place.name
            document.getElementById('searchOrigin').name = place.place_id
        });
    }

    // Autocomplete functionality for end stop destination in search by address tab
    function initialize_destination() {
            var circle = new google.maps.Circle({
                center: {
            lat: 53.3498053,
            lng: -6.260309699999993
        },
                radius: 3000
        });

        var input = document.getElementById('searchDest');
        var autocomplete = new google.maps.places.Autocomplete(input);
        autocomplete.setBounds(circle.getBounds());

        // Centre on selected location on map
        google.maps.event.addListener(autocomplete, 'place_changed', function() {
            var place = autocomplete.getPlace();
            if (place == undefined) {
                alert("Oops! Place not found. Please try again.");
            }
            document.getElementById('searchDest').value = place.name
            document.getElementById('searchDest').name = place.place_id
        });
    }

    // Invoking the autocomplete functions
    initialize_origin();
    initialize_destination();

}
var map;
var markerArray = [];


// Function to display markers for a bus route on the map when the direction is selected

function displayMarkers(locationList) {
    console.log(locationList)
    while (markerArray.length) {
        var markerToRemove = markerArray.pop();
        markerToRemove.setMap(null);
    }
    var myLatLng = {
        lat: 53.3498,
        lng: -6.2603
    };
    var infowindow = new google.maps.InfoWindow;
    var stopMarkers = "../../static/DublinBusTest/images/DublinBusMarkerIcon.png"
    var marker, i;

    for (i = 0; i < locationList.length; i++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locationList[i].lat, locationList[i].lon),
            map: map,
            icon: stopMarkers
        });
        markerArray.push(marker);
        var csrf = $("#Direction").attr('csrf-token');
        google.maps.event.addListener(marker, 'click', (function(marker, locationList, i) {
            // Displays the real time info when the marker is clicked 
            return function() {
                infowindow.close();
                $.ajax({
                    type: 'POST',
                    url: 'realTimeInfo/',
                    data: {
                        stopId: locationList[i].id,
                        stopName: locationList[i].name,
                        csrfmiddlewaretoken: csrf
                    },
                    success: function(data) {
                        infowindow.setContent(data);
                    }
                });
                map.setCenter(marker.getPosition());
                map.setZoom(16);
                infowindow.open(map, marker);
            }
        })(marker, locationList, i));
        marker.addListener('dblclick', function() {
            map.setZoom(13);
            map.setCenter({
                lat: 53.3498053,
                lng: -6.260309699999993
            });
        });
    }
}

// Jquery date and time picker function (modal)
(function($) {
    'use strict';
    $.fn.dateTimePicker = function(options) {

        var settings = $.extend({
            selectData: "now",
            dateFormat: "DD/MM/YYYY HH:mm",
            showTime: true,
            locale: 'en',
            positionShift: {
                top: 20,
                left: 0
            },
            title: "Select Date and Time",
            buttonTitle: "Select"
        }, options);
        moment.locale(settings.locale);
        var elem = this;
        var limitation = {
            "hour": 23,
            "minute": 59
        };
        var mousedown = false;
        var timeout = 800;
        var selectDate = settings.selectData == "now" ? moment() : moment(settings.selectData, settings.dateFormat);
        if (selectDate < moment()) {
            selectDate = moment();
        }
        var startDate = copyDate(moment());
        var lastSelected = copyDate(selectDate);
        return this.each(function() {
            if (lastSelected != selectDate) {
                selectDate = copyDate(lastSelected);
            }
            elem.addClass("dtp_main");
            updateMainElemGlobal();
            //  elem.text(selectDate.format(settings.dateFormat));
            function updateMainElemGlobal() {
                var arrF = settings.dateFormat.split(' ');
                if (settings.showTime && arrF.length != 2) {
                    arrF.length = 2;
                    arrF[0] = 'DD/MM/YY';
                    arrF[1] = 'HH:mm';
                }
                var $s = $('<span>');
                $s.text(lastSelected.format(arrF[0]));
                elem.empty();
                elem.append($s);
                $s = $('<i>');
                $s.addClass('fa fa-calendar ico-size');
                elem.append($s);
                $s = $('<span>');
                $s.text(lastSelected.format(arrF[1]));
                elem.append($s);
                $s = $('<i>');
                $s.addClass('fa fa-clock-o ico-size');
                elem.append($s);
            }

            elem.on('click', function() {
                var $win = $('<div>');
                $win.addClass("dtp_modal-win");
                var $body = $('body');
                $body.append($win);
                var $content = createContent();
                $body.append($content);
                var offset = elem.offset();
                $content.css({
                    top: (offset.top + settings.positionShift.top) + "px",
                    left: (offset.left + settings.positionShift.left) + "px"
                });
                feelDates(selectDate);
                $win.on('click', function() {
                    $content.remove();
                    $win.remove();
                })
                if (settings.showTime) {
                    attachChangeTime();
                    var $fieldTime = $('#field-time');
                    var $hour = $fieldTime.find('#d-hh');
                    var $minute = $fieldTime.find('#d-mm');
                }

                function feelDates(selectM) {
                    var $fDate = $content.find('#field-data');
                    $fDate.empty();
                    $fDate.append(createMonthPanel(selectM));
                    $fDate.append(createCalendar(selectM));
                }

                function createCalendar(selectedMonth) {
                    var $c = $('<div>');
                    $c.addClass('dtp_modal-calendar');
                    for (var i = 0; i < 7; i++) {
                        var $e = $('<div>');
                        $e.addClass('dtp_modal-calendar-cell dtp_modal-colored');
                        $e.text(moment().weekday(i).format('ddd'));
                        $c.append($e);
                    }
                    var m = copyDate(selectedMonth);
                    m.date(1);
                    // console.log(m.format('DD--MM--YYYY'));
                    // console.log(selectData.format('DD--MM--YYYY'));
                    // console.log(m.weekday());
                    var flagStart = totalMonths(selectedMonth) === totalMonths(startDate);
                    var flagSelect = totalMonths(lastSelected) === totalMonths(selectedMonth);
                    var cerDay = parseInt(selectedMonth.format('D'));
                    var dayNow = parseInt(startDate.format('D'));
                    var d = new Date();
                    //                    d.setDate(d.getDate() + 5); 
                    //                    var lim = d.toLocaleDateString();
                    for (var i = 0; i < 6; i++) {
                        for (var j = 0; j < 7; j++) {
                            var $b = $('<div>');
                            $b.html('&nbsp;');
                            $b.addClass('dtp_modal-calendar-cell');
                            if (m.month() == selectedMonth.month() && m.weekday() == j) {
                                var day = parseInt(m.format('D'));
                                $b.text(day);
                                if (flagStart && day < dayNow || flagStart && day > dayNow + 5) {
                                    $b.addClass('dtp_modal-grey');
                                } else if (flagSelect && day == cerDay) {
                                    $b.addClass('dtp_modal-cell-selected');
                                } else {
                                    $b.addClass('cursorily');
                                    $b.bind('click', changeDate);
                                }
                                m.add(1, 'days');
                            }
                            $c.append($b);
                        }
                    }
                    return $c;
                }

                function changeDate() {
                    // Function to allow the user to change the date 
                    var $div = $(this);
                    selectDate.date($div.text());
                    lastSelected = copyDate(selectDate);
                    updateDate();
                    var $fDate = $content.find('#field-data');
                    var old = $fDate.find('.dtp_modal-cell-selected');
                    old.removeClass('dtp_modal-cell-selected');
                    old.addClass('cursorily');
                    $div.addClass('dtp_modal-cell-selected');
                    $div.removeClass('cursorily');
                    old.bind('click', changeDate);
                    $div.unbind('click');
                    // console.log(selectDate.format('DD-MM-YYYY'));
                }

                function createMonthPanel(selectMonth) {
                    // Function to create a div to display a month 
                    var $d = $('<div>');
                    $d.addClass('dtp_modal-months');
                    var $s = $('<i></i>');
                    $s.addClass('fa fa-angle-left cursorily ico-size-month hov');
                    //$s.attr('data-fa-mask', 'fas fa-circle');
                    $s.bind('click', prevMonth);
                    $d.append($s);
                    $s = $('<span>');
                    $s.text(selectMonth.format("MMMM YYYY"));
                    $d.append($s);
                    $s = $('<i></i>');
                    $s.addClass('fa fa-angle-right cursorily ico-size-month hov');
                    $s.bind('click', nextMonth);
                    $d.append($s);
                    return $d;
                }

                function nextMonth() {
                    // Function to change to the next month
                    selectDate.add(1, 'month');
                    feelDates(selectDate);
                }

                function prevMonth() {
                    // Function to go back to the previous month 
                    if (totalMonths(selectDate) > totalMonths(startDate)) {
                        selectDate.add(-1, 'month');
                        feelDates(selectDate);
                    }
                }

                function close() {
                    // Function to reset content and close the date/time picker 
                    lastSelected.hour(parseInt($hour.text()));
                    lastSelected.minute(parseInt($minute.text()));
                    selectDate.hour(parseInt($hour.text()));
                    selectDate.minute(parseInt($minute.text()));
                    updateDate();
                    $content.remove();
                    $win.remove();
                }

                function attachChangeTime() {
                    // Allows time change by scrolling 
                    var $angles = $($content).find('i[id^="angle-"]');
                    $angles.bind('mouseup', function() {
                        mousedown = false;
                        timeout = 800;
                    });
                    $angles.bind('mousedown', function() {
                        mousedown = true;
                        changeTime(this);
                    });
                }

                function changeTime(el) {
                    var $el = this || el;
                    $el = $($el);
                    ///angle-up-hour angle-up-minute angle-down-hour angle-down-minute
                    var arr = $el.attr('id').split('-');
                    var increment = 1;
                    if (arr[1] == 'down') {
                        increment = -1;
                    }
                    appendIncrement(arr[2], increment);
                    setTimeout(function() {
                        autoIncrement($el);
                    }, timeout);
                }

                function autoIncrement(el) {
                    if (mousedown) {
                        if (timeout > 200) {
                            timeout -= 200;
                        }
                        changeTime(el);
                    }
                }

                function appendIncrement(typeDigits, increment) {

                    var $i = typeDigits == "hour" ? $hour : $minute;
                    var val = parseInt($i.text()) + increment;
                    if (val < 0) {
                        val = limitation[typeDigits];
                    } else if (val > limitation[typeDigits]) {
                        val = 0;
                    }
                    $i.text(formatDigits(val));
                }

                function formatDigits(val) {

                    if (val < 10) {
                        return '0' + val;
                    }
                    return val;
                }

                function createTimer() {
                    var $div = $('<div>');
                    $div.addClass('dtp_modal-time-mechanic');
                    var $panel = $('<div>');
                    $panel.addClass('dtp_modal-append');
                    var $i = $('<i>');
                    $i.attr('id', 'angle-up-hour');
                    $i.addClass('fa fa-angle-up ico-size-large cursorily hov');
                    $panel.append($i);
                    var $m = $('<span>');
                    $m.addClass('dtp_modal-midle');
                    $panel.append($m);
                    $i = $('<i>');
                    $i.attr('id', 'angle-up-minute');
                    $i.addClass('fa fa-angle-up ico-size-large cursorily hov');
                    $panel.append($i);
                    $div.append($panel);

                    $panel = $('<div>');
                    $panel.addClass('dtp_modal-digits');
                    var $d = $('<span>');
                    $d.addClass('dtp_modal-digit');
                    $d.attr('id', 'd-hh');
                    $d.text(lastSelected.format('HH'));
                    $panel.append($d);
                    $m = $('<span>');
                    $m.addClass('dtp_modal-midle-dig');
                    $m.html(':');
                    $panel.append($m);
                    $d = $('<span>');
                    $d.addClass('dtp_modal-digit');
                    $d.attr('id', 'd-mm');
                    $d.text(lastSelected.format('mm'));
                    $panel.append($d);
                    $div.append($panel);

                    $panel = $('<div>');
                    $panel.addClass('dtp_modal-append');
                    $i = $('<i>');
                    $i.attr('id', 'angle-down-hour');
                    $i.addClass('fa fa-angle-down ico-size-large cursorily hov');
                    $panel.append($i);
                    $m = $('<span>');
                    $m.addClass('dtp_modal-midle');
                    $panel.append($m);
                    $i = $('<i>');
                    $i.attr('id', 'angle-down-minute');
                    $i.addClass('fa fa-angle-down ico-size-large cursorily hov');
                    $panel.append($i);
                    $div.append($panel);
                    return $div;
                }

                function createContent() {
                    var $c = $('<div>');
                    $c.addClass("dtp_modal-content");
                    var $el = $('<div>');
                    $el.addClass("dtp_modal-title");
                    $el.text(settings.title);
                    $c.append($el);
                    $el = $('<div>');
                    $el.addClass('dtp_modal-cell-date');
                    $el.attr('id', 'field-data');
                    $c.append($el);
                    $el = $('<div>');
                    $el.addClass('dtp_modal-cell-time');
                    var $a = $('<div>');
                    $a.addClass('dtp_modal-time-block');
                    $a.attr('id', 'field-time');
                    $el.append($a);
                    var $line = $('<div>');
                    $line.attr('id', 'time-line');
                    $line.addClass('dtp_modal-time-line');
                    $line.text(lastSelected.format(settings.dateFormat));
                    $a.append($line);
                    $a.append(createTimer());
                    var $but = $('<div>');
                    $but.addClass('dpt_modal-button');
                    $but.text(settings.buttonTitle);
                    $but.bind('click', close);
                    $el.append($but);
                    $c.append($el);
                    return $c;
                }

                function updateDate() {
                    $('#time-line').text(lastSelected.format(settings.dateFormat));
                    updateMainElem();
                    elem.next().val(selectDate.format(settings.dateFormat));
                }

                function updateMainElem() {
                    var arrF = settings.dateFormat.split(' ');
                    if (arrF.length != 2) {
                        arrF.length = 2;
                        arrF[0] = 'DD/MM/YY';
                        arrF[1] = 'HH:mm';
                    } else {
                        var $s = $('<span>');
                        $s.text(lastSelected.format(arrF[0]));
                        elem.empty();
                        elem.append($s);
                        $s = $('<i>');
                        $s.addClass('fa fa-calendar ico-size');
                        elem.append($s);
                        $s = $('<span>');
                        $s.text(lastSelected.format(arrF[1]));
                        console.log($s[0].innerHTML);
                        if ($s[0].innerHTML > "23:45" || $s[0].innerHTML < "06:45") {
                            alert("Buses not running between these hours, please try another time");
                        }
                        elem.append($s);
                        $s = $('<i>');
                        $s.addClass('fa fa-clock-o ico-size');
                        elem.append($s);
                    }
                }
            });

        });

    };

    function copyDate(d) {
        return moment(d.toDate());
    }

    function totalMonths(m) {
        var r = m.format('YYYY') * 12 + parseInt(m.format('MM'));
        return r;
    }

}(jQuery));
// fa-caret-down

function closeNav() {
    // Functiont to close the side nav when button is clicked 
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("mySidenav").style.padding = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.getElementById("main").style.paddingLeft = "0";
    document.getElementById("map").style.marginLeft = "0";
}

function startTime() {
    // Function to display date and time on webpage 
    var today = new Date();
    var date = today.toDateString();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('Time').innerHTML = date + " " + h + ":" + m + ":" + s;
    var t = setTimeout(startTime, 500);
}

function checkTime(i) {
        if (i < 10) {
            i = "0" + i
        }; // add zero in front of numbers < 10
        return i;
    }
    //Show directions from start to finish
function showDirectionsMap(startLat, startLong, endLat, endLong) {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: {
            lat: 53.3498053,
            lng: -6.260309699999993
        }
    });
    var lat = [startLat, endLat];
    var long = [startLong, endLong];
    for (var i = 0; i < 2; i++) {
        var journeyMarker = new google.maps.Marker({
            position: {
                lat: parseFloat(lat[i]),
                lng: parseFloat(long[i])
            },
        });
        directionsDisplay.setMap(map);
        var origin = [startLat, startLong],
            destination = [endLat, endLong];
        calculateAndDisplayRoute(directionsService, directionsDisplay, origin, destination);
    };
}

//Function that calculates distances between two points
function calculateAndDisplayRoute(directionsService, directionsDisplay, origin, destination) {
    directionsService.route({
        origin: {
            lat: parseFloat(origin[0]),
            lng: parseFloat(origin[1])
        },
        destination: {
            lat: parseFloat(destination[0]),
            lng: parseFloat(destination[1])
        },
        travelMode: 'TRANSIT'
    }, function(response, status) {
        directionsDisplay.setDirections(response);
    });
}

function swapLocation() {
    // Function to allow the user to swap direction when searching by address 
    var oldStart = document.getElementById('searchOrigin');
    var oldEnd = document.getElementById('searchDest');
    var oldStartValue = oldStart.value;
    var oldStartName = oldStart.name;
    var oldEndValue = oldEnd.value;
    var oldEndName = oldEnd.name;
    oldStart.value = oldEndValue;
    oldStart.name = oldEndName;
    oldEnd.value = oldStartValue;
    oldEnd.name = oldEndName;
}

function showDetailedJourney() {
    $("#journeyBreakdown").show();
}