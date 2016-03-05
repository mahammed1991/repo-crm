function validatethis(frm) {
    $(".error-txt").remove();
    $(".lead-form .form-control").removeClass('error-box');
    $('.shopping-policy').removeClass('error-box');
    $('.web-access').removeClass('error-box');
    // var check = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var check = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var cidFormat = /^\d{3}-\d{3}-\d{4}$/;
    var phoneFormat = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    var numericExpression = /^[0-9]+$/;
    window.failedFields = new Array();
    var fix_slots = new Array();
    
    window.is_error = false;

    if(window.is_reset == true){
      window.is_reset = false;
      return false;
    }
    // Google Rep Name Validation
    grefElem = document.getElementById('gref');
    validateFiled(grefElem);

    cidElem = document.getElementById('cid');
    validateFiled(cidElem);

    if(!$(cidElem).val().match(cidFormat)){
      $(cidElem).addClass('error-box');
      /*frm.cid.focus();*/
      window.is_error = true;
    }

    if($('#install_mobile_app').prop("checked") || $('#drive_foot_traffic').prop("checked") || $('#buy_online').prop("checked") || $('#form_entry').prop("checked") || $('#call_your_business').prop("checked") || $('#engage_with_your_content').prop("checked") || $('#become_a_fan').prop("checked")){
      $('.checkboxvalidation').removeClass('error-box');

    }else{
      alert('Please select atleast one objective')
      $('.checkboxvalidation').addClass('error-box');
      window.is_error = true;
    }


     ValidateUrlField();


    podElem = document.getElementById('picasso_pod');
    validateFiled(podElem);


    teamElem = document.getElementById('team');
    validateFiled(teamElem);


    // Check If Error in Form
    if(window.is_error){
      focusElem = failedFields[0];
      $(focusElem).focus();
      return false;
    }else{
      $('#company').val($('#url').val());
      $('#preloaderOverlay').show();
      return true;
    }  
  }

  function validateFiled(elem){
    // Validate Form Field
    if ($(elem).val() == "" || $(elem).val() == "0" || !$(elem).val()) {
    $(elem).addClass('error-box');
    window.failedFields.push(elem);
    window.is_error = true;
    return false;
  }
}

function ValidateUrlField() {
  var regexp = new RegExp("^http(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?$");
    var url = document.getElementById("url").value;
    var Elementurl = document.getElementById("url");
    if (!regexp.test(url)) {
      var expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&/=]*)?/
      var regex = new RegExp(expression);
      var check_one_more = url;
        if (check_one_more.match(regex) )
          {   var inValid = /\s/;
              var value = url;
              var check = inValid.test(value);
              if(check){alert("URL contains space"); 
                        window.failedFields.push(Elementurl);
                        $("#url").addClass('error-box');
                        window.is_error = true;
                        return false;}
              if(!check){/*alert("valid with no space url");*/
                          string = url
                          re = new RegExp(/,\s*/);
                          var check_coma = re.test(string);
                          if (check_coma){
                                  alert("URL contains comma");
                                  window.failedFields.push(Elementurl);
                                  $("#url").addClass('error-box');
                                  window.is_error = true;
                                  return false;
                                  }
                          $("#url").removeClass('error-box');
                          return true} 
          }
        else {  alert("Invalid URL pattern");
               $("#url").addClass('error-box'); 
                window.is_error = true;
                window.failedFields.push(Elementurl);
                return false;}
  } else {  /*alert("Valid Url!");*/
            string = url
            re = new RegExp(/,\s*/);
            var check_coma = re.test(string);
            if (check_coma){
                    alert("URL contains comma");
                    window.failedFields.push(Elementurl);
                    $("#url").addClass('error-box');
                    window.is_error = true;
                    return false;
                    }
            $("#url").removeClass('error-box');
            return true; }
}


function validateEmailField(elem) {
  var check = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  // Validate Email Field
  if (!$(elem).val().trim().match(check)) {
      $(elem).addClass('error-box');
      /*$(elem).focus();*/
      window.is_error = true;
      return false;
    }
}

function resetBtn(elem){
  elemId = $(elem).attr('id');
  if(elemId == 'formReset'){
    window.is_reset = true;
    window.location.reload();
  }
}

