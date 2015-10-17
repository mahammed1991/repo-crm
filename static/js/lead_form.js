 // lead form controls
    $("#appointmentCheck1" ).click(function() {
      $( "#tag_appointment" ).animate({
      height: "toggle"
      }, 300, function() {
      });
    });
  
    $("#appointmentCheck2" ).click(function() {
      $( "#shopping_appointment" ).animate({
      height: "toggle"
      }, 300, function() {
      });
    });

    $("#appointmentCheck" ).click(function() {
      $( "#appointment" ).animate({
      height: "toggle"
      }, 300, function() {
      });
      if($(this).is(":checked")){
        $("#setup_datepick").val('');
        $("#setup_datepick").hide();
        $("#tag_datepick").val('');
        $("#tag_datepick").hide();
      }else{
        $("#setup_datepick").show();
        $("#tag_datepick").show();
      }

    });
    
    $("#webmasterCheck" ).click(function() {
      /* this line for uncheck other check box*/ 
      $("#tag_contact_person_name, #shop_contact_person_name").val(''); 
      $("#web_access").prop("checked", false);

      $( "#webmaster" ).animate({
      height: "toggle"
      }, 300, function() {
      });
      $( "#web-dum1, #web-dum2" ).toggle(500);
    });

    /* this line for uncheck webmasterCheck box*/ 
    $("#web_access").on('click', function() {
      $("#webmasterCheck").prop("checked", false);
      $( "#webmaster").hide();

      if($("#web_access").is(":checked")){
          $("#web_access").val(1);
          var advertiser_name = $("#advertiser_name").val();
          $("#tag_contact_person_name, #shop_contact_person_name").val(advertiser_name);
          // clear webmaster fields
          $('#webmaster_name').val('');
          $('#web_master_email').val('');
          $('#popt').val('');
      }else{
        $("#web_access").val(0);
        $("#tag_contact_person_name, #shop_contact_person_name").val('');
      }


    });
    
    $("#tagImplementation" ).click(function() {
      
      if($(this).children().is(':visible')){
        if($( "#shoppingSetup .check-icon" ).is(":visible")){
          $("#submit_buttons").show();
          //$("#heads_up").show();
        }else{
          $("#submit_buttons").hide();
          //$("#heads_up").hide();
        }
      }else{
        $("#submit_buttons").show();
        //$("#heads_up").show();
      }

      $( "#tasks" ).animate({
      height: "toggle"
      }, 300, function() {
      });
      //$( "#tagImplementation .check-icon" ).toggle();
      $( "#tagImplementation .check-icon" ).animate({
      opacity: "toggle"
      }, 200, function() {
        if($(".tag-policies").is(":visible")){
            $(".tag-policies").hide();
            $("#is_tag_lead").val('no');
          }else{
            $(".tag-policies").show();
            $("#heads_up").show();
            $("#is_tag_lead").val('yes'); 
          }

          // Hide Heads Up section
          if($("#is_tag_lead").val() == 'no' && $("#is_shopping_lead").val() == 'no'){
            $("#heads_up").hide();
          }

      });
    });
    
    $("#shoppingSetup" ).click(function() {

      if($(this).children().is(':visible')){
        if($( "#tagImplementation .check-icon" ).is(":visible")){
          $("#submit_buttons").show();
          //$("#heads_up").show();
        }else{
          $("#submit_buttons").hide();
          //$("#heads_up").hide();
        }
      }else{
        $("#submit_buttons").show();
        //$("#heads_up").show();
      }
      $( "#shoppingInfo" ).animate({
      height: "toggle"
      }, 300, function() {
      });

      $( "#shoppingSetup .check-icon" ).animate({
      opacity: "toggle"
      }, 200, function() {
          if($(".shopping-policy").is(":visible")){
            $(".shopping-policy").hide();
            $("#shoppingTerms").hide();
            $("#is_shopping_policies").attr('checked', false);
            $("#is_shopping_lead").val('no'); 
          }else{
            $(".shopping-policy").show();
            $("#heads_up").show();
            $("#is_shopping_lead").val('yes'); 
          }

        // Hide Heads Up section
        if($("#is_tag_lead").val() == 'no' && $("#is_shopping_lead").val() == 'no'){
          $("#heads_up").hide();
        }

      });
    });


    $(".add" ).click(function() { 
      $( ".add" ).hide();
      $( ".remove" ).hide();
      id = $(this).attr('id');
      indx = id.split('_')[1];
      next_id = parseInt(indx) + 1
      $( "#task_" + indx ).animate({
      height: "toggle"
      }, 300, function() {
      });
      setTimeout(function() {
        $( "#removeTask_" + indx).show();
      }, 300); 

       setTimeout(function() {
        $("#addTask_" + next_id).show();
      }, 300); 
    });
    
    $(".remove" ).click(function() {    
      $( ".add" ).hide();
      $( ".remove" ).hide();
      id = $(this).attr('id');
      indx = id.split('_')[1];
      next_id = parseInt(indx) + 1
      prev_id = parseInt(indx) - 1
      $("#ctype" + indx).val('');
      $("#url" + indx).val('');
      $("#code" + indx).val('');
      $("#comment" + indx).val('');
      $("#rbid" + indx).val('');
      $("#rbudget" + indx).val('');
      $("#ga_setup" + indx).val('0');

      
      $("#user_list_id"+ indx).val('');
      $("#internal_cid"+ indx).val('');
      $("#rsla_bid_adjustment"+ indx).val('');
      $("#campaign_ids"+ indx).val('');
      $("#overwrite_existing_bid_modifiers"+indx).val('');
      $("#create_new_bid_modifiers"+indx).val('');
      $("#rsla_policies"+indx).prop('checked', false);
      $("#rsla_policies"+indx).val(0);

      $( "#task_" + indx).animate({
      height: "toggle"
      }, 300, function() {
      });

      setTimeout(function() {
        $("#removeTask_" + prev_id ).show();
      }, 300); 

      setTimeout(function() {
        $("#addTask_" + indx).show();
      }, 300); 
      
    });
    
    // media query for team page
    if ($(window).width() <= 767){  
      $("div.team-slider").removeClass('slider1');
    }

  $('#team').change(function(){
    var selectedTeam = $(this).val();
    $("#team_service_gce").hide();
    $('#g_cases_id').val('')
    $("#service_segment").val('');
    if (selectedTeam.indexOf('Services') != -1){
      if(selectedTeam == 'Services/GCE'){
        $("#team_service_gce").show();
      }
      $(".tr_service_segment").show();
      $('label[for="g_cases_id"]').hide();
      $('label[for="service_segment"]').hide();
      $('#g_cases_id').show();
      $('#GCaseId').show();
      $("#service_segment").hide();
    }else if(selectedTeam == 'ETO' || selectedTeam == 'ETO: Agency' || selectedTeam == 'ETO: Inbound' || selectedTeam == 'ETO: Outbound' || selectedTeam == 'ETO: CS'){
      if (window.is_loc_changed){
        setLocations(window.locations);
        window.is_loc_changed = false;
      }
      $("#service_segment").show();
      $("#service_segment").val('');
      $(".tr_service_segment").show();
      $('#g_cases_id').hide();

      $('label[for="g_cases_id"]').hide();
      $('label[for="service_segment"]').show();
    }else{
      if (window.is_loc_changed){
        setLocations(window.locations);
        window.is_loc_changed = false;
      }
      $(".tr_service_segment").hide();
      $('#g_cases_id').hide();
      $('#GCaseId').hide();

      $('label[for="g_cases_id"]').hide();
      $('label[for="service_segment"]').hide();
    }
  });

  $('#team').trigger("change");
  
  $('#setup_lead_check').click(function() {
    $('#setup_lead_form').toggle();
  })

  function submitbtn(ths){
      $(ths).submit().attr('disabled', true);
  }

  $("#tag_contact_person_name").change(function(){
      var tag_name = $(this).val();
      $("#shop_contact_person_name").val(tag_name);
  });

  $("#shop_contact_person_name").change(function(){
    var shop_name = $(this).val();
      $("#tag_contact_person_name").val(shop_name);
  });

  $("#tag_primary_role").change(function(){
      var tag_role = $(this).val();
      $("#shop_primary_role").val(tag_role);
  });

  $("#shop_primary_role").change(function(){
      var shop_role = $(this).val();
      $("#tag_primary_role").val(shop_role);
  });

  function setLocations(newLocations){
    $("#country option").remove()
    $("#country").append('<option value="0">Market Served</option>');
    for(i=0; i<newLocations.length; i++){
      $("#country").append('<option value="' + newLocations[i]['name'] + '" location_id="' + newLocations[i]['id']+ '">'+ newLocations[i]['name'] +'</option>');
    }
    $("#country").val('0');
  }
  

function setLocationsForRegion(newLocations, countryIds){
    $("#country option").remove()
    $("#country").append('<option value="0">Market Served</option>');
    if(countryIds && countryIds.length > 0){
        for(i=0; i<newLocations.length; i++){
          if(countryIds.indexOf(newLocations[i]['id']) != -1){
           $("#country").append('<option value="' + newLocations[i]['name'] + '" location_id="' + newLocations[i]['id']+ '">'+ newLocations[i]['name'] +'</option>');
         }
        }
    }else{
        for(i=0; i<newLocations.length; i++){
          $("#country").append('<option value="' + newLocations[i]['name'] + '" location_id="' + newLocations[i]['id']+ '">'+ newLocations[i]['name'] +'</option>');
        }
    }
    
   $("#country").val('0');
  }

   //shopping check 
    $("#is_shopping_policies" ).click(function() {
        $(".shopping-policy").removeClass('error-box');
        $( "#shoppingTerms" ).animate({
        height: "toggle"
        }, 300, function() {
        });
    }); 


function validatethis(frm) {
    $(".error-txt").remove();
    $(".lead-form .form-control").removeClass('error-box');
    $('.web-access').removeClass('error-box');
    $('.error-box').removeClass('error-box');
    var check = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var cidFormat = /^\d{3}-\d{3}-\d{4}$/;
    var phoneFormat = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    var numericExpression = /^[0-9]+$/;
    var emailFormat = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i; 
    var ct = 0;
    var rc = 0;
    var fix_slots = new Array();
    window.failedFields = new Array();
    window.is_error = false;

    if(window.is_reset == true){
      window.is_reset = false;
      return false;
    }
    
    grefElem = document.getElementById('gref');
    validateFiled(grefElem);
    
    emailrefElem = document.getElementById('emailref');
    validateFiled(emailrefElem);
    validateFormatField(emailrefElem, emailFormat);
    
    teamElem = document.getElementById('team');
    validateFiled(teamElem);
    // Service Segment Validation
    if ($(frm.service_segment).is(":visible")) {
      service_segmentElem = document.getElementById('service_segment');
      validateFiled(service_segmentElem);
    }
    // GcaseId validation
    if ($(frm.g_cases_id).is(":visible")) {
      gCasesIdElem = document.getElementById('g_cases_id');
      validateFiled(gCasesIdElem);
    }
    // Google Manager details validation
    teamElem = document.getElementById('team');
    validateFiled(teamElem);
    
    managerElem = document.getElementById("manager_name");
    validateFiled(managerElem);

    emailElem = document.getElementById("manager_email");
    validateFiled(emailElem);
    validateFormatField(emailElem, emailFormat)

    // Advertiser Info
    // Advertiser Name Validation
    advertiserNameElem = document.getElementById('advertiser_name');
    validateFiled(advertiserNameElem);

    aemailElem = document.getElementById('aemail');
    validateFiled(aemailElem);
    // Email Validation
    validateFormatField(aemailElem, emailFormat);

    // Advertiser Phone Validation
    phoneElem = document.getElementById('phone');
    validateFiled(phoneElem);

    // Advertiser Company Validation
    companyElem = document.getElementById('company');
    validateFiled(companyElem);

    // Customer Id validation
    cidElem = document.getElementById('cid');
    validateFiled(cidElem);
    validateFormatField(cidElem, cidFormat);

    // Advertiser Email Validation
    countryElem = document.getElementById('country');
    validateFiled(countryElem);

    // Language validation
    languageElem = document.getElementById('language');
    validateFiled(languageElem);

    // Timezone Validation
    tzoneElem = document.getElementById('tzone');
    validateFiled(tzoneElem);

    // Does the advertiser have edit access for the website or has a webmaster validation for selection
    if(document.getElementById("web_access").checked == false && document.getElementById("webmasterCheck").checked == false){
      $('.web-access').addClass('error-box');
      window.is_error = true;
    }

    // Webmaster Validation
    if(document.getElementById("webmasterCheck").checked == true){

      // Contact Person Name
      webMasterNameElem = document.getElementById('webmaster_name');
      validateFiled(webMasterNameElem);

      // Contact Person Role
      webMasterEmailElem = document.getElementById('web_master_email');
      validateFiled(webMasterEmailElem);

      // Contact Person Name
      poptElem = document.getElementById('popt');
      validateFiled(poptElem);

    }

    // Tag Implementation lead form related Validation
    // validate Tag Implementation fields
    if($("#tagImplementationBtn").is(":visible")){
      // Hava an appointment 

      for( i=1; i <= $(".task").length; i++){
        if($("#task_" + i).is(":visible")){
          validateTaskFields(i);
        }
      }

      if (document.getElementById("appointmentCheck1").checked == true) {

        // Contact Person Name Validation 
        contactElem = document.getElementById('tag_contact_person_name');
        validateFiled(contactElem);

        // Contact Person Role Validation 
        roleElem = document.getElementById('tag_primary_role');
        validateFiled(roleElem);

        // Appointments Date and Time Validation
        setupDateElem = document.getElementById('tag_datepick');
        validateFiled(setupDateElem);

        if(frm.tag_datepick.value != ''){
            var slot = {
              'type' : 'TAG',
              'time' : frm.tag_datepick.value
            }
          fix_slots.push(slot)  
        }

      }else{
          frm.tag_datepick.value = '';  
      }

    }else{
      frm.tag_datepick.value = '';
    }
    
    // Check If Shopping related lead fields
    if ($('#shoppingSetupBtn').is(':visible')) {
        
      rbidElem = document.getElementById('rbid');
      validateFiled(rbidElem);

      rbidmodifierElem = document.getElementById('rbidmodifier');
      validateFiled(rbidmodifierElem);

      rbudgetElem = document.getElementById('rbudget');
      validateFiled(rbudgetElem);

      shoppingElem = document.getElementById('shopping_url');
      validateFiled(shoppingElem);
      
      // MC-ID Validation
      MCIDElem = document.getElementById('mcIdCheck');
      if(MCIDElem.checked == true){
          MCElem = document.getElementById('mc_id');
          validateFiled(MCElem);
      }

    // Hava an appointment 
    if (document.getElementById("appointmentCheck2").checked == true) {

      // Contact Person Name Validation 
      shopcontactElem = document.getElementById('shop_contact_person_name');
      validateFiled(shopcontactElem);

      // Contact Person Role Validation 
      shoproleElem = document.getElementById('shop_primary_role');
      validateFiled(shoproleElem);

      // Appointments Date and Time Validation
      setupdateElem = document.getElementById('setup_datepick');
      validateFiled(setupdateElem);

        // If Setup Date Slot Selected
        if(frm.setup_datepick.value != ''){
            var slot = {
              'type' : 'SHOPPING',
              'time' : frm.setup_datepick.value
            }
          fix_slots.push(slot)
        }
    }else{
      frm.setup_datepick.value = '';
    }

      if($("#is_shopping_policies").is(":checked")){
          $("#is_shopping_policies").val(1);
          $(".shopping-policy").removeClass('error-box');
      }else{
          $(".shopping-policy").addClass('error-box');
          window.failedFields.push($("#is_shopping_policies"));
          window.is_error = true;
          $("#is_shopping_policies").val(0);
      }

      isAgree = ensureAllPolicies()

      }else{
        // If Setup Date Slot Not Selected
        frm.setup_datepick.value = '';
      }

      // Check Box Options
      if($("#tag_via_gtm").is(":checked")){
        $("#tag_via_gtm").val(1);
      }else{
        $("#tag_via_gtm").val(0);
      }

      if($("#web_access").is(":checked")){
          $("#web_access").val(1);
      }else{
        $("#web_access").val(0);
      }

      // Analytics setup check box
      $('.is_ga_setup').each(function(){
        if(!$(this).is(":visible")){
          $(this).val(0);
        }
      });

    if(window.is_error){
      focusElem = failedFields[0];
      $(focusElem).focus();
      return false;
    }else{
      var status = true;
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

function validateFormatField(elem, check) {
  // Validate Email Field
  if (!$(elem).val().trim().match(check)) {
      $(elem).addClass('error-box');
      window.failedFields.push(elem);
      window.is_error = true;
      return false;
    }
}

function ensureAllPolicies(){
  var isAgree = false;
  if($("#shoppingTerms").is(":visible")){
      $(".shopping-group").each(function(){
        if($(this).is(":checked")){
          isAgree = true;
        }else{
          isAgree = false;
          window.failedFields.push($(this));
          $(this).parent().addClass('error-box');
          window.is_error = true;
          return isAgree;
        }
      });
    }
    return isAgree
}

function validateTaskFields(indx){
  ctypeElem = document.getElementById('ctype' + indx);
  validateFiled(ctypeElem)

  urlElem = document.getElementById('url' + indx);
  validateFiled(urlElem)

  if($('#rlsa_bulk' + indx).is(":visible")){

    rlsaUserListEle = document.getElementById('user_list_id' + indx);
    validateFiled(rlsaUserListEle);

    rlsaBidAdjustment = document.getElementById('rsla_bid_adjustment' + indx);
    validateFiled(rlsaBidAdjustment);

    campaignIds = document.getElementById('campaign_ids' + indx);
    validateFiled(campaignIds);

    existingBid = document.getElementById('overwrite_existing_bid_modifiers' + indx);
    validateFiled(existingBid);

    newBid = document.getElementById('create_new_bid_modifiers' + indx);
    validateFiled(newBid);

    rlsaPolicies = document.getElementById('rsla_policies' + indx);
    if(!$(rlsaPolicies).is(":checked")){
       $(rlsaPolicies).parent().addClass('error-box');
        window.failedFields.push(rlsaPolicies);
        window.is_error = true;
        return false;
    }


  }

  if($('#analyticscode' + indx).is(":visible")){
      var analyticsCodeElem = document.getElementById('analytics_code' + indx)
      validateFiled(analyticsCodeElem)
  }

  // New fields for Dynamic Remarketing Code Types
  var isCampaign = document.getElementById('is_campaign_created' + indx)
  if($(isCampaign).is(":visible") && isCampaign.checked == false){

      // rBid validation
      var rbidElem = document.getElementById('rbid' + indx)
      validateFiled(rbidElem)

      // rBudget validation
      var rbudgetElem = document.getElementById('rbudget' + indx)
      validateFiled(rbudgetElem)

  }else{
    $("#rbid" + indx).val('');
    $("#rbudget" + indx).val('');
  }

}

function resetBtn(elem){
  elemId = $(elem).attr('id');
  if(elemId == 'formReset'){
    window.is_reset = true;
    window.location.reload();
  }
}

$("#mcIdCheck").click(function(){
  if($(this).is(':checked')){
      $("#mc_id").show();
  }else{
      $("#mc_id").hide();
  }
});

$("#keep_url").click(function(){
    if($(this).is(":checked")){
      var tagUrl = $("#url1").val();
      if(!tagUrl){
        $("#url1").addClass('error-box');
      }
      $("#url2, #url3, #url4, #url5").val(tagUrl);
    }else{
      $("#url2, #url3, #url4, #url5").val('');
    }
});
  
$("#webmaster_name").change(function(){
    var webmasterName = $(this).val();
    $("#tag_contact_person_name, #shop_contact_person_name").val(webmasterName);
});

$('.code_type').change(function(){

  var selectedCodeType = $(this).val();
  selectedId = $(this).attr('id')
  selectedindex = selectedId[selectedId.length-1]

  $('#ga_setup'+selectedindex).prop('checked', false);
  $('#analytics_code'+selectedindex).val('');
  $('#analyticscode'+selectedindex).hide();
  $('#callextension'+selectedindex).hide();
  $('#call_extension'+selectedindex).prop('checked', false);
  $('#codebehaviour'+selectedindex).hide();

  $('#rbid'+selectedindex).val('');
  $('#rbudget'+selectedindex).val('');

  $('#rlsa_bulk'+selectedindex).hide();
  $("#user_list_id"+ selectedindex).val('');
  $("#internal_cid"+ selectedindex).val('');
  $("#rsla_bid_adjustment"+ selectedindex).val('');
  $("#campaign_ids"+ selectedindex).val('');
  $("#rsla_policies"+selectedindex).prop('checked', false);
  $("#rsla_policies"+selectedindex).val(0);
  $("#overwrite_existing_bid_modifiers"+selectedindex).val('');
  $("#create_new_bid_modifiers"+selectedindex).val('');
  $('#comment'+selectedindex).attr("placeholder", "Special Instructions (Optional)");

  uncheckAllBehaviourCheckBoxs(selectedindex);
    
  $('#ctype_campaign'+selectedindex).hide();
  $('#gasetup'+selectedindex).hide();

  if (selectedCodeType.indexOf('Analytics') != -1){
    $('#gasetup'+selectedindex).show();
  }
  else if(selectedCodeType.indexOf('Dynamic') != -1){
      $('#ctype_campaign'+selectedindex).show();    
  }
  else if(selectedCodeType.indexOf('Website Call Conversion') != -1){
      $('#callextension'+selectedindex).show();
  } else if(selectedCodeType.indexOf('RLSA Bulk Implementation') != -1){
      $('#rlsa_bulk'+selectedindex).show();
      $('#comment'+selectedindex).attr("placeholder", "Special Instructions (Optional, if there is an issue with applying RLSA to a campaign, please provide the Campaign ID for the campaign you wish to exclude)");

  }
  if(selectedCodeType.indexOf('Analytics Enhanced E-Commerce Tracking') != -1){
      $('#gasetup'+selectedindex).hide();
      $('#codebehaviour'+selectedindex).show();
  }
});

$(document).on('click', '.is_campaign_created', function() {
    thisId = $(this).attr('id');
    if($(this).is(":checked")){
        $("."+ thisId).hide().val('');
    }else{
      $("."+ thisId).show().val('');
    }
});

$(document).on('click', '.headsup-policies', function() {
    thisId = $(this).attr('id');
    if($(this).is(":checked")){
        $("#"+ thisId).val(1);
    }else{
        $("#"+ thisId).val(0);
    }
    
});

$("#tagCheck").click(function(){
    var elem = document.getElementById('tag_via_gtm'); 
    if(elem.checked == true){
      $("#comment1, #comment2, #comment3, #comment4, #comment5").val('implement via GTM');
    }else{
      $("#comment1, #comment2, #comment3, #comment4, #comment5").val('');
    }
});

$(".is_ga_setup").click(function(){
    thisId = $(this).attr('id');
    selectedindex = thisId[thisId.length-1]
    $('#analyticscode'+selectedindex).hide();
    if($(this).is(":checked")){
      $('#analyticscode'+selectedindex).show();
      $(this).val(1);
    }else{
      $('#analyticscode'+selectedindex).hide();
      $('#analytics_code'+selectedindex).val('');
      $(this).val(0);
    }
});

$('#region').change(function(){
  var regionId = $('option:selected', this).attr('region_id');
  countryList = regionWiseLocations[regionId];
  console.log(countryList);
  setLocationsForRegion(window.locations, countryList);
});


function uncheckAllBehaviourCheckBoxs(selectedindex){
  $('#product_behaviour'+selectedindex).prop('checked', false);
  $('#cartpage_behaviour'+selectedindex).prop('checked', false);
  $('#checkout_process'+selectedindex).prop('checked', false);
  $('#transaction_behaviour'+selectedindex).prop('checked', false);
}
