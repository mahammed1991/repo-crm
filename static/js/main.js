$(document).ready(function() {
    // getCurrentDomain();

    // table accordian
    $(".clickable").click(function() {
        $(this).find(".row-expand, .row-collapse").toggle();
    });

    $(".fa-bell").click(function() {
        $("#notifications_count").hide();
    });

    $(document).on('click', '.live-transfer-location', function(e) {
        phone_no = $(this).attr('data-phone');
        flag_url = $(this).attr('data-url');
        $("#loc_img").attr('src', flag_url);
        $(".location_number").text(phone_no);
    });

    // Get All Inbound Locations 
    $.ajax({
        url: "/main/get-inbound-locations",
        dataType: "json",
        type: 'GET',
        data: {},
        success: function(data) {
            displayLocations(data['location']);
            showUserLoc(data['user_loc']);
        },
        error: function(errorThrown) {
            console.log('failure');
        }
    });


    function displayLocations(locations) {
        elem = "";
        for (i = 0; i < locations.length; i++) {
            elem = '<li><a href="#" data-phone="' + locations[i]['phone'] + '" id="loc_' + locations[i]['id'] + '" class="live-transfer-location" data-url="' + locations[i]['url'] + '">' +
                '<img src="' + locations[i]['url'] + '"/>' + locations[i]['name'] + '</a>' +
                '</li>'
            $("#loc_list").append(elem);
        }

    }

    function showUserLoc(user_loc) {
        if (user_loc['loc_phone']) {
            $("#loc_img").attr("src", user_loc['loc_flag'])
            $(".location_number").text(user_loc['loc_phone'])
        }
    }

    // Get Notifications
    $.ajax({
        url: "/main/get-notifications",
        dataType: "json",
        type: 'GET',
        data: {},
        success: function(notifications) {
            setNotifications(notifications);
        },
        error: function(errorThrown) {
            console.log('failure');
        }
    });


    function setNotifications(notifications) {
        $("#notifications_count").text(notifications.length);
        //$("#marquee_notofication").html('');
        elem = "";
        for (i = 0; i < notifications.length; i++) {
            elem = '<li><a href="#">' + notifications[i]['text'] + '</a></li>'
            $("#notifications").append(elem);
            //$("#marquee_notofication").append("<div>" + notifications[i]['text'] + "</div>");
        }

    }


    var redirectDomain = $("#redirect_domain").val();
    if (redirectDomain == '') {
        getCurrentDomain();
    } else if ((redirectDomain == 'TAG' && window.location.href.indexOf('gtrack') != -1) || redirectDomain == 'WPP' && window.location.href.indexOf('wpp') != -1) {
        $("#getRedirectDomain").trigger('click');
    }

    function getCurrentDomain() {
        // Swap Domain name
        $.ajax({
            url: "/auth/current_domain",
            dataType: "json",
            type: 'GET',
            data: {},
            success: function(data) {
                if (data['change_url']) {
                    // window.location.assign(data['current_domain']);
                    location.replace(data['url_scheme'] + '://' + data['current_domain']);
                }
            },
            error: function(errorThrown) {
                console.log('failure');
            }
        });
    }

});
// Olark Hide For WPP Domain Starts Here
    /*var wpp_index = window.location.href.indexOf('wpp')
    if (wpp_index === -1) {
        olark('api.box.show');
    } else {
        olark('api.box.hide');
    }
*/
// Olark Hide For WPP Domain Ends Here