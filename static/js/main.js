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


});
// Olark Hide For WPP Domain Starts Here
    var wpp_index = window.location.href.indexOf('wpp')
    if (wpp_index === -1) {
        olark('api.box.show');
    } else {
        olark('api.box.hide');
    }
// Olark Hide For WPP Domain Ends Here



// Report a bug javascript
function showOlark(){
  olark('api.box.show');
}
    function hideOlark(){
      olark('api.box.hide');
    }
  function HandleBrowseClick()
{
    var fileinput = document.getElementById("attachmentfile");
    fileinput.click();
}

function Handlechange()
{
    var fileinput = document.getElementById("attachmentfile");
    var textinput = document.getElementById("filename");
    textinput.value = fileinput.value;
}


$('#portalFeedback').submit(function(event){
  event.preventDefault();
  $(".error-box").removeClass('error-box');
    var feedbackType = $('#bugfeedbackType').val();
    var comments = $('#bugcomments').val();
   if(feedbackType === 'Feedback Type'){
      $('#bugfeedbackType').addClass('error-box');
      return false;
    }else if(comments === ''){
      $('#bugcomments').addClass('error-box');
      return false;
    }else{
      var formData = new FormData($('#portalFeedback')[0]);
        $('.footeroverlay').show();
        $.ajax({
            url: '/main/report-a-bug/',
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                $('.footeroverlay').hide();
                $('.close-modal').trigger('click');
                $("#feedbackType").val("Feedback Type");
                $("#comments").val("");
                $("#attachmentfile").val("");
                $("#filename").val("");
                showOlark();
                $('#bugreported').modal('show');
            },
            error: function (error) {
                $('.footeroverlay').hide();
                console.log(error);
            }
        });

    }
    return false;
});

// Report a bug javascript ends

// clearing bug window after done 
$("#closing").click(function(){
    $('#bugfeedbackType').prop('selectedIndex',0);
    $('#bugcomments').val('');
    $('#filename').val('');
});

$("#bug-noti-close").click(function(){
    $('#bugfeedbackType').prop('selectedIndex',0);
    $('#bugcomments').val('');
    $('#filename').val('');
});

$("#bug-cls-btn").click(function(){
    $('#bugfeedbackType').prop('selectedIndex',0);
    $('#bugcomments').val('');
    $('#filename').val('');
});
//end clearing bug window after done 






