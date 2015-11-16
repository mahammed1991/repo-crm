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

    t_typeElem = document.getElementById('treatment_type')
    validateFiled(t_typeElem)
    
    // Google Rep Name Validation
    grefElem = document.getElementById('gref');
    validateFiled(grefElem);

    teamElem = document.getElementById('team');
    validateFiled(teamElem);

    cidElem = document.getElementById('cid');
    validateFiled(cidElem);

    if(!$(cidElem).val().match(cidFormat)){
      $(cidElem).addClass('error-box');
      /*frm.cid.focus();*/
      window.is_error = true;
    }

    urlElem = document.getElementById('url');
    validateFiled(urlElem);

    countryElem = document.getElementById('country');
    validateFiled(countryElem);

    cgoalElem = document.getElementById('conversion_goal');
    validateFiled(cgoalElem);

    ab_testing = document.getElementById('ab_testing');
    validateFiled(ab_testing);
    
    fnameElem = document.getElementById('first_name');
    validateFiled(fnameElem);

    lnameElem = document.getElementById('last_name');
    validateFiled(lnameElem);

    aemailElem = document.getElementById('wpp_aemail');
    validateFiled(aemailElem);
    $("#aemail").val(aemailElem.value);

    validateEmailField(aemailElem)

    phoneElem = document.getElementById('phone');
    validateFiled(phoneElem);

    roleElem = document.getElementById('advertiser_role1');
    validateFiled(roleElem);

    roleOther = document.getElementById('role_other1');
    if($(roleOther).is(":visible")){
      validateFiled(roleOther);
    }


    //advertiser_details

    for(i=2; i<4; i++){

        advertiserDetails = document.getElementById('advertiser_details'+i);
        if($(advertiserDetails).is(":visible")){


        fnameElemAdditional = document.getElementById('first_name'+i);
        validateFiled(fnameElemAdditional);

        lnameElemAdditional = document.getElementById('last_name'+i);
        validateFiled(lnameElemAdditional);

        aemailElemAdditional = document.getElementById('wpp_aemail'+i);
        validateFiled(aemailElemAdditional);

        validateEmailField(aemailElemAdditional)

        phoneElemAdditional = document.getElementById('phone'+i);
        validateFiled(phoneElemAdditional);

        roleElemAdditional = document.getElementById('advertiser_role'+i);
        validateFiled(roleElemAdditional);

        roleOtherAdditional = document.getElementById('role_other'+i);
        if($(roleOtherAdditional).is(":visible")){
          validateFiled(roleOtherAdditional);
        }
      }
    }

   

    tzoneElem = document.getElementById('tzone');
    validateFiled(tzoneElem);


    // Appointments Date and Time Validation
    tagDateElem = document.getElementById('tag_datepick');
    if ($(tagDateElem).val() == "" || $(tagDateElem).val() == "0" || !$(tagDateElem).val()) {
        $(tagDateElem).addClass('error-box');
        window.is_error = true;
        return false;
      }
    // validateFiled(tagDateElem);

    if(tagDateElem.value){
        var slot = {
        'type' : 'WPP',
        'time' : tagDateElem.value
        }
        fix_slots.push(slot)
      }

    // Check If Error in Form
    if(window.is_error){
      focusElem = failedFields[0];
      $(focusElem).focus();
      return false;
    }else{

      var url = $(urlElem).val();
      $("#company").val(url);
      var status = true;

      //updating Advertiser2 details to Advertaiser Optional
      $('#fopt').val($('#first_name2').val());
      $('#lopt').val($('#last_name2').val());
      /*$('#web_master_email').val($('#wpp_aemail2'));
      $('#popt').val($('#phone2'));*/

      if (fix_slots.length) {
        status = check_and_create_appointment(fix_slots);
      }
      if (status) {
        if(window.tz_name){
            console.log(window.tz_name);
            $("#tzone").append("<option value=" + window.tz_name + "></option>").val(window.tz_name)
        }
        $('#preloaderOverlay').show();
        $('form input[type=submit]').attr('disabled', 'disabled');
      }
      return status;  
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