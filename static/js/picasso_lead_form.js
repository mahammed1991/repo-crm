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
    var emailFormat = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i; 
    window.failedFields = new Array();
    var fix_slots = new Array();
    $('#display_url_has_space').hide();
    $('#display_url_has_comma').hide();
    $('#display_invalid_url').hide();
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

    validateCorpEmail();
    validateCheckBox();
    validateCasesAliasInput();
    validateAvertiserEmailInput();
    removeCasesErrorClass();
    removeAdvertiserErrorClass();

    validateEmailField($('#cases_alias'));
    validateEmailField($('#advertiser_email'));

    if(!$(cidElem).val().match(cidFormat)){
      $(cidElem).addClass('error-box');
      /*frm.cid.focus();*/
      window.is_error = true;
    }

    if($('#install_mobile_app').prop("checked") || $('#drive_foot_traffic').prop("checked") || $('#buy_online').prop("checked") || $('#form_entry').prop("checked") || $('#call_your_business').prop("checked") || $('#engage_with_your_content').prop("checked") || $('#become_a_fan').prop("checked")){
      $('.checkboxvalidation').removeClass('error-box');
      $('#display_error_for_objective').hide();

    }else{
      $('#display_error_for_objective').show();
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


$('#team').change(function(){

      $('#Picasso input[type="checkbox"]').attr('disabled', false);
      var checked_elements = $('.is-checked');
      for(var i=0;i<checked_elements.length;i++)
      {
        $(checked_elements[i]).trigger('click');
      }
      if ($(this).find('option:selected').attr("class") == 'A'){
        $('#checkbox3').trigger('click').attr('disabled', true);
      }
      else if ($(this).find('option:selected').attr("class") == 'B'){
      }
      else{
        $('#checkbox3').trigger('click').attr('disabled', true);
      }

  });


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
              if(check){
                        // alert("URL contains space");
                        $('#display_url_has_space').show(); 
                        window.failedFields.push(Elementurl);
                        $("#url").addClass('error-box');
                        window.is_error = true;
                        return false;}
              if(!check){/*alert("valid with no space url");*/
                          string = url
                          re = new RegExp(/,\s*/);
                          var check_coma = re.test(string);
                          if (check_coma){
                                  $('#display_url_has_comma').show();
                                  // alert("URL contains comma");
                                  window.failedFields.push(Elementurl);
                                  $("#url").addClass('error-box');
                                  window.is_error = true;
                                  return false;
                                  }
                          $("#url").removeClass('error-box');
                          return true} 
          }
        else {
               $('#display_invalid_url').show();
               $("#url").addClass('error-box'); 
                window.is_error = true;
                window.failedFields.push(Elementurl);
                return false;}
  } else {  /*alert("Valid Url!");*/
            string = url
            re = new RegExp(/,\s*/);
            var check_coma = re.test(string);
            if (check_coma){
                    $('#display_url_has_comma').show();
                    // alert("URL contains comma");
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
  if($(elem).val()){
    if (!$(elem).val().trim().match(check)) {
      $(elem).addClass('error-box');
      /*$(elem).focus();*/
      window.is_error = true;
      $('#display_error_for_email_fields').show();
      return false;
    }
    else{
      $('#display_error_for_email_fields').hide();
      return true;
    }
  }
}

function resetBtn(elem){
  elemId = $(elem).attr('id');
  if(elemId == 'formReset'){
    window.is_reset = true;
    window.location.reload();
  }
}


function validateCorpEmail()
{
  var corp_email_checkbox = $('#checkbox11').attr('class');
  if(corp_email_checkbox.search('is-checked') == -1){
      $('#checkbox11 .mdl-checkbox__ripple-container').addClass('error-box');
      window.is_error = true;
      return false;
  }
  else{
    $('#checkbox11 .mdl-checkbox__ripple-container').removeClass('error-box');
      window.is_error = false;
      return true;
  }
}

function validateCheckBox()
{
  var cases_alias_checkbox = $('#checkbox22').attr('class');
  var advertiser_email_checkbox = $('#checkbox33').attr('class');
  if(cases_alias_checkbox.search('is-checked') != -1){
      var cases_alias = document.getElementById('cases_alias');
      validateFiled(cases_alias);
  }
  if(advertiser_email_checkbox.search('is-checked') != -1){
      var advertiser_email = document.getElementById('advertiser_email');
      validateFiled(advertiser_email);
  }
}


function validateCasesAliasInput()
{
  if($('#cases_alias').val()){
    var cases_alias_checkbox = $('#checkbox22').attr('class');
    if(cases_alias_checkbox.search('is-checked') == -1){
        $('#checkbox22 .mdl-checkbox__ripple-container').addClass('error-box');
        window.is_error = true;
        return false;
    }
  }
  else{
    $('#checkbox22 .mdl-checkbox__ripple-container').removeClass('error-box');
      window.is_error = false;
      return true;
  }
}

function validateAvertiserEmailInput()
{
  if($('#advertiser_email').val()){
    var advertiser_email_checkbox = $('#checkbox33').attr('class');
    if(advertiser_email_checkbox.search('is-checked') == -1){
        $('#checkbox33 .mdl-checkbox__ripple-container').addClass('error-box');
        window.is_error = true;
        return false;
    }
  }
  else{
      $('#checkbox33 .mdl-checkbox__ripple-container').removeClass('error-box');
        window.is_error = false;
        return true;
  }
}


function removeCasesErrorClass()
{
  var cases_alias_checkbox = $('#checkbox22').attr('class');
  if($('#cases_alias').val() && cases_alias_checkbox.search('is-checked') != -1){
     $('#checkbox22 .mdl-checkbox__ripple-container').removeClass('error-box');
      window.is_error = false;
      return true;
  }
}

function removeAdvertiserErrorClass()
{
  var advertiser_email_checkbox = $('#checkbox33').attr('class');
  if($('#advertiser_email').val() && advertiser_email_checkbox.search('is-checked') != -1){
     $('#checkbox33 .mdl-checkbox__ripple-container').removeClass('error-box');
      window.is_error = false;
      return true;
  }
}

$("#picasso").click(function(){
 $('#ctype1').val('PICASSO');
 $('.tab-content').css("background-color","#ccddff");
});

$("#bolt").click(function(){
$('#ctype1').val('BOLT');
$('.tab-content').css("background-color","#b1e7bf");
});

