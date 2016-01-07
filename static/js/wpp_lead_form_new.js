function validatethis(frm) {
    $(".error-txt").remove();
    $(".lead-form .form-control").removeClass('error-box');
    $('.shopping-policy').removeClass('error-box');
    $('.web-access').removeClass('error-box');
    // var check = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var check = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var cidFormat = /^\d{3}-\d{3}-\d{4}$/;
    var cidFormatWithoutDashes = /^\d{10}$/;
    var phoneFormat = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    var numericExpression = /^[0-9]+$/;
    window.failedFields = new Array();
    var fix_slots = new Array();
    
    window.is_error = false;

    if(window.is_reset == true){
      window.is_reset = false;
      return false;
    }
  
    cidElem = document.getElementById('cid');
    validateFiled(cidElem);

     if($(cidElem).val().indexOf('-') == -1){
        if(!$(cidElem).val().match(cidFormatWithoutDashes)){
            $(cidElem).addClass('error-box');
            window.is_error = true;
          }
     } else{
        if(!$(cidElem).val().match(cidFormat)){
              $(cidElem).addClass('error-box');
              window.is_error = true;
            }
     }

    urlElem = document.getElementById('url');
    if ($('#url').is(':visible')){
      validateFiled(urlElem);
    }

    if ($('#multipleUrls').is(':visible')){
      multiUrlElem = document.getElementById('multipleUrls');
      validateFiled(multiUrlElem);
    }
    
    t_typeElem = document.getElementById('treatment_type')
    validateFiled(t_typeElem)

    grefElem = document.getElementById('gref');
    validateFiled(grefElem);

    teamElem = document.getElementById('team');
    validateFiled(teamElem);

    podElem = document.getElementById('picasso_pod');
    validateFiled(podElem);


     if($('#install_mobile_app').parent().hasClass('is-checked') || $('#drive_foot_traffic').parent().hasClass('is-checked') || $('#buy_online').parent().hasClass('is-checked') || $('#form_entry').parent().hasClass('is-checked') || $('#call_your_business').parent().hasClass('is-checked') || $('#engage_with_your_content').parent().hasClass('is-checked') || $('#become_a_fan').parent().hasClass('is-checked') ){
      $('.checkboxvalidation').removeClass('error-box');

    }else{
      alert('Please select atleast one objective')
      $('.checkboxvalidation').addClass('error-box');
      window.is_error = true;
    }

    ab_testing = document.getElementById('ab_testing');
    validateFiled(ab_testing);

    countryElem = document.getElementById('country');
    validateFiled(countryElem);
    
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
    }
    else{

      var url = $(urlElem).val();
      $("#company").val(url);
      var status = true;

      //updating Advertiser2 details to Advertaiser Optional
      $('#fopt').val($('#first_name2').val());
      $('#lopt').val($('#last_name2').val());
      if($('#cid').val().indexOf('-') == -1){
        var newCid = $('#cid').val().substring(0,3) + '-' + $('#cid').val().substring(3, 6) + '-' +  $('#cid').val().substring(6,12);
        $('#cid').val(newCid);
      }
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
    if ($(elem).val().trim() == "" || $(elem).val() == "0" || !$(elem).val()) {
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


// Verify the CID and get the eligible picasso lead details for the given CID
$('input[name=cid]').on('focusout', function(){
        if(!$(this).val()){
            clearLeadDetails();
        }else{
            $.ajax({
                'method': 'GET',
                'dataType': 'json',
                'url': "/leads/get-eligible-picasso-lead/",
                'data': {'cid': $('input[name=cid]').val(), 'lead_type': 'wpp'},
                success: function(response){
                    if(response['status'] == 'FAILED'){
                        //alert('Lead for Selected CID not available.');
                        clearLeadDetails();
                        //$('input[name=cid], input[name=url1], input[id=treatment_type], input[name=treatment_type], input[id=lead_owner], input[id=lead_owner]' ).val('')
                    }
                    else if(response['status'] == 'MULTIPLE'){
                        //clearLeadDetails();
                        alert(" We have more than one website URL for this customer ID (" + $('input[name=cid]').val() + "). Please select the right URL from the list.");
                        multiple_leads(response['details']);
                    }
                    else{
                        clearLeadDetails();
                        populateLeadDetails(response);
                    }
                },
                error:function(xhr, status, error){
                    alert('Something went wrong!. Please check CID');
                    clearLeadDetails();
                    $('input[name=cid], input[name=advertiser], input[id=advertiser], input[name=lead_owner], input[id=lead_owner]').val('')
                }
            })
        }
    });

// Providing website URL to select elegible lead from Multiple lead with same CID
function multiple_leads(details){
    $('input:checkbox').parent().removeClass('is-checked')
    $('#team option[value=""]').attr('selected', 'selected');
    $('#country option[value=""]').attr('selected', 'selected');
    $('#treatment_type option[value=""]').attr('selected', 'selected');
    $('#url').hide();
    $('#multipleUrls').show();
    $('#multipleUrls option').remove()
    var html = '<option value>Select Website URL</option>'
    for(var i=0; i<details.length; i++){
        var obj = details[i];
        var rec = '<option value='+ obj['lead_details']['l_id']+'>'+ obj['lead_details']['url'] +'</option>';
        html += rec
    }
    html += '<option value="newWebSite">Want to Add New Website URL</option>'
    $('#multipleUrls').append(html);
}

//Geting lead details of multiple leads for single CID
$('#multipleUrls').change(function(){
  $('input[type="checkbox"]').parent().removeClass('is-checked');
  $('input[type="checkbox"]').val('');
  $('#team option[value=""]').attr('selected', 'selected');
  $('#country option[value=""]').attr('selected', 'selected');
  $('#treatment_type option[value=""]').attr('selected', 'selected');
  $('#url').hide();
  $('#url').val('');
    var lid = $(this).val();
    if(lid){
        if(lid == 'newWebSite'){
          $('#url').show();
        }else{
          $.ajax({
          'url': "/leads/get-eligible-picasso-lead-by-lid/",
          'dataType': "json",
          'type': 'GET',
          'data': {'lid': lid, 'lead_type':'wpp'},
          success: function(response) {
             if(response['status'] == 'FAILED'){
                alert('Lead for Selected CID not available.');
                clearLeadDetails();
            } else{
                populateLeadDetails(response);
            }
          },
          error: function(errorThrown) {
              alert('Something went wrong!. Please check CID');
              clearLeadDetails();
          }
      }); 
    }
  }
});

// Populating Lead Details for selected CID/Lead Id
function populateLeadDetails(response){
    $('input[name=url1], input[id=url]').val(response.details.url);
    $('#team').val(response.details.team);
    $('#country').val(response.details.country);
    $("#country").trigger('change');
    $('#treatment_type').val(response.details.treatment_type);
    $('#picasso_pod').val(response.details.pod_name);
    for(i=0;i<=response.details.picasso_objectives.length;i++){
        //$('input[value="'+response.details.picasso_objectives[i]+'"]').prop('checked', true);
        $('input[data="'+response.details.picasso_objectives[i]+'"]').parent().addClass('is-checked');
        $('input[data="'+response.details.picasso_objectives[i]+'"]').val(response.details.picasso_objectives[i]);
    }
    //populateObjectives(response.details.picasso_objectives);
}

// To clear prepopulated lead Details 
function clearLeadDetails(){
  $('input[name=url1], input[id=picasso_pod]').val('');
  $('#multipleUrls').hide();
  $('#url').show();
  $('#multipleUrls option').remove();
  //$('input[type=checkbox]').prop('checked', false);
  $('input:checkbox').parent().removeClass('is-checked')
  $('#team option[value=""]').attr('selected', 'selected');
  $('#country option[value=""]').attr('selected', 'selected');
  $('#treatment_type option[value=""]').attr('selected', 'selected');
  $("#country").trigger('change');
}



