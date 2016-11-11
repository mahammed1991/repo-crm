// Global variables
window.failedFields = new Array();
window.is_error = false;

var resetTimeline = function(){
    $("#steps").hide();
    $('.circle').each(function() {
        $(this).css('background','#EEECEB');
    });
    $('.steps-timeline > div > h3').each(function() {
        $(this).text("");
    });
    $('upload-status').text("Uploading..");
}


var handleBrowseClick = function(){
    var fileInput = document.getElementById("attachment_name");
    fileInput.click();
}


var handleChange = function(){
    $("#status").empty();
    var file = document.getElementById("attachment_name");
    var textInput = document.getElementById("filename");
    textInput.value = file.value;
    if(validateExtension(textInput.value)){
        validateFileSize(file)
    }
}


var validateExtension = function(UploadFileName) {
    $("#status").empty();
    var allowedFiles = [".csv"];
    var errState = document.getElementById("status");
    var regex = new RegExp("([a-zA-Z0-9\s_\\.\-:()])+(" + allowedFiles.join('|') + ")$");
    if (!regex.test(UploadFileName.toLowerCase())) {
        $("#file_submit").prop("disabled",true);
        errState.innerHTML = "<div class='alert alert-warning'><a id='errAlert'  href='#' class='close' data-dismiss='alert'\
                             aria-label='close'>&times;</a> Please upload files only with extension<b>" + allowedFiles.join(', ') + "</b></div>";
        return false;
    }
    $("#file_submit").prop("disabled",false);
    return true;
}


var validateFileSize = function(element){
    $("#status").empty();
    var maxAllowedFileSize = 2; // 2 MB
    var errState = document.getElementById("status");
    if (element.files[0].size > 1024 * 1024 * maxAllowedFileSize)
    {
        $("#file_submit").prop("disabled",true);
        errState.innerHTML = "<div class='alert alert-danger'><a id='errAlert' href='#' class='close' data-dismiss='alert' \
                             aria-label='close'>&times;</a> Max file upload size is <b>" + maxAllowedFileSize+ " MB</b>.</div>";
        return true;
    }
    $("#file_submit").prop("disabled",false);
    return false;
}

var progressHandlingFunction = function(e){
    if(e.lengthComputable){
        var percent = (e.loaded / e.total) * 100;
        if(percent == 100){
            $(".steps-one > div").css('background','#4CAF50');
            $(".steps-one > h3").text("Uploaded");
            $(".steps-two > div").css('background','#0062B7');
            $(".steps-two > h3").text("Processing..");
        }
    }
}

var validateFormFields = function(repName, repEmail, repTeam, managerName, managerEmail, ldap){
    // Validate mandatory fields and format
    var emailRegex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    valid = true;
    if(repName.val() === ""){
        repName.addClass('error-box');
        valid = false;
    }else
        repName.removeClass('error-box');

    if(repEmail.val() === ""){
        repEmail.addClass('error-box');
        valid = false;
    }else{
        // Validate Email
        email_valid = validateEmailFormat(repEmail, emailRegex)
        if(email_valid)
            repEmail.removeClass('error-box');
        else{
            valid = false;
            repEmail.addClass('error-box');
        }
    }

    if(repTeam.val() === ""){
        repTeam.addClass('error-box');
        valid = false;
    }else
        repTeam.removeClass('error-box');

    if(managerName.val() === ""){
        managerName.addClass('error-box');
        valid = false;
    }else
        managerName.removeClass('error-box');

    if(managerEmail.val() === ""){
        managerEmail.addClass('error-box');
        valid = false;
    }else{
        // Validate Email
        email_valid = validateEmailFormat(managerEmail, emailRegex)
        if(email_valid)
            managerEmail.removeClass('error-box');
        else{
            valid = false;
            managerEmail.addClass('error-box');
        }
    }

    if(ldap.val() !== ""){
        // Validate Email
        email_valid = validateEmailFormat(ldap, emailRegex)
        if(email_valid)
            ldap.removeClass('error-box');
        else{
            valid = false;
            ldap.addClass('error-box');
        }

    }else
        ldap.removeClass('error-box');

    return valid;
}

function validateEmailFormat(elem, regex) {
  // Validate Email Field
  if (!$(elem).val().trim().match(regex)) {
      $(elem).addClass('error-box');
      window.failedFields.push(elem);
      window.is_error = true;
      return false;
    }
    return true;
}

var clearAttachment = function(){
    $("#attachment_name").val("");
    $("#filename").val("");
}