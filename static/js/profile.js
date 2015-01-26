$(document).ready(function(){
    if (window.loc_id){
        $("#user_location").val(window.loc_id);    
    }else{
        $("#user_location").val("");
    }

    if (window.team_id){
        $("#user_team").val(window.team_id);
    }else{
        $("#user_team").val("");
    }

    // Click on edit button on profile
    $("#profileEdit").click(function(){
        $(this).hide();
        $("#profileUpdate").show();
        $("#profileCancel").show();
        $(".allow-edit").removeClass('non-edit');
        $(".allow-edit").attr('disabled', false);
        return false;
    });

    // Click on cancel button on profile
    $("#profileCancel").click(function(){
        $(this).hide();
        $("#profileUpdate").hide();
        $("#profileEdit").show();
        $("#user_full_name").val("{{user.get_full_name}}");
        $("#user_phone").val("{{user.profile.phone}}");
        $("#user_team").val("{{user.profile.team.id}}");
        $("#user_manager_name").val("{{user.profile.user_manager_name}}");
        $("#user_manager_email").val("{{user.profile.user_manager_email}}");
        $("#user_location").val("{{user.profile.location.id}}");
        $(".allow-edit").addClass('non-edit');
        $(".allow-edit").attr('disabled', true);
        return false;
    });
});

function validateProfile(){
    // Remove all error messages
    $(".error-txt").remove();

    // Use Full Name Validation
    full_name = $("#user_full_name");
    if (full_name.val() == "") {
       $(full_name).addClass('error-box');
       // $(full_name).after('<span class="error-txt">Please Enter Full name</span>');
       $(full_name).focus();   
        return false;
    }

    // Phone Validation
    user_phone = $("#user_phone");
    if (user_phone.val() == "") {
       $(user_phone).addClass('error-box');
       // $(user_phone).after('<span class="error-txt">Please Enter Phone name</span>');
       $(user_phone).focus();   
        return false;
    }

    // Team Validation
    team_elem = $("#user_team");
    if (team_elem.val() == "") {
       $(team_elem).addClass('error-box');
       // $(team_elem).after('<span class="error-txt">Please choose Team name</span>');
       $(team_elem).focus();   
        return false;
    }

    // User Manager Name Validation
    name_elem = $("#user_manager_name");
    if (name_elem.val() == "") {
       $(name_elem).addClass('error-box');
       // $(name_elem).after('<span class="error-txt">Please enter Google Manager name</span>');
       $(name_elem).focus();   
        return false;
    }

    // User Manager Email Validation
    email_elem = $("#user_manager_email");
    if (email_elem.val() == "") {
       $(email_elem).addClass('error-box');
       // $(email_elem).after('<span class="error-txt">Please enter Google Manager Email ID</span>');
       $(email_elem).focus();   
        return false;
    }else{
        var error = true;
        if(email_elem.val().split('@')[1] == "regalix-inc.com") {
            var error = false;
        }
        if(error){
            if(email_elem.val().split('@')[1] == "google.com") {
                var error = false;
            }
        }

        if(error){
            $(email_elem).addClass('error-box');
            $(email_elem).after('<span class="error-txt">Please enter a valid regalix or google Email ID</span>');
            $(email_elem).focus();
            return false;
        }
    }

    // User Location Validation
    location_elem = $("#user_location");
    if (location_elem.val() == "") {
       $(location_elem).addClass('error-box');
       $(location_elem).after('<span class="error-txt">Please choose Location name</span>');
       $(location_elem).focus();   
        return false;
    } 
}