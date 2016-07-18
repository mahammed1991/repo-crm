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
      $('#webaccess-inline').hide();

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
        if($( "#shoppingSetup .check-icon" ).is(":visible") || $('#rlsaSetup .check-icon').is(":visible")){
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
            $('#tagCheckBoxs').hide();
            $("#is_tag_lead").val('no');
          }else{
            $(".tag-policies").show();
            selectedTeam = $('#team').val()
            if((selectedTeam.indexOf('ETO') != -1) || (selectedTeam.indexOf('UMM') != -1)){
              $('#tagCheckBoxs').show();
            }else{
              $('#tagCheckBoxs').hide();
            }
            $("#heads_up").show();
            $("#is_tag_lead").val('yes'); 
          }

          // Hide Heads Up section
          if($("#is_tag_lead").val() == 'no' && $("#is_shopping_lead").val() == 'no' && $("#is_rlsa_lead").val() == 'no'){
            $("#heads_up").hide();
          }

      });
    });
    
    $("#shoppingSetup" ).click(function() {
      $('#Shopping_Campaign_Setup').attr('checked', true);
      if($(this).children().is(':visible')){
        if($( "#tagImplementation .check-icon" ).is(":visible") || $('#rlsaSetup .check-icon').is(":visible")){
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
        if($("#is_tag_lead").val() == 'no' && $("#is_shopping_lead").val() == 'no' && $("#is_rlsa_lead").val() == 'no'){
          $("#heads_up").hide();
        }

      });
    });

 /* start RLSA bulk implimentation code */
  $("#rlsaSetup" ).click(function() {

      if($(this).children().is(':visible')){
        if($( "#tagImplementation .check-icon" ).is(":visible") || $( "#shoppingSetup .check-icon" ).is(":visible")){
          $("#submit_buttons").show();
          $('#tagCheckBoxs').show();
          //$("#heads_up").show();
        }else{
          $("#submit_buttons").hide();
          //$("#heads_up").hide();
        }
      }else{
        $("#submit_buttons").show();
        //$("#heads_up").show();
      }

      $( "#rlsa-impl-initial1" ).animate({
      height: "toggle"
      }, 300, function() {
      });
      //$( "#tagImplementation .check-icon" ).toggle();
      $( "#rlsaSetup .check-icon").animate({opacity: "toggle"}, 200, function(){ 
        if($('.rlsa-policy').is(':visible')){
          //for closing RLSA Fields am making '' as value
          $('#internal_cid1, #user_list_id1, #rsla_bid_adjustment1, #authEmail').val('');
          $('#rlsa-impl-initial2, #rlsa-impl-initial3, #rlsa-impl-initial4, #rlsa-impl-initial5').remove();
          $('#removeRlsa_1').hide();
          $('#add_rlsa1').show();
          $(".rlsa-policy").hide();
          if($( "#tagImplementation .check-icon" ).is(":visible")){
            selectedTeam = $('#team').val()
            if((selectedTeam.indexOf('ETO') != -1) || (selectedTeam.indexOf('UMM') != -1)){
              $('#tagCheckBoxs').show();
            }else{
              $('#tagCheckBoxs').hide();
            }
          }
          $("#is_rlsa_lead").val('no');
        }else{
          var cid = $('#cid').val()
          if(cid){
          $('#internal_cid1').val($('#cid').val());
          $('#internal_cid1').attr('readonly', true);
          }
          $('#removeRlsa_1').hide();
          $('#add_rlsa1').show();
          $(".rlsa-policy").show();
          $("#heads_up").show();
          if($( "#tagImplementation .check-icon" ).is(":visible")){
            selectedTeam = $('#team').val()
            if((selectedTeam.indexOf('ETO') != -1) || (selectedTeam.indexOf('UMM') != -1)){
              $('#tagCheckBoxs').show();
            }else{
              $('#tagCheckBoxs').hide();
            }
          }
          $('#is_rlsa_lead').val('yes')
        }

        // Hide Heads Up section
        if($("#is_tag_lead").val() == 'no' && $("#is_shopping_lead").val() == 'no' && $("#is_rlsa_lead").val() == 'no'){
          $("#heads_up").hide();
        }

      });
    });
/* end of RLSA bulk implimentation code*/

    /*Shopping Comapaign changes code starts here*/

    $('#Shopping_Campaign_Setup').click(function(){
      $('#description').val('');
      $('#shopping_url').val('');
      $('#Shopping_Trobleshoot').prop('checked', false);
      $('#shopping_campaing_issues, #issues_description').val();
      $( "#shopping_trobleshooting" ).hide();
      $( ".shoppingInfo" ).animate({
      height: "toggle"
      }, 300, function() {
      });
    });

    $('#Shopping_Trobleshoot').click(function(){
      $('#issues_description').val('');
      $('#rbid, #rbidmodifier, #rbudget, #shopping_url, #mc_id, #description').val('');
      $('#Shopping_Campaign_Setup').prop('checked', false);
      $('#shopping_trobleshooting_url').val('');
      $('#mcIdCheck').prop('checked', true);
      $( ".shoppingInfo" ).hide();
      $( "#shopping_trobleshooting" ).animate({
      height: "toggle"
      }, 300, function() {
      });
    });

    $('#shopping_trobleshooting_url').focusout(function(){
      if($('#Shopping_Trobleshoot').prop('checked', true)){
        $('#shopping_url').val($('#shopping_trobleshooting_url').val());
      }else if($('#Shopping_Campaign_Setup').prop('checked', true)){
        $('#shopping_url').val('');
      }else{
        $('#shopping_url').val('');
      }
    });

    /*Shopping Comapaign changes code starts here*/

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
      $('#code_type_avg_time_'+indx).html('');
      $('#code_type_avg_time_'+indx).hide('');
      next_id = parseInt(indx) + 1
      prev_id = parseInt(indx) - 1
      $("#ctype" + indx).val('');
      $("#url" + indx).val('');
      $("#code" + indx).val('');
      $("#comment" + indx).val('');
      $("#ga_setup" + indx).val('0');

      $('#ctype_campaign'+indx).hide();
      $('#is_campaign_created'+indx).prop('checked', false);
      $('#product_expectations'+indx).prop('checked', false);
      $('#campaign_implemented'+indx).prop('checked', false);

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
    $('#g_cases_id').val('');
    $('#ldap').val('');
    $("#service_segment").val('');
    $('#tagCheckBoxs').hide();
    $('#tag_appointment_aware, #tag_admin_access, #tag_admin_code').prop('checked', false);
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
      //$('#ldap').hide();
      $('#tagCheckBoxs').hide();
    }else if(selectedTeam =='GCE Kickstart Reactive'){
      if (window.is_loc_changed){
        setLocations(window.locations);
        window.is_loc_changed = false;
      }
      $("#service_segment").hide();
      $("#service_segment").val('');
      $(".tr_service_segment").show();
      $('#g_cases_id').show();
      $('label[for="g_cases_id"]').show();
      $('label[for="service_segment"]').hide();
      $('#tagCheckBoxs').hide();
      //$('#ldap').hide();
    }
    else if(['ETO', 'ETO: Agency', 'ETO: Inbound', 'ETO: Outbound', 'ETO: CS'].indexOf(selectedTeam) != -1 && $('#tasks').is(':visible')){
      if (window.is_loc_changed){
        setLocations(window.locations);
        window.is_loc_changed = false;
      }
      //$('#ldap').show();
      $('#tagCheckBoxs').show();
      $("#service_segment").show();
      $("#service_segment").val('');
      $(".tr_service_segment").show();
      $('#g_cases_id').hide();

      $('label[for="g_cases_id"]').hide();
      $('label[for="service_segment"]').show();
    }else if(selectedTeam == 'UMM'){
      $("#team_service_gce").hide();
      $('#g_cases_id').val('')
      $("#service_segment").val('');
      $('#tagCheckBoxs').show();
    }else if(['ETO', 'ETO: Agency', 'ETO: Inbound', 'ETO: Outbound', 'ETO: CS'].indexOf(selectedTeam) != -1 ){
      //$('#ldap').show();
      $('#g_cases_id').hide();
      }
    else{
      if (window.is_loc_changed){
        setLocations(window.locations);
        window.is_loc_changed = false;
      }
      $(".tr_service_segment").hide();
      $('#g_cases_id').hide();
      $('#GCaseId').hide();

      $('label[for="g_cases_id"]').hide();
      $('label[for="service_segment"]').hide();
      $('#tagCheckBoxs').hide();
      //$('#ldap').hide();
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

    if($("#rlsaSetupBtn").is(":visible")){
      authEmail = document.getElementById('authEmail');
      validateFiled(authEmail);
      for( i=1; i <= $(".rlsa-codes").length; i++){
        if($("#rlsa-impl-initial" + i).is(":visible")){
            validateRLSAFields(i);
        }
      }

      if($('.rlsa-policy').is(':visible') && $('#rsla_policies1').is(':checked')==false){
         $('.rlsa-policy').addClass('error-box');
          window.is_error = true;
      }
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
        
       if($('.shoppingInfo').is(':visible')){
        
            rbidElem = document.getElementById('rbid');
            validateFiled(rbidElem);

            bidmodifiercontrolerElem = document.getElementById('bidmodifiercontroler');
            validateFiled(bidmodifiercontrolerElem);


            rbidinpercentageElem = document.getElementById('rbidinpercentage');
            validateFiled(rbidinpercentageElem);


            // rbidmodifierElem = document.getElementById('rbidmodifier');
            // validateFiledAllowZero(rbidmodifierElem);

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
        }

        if($('#shopping_trobleshooting').is(':visible')){

          shoppingCampaingIssuesElem = document.getElementById('shopping_campaign_issues');
          validateFiled(shoppingCampaingIssuesElem);

          issuesDiscriptionEle = document.getElementById('issues_description');
          validateFiled(issuesDiscriptionEle);

          shoppingElem = document.getElementById('shopping_trobleshooting_url');
          validateFiled(shoppingElem);
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
      // if($("#tag_via_gtm").is(":checked")){
      //   $("#tag_via_gtm").val(1);
      // }else{
      //   $("#tag_via_gtm").val(0);
      // }

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

      if($('.tag-policies-aware').is(':visible')){
        if($('#tag_appointment_aware').is(':checked')){

        }else{
           window.failedFields.push($("#tag_appointment_aware"));
           window.is_error = true;
           $('.tag-policies-aware').addClass('error-box');
          
        }
      }
      if($('.tag-policies-access').is(':visible')){
        if($('#tag_admin_access').is(':checked')){
          
        }else{
           window.failedFields.push($("#tag_admin_access"));
           window.is_error = true;
           $('.tag-policies-access').addClass('error-box');
          
        }
      }
      if($('.tag-policies-code').is(':visible')){
        if($('#tag_admin_code').is(':checked')){
          
        }else{
           window.failedFields.push($("#tag_admin_code"));
           window.is_error = true;
           $('.tag-policies-code').addClass('error-box');
          
        }
      }

      // For Adwords Conversion Code code type we are validating dynamic conversion value tracking
      if($('.tag-add-policies').is(':visible')){
       if($("#add_tracking_yes[type='radio']").is(':checked') || $("#add_tracking_no[type='radio']").is(':checked') ){
        // Nothoing to do here
       }
       else{
          window.failedFields.push($("#tagAddwordsCheck"));
          window.is_error = true;
          $('#tagAddwordsCheck').addClass('error-box');
        }
      }

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
      //to workon picasso modal
      if(status && isBoth != 'both'){
        $("#myModal").modal();
      }
      return status;  
    $('.lead-form').delay(15000).submit();
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

function validateFiledAllowZero(elem){
  if ($(elem).val() == "" || !$(elem).val()) {
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

  if($('#analyticscode' + indx).is(":visible")){
      var analyticsCodeElem = document.getElementById('analytics_code' + indx)
      validateFiled(analyticsCodeElem)
  }
  var isCampaign = document.getElementById('ctype_campaign' + indx)
  if($(isCampaign).is(':visible')){
    validateDynamicFields($('#is_campaign_created'+indx))
    validateDynamicFields($('#product_expectations'+indx))
    validateDynamicFields($('#campaign_implemented'+indx))
  }
}

function validateRLSAFields(indx){
  if($('.rlsa-impl-section').is(':visible')){

    rlsaUserListEle = document.getElementById('user_list_id' + indx);
    validateFiled(rlsaUserListEle);

    rlsaBidAdjustment = document.getElementById('rsla_bid_adjustment' + indx);
    validateFiled(rlsaBidAdjustment);

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

  conversionTracking()
  var selectedCodeType = $(this).val();
  selectedId = $(this).attr('id')
  selectedindex = selectedId[selectedId.length-1]

  $('#ga_setup'+selectedindex).prop('checked', false);
  $('#analytics_code'+selectedindex).val('');
  $('#analyticscode'+selectedindex).hide();
  $('#callextension'+selectedindex).hide();
  $('#call_extension'+selectedindex).prop('checked', false);
  $('#codebehaviour'+selectedindex).hide();

  $('#is_campaign_created'+selectedindex).prop('checked', false);
  $('#product_expectations'+selectedindex).prop('checked', false);
  $('#campaign_implemented'+selectedindex).prop('checked', false);
    
  $('#ctype_campaign'+selectedindex).hide();
  $('#gasetup'+selectedindex).hide();

  if (selectedCodeType.indexOf('Analytics') != -1){
    $('#gasetup'+selectedindex).show();
  }
   if(['Google Analytics Dynamic Remarketing (Retail)', 'Google Analytics Dynamic Remarketing (Non-Retail)', 'Dynamic Remarketing - Extension (non retail)', 'Dynamic Remarketing - Retail'].indexOf(selectedCodeType) != -1){
      $('#ctype_campaign'+selectedindex).show();
      $('#gasetup'+selectedindex).hide();
  }

  if(['GA Smart Goals'].indexOf(selectedCodeType) != -1){
    $("#smart-goal-messsage").show();   
  }
  if(['GA Smart Goals'].indexOf(selectedCodeType) == -1){
    $("#smart-goal-messsage").hide();   
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

$(document).on('click', '#is_campaign_created', function() {
    thisId = $(this).attr('id');
    if($(this).is(":checked")){
        $("#"+ thisId).val(1);
    }else{
        $("#"+ thisId).val(0);
    }
    
});

// $("#tagCheck").click(function(){
//     var elem = document.getElementById('tag_via_gtm'); 
//     if(elem.checked == true){
//       for( i=1; i <= $(".task").length; i++){
//         if($("#comment" + i).is(":visible")){
//          $("#comment"+i).val('implement via GTM');
//         }
//       }
//     }else{
//       $("#comment1, #comment2, #comment3, #comment4, #comment5").val('');
//     }
// });

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


/*function uncheckAllBehaviourCheckBoxs(selectedindex){
  $('#product_behaviour'+selectedindex).prop('checked', false);
  $('#cartpage_behaviour'+selectedindex).prop('checked', false);
  $('#checkout_process'+selectedindex).prop('checked', false);
  $('#transaction_behaviour'+selectedindex).prop('checked', false);
}*/

function conversionTracking(){
  var codeTypeValues = Array()
  for( i=1; i <= 5; i++){
  if($("#ctype" + i).is(":visible")){
      codeTypeValues.push($("#ctype"+i).val());
      }
   }
   console.log(codeTypeValues);
   if(codeTypeValues.indexOf('Adwords Conversion Code') != -1){
      $('.tag-add-policies').show();
   }else{
      $('.tag-add-policies').hide();
   }
}

/*Adding More RLSA Task types*/
function addMoreRLSAs(indx){
  nextIndex = indx + 1;

  rlsa = '<div class="rlsa-codes" id="rlsa-impl-initial'+nextIndex+'">' + 
            '<div class="row">' + 
                '<div class="col-md-4">' + 
                     '<input type="text" class="form-control " id="user_list_id'+nextIndex+'" name="user_list_id'+nextIndex+'" placeholder="User List ID/ Audieance ID">' + 
                '</div>' + 
                '<div class="col-md-4">' + 
                    '<input type="text" class="form-control " id="rsla_bid_adjustment'+nextIndex+'" name="rsla_bid_adjustment'+nextIndex+'" placeholder="RLSA BID Adjustment(%)">'+
                '</div>'+
                '<div class="col-md-4" >'+
                   '<p style="height:80px;text-align:left;font-size:13px;line-height:19px;color:#8c8c8c">'+
                  'Check PitchIQ or <a href="https://goto.google.com/rlsa-bid-dash" target="_blank">go/rlsa-bid-dash</a> for customer  <br> specific recomandations! we recommend at <br>least + 40%'+
                    '</p>'+
                '</div>'+
              '</div>'+
               '<div class="row">'+
                  '<div class="col-md-8 row" >'+
                    '<div class="form-heading" style="font-family:none;margin-left:17px;">&nbsp;</div>'+
                  '</div>'+
                  '<div class="col-md-4" >'
 
      add =     '<a id="add_rlsa'+nextIndex+'" class="btn std-btn task-btn" style="margin-right:10px;background:#109d59 !important;" onclick="addMoreRLSAs('+nextIndex+');"><i class="fa fa-plus-circle" ></i>Add User List</a>'
      remove =  '<a id="removeRlsa_'+nextIndex+'" class="btn std-btn task-btn remove-rlsa" style="display:none" onclick="removeRLSAs('+nextIndex+');"><i class="fa fa-minus-circle"></i>Remove User List</a>'
                  '</div>'+
        '</div>'
    $('#add_rlsa'+indx).hide();
    $('#removeRlsa_'+indx).show();
    prevIndex = indx - 1;
    $('#removeRlsa_'+ prevIndex).hide();
    if((indx=>1) &&(indx<4)){
     $(rlsa+add+remove).insertAfter($('#rlsa-impl-initial'+indx)); 
    }else{
      $(rlsa+remove).insertAfter($('#rlsa-impl-initial'+indx)); 
    }

}

function removeRLSAs(indx){
   prevIndex = indx - 1;
   nextIndex = indx + 1
   $('#rlsa-impl-initial'+nextIndex).remove();
   $('#add_rlsa'+indx).show();
   $('#removeRlsa_'+indx).hide();
   $('#removeRlsa_'+prevIndex).show();
}

function validateDynamicFields(elemId){
  if (elemId.is(':visible')){
    if (elemId.is(':checked')){
      //do nothing
    } 
    else {
       window.failedFields.push(elemId);
       window.is_error = true;
       elemId.parent().addClass('error-box');
       return false;
    }
  }

}

function rlsaInternalCIDPrepopulate(){
  if($('#rlsa-impl-initial1').is(":visible")){
    var cid = $('#cid').val()
    if(cid){
    $('#internal_cid1').val($('#cid').val());
    $('#internal_cid1').attr('readonly', true);
    }else{
      $('#internal_cid1').val('');
    $('#internal_cid1').attr('readonly', false);
    }
  }
}
/*Ends Here*/
 $('#active_campaigns').click(function(){
  if($('#active_campaigns').is(':checked')){
    $('#active_campaigns').val($('#active_campaigns').siblings().text());
    $('#paused_campaigns').val('');
  }else{
    $('#active_campaigns').val('');
  }
 })

  $('#paused_campaigns').click(function(){
  if($('#paused_campaigns').is(':checked')){
    $('#paused_campaigns').val($('#paused_campaigns').siblings().text());
    $('#active_campaigns').val('');
  }else{
    $('#paused_campaigns').val('');
  }
 })


  $("#tagImplementation").click(function(){
    if($("#tagImplementationBtn .check-icon").is(":visible") == false){
      $('#ctype1').prop('selectedIndex',0);
      $('#tagAddwordsCheck').hide();
    }
  });



//to check whitelist cids for picasso
function checkID()
{
  var cid_to_compare = $('#cid').val().trim();
  var cid_to_compare_with = ['530-633-4889','270-120-4329','203-639-6827','850-166-9935','696-163-3212','666-208-8600','919-624-9140','225-442-7239','872-219-5759','842-969-6157','369-047-3229','273-477-6884','151-502-3475','693-990-0414','448-863-4271','552-478-3202','442-014-7314','814-887-2273','209-436-3612','193-991-1867','281-961-8543','486-162-9627','288-908-0073','403-095-0920','602-843-8999','144-647-4420','137-428-5553','300-302-0902','135-882-8083','647-931-5889','285-023-7274','383-141-5659','422-050-9186','394-212-1540','340-594-6072','627-891-6061','575-624-0858','402-807-8006','960-160-4635','842-101-8414','519-648-5458','796-172-5872','147-474-9029','282-478-3829','261-981-9455','977-115-0878','342-519-6720','604-677-8678','800-252-7324','359-735-2883','567-252-3381','453-193-3829','985-279-3078','112-682-0026','807-193-7667','830-129-1916','526-824-5986','108-541-0415','968-956-9783','938-990-2116','638-373-2018','571-299-9406','777-693-9724','159-035-4323','885-425-1438','668-228-1929','703-598-3369','260-794-8824','484-402-6375','627-913-8486','172-131-3192','470-520-8961','538-763-4230','775-464-0957','990-703-4476','615-194-0833','167-049-8551','730-958-2951','176-232-6286','867-464-3120','567-469-9514','844-757-3884','274-565-4075','890-871-0781','379-686-3846','214-372-9242','812-991-5080','349-865-3690','534-941-2782','873-261-0653','930-472-5425','205-222-0273','608-879-7221','483-979-0678','696-878-8730','538-425-5206','311-817-4022','261-452-6369','239-524-4608','700-086-8626','391-010-6406','897-537-7926','317-866-0059','890-133-3263','327-986-6055','967-746-2029','221-668-7926','264-237-7259','776-802-5756','267-340-5389','730-745-0576','497-361-2981','857-974-5872','150-726-5936','472-117-8129','597-378-7602','963-485-3539','279-453-2610','578-655-8765','451-671-1198','852-854-3606','871-215-6396','426-775-8332','695-085-1414','981-290-5449','124-449-9329','941-599-2753','474-566-9828','968-954-4172','925-985-5827','690-955-0040','941-548-7103','844-593-0180','243-323-1802','861-264-3828','669-939-0502','946-146-5840','522-219-5924','919-146-3610','775-170-0082','719-145-3630','590-263-5188','394-805-0855','231-617-2049','348-079-4660','602-812-1036','601-710-6145','493-119-9229','705-551-2169','196-681-9671','804-869-0561','883-392-5684','522-956-4840','934-369-3030','670-334-8437','227-375-9280','590-865-4463','946-079-8432','562-599-3310','765-288-3877','972-950-6000','832-262-6566','280-769-4959','789-218-9310','926-870-5636','587-063-4429','511-869-2033','557-622-7406','344-798-8155','705-680-8572','338-759-4622','511-816-5367','362-854-1290','803-767-5232','207-672-1602','570-912-2989','989-341-2624','899-061-7831','844-584-1463','129-788-8724','799-671-5714','732-899-5357','432-952-6627','710-334-7420','705-391-3969','760-871-3704','674-391-4202','467-788-8839','177-184-3838','194-344-5663','939-954-0412','280-206-0365','382-431-6583','342-032-8161','435-879-5284','105-550-9571','501-067-2022','167-751-0238','613-056-5832','842-091-3731','887-732-1973','223-686-2740','440-518-0008','986-750-2325','930-193-5900','255-210-2580','367-996-9483','103-005-8910','157-448-1831','493-391-8124','640-425-9426','124-908-9831','173-264-2637','605-453-3453','906-588-1351','572-595-1939','986-415-5653','393-797-5598','577-563-5002','694-396-6929','492-533-5859','807-053-1461','668-768-6629','914-884-3724','768-326-4212','817-915-8383','586-387-1671','827-606-4363','466-049-3377','768-086-4123','615-639-5751','524-419-2924','859-582-6684','509-315-1387','351-309-0040','581-744-4537','989-592-6438','400-134-8674','428-612-8622','439-032-6670','923-037-9175','317-779-8736','194-435-4526','768-612-4304','476-404-1629','361-585-6606','571-959-9383','117-054-5474','773-185-2421','107-675-0814','891-806-9129','697-022-9657','674-834-7736','396-693-4534','527-453-9651','826-840-8190','184-849-6640','635-171-6006','168-700-0981','991-956-3290','648-622-6090','804-795-3979','577-642-2108','211-811-0970','318-330-2571','682-390-9121','641-072-8969','271-913-7878','794-508-8971','778-030-0606','279-635-3125','381-748-3833','114-410-0162','716-980-8436','823-516-7523','147-655-3278','332-378-5678','244-860-0110','155-977-7802','252-572-9524','942-617-4321','365-679-8980','378-730-9227','466-917-5785','284-575-3676','805-542-0349','877-734-5337','158-472-7563','223-674-9010','705-708-2822','237-588-2326','710-367-0861','911-710-0476','624-371-7969','386-748-0887','460-406-4380','674-120-6678','981-431-4274','615-526-8475','827-300-4978','427-899-9718','162-070-6738','603-682-9908','270-272-5921','298-237-4381','825-138-0670','511-229-3230','458-832-8025','280-220-9929','906-545-6869','802-950-2221','741-988-1977','754-112-2673','804-309-4022','845-647-3029','975-887-2759','774-077-4443','334-441-5988','606-647-3826','489-237-1528','396-470-9330','158-818-4971','470-202-7319','311-528-6055','615-521-3681','966-633-0979','737-025-2485','127-411-7621','189-205-5640','130-802-3157','135-289-0979','983-784-7076','830-035-2672','801-062-8970','598-747-7710','366-250-6928','320-412-0510','644-012-5824','769-023-9880','968-416-5028','741-852-4927','157-752-7729','264-162-8238','358-861-1031','457-396-6487','636-977-2480','648-665-7373','294-413-7675','607-530-7624','993-938-8812','997-698-8914','929-098-7439','791-980-8655','815-877-3778','986-460-3925','874-438-5581','229-990-2980','442-516-5337','947-775-6573','488-172-0089','484-536-3737','743-267-0896','535-288-0373','218-638-8559','337-636-0770','453-008-9984','929-817-2653','704-385-6434','477-225-4451','575-519-5858','614-443-9422','765-032-2778','951-972-5885','650-107-5481','124-114-7727','487-428-8865','197-341-8675','820-427-1728','337-894-5504','456-930-3204','894-016-1009','101-351-1131','445-172-6440','668-339-3339','545-575-9651','934-247-8728','445-242-5022','422-337-0979','597-621-2529','629-086-6114','265-979-7702','523-889-7289','883-186-6943','306-043-5330','344-062-9502','286-776-0371','487-084-2653','105-746-3599','950-090-3536','622-062-4074','729-967-8632','100-481-3340','281-453-1336','622-973-7012','352-422-5655','952-406-0787','760-125-1221','706-047-3157','506-457-5366','401-899-8178','799-273-3336','698-353-1247','771-242-0167','298-171-7186','662-311-8929','694-586-3657','463-233-6030','500-156-5865','233-651-4059','835-210-2375','755-576-9882','316-161-7606','867-868-1140','837-412-3080','348-748-5490','318-424-1625','244-646-3075','522-026-1311','733-652-2174','828-716-5970','633-784-0870','667-692-0837','790-246-7329','339-778-6733','538-847-8739','202-002-1204','250-222-7881','328-630-5522','741-188-5189','211-756-5489','849-678-6348','337-703-8073','142-979-2500','999-916-1114','554-857-4178','139-147-3668','602-563-4984','436-614-8039','713-208-1587','266-598-6474','322-169-7023','376-784-9716','685-112-8447','974-257-1728','918-707-4702','776-737-0077','437-363-9655','266-918-2914','688-515-3804','659-555-3690','357-648-1488','380-661-7508','448-381-0936','428-875-1859','154-706-6924','105-978-2270','916-207-0577','365-891-7350','570-327-0705','857-109-1679','673-308-0274','413-317-9324','560-977-6126','593-353-6931','405-906-0977','723-222-0829','571-149-3082','714-830-3316','281-959-5706','979-120-9826','394-734-2438','254-786-6673','487-854-9270','115-160-7779','413-434-6516','105-565-3222','794-241-3589','672-137-0778','682-664-9725','276-791-6155','223-071-7316','306-417-1978','170-525-5027','301-824-4961','804-856-4667','110-243-0711','964-330-1618','945-948-1083','634-559-8269','212-373-5664','800-920-0940','534-064-1227','895-931-7117','680-470-5563','176-272-5412','840-615-1151','213-547-6979','429-590-8863','803-587-9350','425-120-4630','915-491-7953','189-010-0354','394-645-6612','111-148-8620','119-791-8874','546-723-4623','212-794-5492','201-044-8608','726-050-3027','931-643-9816','117-759-5409','298-138-1271','296-370-1526','834-868-5581','276-663-4580','976-926-4876','990-008-9429','629-594-4429','270-243-3969','156-131-6748','227-518-9814','727-155-8950','377-643-4625','155-117-5994','111-775-3620','404-736-1679','986-267-8327','146-820-4659','498-360-9081','308-794-6678','755-395-2006','306-871-0395','689-420-8889','284-228-0282','218-284-0573','145-310-0228','447-155-0869','700-583-5592','899-582-9669','341-305-7902','750-744-7371','473-401-3320','510-773-0465','879-605-3233','853-614-4512','879-636-3377','297-028-4414','745-798-2506','335-792-1521','711-498-9110','493-125-7132','181-941-5272','641-729-6629','384-071-0023','204-139-6833','363-354-4025','828-988-5908','474-150-1174','388-655-7683','795-238-1982','904-987-2357','246-803-2429','386-836-4159','304-229-2070','107-335-4133','761-368-3524','994-998-4684','123-215-6921','816-414-9270','459-465-4900','536-566-4357','298-396-2338','549-432-5744','797-407-0889','506-344-7122','514-506-9429','328-223-8219','991-546-2727','622-911-5381','775-679-4278','300-768-1501','797-803-4332','178-915-3940','290-576-6185','899-289-1378','935-229-4270','455-325-6640','448-523-6382','154-930-9167','555-036-2621','935-659-5329','153-972-6223','423-279-7438','584-913-6708','218-068-5081','600-533-1457','160-671-6031','951-702-6788','602-882-4578','508-842-4728','622-020-7196','508-736-2969','548-487-8684','975-485-7396','758-075-8869','926-006-0908','266-983-2735','403-846-0723','467-270-2322','287-934-5206','666-238-8181','659-385-6300','117-913-3582','793-308-8016','600-823-5052','985-995-2981','143-536-4316','442-634-2902','480-548-9370','324-286-2886','656-016-4682','449-331-8355','276-205-9136','235-957-0672','942-916-3824','921-531-1306','116-942-9514','382-923-0126','307-434-4879','248-560-0865','580-929-5306','600-646-9331','555-530-2838','940-057-0224','474-039-8376','596-599-4389','467-442-8517','553-049-0737','605-497-0614','889-540-8263','422-037-1153','948-155-8173','230-172-1404','373-000-4402','246-176-9210','836-060-1521','257-621-3070','347-915-0073','140-515-6057','794-528-1240','496-317-6163','962-711-3767','945-783-5228','203-567-3157','864-228-1125','197-018-8157','709-660-9555','608-493-2310','397-903-5772','949-483-2969','471-603-7441','350-250-5096','659-824-5298','819-189-4274','231-003-5102','237-653-7720','268-431-6240','271-896-5747','238-634-3632','936-864-8174','549-503-4551','176-647-7961','150-731-4124','613-791-2331','540-054-6822','602-675-4451','591-500-9553','730-669-4006','477-331-1680','383-839-2813','970-968-1076','711-181-6365','431-037-7090','305-480-9238','650-694-0752','300-600-1638','820-106-2659','776-574-9280','222-000-8379','404-258-7082','761-149-4069','582-680-1389','184-470-7912','929-027-7296','153-850-0780','507-863-0167','853-558-7475','932-560-4879','992-709-7816','105-736-7138','287-516-0431','197-568-2987','686-276-3116','595-615-1255','454-076-9538','450-202-8155','346-146-8102','264-029-5481','431-287-3930','801-219-1321','760-776-6363','845-970-4325','178-353-0577','242-855-1230','420-521-9132','390-061-2864','460-820-6485','651-765-7173','179-424-4524','287-668-2771','545-721-2074','739-626-2379','467-993-6932','139-992-4386','909-323-6814','646-498-8274','400-464-3506','478-598-8990','365-056-0967','760-782-3088','243-614-1673','739-803-3663','491-957-1774','975-180-3714','987-945-3281','955-555-0078','937-293-7029','144-450-0036','962-066-6273','599-057-1083','763-093-1073','233-454-1021','852-396-3602','672-519-2316','302-569-4247','975-232-2926','572-371-5324','729-824-8721','556-206-4898','449-291-2463','265-531-7128','552-310-8369','401-198-2989','765-793-5618','292-632-7606','974-753-3759','446-377-0663','987-897-2812','372-202-6479','492-782-5130','189-007-2439','617-105-2485','915-807-1200','549-176-9730','795-533-2059','306-057-7370','436-126-3469','232-511-7286','888-252-3821','663-176-2514','788-426-1506','983-996-0038','893-352-0298','209-016-1853','757-547-6116','768-936-3977','334-267-9520','311-475-3406','363-126-0340','365-013-7468','286-213-2208','756-115-5657','438-394-3370','378-699-6104','167-629-9453','142-246-4233','278-409-0279','774-911-5378','269-384-5776','491-776-3878','322-819-1129','260-825-9861','836-248-0782','577-677-9482','509-915-4721','820-719-1084','624-414-5440','989-213-9781','295-671-9302','832-772-5339','121-265-4680','957-899-4851','649-524-0541','924-762-2429','645-167-2769','558-670-8840','203-940-9665','373-789-2785','983-821-9823','467-424-3089','676-759-4637','483-874-7474','378-480-9000','712-711-9731','550-228-3221','114-077-5812','932-148-8878','642-072-9704','956-244-2342','180-853-2971','276-648-5136','692-461-9735','989-385-5941','916-088-9225','953-695-1630','689-578-3489','152-144-9800','511-312-5580','527-531-7810','998-689-7040','371-748-3622','465-682-9980','356-749-7108','450-171-3036','774-559-5612','248-884-4530','459-709-2839','132-150-2914','247-303-4151','966-976-9627','836-113-1071','757-846-8423','602-195-7162','215-376-5616','202-269-2524','625-524-4163','828-783-0979','362-803-9057','193-678-5369','465-126-2639','579-704-6820','793-869-8002','992-521-7567','513-132-0730','712-594-3349','674-254-4728','176-424-0338','841-243-9018','801-996-0121','565-549-0588','630-406-9825','106-651-0830','411-918-0025','601-615-9677','135-086-3177','544-294-6359','641-388-5663','521-368-2723','426-668-6663','186-453-9457','247-311-5779','894-214-6689','422-648-4878','572-967-9910','215-636-7289','525-729-5814','314-882-9027','342-643-8624','569-628-5034','801-601-7749','414-801-5453','425-039-4079','641-283-1123','720-926-6838','739-199-7004','492-240-7263','153-398-5060','502-165-3678','117-569-9474','282-866-1284','378-812-8410','240-293-5059','619-927-5722','404-677-2465','833-390-4566','192-988-6179','429-324-6778','466-208-9771','147-575-1329','490-354-6974','401-158-2157','265-221-0643','183-265-0222','753-609-2576','852-381-0526','738-108-5465','773-466-5228','965-605-0436','349-052-9622','389-311-0430','290-998-1834','681-011-6076','226-337-2651','257-747-3524','155-953-7740','484-880-5972','153-532-5031','998-283-8074','127-914-6187','591-998-0181','613-303-8857','617-076-4035','182-416-1604','545-252-0626','764-495-2021','241-333-6133','404-090-2474','582-778-7623','162-162-5924','119-200-5265','297-352-4687','205-340-2318','434-300-0213','283-531-1230','410-267-0231','487-486-9487','749-864-2676','503-097-0679','382-351-0672','813-320-2328','448-343-2008','747-991-4319','392-044-7676','490-205-4540','745-571-5720','907-229-3051','772-579-1424','447-267-8365','830-207-1038','277-282-5208','694-436-2921','885-159-1414','449-175-0121','826-010-1921','196-436-6624','906-957-9804','110-242-8295','773-196-4953','826-929-6122','928-430-3978','682-247-5618','837-095-5883','571-661-5055','194-870-7305','677-975-6272','693-941-8757','721-444-1051','620-505-7714','995-080-8302','283-850-8618','219-309-1673','434-096-4104','317-128-5800','493-103-2861','106-570-6172','720-138-4523','134-903-3377','933-038-4281','828-551-7731','650-314-3477','551-486-7822','952-713-4582','334-966-2627','611-713-3913','881-295-7363','975-152-0667','842-917-6072','217-081-0085','340-592-3545','602-091-8788','198-726-6569','942-278-5702','377-084-8279','295-108-0328','889-267-4255','275-360-5819','588-137-9630','496-011-5785','204-338-1790','496-052-9261','977-200-8629','156-200-8989','830-638-6577','493-138-4512','106-682-0331','933-849-7478','739-070-8280','850-364-3326','374-062-8709','839-285-8283','636-959-2890','371-339-9953','711-624-0459','241-122-7233','719-643-1039','712-605-7472','946-454-5976','700-395-4555','684-214-5978','303-704-8330','808-208-7861','602-896-5555','331-063-7594','941-297-4800','683-727-6256','916-274-2880','756-938-1176','808-049-7500','862-923-8967','679-109-9802','637-442-1638','238-063-9226','117-168-7075','743-109-9783','343-054-4840','485-971-9372','361-818-9812','776-873-5979','463-334-9008','319-633-1527','682-996-9180','928-426-6228','442-930-4838','531-018-1120','464-866-6424','914-395-2848','625-076-4612','130-573-4557','352-749-8080','585-985-2406','819-718-2735','803-080-5665','789-090-4178','241-747-8328','535-312-4487','312-153-6067','928-886-4429','780-315-2623','801-426-0575','421-134-6409','126-282-9763','521-081-6310','507-841-8325','210-560-9638','105-186-2025','966-977-6278','810-753-4132','375-402-8231','182-149-5034','914-074-4937','284-844-5104','226-159-4551','650-192-7599','116-208-6274','788-696-4620','897-378-9161','457-267-2090','363-626-4676','518-084-0489','144-317-3137','523-873-2637','302-240-6051','388-928-5923','264-465-1669','512-841-8523','363-711-8002','515-283-1728','159-231-8474','487-030-0071','425-002-3378','401-356-5418','381-306-8216','857-315-9122','708-490-4404','258-370-7835','991-725-1928','189-370-1978','774-045-8361','809-865-0010','448-148-3563','786-681-3526','405-224-5321','762-494-2219','487-058-8236','388-581-5238','408-951-3590','300-888-0470','566-722-1853','826-618-4722','431-925-6212','836-432-6733','384-178-9136','501-975-0757','836-271-6034','648-599-1536','899-492-2712','460-800-2487','575-415-3692','542-593-8732','969-842-4612','632-665-7785','105-034-0263','211-423-9118','799-230-8091','689-873-2826','619-850-3281','856-473-4678','559-528-9249','535-642-6753','356-516-1538','832-594-0518','991-712-8080','779-151-0983','909-136-0547','230-991-1224','657-546-4236','357-079-2130','507-441-0351','362-219-2776','540-389-3434','231-946-7534','366-160-1004','569-270-0824','395-282-9194','598-401-6490','864-435-7240','854-239-4429','828-920-5716','130-191-2834','585-148-1110','802-609-2263','390-718-2355','999-375-6289','529-908-0436','585-488-8759','770-329-1463','338-595-9800','355-272-8077','615-793-3629','677-044-3806','824-465-3781','951-487-1371','424-782-2832','371-591-0618','780-047-9067','332-828-3176','140-248-6053','843-476-8051','528-601-8710','928-318-0639','372-051-4592','110-360-1490','386-541-3824','874-237-9095','203-321-6278','465-205-8920','532-239-1238','437-863-7990','861-670-1108','605-127-6516','192-549-6558','592-210-0427','248-591-8633','718-240-1329','238-102-6173','998-313-5969','355-368-3277','182-600-1059','809-446-4332','677-657-6706','486-946-7581','660-292-7431','332-165-4704','757-230-8306','879-667-6913','255-461-5116','955-410-2928','374-222-4828','982-574-2076','530-447-1974','216-120-5522','178-206-0910','107-112-5990','392-368-6676','595-403-4761','150-148-7606','900-284-2039','141-382-6241','536-336-1577','205-033-8283','376-918-1300','237-358-5534','649-775-5916','129-501-4827','365-163-9222','690-544-5710','229-708-2804','448-980-6836','857-221-6061','539-185-9439','215-127-7583','405-895-5934','746-384-7472','941-973-4879','189-729-3782','302-551-9137','971-991-6610','203-155-1853','259-250-0779','378-364-6563','212-500-6153','158-337-6814','314-538-2775','915-044-3970','439-338-6828','963-344-3121','778-983-9932','827-781-5061','860-217-8985','448-612-3466','159-696-1131','326-483-8940','319-642-6292','352-226-5481','812-307-1687','987-836-4888','715-560-4719','870-306-7976','175-582-9161','344-526-0563','330-486-2986','900-911-3680','876-140-3741','961-128-2084','552-763-2786','866-523-9906','329-102-8289','677-712-4318','324-075-7678','440-698-3159','310-085-0683','884-376-9381','691-707-8483','535-397-6735','939-681-5021','952-508-3385','892-138-0122','823-305-2012','884-850-9172','391-832-1757','776-826-7859','723-536-7240','296-591-0559','644-258-3946','689-720-1729','449-481-0669','601-491-5214','616-851-1429','901-514-4656','289-386-0763','354-121-6398','431-987-7788','464-332-9830','707-484-3067','632-112-8274','618-437-9271','538-665-6796','942-495-7345','663-683-6499','897-531-1751','955-848-9012','759-358-9385','698-963-5752','459-959-4932','390-917-6029','334-016-9628','325-305-2836','784-324-7514','645-804-9678','260-236-5502','992-887-5751','953-042-6470','753-241-2683','131-376-9973','818-992-9878','665-574-0759','454-671-9859','693-489-8082','155-298-6724','334-308-1690','166-145-2153','749-028-6758','925-642-6734','686-234-6063','581-698-8671','702-441-0010','649-395-2420','533-092-0570','200-112-5824','384-952-5874','339-659-6814','846-197-3875','737-278-0624','295-544-8480','171-297-0086','276-322-7221','839-181-9021','480-263-1274','799-997-5690','831-625-0940','517-210-0048','395-346-2176','174-391-5112','164-461-9506','921-118-7333','568-725-0102','464-565-7223','968-625-4395','217-800-6830','755-033-3070','132-548-3426','335-730-3872','666-032-8432','238-823-2278','396-066-2010','306-908-5536','162-075-7630','926-380-5245','784-688-9612','855-904-0345','115-753-8277','786-027-2220','861-831-2470','678-828-2565','190-038-9141','262-767-2267','440-111-8881','704-371-3681','405-623-2559','198-802-8927','193-756-7165','924-916-2761','705-783-3999','725-256-3179','210-789-3478','538-195-0570','986-942-7130','649-595-8981','376-538-9823','907-286-3285','195-056-4239','762-672-9289','243-672-0494','105-506-3410','565-705-0753','853-867-0435','296-973-4233','132-299-7379','375-247-1718','516-446-3933','108-108-4040','672-333-6885','620-798-8536','528-329-4820','512-721-6680','691-495-0888','500-902-4736','237-142-1465','560-399-6030','984-561-7877','230-922-3783','134-583-9786','378-421-7780','698-620-4538','803-450-3983','290-388-6789','528-032-7181','658-073-2814','519-867-6649','920-570-1415','879-908-0884','169-208-7908','200-221-1783','653-899-0432','573-429-8527','134-828-5339','393-030-5968','703-752-0772','652-005-4773','823-349-2920','665-837-2888','401-901-3361','327-565-3010','703-597-9792','262-612-5284','670-752-0883','115-564-3375','151-610-6365','959-195-9548','434-609-3581','877-756-1829','842-320-5175','971-460-6500','345-140-5772','114-335-5376','771-714-6128','574-586-8114','293-339-8617','904-597-7165','328-837-3753','102-237-2381','436-628-8028','762-390-0043','908-980-2038','233-427-8382','781-154-5638','484-404-4472','935-595-0528','800-546-3729','297-859-2694','184-329-8024','274-843-4440','633-676-8553','484-908-5072','730-590-9974','693-664-3377','953-747-3008','295-053-4622','446-651-8816','540-369-3826','766-909-8520','670-458-2472','333-689-9474','477-882-9925','868-754-1412','835-910-9067','849-673-8718','648-831-9602','167-448-3678','122-477-8510','326-205-4773','468-638-5949','917-375-6533','212-841-3312','948-261-2738','153-525-6730','523-585-7737','949-643-3270','210-762-2382','430-228-9404','273-108-2073','879-528-8201','921-950-6529','560-811-1736','390-209-0728','323-277-5070','200-398-6514','673-561-9374','374-235-9029','603-470-7103','313-661-6140','725-619-0587','406-591-1854','709-075-9482','232-730-5788','558-119-5390','310-407-1861','862-202-3267','813-628-0588','994-487-3139','749-737-7622','160-674-9131','868-015-1810','718-228-5973','583-421-2575','943-916-2428','931-260-5076','622-541-6115','568-089-5865','441-275-2014','657-922-4379','482-205-7097','536-819-6936','555-018-0222','163-375-8106','692-623-1262','778-099-9763','312-728-3926','982-346-1170','399-139-7923','841-666-8324','971-282-2572','154-167-5436','923-323-1408','957-496-7872','559-079-4040','857-595-9450','510-117-0872','982-589-4584','200-473-4802','768-325-1978','509-955-4880','211-948-7150','197-913-6688','188-919-8677','664-556-3083','333-525-4189','303-688-8263','935-863-1528','696-348-4053','512-089-0583','976-058-2478','580-176-4987','388-950-8363','642-581-5718','431-086-1526','197-679-9790','102-544-8755','243-221-3061','940-252-4387','363-229-0002','927-962-9489','623-011-5112','186-121-6983','771-836-4830','103-042-2925','806-625-1163','830-062-9951','184-600-5453','997-418-1322','259-169-7169','204-180-4171','305-139-1771','523-777-6514','818-893-5297','901-519-2879','776-275-6963','690-827-7980','101-050-1890','201-988-9627','613-804-9276','690-234-8540','821-038-5383','743-285-4073','583-089-7930','542-804-4778','857-583-9324','688-192-2343','675-473-3202','519-735-4480','275-117-3223','901-184-7000','183-977-6357','816-015-9473','242-154-2772','731-860-9786','143-362-4171','557-375-4416','257-375-5108','628-483-1121','944-879-2737','245-246-2332','786-132-6680','270-259-7273','811-342-5832','174-116-1321','602-260-0910','164-244-4606','769-551-7000','558-134-4729','704-277-2246','534-328-1818','800-289-8988','254-522-0424','588-916-4436','450-000-6036','868-490-4150','259-569-5283','403-848-6424','197-251-2886','255-244-3020','267-637-5189','392-510-4588','479-201-7835','403-845-4127','624-379-9287','537-389-3080','178-071-8110','367-050-8621','944-658-5285','792-577-8674','884-288-9886','508-025-5729','118-307-0581','351-409-8178','932-871-5181','775-832-7596','978-421-6371','904-596-2925','313-627-9402','773-509-5353','908-775-3480','308-604-9800','922-728-7673','199-966-7733','994-986-2432','556-637-5112','470-238-3122','136-261-7479','274-550-9371','685-100-3316','417-348-1212','408-951-6414','963-966-6151','532-108-6133','543-162-3175','392-208-6585','287-065-3926','170-050-3710','903-617-7679','826-409-8624','353-826-1931','594-040-4427','647-251-4408','883-069-9781','896-608-9065','653-267-6829','379-898-7729','302-331-3926','978-631-8970','904-023-2080','564-355-4675','437-426-3167','936-776-6738','929-751-5473','471-837-4902','957-293-1938','768-365-5689','121-535-2729','574-494-2427','549-983-5812','372-854-3592','709-938-4002','931-682-1210','387-645-4889','711-490-1206','463-390-3051','367-400-6948','734-893-6690','840-703-7277','132-237-4880','285-430-4882','481-653-8622','627-725-7529','900-333-2676','877-725-2733','407-514-0936','902-238-5727','442-558-7010','427-938-2833','289-206-2047','443-990-1178','902-522-5526','592-278-8971','676-397-8793','679-534-9924','890-288-2272','577-190-4382','790-700-0921','773-765-0474','514-966-7320','704-387-8283','611-385-0782','996-940-0757','889-800-1679','989-888-0955','449-350-2555','611-076-9793','539-058-3677','716-513-6721','932-707-2320','824-837-1334','753-793-6621','107-588-2975','469-246-4918','823-787-9922','966-251-6157','398-360-2804','709-837-7545','803-986-8074','861-580-0862','112-916-3465','741-901-7790','130-302-7971','501-922-3038','105-634-6426','894-594-4912','760-356-5272','668-882-7127','255-211-2673','181-290-4127','730-757-9239','704-058-8834','490-421-3729','439-709-9008','258-939-7871','991-528-0073','988-823-5877','354-909-9481','779-528-5506','807-222-5459','104-357-9581','304-535-6953','945-774-5718','567-733-9775','895-701-8767','821-087-4084','626-930-9802','684-483-6508','315-180-4065','206-635-1867','390-507-6514','498-245-6384','313-589-8323','442-789-6691','551-010-6875','826-879-8459','866-899-3673','724-114-1010','922-681-7019','853-634-4708','263-854-5936','597-331-4767','419-852-4325','269-597-8271','516-339-1271','527-682-1655','346-901-4772','954-036-4727','684-799-9938','890-071-2810','537-640-8520','498-545-8704','104-818-0421','472-130-7540','582-016-5283','397-212-7677','523-027-7857','728-751-6932','869-567-9462','946-293-1890','307-080-5753','985-555-6534','543-385-5340','636-728-1383','427-789-5134','107-791-1520','825-052-2804','258-963-3338','432-956-8429','627-627-3056','888-927-7579','257-238-0929','621-412-6346','335-153-7961','769-828-6732','594-435-8440','824-585-9786','766-247-1051','919-347-6334','874-777-9928','535-711-7073','768-180-3332','184-294-8129','131-634-6908','175-527-0153','797-222-4250','773-861-0639','166-011-4681','490-856-3116','523-040-8506','891-978-3678','921-396-9639','985-416-6987','909-970-7963','215-660-3704','507-209-8151','588-137-2166','505-795-5171','556-848-3359','785-890-9337','685-816-3234','549-765-1032','792-859-3227','886-230-2132','235-594-5175','251-743-1159','354-438-6089','928-796-3908','197-948-0770','168-557-8904','246-085-5402','740-661-0953','610-300-6536','357-429-6718','838-214-8228','409-319-1327','740-216-7036','914-400-9338','122-318-1238','573-716-0110','248-314-2100','663-546-8496','291-527-3319','913-236-4131','753-978-2757','177-043-4428','387-795-0870','164-132-2708','181-997-4978','241-535-7912','334-805-7876','555-768-2216','174-990-7400','698-165-3732','141-617-6006','699-106-6371','854-934-9021','277-353-2387','919-848-8484','815-791-5224','556-778-9865','505-606-2863','134-759-3806','478-515-7753','704-223-0782','205-507-8314','806-601-7782','271-097-0785','887-582-1925','860-807-6123','760-727-3420','980-781-7579','525-688-7163','900-034-9006','887-401-6518','599-549-3463','576-020-5887','663-459-6875','889-569-1235','908-018-7870','187-946-4473','537-569-2724','429-498-1320','693-506-0320','990-971-0053','811-320-3592','351-552-9980','190-321-2061','662-349-1421','226-790-5085','273-737-2349','456-557-2379','357-467-9888','966-836-9309','635-497-2170','562-856-7496','882-532-6210','842-649-1225','356-243-6675','794-835-9370','107-401-5978','420-135-5024','163-830-3229','815-771-7432','497-283-9412','479-170-9257','351-010-9179','507-052-9189','875-840-8375','556-847-6423','798-613-1408','959-710-1024','476-956-8516','969-656-0119','341-076-3414','518-343-8425','421-395-2712','574-359-8429','703-152-9304','800-209-6874','230-772-4040','432-156-5908','545-615-0230','832-483-7132','639-568-2859','667-368-7320','383-838-9516','164-485-9753','980-463-9804','139-960-7371','215-490-4583','448-878-1834','781-037-8781','977-529-1830','143-380-7663','718-469-5632','443-426-1021','656-977-9718','779-225-0784','462-510-4559','287-823-6510','659-055-9302','388-170-3279','580-425-5829','735-824-8961','955-124-8081','178-345-5137','698-214-6430','668-400-3014','419-238-9679','705-914-4487','646-668-6069','345-819-1167','978-817-2385','963-461-7184','129-789-6598','599-769-9602','339-145-0548','550-613-9960','859-058-1676','203-255-6424','159-802-3170','915-681-1534','451-335-6512','933-810-1161','248-534-2576','664-433-8733','888-757-1272','465-332-3036','453-190-3638','798-681-9034','815-906-8021','475-699-2837','639-527-4028','522-584-9223','920-597-9452','928-747-1110','173-861-4737','864-418-6062','377-382-4480','833-201-2088','670-130-0179','482-771-2167','542-046-3072','807-978-1439','670-674-5228','715-977-7465','342-499-5281','964-840-7285','888-045-4209','638-499-8110','407-645-2332','909-818-7274','166-050-6548','512-715-9940','831-699-7077','987-212-2120','490-747-1674','410-379-3465','373-532-4920','133-430-5973','286-024-8162','608-042-5810','970-444-9365','922-828-5463','770-937-9937','919-398-1261','246-210-9525','306-428-5318','841-780-7759','840-403-8639','760-161-5416','852-278-5304','271-003-7214','123-262-5136','406-974-9218','197-909-6702','749-755-8250','311-831-8821','584-776-2919','859-077-5681','761-070-7433','467-791-1526','751-422-2128','213-851-1521','193-988-5383','572-896-3759','488-723-9492','882-297-6410','940-196-2590','437-596-3541','462-237-9706','513-837-4054','128-485-0628','908-611-4451','642-543-3481','246-586-6689','634-606-2802','605-746-4125','937-292-6651','355-403-0423','711-640-4063','337-318-3400','445-249-5074','165-927-4174','670-155-9106','704-840-3183','116-614-2376','299-789-8869','707-643-7810','336-209-3887','776-789-9767','934-506-2389','920-981-3034','608-290-9288','324-389-1770','958-667-7708','287-702-1630','829-003-6360','706-643-3123','167-469-2038','692-814-7075','420-231-6685','818-881-8763','379-965-6500','717-414-2785','969-714-9528','316-158-7340','856-797-2920','203-162-7508','459-880-3381','560-296-1608','671-921-3580','350-933-0022','644-614-1467','223-169-6336','676-261-4379','777-267-5532','516-992-8122','723-771-4426','489-846-6563','305-857-7200','675-632-9021','881-484-4283','101-742-5373','588-213-8171','408-291-0534','391-728-4531','870-223-4100','416-963-8165','298-156-9768','821-086-2020','455-498-5489','718-203-9430','831-554-6285','357-439-1283','718-389-6782','887-990-4451','727-633-2116','460-032-9753','213-350-7818','482-063-9210','217-590-5524','527-227-0834','313-692-6439','581-309-6363','610-582-3778','112-580-1530','586-013-5453','170-561-9002','255-673-7138','939-510-4419','251-238-0016','807-420-5636','795-144-7210','547-289-0771','504-208-9280','230-352-2171','120-749-2073','697-826-8112','275-301-4604','356-696-2878','925-201-0469','279-976-0684','511-235-9635','514-218-3338','993-835-0588','379-352-0616','733-328-4272','583-731-1821','924-492-9718','731-689-3939','906-250-1554','612-689-4706','103-620-3061','299-735-8228','653-252-0714','812-618-0208','483-207-6787','962-974-0926','707-949-6865','906-918-0773','288-759-7399','663-924-8667','858-536-1486','960-978-1108','473-123-8588','387-988-1218','857-508-6451','330-889-4680','862-961-1869','283-584-3774','721-516-9026','348-981-0004','126-242-4744','474-531-6206','915-296-4130','258-522-1738','656-095-7271','479-783-0138','420-096-8930','215-344-3183','658-185-0380','239-156-9620','973-686-8938','971-439-8140','222-103-8361','322-561-1560','769-158-6667','474-965-3927','694-480-6573','233-592-1118','347-115-4951','440-750-7121','490-972-2589','221-162-2933','813-500-2835','313-058-4436','951-970-1407','974-866-5610','882-748-4281','217-846-6713','151-819-2798','329-451-7829','360-222-5229','920-199-0223','636-273-8271','847-912-8865','101-690-2434','310-192-3335','182-792-6527','391-197-9929','717-349-5998','900-170-3102','931-642-7737','887-291-0343','527-999-2569','740-040-1705','388-489-8018','263-267-9757','381-604-9980','946-760-5276','906-160-4870','912-472-3394','198-853-3769','488-228-4980','230-721-1434','217-713-2010','473-893-1888','949-244-4116','666-239-4857','816-323-1122','526-084-3167','264-294-0602','693-541-8742','239-080-0771','452-997-3635','130-424-7926','834-877-4463','677-108-4057','535-817-0685','490-510-6471','734-918-5404','195-764-7224','406-866-1883','945-631-6780','220-676-0177','907-933-5019','212-951-0322','969-057-0052','688-105-0227','534-027-3370','887-079-9257','373-782-8491','572-632-7175','394-396-5375','421-800-5077','112-289-6469','126-669-0379','836-622-9559','332-064-6676','323-128-0032','450-819-1176','308-450-0751','868-452-6508','836-048-6190','113-600-1808','765-158-2314','522-591-2614','349-750-3259','858-455-1953','918-669-1587','827-248-5781','583-547-3539','387-359-4802','921-879-9370','452-796-5033','502-084-4938','110-647-3271','938-333-7070','429-562-0618','320-011-7061','838-245-1816','539-783-5496','476-165-3061','295-207-8736','335-636-0028','533-417-5481','673-388-9019','369-508-8504','599-930-0916','745-055-3118','931-882-7996','545-851-3482','941-774-7138','164-451-2702','914-228-2730','884-585-0939','932-167-7120','442-295-4458','923-728-0241','321-153-6421','586-187-6421','447-933-9727','126-397-5271','326-870-2400','129-953-5497','256-400-3137','534-035-0826','806-516-2710','703-243-5318','443-328-7824','580-212-8867','322-483-6085','585-655-1951','953-761-7537','275-490-7725','202-563-7586','255-263-0259','320-730-0904','666-151-4559','687-588-6602','455-762-2063','256-315-4028','926-402-9081','649-544-6585','121-540-9769','921-251-5838','696-895-2034','274-945-7951','772-488-1838','599-925-7218','236-427-6785','633-058-5524','669-847-7912','687-155-3406','223-763-0521','849-008-7659','308-189-6174','777-833-7383','152-083-5728','909-045-5506','311-113-0633','344-580-6279','767-357-6760','873-598-2078','351-865-9267','630-684-2536','740-674-0734','939-837-0346','265-122-7771','121-962-9485','744-075-1716','248-278-0784','532-332-6490','572-393-6371','138-954-6129','547-656-2830','314-111-0286','796-858-1404','903-748-8432','133-548-2520','759-564-8016','937-058-9683','379-879-6853','458-360-3172','699-377-7772','415-549-4202','829-911-3134','819-121-9990','137-644-5540','358-253-3120','168-696-8834','238-776-2357','947-669-2788','984-044-6055','394-610-1049','240-537-5184','547-748-6806','445-906-4785','687-057-2825','405-505-6965','834-841-3227','834-784-3926','549-530-4804','629-288-9959','389-450-2551','784-292-5226','701-009-7788','999-373-9460','371-354-3844','674-700-8663','253-702-0236','490-324-0602','990-252-9179','267-248-8359','325-129-4899','171-986-8921','669-008-9557','530-803-3657','468-488-0183','966-941-6828','291-392-8428','804-822-5465','254-744-5943','555-403-2081','236-140-6670','521-599-6196','960-981-8883','747-388-2535','188-949-1627','540-185-7560','819-076-0487','327-230-4577','531-190-5369','194-867-5633','819-237-8490','368-786-4077','533-231-8024','260-628-8081','432-661-2006','605-969-8924','603-908-8377','873-951-4533','833-231-5661','490-977-9024','547-990-2866','841-014-8732','100-320-0112','229-668-5589','361-481-3657','394-956-8770','416-397-0306','159-578-3461','778-325-7867','947-269-8021','541-992-4925','459-762-3272','183-904-2189','992-542-7578','648-046-3681','935-283-8978','863-459-8558','252-928-8153','675-557-4557','584-240-1677','223-297-5875','640-670-3776','983-841-9481','216-819-0420','537-784-9712','846-319-9628','571-625-0955','622-663-0202','307-460-5787','146-622-0890','875-038-4435','838-591-1380','860-386-5169','936-054-3629','203-747-1280','448-036-4789','907-134-3559','710-892-1587','754-480-1373','975-528-9272','414-940-6796','432-372-5780','378-563-9279','475-752-9751','429-561-3987','866-319-2451','596-748-5575','578-055-4528','530-456-8470','682-342-0085','905-911-8438','250-694-3489','614-631-9416','568-443-1887','372-549-0723','836-391-6281','266-712-7002','116-166-7220','291-852-6524','475-580-8721','471-695-2725','169-808-9406','521-077-4050','903-382-1283','483-413-6376','795-512-7621','433-866-6059','956-397-8149','785-235-9549','681-173-9827','432-770-5399','958-787-2182','183-616-4440','874-946-4271','983-797-3065','834-170-4705','675-558-0255','926-198-0998','693-319-8836','940-358-8940','902-156-5826','279-976-0529','271-341-7934','166-445-3900','843-544-2540','555-430-8690','884-959-6837','325-664-9280','776-482-7270','447-945-6206','306-607-1865','342-778-3140','938-761-7308','408-119-5312','325-801-2861','818-834-1108','336-721-5730','280-636-6214','359-947-0425','796-847-8032','853-529-3077','172-960-7820','531-279-7028','434-435-5302','137-054-2159','793-422-6773','456-655-7965','483-941-6180','907-721-1914','190-404-9659','459-476-2687','164-229-1400','346-185-3971','143-438-7327','956-174-3470','325-123-9097','316-248-4139','496-025-0276','340-967-2965','197-789-4839','953-445-2121','254-834-4353','696-535-7686','790-308-7522','980-757-1574','714-654-0404','767-672-7576','639-162-0824','714-741-8018','631-410-0781','863-955-4951','206-519-2074','553-228-1839','824-014-2133','409-697-5978','170-236-9614','964-562-9614','714-577-9114','304-632-3479','728-125-8578','208-458-0402','226-459-9990','909-372-5455','971-239-3555','265-623-5251','961-039-7759','167-677-8121','716-342-4936','758-353-6380','706-777-3074','932-460-9873','965-146-3661','575-704-3760','880-448-0076','798-222-2834','915-979-3971','684-844-9238','900-063-2826','988-520-9622','625-030-2873','743-016-1932','521-087-8718','157-287-4789','856-349-6053','939-730-6013','860-194-3518','159-728-8349','320-320-6029','225-436-2665','356-745-0871','116-397-6636','185-127-2030','276-863-6471','102-699-4825','269-852-5365','958-485-6813','448-982-6529','580-058-8435','899-377-2579','923-957-2478','792-522-7660','689-056-7804','462-689-6624','223-453-3511','260-340-6670','527-592-9028','156-468-9989','919-667-5638','138-663-7181','780-440-1816','702-551-7253','116-502-7269','796-724-0120','951-559-9676','953-880-3609','577-083-8381','394-371-7804','148-544-5867','869-371-0506','502-165-5689','290-741-0527','680-871-0863','795-862-0180','154-241-9457','625-931-5578','507-156-6630','405-187-1038','477-631-8002','522-117-2963','593-927-3589','502-256-4332','320-313-2918','938-675-9512','505-588-5114','511-433-4349','401-847-0779','173-516-2024','332-276-0251','763-426-1789','758-863-6479','112-799-9332','315-482-3989','937-255-1170','865-285-6236','577-168-9706','282-648-0351','690-307-9434','291-956-3780','164-711-3227','533-985-9076','348-500-9646','559-475-8671','312-171-2180','327-663-7618','442-412-2373','713-741-6310','977-689-0040','806-196-5547','913-767-2435','875-162-1429','171-619-5704','159-659-2979','326-307-1703','545-015-0633','976-178-0629','412-427-6622','409-471-2829','906-032-5236','783-959-6061','550-742-0132','830-708-7040','384-900-3883','857-616-3453','486-191-9175','722-382-9445','978-550-4502','189-890-3408','172-227-6569','398-715-8424','273-426-9771','624-609-7642','568-186-6981','645-008-7771','679-665-3228','458-925-9375','908-863-5989','568-855-6130','632-193-9030','544-876-6196','698-219-4888','262-908-5174','751-938-5818','736-441-3738','882-560-9072','383-903-0740','237-711-4665','677-619-3781','575-027-5174','592-424-1589','486-152-5772','188-420-5367','492-413-2978','208-908-1932','274-512-0040','993-794-6612','571-097-3012','490-569-6588','442-066-3029','283-409-1550','979-173-1204','505-327-6810','872-328-3504','476-230-3655','921-633-2916','295-997-8390','545-884-3369','899-186-0323','821-020-9680','142-318-0972','947-327-1004','196-206-1065','131-302-1012','597-962-3520','580-228-3879','977-356-0432','769-023-6218','576-943-4286','484-174-6372','341-709-7883','121-907-1520','114-650-6677','618-586-0014','822-942-7023','946-745-4929','832-185-1481','205-753-8087','661-303-5110','173-981-7688','176-988-1538','535-320-4109','316-332-1104','823-657-9687','914-519-8977','572-891-8340','281-759-2737','217-354-1334','351-836-3263','380-548-9374','845-998-2212','513-039-7872','806-976-2812','199-627-2483','330-873-0876','338-461-8676','220-289-8678','534-036-9053','361-853-3036','142-642-6423','517-671-3692','959-430-0143','236-398-0038','910-505-3344','571-222-8721','857-001-6583','604-700-3099','199-213-8970','174-004-9223','938-870-5771','438-571-4504','848-751-6327','362-102-7860','163-795-1283','844-837-1871','182-361-2171','856-790-2883','347-223-4832','343-352-7537','498-072-3583','518-216-3726','417-685-5761','603-205-2517','603-962-2557','842-881-1922','743-392-8451','758-073-9889','410-098-2021','496-122-6227','704-369-4826','380-255-0275','938-847-0977','951-557-6261','836-474-2783','204-514-4372','584-874-3380','687-140-6088','412-763-0025','262-696-7712','947-483-5321','430-005-1871','950-098-7833','704-828-1351','565-198-7571','902-297-2875','157-883-3014','796-973-2973','281-345-3236','468-742-6877','538-274-6561','576-435-3500','519-235-3476','785-250-7067','521-979-4134','883-783-6857','384-620-1879','769-976-3838','177-429-5822','194-396-1188','181-469-4431','213-686-8970','640-032-7855','866-144-5885','677-123-0672','492-576-1669','454-231-6991','545-751-0802','728-084-0312','344-971-1326','319-058-4696','190-410-7302','790-156-7816','881-289-8967','565-108-0779','631-149-2627','715-078-3117','585-670-3271','528-059-0390','250-159-1527','455-733-8273','911-047-5033','807-414-9949','698-270-5658','148-574-7374','403-364-0572','646-252-7518','818-904-2814','828-387-7879','503-220-2150','505-006-8176','656-419-6016','293-796-9869','447-801-1985','907-560-8669','511-870-9810','490-157-0634','476-083-4018','293-057-5372','610-199-2485','207-720-0923','457-421-7362','424-450-7179','683-900-6453','654-426-4428','595-282-2375','115-541-9249','485-688-3280','686-408-8324','500-536-3170','825-374-9755','587-130-0161','237-431-0875','363-343-5450','279-773-1974','775-563-6771','573-357-8081','811-853-8723','306-819-1203','398-596-1071','912-129-6702','669-703-7653','388-842-3522','772-689-6293','806-568-1209','157-318-3382','652-617-6087','687-798-9914','130-010-7432','777-032-0029','548-078-2366','271-742-8987','858-665-9765','538-822-4057','916-077-3714','789-812-6614','979-506-6700','138-462-5735','154-490-0231','731-054-1250','886-850-0234','895-223-0040','994-824-1810','854-655-6377','773-727-9953','552-005-5640','227-164-4502','760-271-8912','277-481-0180','873-089-1379','941-096-4477','229-152-4185','148-859-1185','845-656-7594','255-611-2983','768-881-5722','670-963-1794','201-231-3754','794-637-1324','315-506-9704','321-182-3245','189-372-1951','801-306-5083','932-326-6165','953-953-2472','244-443-4285','124-355-0630','145-407-5974','381-923-1547','764-742-8140','441-717-1208','593-382-0576','682-918-6016','636-138-5023','463-002-3820','755-419-2218','446-146-3383','324-884-6477','419-537-5140','117-073-8371','912-472-2671','952-332-8825','915-929-7606','100-825-3779','990-234-6675','351-875-2076','594-011-6072','695-645-4899','186-467-6357','395-975-2029','854-963-1150','929-877-9086','298-988-2263','759-866-7510','124-907-4623','302-780-3012','703-207-0928','724-904-4924','547-511-8086','975-268-0225','629-640-2924','191-505-0055','564-963-6738','521-065-2781','938-563-1038','157-381-4781','149-256-2337','372-762-9759','101-932-7026','475-302-3791','411-345-9473','734-456-6312','371-669-3727','519-668-7840','353-792-2229','290-855-3136','429-611-1140','983-695-1485','586-959-0312','897-083-7323','800-193-6912','918-032-5286','573-032-0156','952-827-5130','337-840-8385','561-391-1975','633-061-5730','897-991-5390','347-027-1724','623-270-0849','684-564-7802','901-642-6829','647-227-7708','411-477-6194','158-816-8970','635-302-9883','778-383-0302','206-032-9733','718-746-1802','199-225-6227','903-607-8389','171-247-2483','309-161-2116','142-510-4524','794-477-1508','113-487-5690','369-542-3216','606-776-2102','147-610-8190','210-643-7123','245-873-5261','580-077-1827','940-489-0508','156-869-6995','400-650-9570','629-598-7114','568-160-9710','244-934-0729','862-000-6123','932-390-5173','943-521-5361','134-065-8987','859-075-8682','320-994-2123','912-935-0010','819-193-1121','102-593-5565','681-494-0279','817-454-0784','874-258-1477','652-775-7363','593-260-3310','555-475-4323','703-110-4712','626-772-7563','722-504-6138','553-011-4278','343-193-5778','134-017-4133','237-097-4261','223-088-0930','675-871-8124','626-842-9074','385-577-1336','447-724-0272','547-913-9925','141-284-4272','260-107-0625','727-578-6485','913-004-2526','334-011-0014','640-249-8540','449-929-1118','663-872-6776','270-386-5461','761-066-1874','562-038-7021','490-267-0353','493-721-8829','346-066-0420','516-056-6805','943-071-3731','901-622-8429','129-332-6687','748-881-5928','899-091-1071','612-254-2820','840-877-5631','420-888-2849','894-422-9400','685-825-1468','106-032-2178','786-512-4563','255-615-4875','522-941-4743','435-378-7819','187-029-8702','284-235-8581','497-439-4024','806-553-1790','297-016-3375','256-157-8495','413-033-5798','848-783-2224','285-368-4579','298-807-6881','360-244-1836','485-202-5394','132-054-8019','404-071-1773','686-813-7510','201-239-1235','943-532-2883','218-267-3930','147-912-7809','422-464-8487','683-582-7017','443-113-7302','116-314-7520','124-325-6727','884-478-9005','631-998-4932','347-191-1561','179-647-6529','636-678-9828','104-984-7725','374-987-4670','190-382-2839','323-619-1714','994-797-8901','243-841-9680','119-286-1390','248-869-6199','329-799-8129','770-822-1427','258-638-7787','713-260-4651','885-962-7773','847-232-7529','344-608-8283','337-024-7833','221-046-7965','709-515-4816','399-979-9520','140-063-4669','617-863-9634','602-041-0832','522-367-5934','971-842-2280','723-549-7704','229-253-5202','385-886-3661','366-300-8323','371-115-0924','407-707-5824','860-853-3810','411-573-2955','319-247-4220','839-555-2835','893-702-8708','389-412-4411','119-926-6654','832-829-0883','171-173-0238','671-761-5125','484-220-1430','684-425-3212','220-279-9453','859-996-0087','487-572-9369','113-563-0304','903-576-6589','282-039-1079','234-128-2285','821-142-4935','573-628-1563','378-860-9622','931-304-5979','257-151-4028','297-933-7908','290-773-5141','269-764-1160','786-107-0377','345-289-3406','462-728-5057','536-833-5977','571-437-0916','304-243-0128','214-586-6512','902-708-4126','445-066-1437','482-204-1659','756-619-6127','291-272-3526','991-834-1374','792-530-7755','369-738-7202','919-100-9655','706-437-0680','731-535-1726','113-740-3474','852-786-9402','624-052-1579','383-195-6725','646-007-9396','244-548-3157','281-707-4378','176-408-7177','832-105-1318','420-673-4038','122-498-5612','992-562-9810','741-722-3524','749-469-6537','130-662-4165','527-467-2924','995-499-0018','846-651-3390','637-838-4761','125-265-0321','406-195-4089','300-850-8961','174-914-8944','352-274-3519','747-739-5610','137-327-5029','641-097-4534','196-976-4523','791-953-3372','746-876-2618','264-162-2590','376-380-0863','935-503-7628','475-833-5782','294-347-0122','424-671-7435','717-148-0580','627-940-7751','984-949-6185','600-711-9765','568-492-9055','921-990-8379','722-759-2907','293-240-9274','203-661-8114','446-577-4675','203-107-8055','412-995-8181','694-174-0637','229-101-4408','655-005-0482','772-995-1751','692-754-1052','706-810-9672','717-180-6935','207-720-3877','433-138-3879','121-025-2780','226-648-9679','703-354-0555','772-022-2322','308-716-0930','599-424-7184','523-452-8024','184-815-6978','669-941-0670','250-881-5679','362-458-8410','430-929-7339','632-732-2909','361-048-9681','630-695-2214','447-261-8571','320-005-7522','630-218-1274','755-773-4886','921-985-1629','570-763-7221','107-232-8981','774-745-8657','185-285-7078','499-146-5147','597-077-5672','845-344-6789','979-042-3235','777-597-4326','835-115-1307','189-529-5598','729-693-5324','175-842-7855','438-772-2263','628-769-9007','870-821-6613','371-653-0188','697-144-1140','476-197-3908','651-725-2424','621-392-8684','242-884-8187','742-038-5951','255-199-4623','667-429-7320','617-110-2604','622-264-4012','638-845-0155','812-489-7830','304-921-2589','973-413-7106','983-415-7230','123-909-5777','880-234-8574','656-054-9453','785-745-9473','351-776-0857','205-835-4879','311-962-8801','710-130-1871','701-790-6229','835-272-3053','571-286-5360','371-729-0485','763-547-7104','665-920-7777','370-114-0679','156-316-9085','336-859-0787','108-557-3306','208-938-4267','930-201-2183','297-546-6081','808-937-7340','133-837-7971','440-462-3949','136-743-8688','715-931-6036','162-129-0224','480-665-6282','305-337-0785','112-099-1687','319-092-3065','314-798-8155','386-673-7569','429-251-1972','832-965-8161','485-930-4380','220-447-4844','128-229-4289','492-037-1802','653-193-6565','488-115-4835','939-099-7030','350-750-3779','743-171-5576','143-385-2384','600-628-3548','578-157-1448','564-648-0827','605-111-7317','129-954-5780','399-442-1314','123-139-2757','951-350-6039','682-749-0147','544-938-3430','767-763-4608','511-510-9514','441-544-1471','699-079-0440','402-014-2788','876-854-6630','797-600-3118','801-519-0189','596-285-0587','689-098-1190','166-983-6516','329-030-3153','262-291-1725','229-311-7455','316-287-1629','282-714-6328','213-765-8735','326-749-6640','591-827-5002','528-607-8289','943-242-3385','917-278-1310','357-775-7973','396-373-5480','923-593-7061','851-575-0322','797-127-3820','506-290-1171','465-505-1112','343-769-2159','517-162-5737','223-887-6830','790-628-9880','651-240-9621','183-591-6669','265-483-3730','417-478-7380','150-358-5210','937-617-9033','611-451-2557','350-868-9676','379-196-9786','246-179-4676','504-441-3036','684-467-3757','998-432-2914','983-123-8787','158-650-6106','774-922-4123','247-513-2653','387-898-8326','975-051-5483','619-409-2334','709-030-6430','524-361-9826','462-354-2188','662-003-7840','530-601-0510','686-104-3169','327-096-2620','658-516-0310','286-444-0931','795-286-7476','463-566-3234','331-453-8324','872-654-6179','395-073-3806','351-901-9575','484-491-2671','234-496-6683','591-080-5200','286-245-7830','574-799-1169','598-964-1634','673-129-4955','381-179-7389','732-075-8367','176-881-5387','360-165-4067','238-349-1529','337-259-8008','264-284-3488','728-512-3559','438-353-1975','955-635-3398','735-984-3449','180-510-4063','942-581-3210','198-944-6414','133-782-1927','968-138-8245','230-093-8530','388-220-6385','859-539-3320','236-124-2248','507-253-5022','531-535-5023','469-401-0070','314-499-3339','499-646-3605','368-149-3111','189-946-7969','735-948-5980','537-687-3821','505-616-7781','510-380-8389','317-530-2106','649-130-2479','590-928-3323','951-081-8153','510-044-1061','888-378-0953','645-111-5109','982-228-6504','209-512-4019','213-068-3302','297-914-4821','705-199-3989','245-470-3732','665-720-5781','317-677-3684','339-486-8963','874-279-1333','682-095-4834','582-779-9179','351-209-0434','228-608-5357','805-652-3042','658-813-1038','188-957-8848','902-824-2406','149-110-8366','395-842-8259','873-727-3976','239-015-9867','440-049-9451','660-960-5992','439-547-3341','713-125-5170','100-706-3132','949-489-2843','445-192-6651','299-090-2680','544-154-1989','791-385-6263','480-828-7427','976-963-8416','937-926-6463','146-911-6326','522-280-5151','440-049-2840','393-288-4674','427-137-6455','939-214-2388','191-677-0267','647-116-4702','955-518-8532','254-458-8002','402-570-8836','854-890-2012','527-882-3296','380-557-6060','668-215-7951','904-216-8829','139-363-4308','393-844-4371','629-099-8434','129-913-8002','447-267-3690','823-894-2829','837-900-0934','903-631-8881','941-715-0285','198-648-4258','675-242-1885','870-392-1840','727-248-4069','270-453-7874','284-983-6945','805-838-4834','230-959-3686','385-313-6808','343-362-7835','495-080-3814','417-594-8534','247-770-4080','295-361-7682','722-187-7753','628-117-9055','829-066-9980','593-944-4782','517-811-3032','340-274-4867','768-486-5571','833-606-8020','568-952-9910','573-153-3435','733-811-4886','281-274-1277','624-140-0346','313-444-0157','873-521-7729','994-210-8625','439-489-3632','552-666-2528','838-716-9923','288-761-1279','965-288-2226','120-409-8071','375-212-2461','500-344-7027','203-327-0404','638-670-8822','672-280-7953','405-421-5280','689-223-9683','974-736-6498','744-266-4755','103-078-2540','268-422-3561','994-609-8852','431-494-4765','543-017-6255','944-191-2522','728-101-3336','547-817-5285','338-429-0650','250-231-3076','406-449-6926','341-719-6170','363-672-1760','303-536-1851','675-727-3055','668-243-4112','380-778-7534','719-564-6972','672-706-6422','613-537-6918','466-308-8099','609-706-1638','545-892-0830','390-658-3068','748-870-3371','147-810-4253','382-216-9833','845-359-3214','155-213-9326','614-397-9669','102-023-7990','961-992-6472','937-012-8179','487-207-2283','558-080-4676','279-715-3138','310-742-4516','330-056-7775','263-115-7462','930-694-0461','927-609-0848','815-486-0469','918-884-0508','587-645-3578','314-673-4177','150-378-7722','727-424-1478','837-648-7285','350-340-6185','592-533-5620','258-907-9285','479-653-5206','952-022-8586','342-382-6528','778-044-1553','695-361-3812','916-367-5288','627-370-6124','691-631-3416','123-835-6121','480-146-3304','561-535-5088','875-808-4161','348-774-1473','692-689-9863','631-678-0883','578-550-6221','730-243-9274','117-995-8293','256-196-4324','297-892-0335','171-472-9181','896-392-5939','782-856-3788','284-040-2184','101-330-2976','837-104-6956','261-919-7191','473-855-9121','437-381-3667','987-736-2498','154-981-6818','881-324-5818','302-158-3261','438-081-8718','918-395-8812','910-713-3579','591-475-7027','580-491-4082','229-429-1223','918-899-7376','983-278-2023','516-104-1471','266-670-6057','356-435-0787','752-386-7640','907-067-4983','406-203-5287','334-734-0927','555-596-4883','373-178-4323','184-881-2277','365-431-7463','923-875-7287','214-391-1506','663-637-7839','681-334-1774','969-187-5402','791-866-6331','484-821-1240','904-952-3700','483-455-0455','791-003-2141','476-267-6332','367-412-9883','109-425-8623','292-962-6863','730-290-1581','646-070-0477','408-812-0651','611-290-8969','891-154-0032','880-277-1340','278-088-6440','102-674-4110','125-431-7485','755-420-4457','328-598-3932','845-262-1190','957-415-7451','849-139-1028','234-558-6178','767-324-9532','458-892-6479','287-291-5399','718-905-7503','833-757-6520','961-090-2861','603-938-1427','784-211-7274','197-907-2089','265-364-9834','671-985-0089','805-948-1879','405-418-5169','956-869-8147','901-940-1029','460-247-5530','154-430-0759','542-932-1643','482-876-6317','474-982-9865','391-293-7180','260-567-6220','997-381-1514','621-839-7129','381-052-1332','726-740-5959','258-157-6063','655-758-6559','829-680-6412','310-803-3338','913-174-5434','876-405-9923','850-404-9028','677-062-7273','952-567-0663','379-147-5102','958-604-9851','628-642-5804','231-979-9427','990-529-9361','583-765-5180','498-669-4730','658-778-3019','181-025-6930','538-719-6221','753-394-0926','613-791-2076','694-872-5410','166-005-7018','233-728-7353','355-405-3335','374-669-8816','233-472-5751','862-775-0740','908-675-5640','640-774-6222','599-328-7927','311-198-1678','882-906-3806','824-930-8572','467-513-6804','401-945-5072','251-683-9181','426-145-6240','894-744-7389','410-128-6577','779-973-1304','967-116-8514','884-922-4973','372-039-5449','826-889-8039','140-729-0218','642-882-9389','345-724-4529','873-939-6343','629-754-3752','336-697-8502','521-669-6659','835-194-8481','845-884-9273','852-553-3682','279-729-4350','246-462-2436','601-955-4039','420-274-0229','838-739-9712','999-818-6131','448-056-1738','773-279-3681','560-295-1320','361-842-2445','182-913-3225','100-701-1402','682-616-9236','924-793-7223','832-837-2131','490-763-6061','909-145-2961','857-339-6330','452-975-0522','503-208-7657','275-879-4575','522-943-9281','884-792-5786','626-766-3399','296-047-3732','304-947-3772','321-806-4575','479-587-6170','485-367-7480','954-575-9887','421-588-6572','688-053-8489','904-900-0516','549-374-8176','806-728-8604','478-302-2059','661-314-0736','986-744-9427','452-994-6283','934-226-5020','783-642-7023','752-304-5518','714-475-9950','355-643-8276','693-275-1737','977-700-8540','533-442-5038','288-853-5370','376-524-9499','590-950-2939','186-750-9780','375-664-9532','161-143-6827','590-542-2927','365-936-8136','886-143-7775','316-028-7165','129-116-5927','588-165-4928','889-379-9875','166-893-6210','901-025-4438','414-917-7640','626-487-5355','892-554-1112','314-130-1257','175-422-5153','109-474-6836','566-046-8820','190-104-5223','885-119-7033','757-377-4929','458-563-6427','786-179-1821','901-258-8337','684-534-0632','610-686-7830','773-755-3365','549-159-5778','197-887-3604','470-437-4765','410-059-3228','842-385-7520','901-333-1750','842-028-8628','104-719-3184','321-538-9488','891-457-1955','192-647-2229','795-614-6072','987-795-7030','605-599-9548','462-086-4990','477-081-4072','662-986-0053','912-981-2532','790-253-5580','355-502-9171','326-140-6973','956-149-0969','503-121-1829','454-890-1820','760-524-2316','105-778-8606','836-422-2478','690-904-4100','507-103-0684','115-069-9051','873-320-8374','509-333-9629','691-368-7325','435-140-2563','657-045-5788','946-447-3255','946-019-2872','711-857-6762','501-483-3417','248-832-9255','270-266-0624','716-907-8115','784-886-7708','211-996-5363','732-332-7120','518-304-8724','915-925-8723','412-915-8383','589-587-6132','368-406-8070','685-437-7575','747-904-4139','596-724-7449','683-246-8839','348-954-4021','433-659-1187','785-516-8279','774-639-2856','603-226-5292','937-172-1939','828-631-2086','637-904-9585','664-610-1220','383-359-7690','520-457-1198','503-539-3890','135-188-6483','913-242-2802','649-828-8310','936-821-6038','797-665-4670','199-999-6672','278-200-6012','377-899-9381','265-616-6517','868-257-7635','152-315-6680','873-744-1427','529-564-0940','197-964-5222','610-635-3308','919-384-5987','143-177-2792','730-216-8961','169-993-1725','983-573-3476','894-506-8121','602-995-0916','414-409-2729','628-015-6084','112-751-1634','518-889-1483','470-489-5020','295-219-8199','963-494-1608','901-237-2578','133-045-0447','781-822-5122','147-290-9829','244-861-7409','438-772-9009','252-779-6822','610-684-0398','789-361-5724','676-528-9113','445-891-0886','842-636-4463','596-149-0863','709-798-3404','330-340-8367','229-205-3790','128-802-7080','111-913-0608','643-625-6123','167-093-0059','299-303-6308','603-629-8522','892-261-1338','550-695-7985','605-285-2034','567-212-5218','518-539-8704','962-084-2181','405-187-1931','353-868-0935','866-267-5155','763-529-4455','617-646-2723','785-060-7135','251-168-9661','487-454-1321','232-886-9880','274-990-5165','182-037-6983','824-425-9690','257-778-7740','529-556-2406','375-568-6878','555-241-3718','579-309-2727','757-728-9127','703-184-1179','317-357-8775','660-294-1351','608-735-6059','456-759-1789','279-281-7283','449-169-2698','382-895-2174','769-346-4735','917-589-5459','462-413-5932','126-669-7938','634-138-5469','355-370-7855','464-386-4185','858-772-1929','789-595-8230','422-337-3578','317-625-1633','756-375-5104','528-811-3125','793-682-4789','644-862-9810','646-059-5759','539-038-9992','545-059-4240','710-587-2455','587-235-0904','687-729-0309','943-760-3904','581-994-9569','666-833-9375','152-326-3359','948-862-1630','703-322-2104','560-698-1661','120-664-5010','685-039-2453','765-891-1629','997-628-4359','128-168-5402','564-128-1208','238-613-8706','742-264-0798','120-208-6740','643-456-4276','363-435-2630','389-273-3936','898-158-7124','833-300-6914','345-158-0722','166-887-7824','382-115-1322','507-255-2974','526-134-2251','700-781-7485','549-697-6115','492-674-8906','818-970-9779','322-211-6855','104-948-0751','534-156-4430','866-208-7134','654-297-0989','452-670-2283','526-088-0089','498-373-9730','244-899-8223','906-481-0765','631-608-8627','129-490-4116','746-869-6253','738-759-7583','985-880-7678','967-653-6077','510-856-9286','780-706-3328','103-320-2312','236-013-5573','302-530-8208','781-276-7684','129-071-2870','442-964-4973','861-777-3600','464-428-1453','553-434-8029','905-513-6440','258-804-6534','976-802-2424','380-305-7088','314-634-7430','702-341-8706','344-820-2836','187-055-0110','639-963-1827','165-292-8474','125-867-4316','376-111-2514','558-784-9123','828-595-7421','556-311-6519','756-598-6296','224-447-9222','288-563-2230','631-072-4671','404-709-0278','443-709-6175','996-178-8012','154-554-2278','979-561-3957','973-364-0476','627-144-4298','859-110-5463','754-078-3081','480-288-1824','397-923-9132','559-395-3863','864-393-7333','540-225-3802','952-214-5099','997-211-4129','365-366-9643','990-175-7471','281-566-5278','311-526-8173','672-498-7783','482-162-7735','398-897-5975','932-087-9976','301-258-0226','462-707-7127','834-693-8057','777-868-7283','668-074-5079','311-156-4540','752-394-5829','921-996-2580','944-724-1532','549-754-3480','792-538-6539','688-759-3434','834-288-9669','848-748-9080','868-443-8729','919-954-0080','753-959-0843','655-558-9473','937-478-1014','118-348-2624','663-044-4227','765-447-3605','554-484-2480','950-393-6567','170-609-3878','923-148-8779','273-461-4686','920-660-8237','102-305-6165','843-431-2430','597-935-6081','610-865-9640','852-313-2555','355-032-9814','850-464-6789','881-639-9708','267-360-6080','829-213-8474','578-432-7953','708-286-8580','680-228-8700','356-936-7079','276-676-4061','466-591-6972','229-548-9484','273-989-8512','711-817-4414','568-324-8569','429-738-8773','586-736-7932','121-714-6740','533-531-8818','622-134-7429','171-687-3775','769-958-9198','514-616-5381','476-125-7712','769-516-6830','148-973-6423','742-861-3561','911-395-3267','578-742-2384','432-786-7840','306-242-4104','162-654-0475','538-612-1763','614-451-5027','612-916-2720','135-803-1667','514-175-6540','971-232-8961','911-870-1665','795-177-7930','479-602-8408','481-142-3340','770-447-5324','892-964-9404','622-390-2780','651-425-2578','834-106-8889','352-682-0612','272-367-4089','507-446-3614','618-799-4555','994-234-2516','279-710-2071','386-523-8624','119-108-8080','557-755-0438','662-892-3828','630-967-5889','304-934-2270','198-926-2004','225-690-4051','879-516-5914','348-538-8579','400-974-4688','875-535-0018','302-210-3216','705-618-8179','901-805-6163','152-785-0004','227-504-6363','531-703-1064','283-873-3997','987-896-4390','499-817-3006','224-559-5177','551-263-4904','924-090-0390','449-564-8557','740-575-1336','867-143-6850','442-673-3326','784-465-0198','507-577-9870','876-689-4479','269-138-3174','549-587-2169','891-174-9320','191-496-8872','492-765-4960','797-052-8516','852-844-1477','707-403-4722','376-816-0853','318-885-4724','912-520-8773','752-123-7467','284-307-3634','522-421-5234','803-519-5416','490-088-6630','710-564-5630','341-830-6272','615-039-3700','427-639-2322','427-298-6869','257-491-1822','775-582-4330','525-507-1518','874-534-4518','556-106-0277','959-715-9780','700-323-8694','252-494-4614','493-460-3969','449-871-0621','397-748-7616','748-306-6138','714-340-7600','583-196-6780','692-459-7781','180-982-5722','362-028-1473','684-664-9404','404-605-0253','529-997-1532','116-365-7975','842-476-1508','781-055-4729','904-313-4267','543-413-9040','666-715-7545','334-165-9118','645-856-1556','436-556-3520','566-727-0261','190-035-5751','881-529-8701','181-899-0525','364-157-2132','442-065-9027','105-966-3955','637-922-4555','474-996-2425','199-434-3548','359-743-4321','130-614-2923','188-698-6340','702-761-6953','104-679-9571','753-643-7661','561-851-1732','711-583-7306','123-819-3060','246-745-3348','745-163-0978','839-196-3960','319-941-8499','679-893-4284','823-069-5361','346-277-7932','681-589-1367','579-644-8904','409-948-4214','755-536-6814','816-593-7688','798-996-8429','503-546-1028','843-773-2951','301-443-6470','945-797-0807','591-190-9479','104-513-5441','985-534-6428','486-265-2230','961-845-3348','416-289-0420','568-176-8739','420-954-7373','905-426-0687','647-755-1979','295-600-1800','478-656-7481','340-693-3559','557-925-9389','218-639-5390','379-880-8194','521-140-3583','131-443-5960','758-742-0606','786-583-2785','762-133-1530','522-415-3659','443-422-3849','761-528-8365','348-264-2512','398-771-8265','806-378-4126','234-848-1859','665-005-9928','796-343-3765','715-221-8651','439-216-1390','543-994-1868','680-134-7690','936-935-7379','592-509-4720','694-437-6418','251-004-4386','217-526-8347','183-957-1979','311-291-9994','237-164-4000','360-453-5523','151-496-5767','706-572-2820','979-639-6023','691-358-0101','242-323-2663','155-297-6616','702-675-1523','205-760-2351','763-551-5149','967-274-0973','788-172-7161','918-901-4530','644-225-5775','616-538-3983','342-567-3272','547-184-3880','248-424-5616','459-547-9321','887-668-6232','688-534-1661','849-099-2002','991-069-1822','451-710-0704','170-059-8565','692-732-9010','541-607-9667','724-839-8965','505-063-5631','471-397-9428','329-644-9080','473-378-4159','204-844-1110','605-569-6773','584-099-0451','178-544-9369','565-456-3578','877-345-1931','392-687-6860','128-799-1271','384-309-6122','187-500-9390','374-763-6029','850-600-3141','852-458-1261','935-499-9983','742-925-5030','153-833-6228','319-916-1268','958-860-2008','452-177-2304','455-179-2391','659-098-3271','255-206-0953','959-888-4832','589-510-4429','450-303-6073','216-951-9440','493-242-6823','368-487-4904','808-602-5120','512-415-3323','188-461-5574','892-063-0083','992-775-1024','762-956-0496','535-374-7889','985-757-3578','538-433-7477','966-689-2771','695-310-2384','742-806-9771','643-119-0785','143-636-6931','245-383-9570','763-281-7488','818-837-6314','291-755-6889','232-216-1173','950-487-6609','499-512-6873','227-909-1139','979-645-6875','573-014-3310','444-231-6430','727-289-0714','923-179-3170','423-297-2538','313-370-7432','999-742-4536','525-112-8826','928-889-0898','999-823-4339','903-266-8481','299-062-7527','595-253-2349','613-083-2773','704-832-9589','840-254-8989','971-719-0939','862-082-8853','269-640-7953','688-498-8004','449-919-7576','786-920-7194','715-429-6337','688-667-2582','647-835-7905','290-125-4157','970-634-9432','224-021-1373','964-327-9784','887-485-6287','467-019-9341','260-577-9582','658-714-0602','262-709-4469','608-007-9602','861-626-3304','161-422-3963','719-905-2340','588-385-7470','357-871-7065','205-831-6371','167-532-6461','503-207-6236','114-650-5724','423-895-7730','919-182-6099','278-597-3067','388-176-6640','906-219-2298','299-081-8718','941-733-8587','381-159-7576','576-720-9990','211-065-7802','193-139-4879','273-526-4382','939-545-7023','392-210-2961','987-719-0212','598-005-3825','548-229-3037','258-105-2261','348-586-1199','450-211-0431','167-587-5031','766-679-2936','940-043-6273','182-596-8199','999-054-9321','279-751-0667','998-778-6020','299-043-2569','348-584-9430','666-961-5212','684-058-8582','890-326-9832','209-868-4314','896-472-1737','784-519-5784','941-356-9857','182-360-3859','493-293-2673','548-984-3424','278-775-6780','577-671-5083','863-176-1408','670-889-8589','910-012-9726','316-621-4006','309-590-0018','426-103-8877','883-162-0783','885-642-1773','363-768-6155','588-739-1541','803-076-7840','670-967-2153','764-764-0725','979-952-7271','401-765-9380','855-089-2412','680-520-2108','622-914-5667','752-500-4026','539-140-2730','317-608-1138','409-312-2433','694-211-5873','906-863-0427','252-646-4480','447-263-2018','849-044-6061','486-989-5282','960-307-8134','711-242-7083','979-459-3850','715-334-4724','248-578-2481','866-720-1578','979-835-9586','165-656-8451','342-588-3308','872-925-8443','806-540-6949','246-785-1716','776-655-1229','970-023-5622','567-627-1480','453-712-0151','250-646-6757','408-561-2690','656-014-3861','422-703-5054','823-763-4970','283-496-9104','528-216-9710','281-839-8283','466-683-2616','649-892-4051','634-554-3440','316-592-6509','648-487-6619','158-740-5624','353-067-0685','262-910-9732','920-232-9720','401-268-3772','822-688-9759','822-976-7518','292-196-3924','656-056-9306','700-451-6102','318-110-6610','276-636-5090','315-261-4581','110-106-4829','402-983-6218','899-462-8504','800-262-2627','108-790-7590','901-159-8106','230-444-5359','992-391-2412','543-685-5984','704-700-0031','913-063-2643','893-995-1996','478-635-9736','818-424-2686','396-171-7398','446-008-3306','619-905-1621','100-867-3616','251-911-3696','813-500-4626','234-474-4498','755-853-4086','769-815-9297','177-053-2137','824-633-5370','442-961-0292','716-048-0024','693-283-8678','684-613-1085','224-590-8125','497-249-8787','995-075-4226','971-206-0379','723-948-3206','122-659-3327','680-145-0512','880-065-8578','325-689-1263','729-152-4143','274-027-6039','182-123-1037','596-671-3872','198-248-9851','526-722-7530','701-457-4520','218-205-1516','431-689-7640','733-425-7329','973-103-4263','342-882-0651','509-623-2651','386-095-6510','445-931-0012','989-410-6781','324-798-7478','512-268-4879','348-333-9323','641-563-6161','388-080-5169','515-935-9149','624-726-5437','691-221-3836','564-012-0902','258-910-5869','786-070-1557','317-035-1151','838-554-7983','964-724-8675','774-132-3831','261-901-4537','580-577-4237','291-275-3967','719-578-0325','320-334-7569','632-427-9650','553-916-5416','720-478-9836','330-199-3894','973-843-2277','783-694-1630','720-569-0437','813-748-2281','634-320-3753','395-960-9206','350-279-4479','321-729-3027','427-361-6982','706-436-8469','578-818-0780','537-230-8137','654-220-5727','450-503-9795','215-112-0670','671-502-6071','509-575-8838','417-618-9036','841-869-1136','101-005-4606','399-522-9026','395-738-3069','360-607-8904','127-568-2093','328-761-1690','561-782-9729','933-034-1786','682-920-9431','868-066-8138','160-445-8660','735-486-7826','501-400-9539','197-378-4926','162-312-3941','925-477-5706','653-611-7508','130-748-3169','452-629-5833','152-609-3185','135-732-3255','592-813-6098','181-292-7672','454-063-6280','907-196-7824','766-346-3118','603-022-1584','415-734-4778','465-917-0285','867-025-4172','626-576-9963','551-570-8484','689-929-5806','468-686-7306','493-164-9502','253-855-9137','292-730-3277','306-045-7214','196-288-7422','197-648-3045','599-384-3073','881-867-8130','354-018-3602','653-928-6541','431-136-3389','725-621-2421','693-737-2545','823-469-5521','540-161-3281','774-733-9274','954-745-0133','558-054-7385','227-699-4228','892-834-4134','264-746-2290','285-925-0014','380-814-1076','538-622-6881','718-307-2131','352-965-9000','954-266-6489','996-299-8517','764-129-3369','751-733-2680','697-680-8270','136-771-4759','876-427-9629','464-857-8570','154-864-5296','665-791-2067','832-199-1430','815-833-3125','347-148-4010','482-734-6171','403-924-4685','234-758-0660','537-190-0604','292-184-8778','503-907-6172','486-781-5755','578-069-6373','170-617-2322','363-503-1789','852-845-3881','197-146-9882','225-612-9529','548-120-4469','855-555-1030','604-777-2716','962-767-5819','104-613-6638','861-712-8324','674-364-5810','183-794-8028','141-580-9087','938-964-6481','916-997-2830','538-332-6225','737-506-0422','446-002-9430','510-315-7037','938-681-3153','260-439-7629','609-291-8525','929-512-0977','575-326-3489','245-633-6210','382-187-5385','925-722-0176','555-327-4328','655-051-9385','819-469-6498','776-859-8854','818-979-9369','475-646-0433','850-535-3390','197-870-4422','685-309-3381','927-929-1923','113-203-3975','247-803-3174','720-301-6038','189-485-2499','115-255-6328','631-387-8626','605-178-5220','781-693-8977','424-765-7437','589-271-8375','588-158-1772','238-374-4240','456-295-5933','848-188-5585','441-434-5404','925-468-1789','901-667-8287','175-966-2300','903-641-4827','407-253-9018','775-929-4725','653-176-6340','918-044-7418','312-950-0928','923-101-7820','711-554-9974','324-839-7910','440-942-0225','462-810-6216','657-234-6350','682-538-5374','515-491-8136','959-196-5829','668-862-9410','322-961-5522','743-891-5360','597-764-7040','321-619-6132','951-932-3112','678-706-9471','102-232-4861','485-503-9340','492-856-2780','578-369-8110','603-438-0628','659-832-8212','512-038-9363','727-002-5274','980-587-4812','212-688-4116','909-483-8826','588-277-9290','149-943-3625','412-081-7233','549-947-9161','896-924-4771','203-426-6123','786-100-7979','459-505-3681','663-217-0112','665-974-5874','844-472-4565','933-796-4904','722-678-4985','397-994-6421','579-439-9783','878-232-5485','417-167-4922','455-909-3426','518-750-5728','166-415-6723','441-285-5924','692-892-9261','524-083-3140','868-975-5575','871-241-5228','197-312-2981','925-856-1768','299-537-7881','763-722-2139','731-791-0789','250-623-5112','188-769-3116','812-604-2390','210-363-3418','141-401-2512','482-930-4884','363-591-7630','593-943-3441','442-951-3551','339-990-9838','295-348-2453','216-076-3836','178-521-6961','225-345-5888','402-115-3585','883-242-0836','882-849-9075','152-762-0185','799-769-3536','671-601-1227','464-288-6563','687-689-0883','722-545-4534','963-908-0669','973-710-5378','383-402-4198','417-040-5981','161-983-5750','373-260-9169','219-241-4850','514-774-5949','196-516-7740','115-486-0036','853-994-8776','831-068-9267','863-262-5640','213-636-7630','458-592-4912','110-073-1125','185-149-9978','767-078-5472','470-416-7010','706-281-0265','940-545-9624','893-015-8178','857-949-9204','357-152-7026','939-908-4871','208-834-4002','852-277-1304','243-851-0698','768-716-8974','731-365-1657','567-718-0063','247-681-7904','496-543-3459','291-269-7072','762-719-7709','927-868-7686','649-765-5623','501-929-9786','324-886-8934','365-213-0992','686-612-7980','454-943-5910','468-948-2834','386-919-6639','792-610-9874','624-728-0410','865-246-0882','438-497-7837','649-746-8539','910-979-7930','826-958-8159','417-035-4026','940-036-7169','218-672-6225','955-960-3336','941-510-4093','279-876-1876','237-430-8041','787-753-4084','442-475-0973','512-706-4077','710-362-6635','294-952-4423','500-430-0023','440-963-2157','258-008-3774','956-323-8533','143-866-3853','937-366-2540','605-574-7910','316-550-4476','430-783-8883','341-870-3402','991-087-4036','565-279-6974','297-959-1202','989-062-2814','217-608-8936','840-214-5971','572-412-9323','848-626-1526','933-489-3560','794-576-1369','675-141-7429','146-236-8826','603-635-1365','202-183-8840','245-250-6783','713-488-7473','932-933-1892','516-487-3322','169-359-3659','158-055-0407','235-463-6323','610-240-5063','369-967-2125','708-973-7912','309-445-2180','852-422-4900','847-810-8553','644-415-3621','866-922-6959','988-234-0670','556-276-3510','144-377-4375','664-269-6057','544-755-2727','951-029-2555','987-569-3173','415-726-7302','968-265-9622','584-161-1134','979-203-2891','137-297-7624','625-488-6026','591-748-0702','169-331-5657','777-315-7757','793-655-7978','664-301-2587','875-159-6731','724-486-7888','695-782-7825','461-170-6688','496-013-3059','832-141-6376','363-397-4500','827-974-7035','956-875-3934','790-468-8781','849-773-5525','887-167-5978','553-461-5683','552-186-2230','278-791-3623','582-456-5757','359-946-4772','944-691-0317','419-179-0027','183-173-0238','363-489-3576','794-124-4781','452-734-5598','687-670-9647','965-012-6684','569-329-4090','542-987-0158','900-764-3040','622-058-1474','920-542-9999','653-030-3124','444-930-8079','115-080-2128','672-450-6521','749-466-8930','648-638-5957','732-301-0963','474-939-9585','811-586-3516','284-414-5293','364-287-5854','431-284-8124','779-298-3559','538-339-8388','962-237-6755','977-828-7769','306-394-7702','928-689-8965','735-457-3783','612-369-0882','844-725-8102','348-557-5863','449-431-4084','605-568-2738','671-694-9428','454-167-5657','579-082-8910','136-076-2886','463-624-3661','872-665-8426','727-214-1080','713-278-8018','135-468-2789','133-518-6221','988-154-5985','935-744-2572','732-986-1640','998-933-6920','235-823-4908','278-310-6604','753-746-3681','360-747-6788','184-791-9800','350-413-5278','415-496-1848','447-851-4073','564-808-3857','104-465-8629','572-265-3360','566-576-8950','290-614-9853','906-251-5704','841-498-5134','352-609-2572','536-599-6480','542-194-0453','776-789-7138','349-605-7920','268-035-4698','377-751-4616','227-330-5075','767-412-4172','147-592-2737','311-493-2218','282-673-7602','186-801-2143','203-286-5440','145-259-2102','629-759-3751','312-502-2823','763-529-8537','469-180-2623','482-864-5783','361-078-6868','319-120-0324','690-976-9451','785-448-0408','834-712-8300','510-377-8438','983-562-3060','632-608-8469','360-542-7577','770-791-6033','114-593-9512','508-754-2329','858-788-8267','491-425-6934','550-667-1431','190-523-6639','261-750-4171','518-474-9318','402-856-9886','505-392-4790','530-278-0925','482-793-2481','503-132-7220','988-243-1383','875-893-3355','672-421-3421','261-650-3657','340-709-5102','649-273-8228','494-573-6750','235-460-8153','515-906-5774','807-699-4588','270-795-9693','460-582-9293','718-395-4435','192-620-8487','175-547-4726','581-321-9028','635-636-0429','535-993-6406','423-349-7373','679-263-4038','806-959-0726','197-844-2021','979-979-2974','941-138-0727','220-091-9224','347-700-0509','545-929-3602','292-746-1218','216-017-2781','393-764-0616','523-802-3432','600-030-6170','412-528-2624','926-945-9532','556-574-9974','625-634-9675','165-944-7063','178-691-9121','362-412-0923','504-873-0759','535-580-0672','371-249-0965','508-067-5636','787-015-8427','412-790-3227','676-215-4961','896-325-1222','555-762-3790','470-085-5139','183-830-2888','701-051-1134','780-171-9020','480-942-0336','161-998-0134','678-672-6252','858-351-9377','435-948-4516','236-771-8227','489-119-3130','425-994-3988','828-077-2277','360-196-1587','379-215-0259','687-337-1930','150-234-4759','451-905-8339','524-811-5978','976-460-2806','535-033-7421','614-678-7681','313-348-2073','420-495-5075','672-980-4532','775-593-5604','147-365-1006','715-690-8841','327-343-5580','286-938-5728','591-092-2177','700-345-2287','513-967-6025','174-907-6876','143-089-3292','445-507-6774','743-249-1086','889-190-3625','408-686-1728','264-722-1558','931-621-6888','413-740-1126','908-506-1074','803-153-9218','356-197-1389','196-013-7553','830-344-7976','325-077-1785','516-427-7432','655-349-2672','435-867-9628','609-797-4153','855-375-9778','145-014-4778','667-636-9618','825-937-0787','475-546-5587','789-536-5059','178-930-8832','609-258-3968','939-594-4053','882-175-6220','979-056-4137','549-072-1916','875-004-9373','753-781-0099','344-306-3101','738-312-8490','822-817-0276','929-173-5327','205-072-6851','931-699-2178','113-439-0351','326-149-6170','745-280-8378','341-073-7808','848-925-2900','106-536-4724','250-763-0910','964-914-4157','661-461-1486','114-872-4332','916-945-8383','792-203-2781','617-459-4853','910-029-9178','921-337-9327','344-041-9571','199-317-2604','107-447-2677','429-310-5706','856-735-3575','351-108-9067','417-980-2339','606-754-0565','352-415-7569','578-548-3639','311-486-4302','480-891-7380','840-644-9929','470-106-0110','149-347-0027','136-965-5175','104-678-2557','490-389-5976','860-507-7540','760-893-9871','195-415-3039','319-188-5779','752-065-7783','322-066-0580','798-358-0912','438-056-1272','404-210-6483','772-564-7973','240-439-3340','429-309-5463','522-721-9780','728-910-7833','179-771-7285','520-799-3685','951-658-7208','376-931-7432','248-565-7325','117-385-0629','727-017-0228','420-906-3432','653-950-0922','897-290-0924','272-655-9422','508-869-8300','509-263-4076','582-165-8590','214-940-3337','553-319-4329','484-654-3826','848-301-8844','716-811-2937','314-255-0690','902-352-2323','955-886-6644','249-254-6112','800-763-6000','788-154-3569','185-334-9053','878-014-3754','727-080-1967','700-077-9879','325-643-8376','979-845-7933','481-200-3349','104-626-3375','807-937-1820','200-008-1832','533-388-8139','191-599-0067','171-472-7340','590-365-5710','355-875-3275','551-727-8419','803-855-6103','519-125-3612','748-762-8275','275-378-2580','620-625-3221','152-731-2875','379-983-7033','171-235-3610','860-861-8237','931-152-8827','435-398-7357','525-014-0416','179-834-4887','364-286-4723','367-175-9665','654-821-1880','132-226-1465','472-108-1718','286-502-4227','155-475-7370','571-604-1019','446-956-8981','926-471-8803','882-893-5926','442-033-2687','492-814-9374','143-386-8225','804-026-7400','677-770-4980','228-783-6978','634-323-2333','442-725-8126','170-727-9730','713-196-3677','969-286-0823','574-099-6023','907-202-1725','250-187-8186','460-498-5722','904-335-0904','677-197-3312','597-828-5365','374-933-7371','699-276-7753','843-814-3463','853-538-0183','574-683-7489','291-437-3621','807-673-7382','119-547-3326','171-849-6623','934-470-4247','267-946-8357','103-323-3561','297-006-2234','104-506-4281','529-829-3585','150-566-5725','128-475-0420','927-273-4376','840-127-5228','520-709-7939','900-419-2493','909-687-4930','925-700-1883','184-417-4510','625-705-9260','322-006-3139','901-642-2299','370-911-8612','759-488-4720','714-565-5216','265-027-5750','742-077-3681','800-994-1324','899-255-7234','480-893-9972','819-385-5731','837-722-0490','259-909-7184','905-648-5651','283-353-3410','125-711-5967','524-652-3116','241-142-9630','154-502-7996','256-635-0378','156-195-2259','296-223-5661','447-503-0396','963-339-8980','531-196-2767','972-192-5277','689-402-3431','234-455-2259','148-713-3159','446-898-2381','516-296-2079','936-288-6235','958-962-4306','355-962-7072','118-581-0930','219-118-1353','868-101-8916','685-589-8569','266-054-6055','185-476-0049','274-945-9627','392-380-0436','396-424-0322','260-113-0234','561-798-7880','629-632-2629','119-713-6678','354-335-0849','251-210-6889','519-603-9980','845-064-9130','339-985-2150','921-409-6396','181-435-1980','897-854-8585','575-606-4955','118-507-9023','839-576-5485','478-826-8155','628-514-1680','341-379-5037','270-463-3422','156-078-2138','691-598-2696','974-356-3540','462-855-6134','248-543-5140','166-104-3457','557-999-9818','721-138-9280','812-564-8712','822-841-4510','486-475-4314','435-725-3809','593-271-8971','739-170-1923','282-351-9283','899-806-5251','364-353-5530','453-682-3114','904-823-7370','709-316-6735','403-809-3874','920-911-0665','951-010-0351','258-847-7992','110-556-2737','512-628-9575','963-227-7592','825-303-6428','146-806-0265','165-110-4387','312-448-9416','576-111-1871','885-621-5629','982-467-0572','215-304-3289','229-919-0033','210-489-7739','597-006-3738','281-887-5883','994-556-2336','895-769-8071','967-576-1555','480-204-5922','803-896-8771','384-835-9940','404-659-3085','575-649-5025','534-741-2372','459-354-8140','250-073-4669','259-314-0167','911-025-6320','253-910-6639','112-997-4929','100-441-6420','118-137-7686','496-687-9256','395-656-5877','980-681-1227','769-690-7190','673-835-1516','734-986-7885','335-080-5081','936-920-3998','823-245-9051','903-465-7120','220-780-1270','338-591-5059','913-809-9906','765-253-3672','612-033-6281','250-961-2983','130-538-3684','353-936-6620','544-575-2250','665-593-3751','263-643-0590','808-969-9160','518-807-3876','668-978-3270','525-263-0455','898-667-4331','138-782-7035','582-451-8257','941-011-0798','345-159-7916','968-242-9040','972-826-5204','167-054-7044','483-314-9204','876-617-2865','390-215-0422','699-663-5808','163-650-4588','812-631-3616','221-864-9528','924-627-1675','708-577-6430','344-793-4104','697-542-2540','219-522-4323','784-877-8836','843-252-1008','405-141-2163','813-373-9202','409-245-3782','104-366-8463','474-937-4034','690-857-5975','413-571-0202','697-189-7231','607-774-1961','689-588-5318','622-451-8643','288-533-9998','496-008-9571','751-111-8472','633-024-7020','410-475-1639','977-339-8809','113-578-4098','913-410-7160','301-958-3929','714-560-8051','696-192-0874','865-209-1812','580-338-9436','716-465-2455','250-402-6802','512-509-4453','508-371-6081','769-939-0323','171-424-1238','505-548-3394','452-716-4920','974-667-5853','630-315-2355','307-338-3921','251-511-7826','217-694-4128','365-808-7969','429-657-4830','330-605-2780','201-116-3671','827-953-6121','600-424-6931','802-671-7106','272-578-4910','323-907-8973','110-074-0635','932-306-3728','643-150-0231','122-877-2504','171-274-6738','732-538-9693','672-396-2651','342-608-4627','305-157-5028','536-385-9973','724-260-7453','139-715-9932','726-743-9802','691-986-6687','275-480-5916','992-053-8458','500-935-2832','974-678-6634','693-047-5551','232-071-6927','372-130-1118','643-583-6176','880-662-7141','691-378-2878','954-774-0469','428-890-2959','415-147-9487','498-179-5222','233-626-4402','115-638-4512','432-272-0611','559-650-9209','507-624-4791','190-734-0474','307-541-6353','920-115-6277','457-956-8136','352-416-3437','623-092-4790','891-616-5750','468-855-5306','195-542-6965','399-957-8378','392-747-5334','961-707-2373','741-070-6996','516-796-5024','295-998-9536','424-922-1404','985-738-8170','932-518-9722','194-968-3581','877-909-2138','696-181-8620','528-812-0689','148-032-8849','950-159-3876','256-383-3780','465-378-9240','566-596-9671','801-587-4761','955-551-5855','651-898-5200','496-621-1170','656-493-1102','545-321-6664','445-769-8280','509-266-0260','689-090-3379','776-234-9610','779-980-0123','875-636-6000','459-855-2771','469-209-5773','213-968-9061','610-435-4974','420-699-3350','183-867-6308','354-241-2478','633-388-8678','271-051-1980','660-355-3222','845-581-2930','958-464-1424','835-602-0714','512-482-2822','100-219-5626','282-024-3636','357-419-9314','402-850-8456','625-167-1329','291-849-4112','180-497-9317','258-042-2463','398-057-6269','719-978-2631','650-606-1087','874-079-0170','742-234-0069','945-250-0680','681-533-4420','427-429-0128','510-684-7118','161-623-4386','314-575-7378','952-588-6122','553-257-0389','967-196-6476','877-337-7872','379-964-2125','426-365-1023','314-299-5953','100-728-0712','882-871-0932','301-548-0477','114-904-3273','480-772-8264','391-024-0089','307-363-7380','520-194-0157','851-878-0229','254-140-0827','652-386-6781','837-680-5233','696-272-1102','759-569-9916','684-805-0197','918-677-5031','661-822-9779','168-271-0650','431-022-6678','673-094-1123','347-212-0404','597-128-0559','728-494-6518','283-731-4334','273-395-3869','867-341-3725','479-423-6173','491-789-6936','278-308-1413','137-851-3626','826-718-9971','142-289-3330','884-440-9657','178-971-7308','872-234-7269','271-280-4202','847-610-5684','454-654-4081','948-758-8021','619-349-2757','140-661-5924','660-755-9330','293-463-3425','501-739-7923','427-045-9020','313-572-3583','397-802-6651','609-263-5973','684-757-9018','464-749-3071','345-673-6040','552-741-1329','346-967-3863','234-654-5953','400-384-6467','785-169-4720','637-854-7527','890-400-7532','318-143-9731','681-748-0202','660-286-9508','169-255-6023','181-988-2459','143-096-5818','503-006-2679','154-052-9030','421-702-3138','775-279-2187','610-008-9769','574-654-6485','915-040-5067','272-351-8334','915-484-7313','608-139-8029','278-120-8618','990-987-7359','932-093-8282','194-115-2618','154-707-7032','318-128-7488','242-980-5388','344-804-6881','305-577-1967','584-161-1104','392-702-8165','777-636-7489','974-105-0989','106-603-7975','410-811-6578','339-797-9320','953-194-8177','364-665-2558','185-028-0263','981-921-6103','151-218-9499','911-989-5929','620-418-4192','636-429-5967','794-961-7963','299-431-0034','307-500-0078','531-191-4739','345-143-0425','258-110-8158','976-309-7170','849-217-3214','508-083-0983','209-731-4262','780-719-5728','355-770-4588','601-647-7780','996-340-4139','107-780-6512','984-558-4129','513-236-1938','143-801-4412','388-760-0937','647-751-2138','239-885-9089','175-780-4653','773-512-2935','589-600-1976','307-045-7096','882-966-9804','207-122-7975','259-446-0505','361-940-3779','648-673-7453','475-465-2027','544-562-1741','785-329-3863','813-776-5338','907-878-1779','303-317-6478','910-255-2392','260-865-8014','989-785-3672','544-481-4119','589-767-1061','121-250-1559','527-414-1643','925-797-5853','940-262-1551','743-595-0470','900-991-8713','172-547-4237','323-576-5531','792-024-3530','220-128-8354','960-098-6971','559-740-4510','229-656-0953','637-706-7572','874-323-7504','468-982-9920','958-621-0506','896-077-7129','133-626-8208','863-020-4540','979-094-9108','999-041-3369','471-059-3993','104-782-1879','725-592-1287','745-775-8440','999-085-2226','993-872-5869','666-413-2173','770-816-4522','455-133-1067','849-656-0186','357-373-9048','288-787-0661','195-564-0758','453-246-9377','356-145-3445','223-627-8076','337-893-7985','472-599-2832','790-141-8692','905-108-8540','409-935-5596','181-860-8453','524-391-2023','412-840-1618','929-361-0651','237-532-4381','642-988-4902','991-217-1702','363-118-9240','211-136-4238','639-125-1969','917-691-3057','472-393-7828','606-059-3757','701-521-4771','948-238-8512','243-688-2865','282-778-4373','584-782-8071','742-482-4335','852-185-1853','618-718-0327','604-649-7972','606-540-5386','926-487-3895','153-457-1120','380-415-4188','757-011-3053','895-073-0830','250-996-2808','236-512-6877','661-929-3749','243-625-4918','158-941-3208','496-513-7520','258-034-3889','166-254-9188','108-999-2670','305-889-5606','430-702-4740','130-958-6076','878-188-7376','888-967-8261','661-118-6055','540-776-4408','911-424-4606','256-540-1016','244-969-2440','854-104-5771','827-160-8212','679-143-0872','491-635-1659','558-137-4157','723-234-1055','170-587-6528','343-663-6921','213-951-4241','573-416-7190','984-556-2085','502-552-4257','589-890-1584','902-164-6331','984-710-9238','784-830-0373','510-812-2675','648-872-7210','655-129-5478','788-301-9014','983-931-9807','847-365-4513','811-349-9306','621-029-3127','716-100-5039','701-798-1889','931-903-8895','231-567-4611','403-201-6996','455-532-3135','526-388-7114','748-233-3841','940-815-1302','929-632-5789','568-228-5820','641-710-8357','109-587-5723','523-948-9012','257-648-6517','887-109-1739','440-019-3034','561-320-4486','808-597-3923','480-488-6959','345-520-9383','484-463-2853','493-962-1557','573-927-0926','338-291-7204','632-022-3253','926-237-5169','558-036-2012','368-555-9526','141-308-7523','772-453-4667','954-404-8122','951-186-8806','314-844-9824','774-487-7580','401-677-4830','799-072-9669','194-241-6734','878-992-1021','655-604-3418','337-754-0021','735-419-7324','187-749-9124','101-448-4178','152-336-5578','643-031-7876','313-271-0580','428-778-8975','377-245-9736','106-569-4886','102-447-9165','392-531-5372','662-557-7939','678-909-3251','475-492-4131','414-977-6279','511-033-5790','826-683-7377','221-717-9851','392-677-2790','576-986-0574','665-714-8238','379-864-7134','437-464-9734','915-333-0116','771-525-6469','510-595-9021','674-287-0170','994-782-2561','676-900-5408','254-311-8225','718-746-8438','485-623-5660','376-105-6502','127-841-0153','867-097-0018','868-635-2616','116-136-8522','301-187-6629','465-442-8578','381-590-2677','406-681-8436','910-026-4312','763-708-2175','719-231-3372','652-095-1012','966-935-8502','709-420-7240','562-312-7315','520-539-2885','851-728-3125','629-262-6985','391-081-0008','266-178-7614','743-223-0208','298-074-5755','644-835-6218','818-471-6214','628-732-3376','460-490-2208','343-208-9922','984-547-4416','336-286-1080','459-539-4386','447-893-6136','821-446-4187','481-321-9512','960-528-9183','986-813-0277','208-000-6041','246-171-7853','672-550-2310','526-224-1909','429-909-5753','505-091-3728','866-952-7060','608-279-4740','868-476-2295','972-322-2623','994-797-6012','753-240-1472','297-190-7512','766-206-5689','954-037-0580','975-494-2216','759-206-6485','587-663-6097','840-423-3900','456-937-8186','162-507-9590','666-022-6513','200-074-4710','147-445-1034','639-103-0772','271-576-7286','379-188-9431','957-848-2190','700-616-6577','707-563-6804','156-808-2130','651-952-9663','199-893-3965','795-707-9798','587-240-9655','816-778-1868','678-884-0735','132-580-6767','451-564-0372','858-524-8779','953-230-6474','381-839-3474','328-342-1930','830-629-6427','121-614-1686','975-559-7890','246-893-4751','171-323-8708','700-285-9481','395-911-6528','802-793-6383','271-031-6089','458-243-9932','181-890-3614','887-261-0272','393-017-2320','809-561-8127','803-185-5225','424-050-5876','520-217-9386','693-729-4724','603-417-0577','598-749-5832','479-135-6518','499-956-3191','163-941-0282','899-634-3976','139-763-8455','664-308-1906','235-175-3724','210-746-5189','117-947-1981','815-871-2603','785-423-8365','904-658-0379','240-773-6365','164-020-5022','529-688-0080','616-304-5279','791-734-8079','923-020-3387','646-076-5879','597-368-2939','128-779-0835','638-935-2157','257-579-2075','430-386-7033','773-967-7438','809-245-1025','502-871-1367','944-106-6212','364-182-5416','798-127-3372','284-352-0190','797-109-6679','232-975-0223','346-096-8823','451-535-4128','951-854-0986','595-482-0634','116-548-6239','231-913-2084','470-134-8830','999-570-7418','247-858-6649','484-403-8769','163-149-1500','436-458-4880','468-176-6209','963-504-3757','829-133-1970','943-062-6670','315-842-4025','189-735-9857','794-032-1933','133-389-0886','147-306-0171','978-096-0537','357-703-1979','353-802-5326','795-108-9516','132-806-2312','782-986-2067','954-429-1488','886-870-5770','974-825-3287','299-355-9352','827-522-8561','786-121-8868','794-581-3379','624-350-3338','745-092-9272','608-290-1734','590-539-5520','176-221-4567','799-985-1732','197-048-7180','832-441-9086','894-894-4588','250-977-9336','395-720-2481','574-604-8757','694-376-4482','293-275-2438','664-865-6686','333-441-2269','706-122-2218','146-228-1740','673-033-6761','924-785-0342','887-514-9477','989-604-6404','376-577-9534','378-529-4039','204-334-7557','912-127-8590','570-534-6012','311-063-1074','673-110-0142','933-369-3468','269-324-8225','429-474-8377','212-755-0128','102-322-9234','160-053-4000','728-374-9370','658-799-2665','803-100-7089','344-420-5380','108-947-2720','821-711-0251','324-936-1887','419-252-0343','549-397-1629','958-142-3325','928-788-5514','583-099-5649','192-255-8865','915-247-5214','526-972-6929','587-370-1338','465-079-8036','591-176-0280','432-158-2867','959-364-9214','381-855-2538','936-014-0636','479-480-9561','668-056-8528','478-629-8924','858-301-3312','800-376-8090','587-765-4618','960-240-2787','613-921-8114','896-320-7729','822-986-0382','644-179-2165','501-379-5771','954-525-0270','740-034-4012','179-796-0969','686-755-4034','271-988-0128','646-738-5889','754-811-1418','908-811-4776','600-770-1635','502-570-6821','753-566-7141','161-771-8263','259-650-2137','798-341-0722','332-107-3404','426-206-7926','290-697-5457','242-529-1709','777-095-4372','791-894-8938','741-602-5488','460-781-1281','431-269-6171','211-886-5784','941-602-3074','936-944-4430','337-643-9229','984-711-6159','109-911-4783','768-464-6828','938-475-5340','559-325-5729','178-151-1457','272-640-3477','577-767-9723','667-544-0727','204-094-1720','682-110-7980','122-879-8708','883-225-7222','884-476-5025','380-273-5508','590-903-0772','513-412-2181','106-150-0581','596-142-0981','757-834-2624','722-715-3910','775-545-7106','506-128-3123','515-028-0369','856-097-7529','456-681-8978','873-499-3065','625-213-4989','410-887-7553','920-659-5030','261-013-4482','802-727-1334','854-030-9379','807-653-6716','491-783-2612','269-915-7537','859-821-4619','316-915-4083','421-100-8473','584-773-0477','208-867-5022','228-763-3423','123-615-8174','739-327-9332','722-588-1182','786-962-6986','623-926-1818','390-801-8467','296-373-3523','623-236-6880','765-345-3836','738-549-4531','943-197-7074','332-776-3006','403-720-4929','153-530-7857','845-136-6134','285-052-4881','255-183-7565','537-538-2590','762-892-0690','630-217-7677','344-258-6469','142-889-9478','789-421-0526','927-653-7857','616-678-8283','835-554-9580','671-719-0763','642-132-5019','366-465-6282','352-420-2020','990-834-7120','308-827-2878','644-104-5713','121-786-3814','465-850-0083','294-317-1179','287-893-5432','555-782-5034','401-918-6525','401-453-0961','882-918-2031','834-413-6936','743-580-0078','852-601-7663','758-917-2042','817-064-3261','361-715-2116','581-830-4304','447-044-0867','150-649-8928','810-493-2504','918-162-0726','239-429-2322','225-436-4551','757-539-2887','883-245-7763','655-804-5159','926-956-2389','549-832-0561','851-190-2335','373-280-0623','379-668-3218','657-943-6914','224-482-2476','235-666-9473','506-150-4385','943-526-9262','778-025-9114','148-524-9318','966-418-3351','653-999-2687','499-997-0779','630-742-2015','828-637-9034','592-573-3728','289-557-2488','550-029-6318','499-362-0389','701-695-3070','806-036-8075','933-687-2604','239-667-7523','621-774-1760','643-354-1145','888-943-4267','334-067-4640','398-945-2902','438-989-8416','825-523-2689','724-753-0826','327-415-6914','704-531-3837','462-346-6563','943-682-0157','208-776-8360','567-130-3421','924-864-7561','671-365-8553','484-814-1288','813-373-7601','599-875-3274','622-374-4116','535-602-5861','316-866-6938','843-629-6504','410-539-9269','995-317-8055','505-639-3170','755-960-4512','765-613-1114','346-899-8926','602-102-1575','193-843-8173','166-804-1577','834-735-2406','238-109-4089','809-014-5236','759-994-5453','746-576-0931','861-429-1484','343-177-5871','268-709-4414','662-518-8273','585-514-5012','534-237-7440','680-554-3771','645-171-8388','343-579-0651','385-442-8316','673-784-3770','181-623-5776','903-482-1527','440-410-7561','888-037-3574','146-670-1957','439-081-6614','919-255-8904','280-331-6564','405-270-3971','985-921-3265','741-991-1325','335-597-7981','280-974-6126','720-521-8480','711-975-9337','203-034-0570','684-958-8523','447-166-2538','193-450-7012','735-078-2561','391-330-9627','129-811-8683','824-813-7095','778-851-1222','834-330-8308','478-192-9031','193-706-4069','494-959-1083','984-255-5050','116-687-3480','264-573-6285','955-209-0414','663-459-2065','357-959-5767','947-534-5976','310-627-9936','370-353-3434','447-130-7838','613-718-6990','397-701-6667','548-849-4871','338-646-3569','867-391-5763','752-742-3455','180-242-6665','944-631-4772','274-761-4809','284-459-0581','887-512-5139','940-045-9888','799-123-8208','841-791-5621','976-143-1912','497-354-8527','174-620-1976','232-668-2321','380-389-1987','761-558-3371','771-517-5934','422-119-1812','710-315-3510','588-320-6816','220-693-6503','311-377-3663','242-042-0396','812-320-6263','433-896-6783','761-824-2567','178-264-4711','421-809-0192','888-338-0201','422-646-8922','907-949-8573','235-652-8861','581-498-0867','311-920-7018','424-050-8965','615-998-4043','516-087-8885','384-514-8377','921-775-5971','193-731-7623','797-236-5157','154-607-8679','866-824-9272','957-788-7946','563-509-2551','325-336-4726','854-706-6409','190-930-0490','185-662-1611','239-824-7208','134-640-8912','264-990-7573','785-298-8129','797-255-2151','859-534-2003','186-969-7229','357-886-2847','994-459-4179','828-068-6972','727-343-0712','679-928-1130','133-106-7043','442-599-1106','650-277-7781','396-250-3934','950-366-4871','678-883-5810','401-435-6914','444-979-3338','658-495-8198','876-635-2325','917-596-4733','905-912-7928','178-791-3209','784-202-4890','699-498-8202','396-641-8381','946-946-9234','216-998-3528','662-075-6590','121-489-0567','879-936-8786','773-916-7576','425-750-4023','211-579-7912','987-104-0323','249-857-1025','363-711-2334','457-964-9469','260-039-8332','461-065-7751','479-275-1438','357-497-3188','441-640-1561','367-257-7685','620-226-2236','364-344-1908','779-108-5428','414-722-9805','215-085-1923','779-036-4832','742-099-5283','925-377-2318','783-539-4577','703-709-3551','534-899-0669','111-187-6120','629-342-7118','855-249-7553','198-651-5937','153-708-2230','288-794-7124','201-178-8579','854-557-7577','106-175-2129','640-821-0570','139-695-0924','539-821-6425','921-751-4981','365-278-0408','581-367-6955','813-588-0274','880-412-0751','516-998-9757','625-326-5757','700-150-8937','826-925-0508','953-363-8138','320-933-5880','593-488-7390','565-027-8900','490-337-7712','727-139-0183','615-831-2767','972-808-2570','395-314-5236','838-246-5971','118-877-3021','408-559-4423','621-615-7520','851-670-9159','520-737-6141','823-483-5530','268-469-1336','160-840-1287','656-038-7625','891-546-3934','269-547-7221','589-013-0174','243-467-8477','461-518-8759','516-782-6821','512-336-7385','951-881-6134','779-916-2861','206-660-9038','926-348-2627','381-866-0180','602-509-0161','657-407-4774','730-658-9961','472-446-7263','864-154-2737','165-650-5080','960-522-8581','195-276-4610','889-084-8172','284-409-6775','394-715-4351','918-816-4128','764-869-1563','411-628-6185','986-453-3973','557-946-2629','132-005-5006','191-343-0261','938-508-8221','925-869-9418','122-937-0025','262-733-7680','375-968-6455','490-726-6518','263-804-6577','768-419-8341','346-587-2388','678-356-4608','266-295-6582','273-181-6869','260-986-4827','224-045-7288','867-420-0416','361-714-7526','201-103-7054','696-760-8321','653-302-1226','726-459-1551','264-497-4820','733-640-7736','806-493-9767','671-387-1796','397-982-4739','404-183-6863','182-976-0274','260-244-2025','919-092-4540','880-428-9075','148-773-0585','298-609-1021','768-880-6012','187-380-8345','635-788-0390','346-484-7071','960-959-8754','701-147-4811','610-458-3825','461-231-5845','670-182-7583','755-081-5180','374-012-2529','515-897-3235','164-267-9773','769-930-8312','461-713-4923','751-097-4671','337-719-3818','411-964-2252','158-697-9699','212-353-4610','152-926-3171','202-963-0172','439-735-1279','781-524-0559','709-912-1083','312-694-0802','920-651-0818','882-218-7703','738-362-6716','629-210-1910','890-544-4284','954-153-6689','461-279-0416','526-510-3287','792-087-0814','413-740-7467','708-311-6176','388-821-3621','959-985-9930','669-778-4708','783-858-5339','135-392-3465','723-429-6969','924-723-3421','801-136-8651','209-824-7378','496-762-1836','389-449-1255','849-453-1726','473-028-3163','128-787-5960','748-508-2269','288-860-1420','106-962-4226','909-269-9365','963-855-2257','162-370-3320','943-606-1761','921-926-1632','695-291-6751','942-973-8623','333-188-3707','758-506-3920','255-576-5279','848-054-4891','488-041-0304','196-857-1277','108-674-7139','843-744-6267','837-560-4078','481-238-9198','563-968-6012','414-263-3420','978-617-9934','312-013-2860','443-369-5532','513-798-3255','702-687-8983','952-069-5030','969-432-8634','557-329-6979','981-887-0928','782-499-9321','637-602-4533','604-507-7641','731-134-8567','535-472-8480','958-801-7839','438-838-3130','897-138-3179','484-424-7009','622-888-4859','328-662-7865','723-252-8484','150-261-7761','620-662-2131','547-557-6506','289-408-1865','260-724-0527','657-521-2478','918-582-8273','971-493-0784','290-405-6969','400-727-0555','726-480-6027','111-804-5139','708-826-2687','359-756-5933','268-612-0634','787-041-9590','359-618-9030','258-110-5104','780-026-8163','482-676-5739','324-699-4453','359-081-7390','177-278-0098','797-300-0668','847-952-0402','411-829-2961','859-213-8484','516-014-4732','875-285-6272','785-292-0053','831-994-0053','925-776-0324','320-577-0755','974-754-9825','523-691-4143','206-143-0330','848-734-7265','221-574-2331','985-677-5546','889-800-1559','741-696-1573','716-593-1989','728-817-5130','645-960-3512','798-202-8126','821-856-7569','473-425-8122','558-302-3484','700-887-5732','538-393-7473','473-037-0384','695-502-8585','366-799-3879','279-874-0022','106-227-7204','583-099-3753','683-055-1608','849-883-8308','877-254-0034','432-185-9726','384-117-5279','728-417-9540','446-284-2202','992-164-7477','479-271-4716','210-337-5074','302-629-6373','212-402-7173','567-085-1472','200-855-9967','517-603-8255','783-017-7974','478-918-1418','711-148-2586','828-962-7819','741-587-5974','491-587-9827','247-069-0687','211-738-5734','146-480-2340','222-686-6430','244-215-7316','392-510-6439','417-605-0933','367-388-1084','139-659-5531','977-524-9255','258-298-4430','933-998-0327','754-517-1116','803-707-3629','604-733-6638','294-397-2485','601-753-2025','239-188-6730','242-990-3890','258-252-0740','512-965-9424','681-721-9174','619-754-8106','906-332-3061','765-483-3573','507-995-8967','529-689-8870','874-675-0071','155-432-9739','658-837-6573','205-798-4463','972-085-6472','302-942-5995','149-597-9021','174-029-6026','495-367-2861','933-720-4847','754-789-9781','873-002-6074','545-648-6663','362-244-1465','387-366-7663','201-795-6750','255-546-6261','224-551-5920','947-818-5955','844-218-2536','815-229-7659','825-839-4826','254-812-3984','200-353-8512','816-807-8730','519-220-6163','508-947-6539','854-494-3304','685-813-2010','963-516-0984','738-297-8118','585-353-4323','650-439-3040','293-074-2135','797-189-1364','616-784-6320','128-905-6832','176-456-1683','624-660-7089','811-607-0963','314-251-5574','651-598-2600','999-074-1590','837-089-2282','837-187-6332','604-402-5087','408-186-3618','658-810-9932','542-628-4002','795-221-4861','458-258-1857','400-760-1850','172-017-5518','418-309-0465','306-358-5428','766-366-9302','941-202-3004','807-470-1008','450-488-3985','323-124-3210','273-505-5739','816-195-9840','677-911-9773','272-349-0627','162-418-2188','304-891-5632','981-171-0825','645-286-0577','326-512-5769','290-644-1272','547-687-2116','457-337-7563','459-796-9580','949-423-7174','386-563-0151','522-389-5470','921-118-5232','458-628-9975','145-474-5583','814-532-4312','742-475-7112','113-834-1795','161-150-0288','104-781-4535','524-669-3336','164-040-1581','129-082-4654','933-472-5021','461-664-2140','345-298-5077','480-150-6912','765-732-8367','193-625-8318','246-835-7761','377-445-5466','388-406-0270','583-939-0530','558-476-7081','546-677-4650','554-620-0718','957-263-9621','934-336-8926','867-439-8078','401-708-7230','193-325-5035','586-149-0707','978-347-1432','982-509-9006','303-143-3574','496-634-7985','726-588-5235','339-187-9895','294-022-7225','163-707-6813','445-965-1330','307-825-8173','868-569-4753','854-388-4912','885-557-9125','906-507-8589','593-892-4487','396-770-4451','214-988-1970','812-603-5529','627-810-0027','357-782-8190','330-098-6424','792-831-6163','864-631-1058','358-279-9516','347-698-3255','362-703-8633','506-225-5557','804-366-7080','598-045-8879','600-080-8438','851-217-6680','668-083-5877','514-764-6649','176-853-8408','351-435-5369','344-564-5624','225-112-9598','412-559-7838','992-699-4754','731-125-4955','893-413-8685','259-080-1283','766-803-2929','889-662-6582','117-583-5681','490-016-1549','143-504-2083','871-757-6867','626-809-6238','221-235-9385','548-557-6643','588-437-3818','805-995-1207','518-632-8318','302-767-1710','676-025-1077','868-981-0124','347-442-7914','909-400-0933','180-885-2910','356-758-5237','995-529-2933','676-175-7606','332-091-8302','832-826-9084','305-047-2560','311-281-7520','298-004-6978','150-960-1113','841-659-0638','316-372-0195','476-049-4826','334-897-5071','328-301-1483','589-269-5040','695-454-1735','987-896-8985','631-782-0490','819-097-8875','283-458-9626','531-871-1420','762-695-4463','851-680-7521','964-456-7920','593-918-9157','501-029-7759','401-026-4948','183-517-7123','189-422-9282','198-929-4456','199-986-6438','387-317-3229','544-218-2230','887-786-6576','311-426-7424','684-177-9124','288-047-7137','699-109-0236','376-103-4738','855-466-2155','451-614-5639','644-459-3316','380-608-7260','938-926-5367','931-837-6710','827-805-5936','228-901-8778','784-070-2721','970-204-4471','138-790-2580','777-266-7210','194-347-4173','484-276-6041','211-544-5228','972-806-5416','718-527-3760','229-351-8742','189-127-9137','771-195-5829','129-623-1030','802-869-2678','941-112-6265','976-299-2317','514-632-6236','780-786-4134','209-208-9112','176-666-0465','466-503-1804','134-888-7610','251-636-8122','321-812-5382','945-039-8571','348-524-8730','328-515-1887','589-167-7312','358-722-1899','656-394-8530','517-730-7416','427-824-5074','478-173-8728','912-724-7721','681-374-6508','468-545-5282','423-025-2555','774-066-9475','885-741-2857','274-869-3727','465-244-8451','273-680-3553','507-220-2416','124-126-3288','642-200-7087','905-099-1136','608-100-1687','817-818-9178','242-009-7908','990-916-2316','644-643-9422','462-846-2612','882-453-8686','448-367-5054','320-641-0781','447-890-8589','791-658-2702','122-148-7475','232-747-0040','659-889-1067','320-952-6133','761-534-4002','539-199-6434','860-747-5763','530-116-2827','945-436-5686','931-947-0981','571-135-2240','892-517-1369','811-923-8763','428-308-0628','988-612-1579','600-896-8685','577-214-7238','750-113-0126','647-173-4218','252-710-5514','747-018-4940','350-602-2163','627-334-0438','677-050-5306','574-795-8114','776-779-3751','989-729-0927','692-609-9810','295-603-2869','223-809-6610','745-423-9172','754-071-9012','352-164-9563','243-444-3250','589-278-5303','954-929-8993','534-710-9872','103-756-9536','991-779-4975','483-895-4636','517-200-6776','863-981-8618','959-419-8967','855-127-1940','651-551-2324','413-226-3102','729-230-2267','865-271-3253','736-101-0221','171-561-6953','471-747-8683','637-298-9836','867-115-3355','933-376-8823','272-360-0490','903-922-3039','831-737-5612','355-742-2869','729-076-1655','286-350-4626','287-664-8080','629-325-4912','478-960-8081','127-011-2736','389-864-4561','335-943-1657','541-967-0733','300-197-5832','752-942-3390','221-677-7751','263-553-7948','547-674-2860','154-809-9535','378-184-1221','457-057-6227','877-866-6373','523-132-8850','974-660-0483','635-971-0320','691-043-9683','750-698-1855','986-666-2836','586-390-3135','240-850-6157','194-261-2790','791-669-9036','141-556-6989','902-813-0064','709-261-2039','707-002-0102','599-836-0989','882-048-6281','797-054-1538','390-466-5084','996-476-8573','839-793-9782','600-173-4908','876-137-6977','466-303-0721','347-010-9826','366-264-0371','741-424-6755','519-449-4478','153-630-8481','436-301-7674','871-475-2346','485-159-2090','238-214-6653','535-290-9651','736-050-4206','198-484-2985','133-147-0569','680-919-3916','774-694-9723','199-863-1360','343-936-7072','922-586-7187','275-186-1004','699-804-4578','371-822-0972','478-457-6148','623-466-6751','785-022-1121','618-180-7979','628-852-4316','315-753-9875','680-443-3549','496-511-9628','866-788-4369','646-030-9938','810-566-8921','894-840-6381','501-127-5451','103-874-5040','540-425-0130','214-285-7076','356-084-6737','422-175-0930','409-698-9410','700-637-6238','307-875-6569','155-523-4950','822-645-6680','668-748-5110','189-690-7075','745-181-0638','459-085-5889','748-503-6830','284-014-7297','271-030-7867','921-755-2936','617-164-0461','468-820-1574','925-299-8424','871-926-4079','933-277-1123','759-474-3010','195-037-9524','474-783-4440','517-099-5689','347-472-3878','737-578-0290','951-034-2469','119-020-0133','288-636-7839','948-376-9512','609-472-0310','250-959-8708','830-206-1708','306-011-1136','283-928-0306','202-763-0955','406-440-5265','922-405-1572','486-794-8160','906-231-9678','754-112-2623','893-191-0682','765-806-3373','371-719-2178','136-472-4238','437-901-6180','799-880-4098','522-075-2876','146-376-2070','306-064-7057','957-951-8333','465-737-1729','782-093-0132','399-244-6720','506-223-9261','503-541-0574','160-462-8680','306-347-9712','474-250-2581','728-159-2402','999-165-2299','296-860-2925','902-073-3746','335-117-7883','132-814-1051','945-475-0402','193-451-1577','376-446-1177','859-254-8621','860-980-1030','572-526-9816','237-862-0271','835-943-0392','381-725-8529','290-821-6498','602-048-5659','506-801-5520','621-290-0478','918-828-3276','452-464-9420','884-702-6488','941-023-5414','544-277-8010','170-090-7676','804-808-5501','800-747-2051','942-287-8451','473-892-3401','415-626-5665','799-066-1338','678-567-9061','322-489-5429','107-996-4638','980-196-3679','666-690-6880','219-402-7265','985-526-2426','484-370-6821','229-126-9678','230-964-7667','963-695-5010','956-328-3727','353-499-7185','761-772-0761','367-119-1302','140-091-2521','855-572-7781','402-443-5320','469-830-2577','838-351-9798','225-288-1702','494-733-9690','900-855-5655','256-869-1761','242-402-3236','973-805-1218','717-027-3922','380-555-9386','726-587-3704','434-262-5715','699-042-2228','828-702-9030','715-593-0361','473-357-5466','108-739-3936','511-801-6676','106-107-0276','325-941-3474','741-142-7327','936-679-5812','277-928-5071','151-454-2398','957-418-3202','843-098-5151','835-276-8157','561-787-7239','781-052-4423','156-837-5165','173-982-1420','950-918-7083','740-565-2131','529-943-1234','897-317-4161','687-598-6830','996-456-4470','704-344-0304','523-197-0902','916-234-8524','188-987-2821','165-085-4590','536-357-7281','368-604-0673','883-668-1216','380-178-7812','274-411-1772','204-222-2172','313-898-3334','487-953-1732','638-771-0439','582-857-0567','846-622-1308','835-552-1355','986-475-4132','206-555-3555','555-514-6953','723-668-3761','469-225-9692','786-678-2412','452-777-3069','584-068-0412','711-033-3306','661-103-9685','342-339-0320','419-028-5369','480-260-0255','186-534-2439','289-849-8490','962-145-9730','243-828-7230','744-185-3351','663-244-6553','404-283-5526','386-478-5882','840-747-3450','218-241-2832','686-757-3927','188-515-8521','834-976-6735','413-533-0674','676-214-4338','391-134-4363','616-571-3935','609-048-5161','579-107-5738','513-744-2962','668-610-2479','375-370-9535','313-949-3086','912-796-5773','940-385-4030','632-039-3578','838-345-1702','170-195-6528','348-764-1390','373-638-8082','695-348-2365','973-644-7445','987-680-4278','330-556-5670','680-654-1511','660-579-0870','140-280-2863','635-843-8055','997-620-3979','653-089-4174','639-801-7516','238-571-8579','289-850-0381','401-500-5577','820-559-0973','190-902-1505','256-136-4457','409-816-5632','470-131-2781','776-556-0040','467-802-6722','159-159-5877','354-739-5365','337-268-3861','584-031-3338','578-908-2912','271-069-9284','481-592-9875','950-080-3173','460-745-1826','585-853-7926','489-585-3579','747-369-1474','497-701-1728','272-931-0629','431-704-7029','133-250-2322','776-576-1579','533-171-9375','621-374-3051','387-979-6033','772-300-0661','954-325-7859','825-255-2277','284-676-0926','930-589-5546','171-564-7229','908-528-9970','334-786-3871','699-365-9522','318-765-4672','469-519-4021','359-209-0178','975-473-9959','360-805-8433','668-631-3653','320-213-6331','437-739-6216','424-670-7012','180-903-2480','233-079-5353','823-515-3528','566-530-5087','991-037-3724','184-602-1779','972-669-0604','308-926-0165','150-058-1822','503-038-2328','292-444-8510','110-454-7978','525-988-9933','117-954-1240','791-441-7172','148-268-1518','107-626-5930','888-464-0625','618-007-0638','916-235-8492','845-622-4310','481-426-1383','184-959-0761','304-963-6408','778-815-4751','207-051-4823','126-127-9501','615-906-3729','916-820-0603','394-683-1080','431-061-7387','232-041-7186','342-860-7018','468-723-4125','937-976-7035','991-105-1930','473-355-8442','101-323-9530','329-042-7774','312-899-3820','741-078-1673','608-475-8008','355-081-0538','868-905-1773','444-734-1239','643-358-7272','655-835-0403','804-291-9855','201-474-9632','353-101-6035','430-885-9175','113-519-6212','811-567-4526','978-037-1153','216-341-3702','362-782-9036','685-059-9520','654-792-8355','674-296-9620','654-817-3282','287-295-0085','975-919-5975','517-518-2610','515-159-0902','313-348-6150','407-409-7832','419-968-0021','256-558-1434','571-562-1865','106-001-4145','661-832-4114','272-469-1024','420-109-7843','536-346-4774','882-870-7020','561-079-0980','573-274-8525','360-877-0322','342-819-0070','526-603-4802','155-902-5319','350-970-9380','920-213-2053','149-953-1932','229-359-6926','694-780-2472','781-238-0992','714-561-2721','454-329-0118','332-459-9661','548-187-9806','324-301-6910','651-385-2629','579-074-5681','462-892-8028','146-154-1261','226-655-5879','313-296-9512','263-055-6772','229-279-6230','319-514-3624','511-675-0614','520-139-0784','503-537-9510','205-213-2169','380-369-9370','460-923-8533','972-808-1602','211-588-5916','212-586-8434','724-641-0456','961-907-6325','630-189-4920','455-894-2386','780-642-2857','399-410-2908','227-292-8751','383-389-5310','701-819-8551','951-440-8016','502-493-4140','809-484-3625','967-902-9180','421-211-4310','824-677-4027','337-050-9559','838-781-9899','118-240-1725','918-014-6469','860-696-1401','154-969-5026','285-644-6657','572-863-7574','739-941-0531','646-317-4465','575-233-9833','139-759-0880','472-612-7118','803-253-3456','273-964-4155','735-389-8481','150-079-3489','722-950-9833','295-235-8879','453-729-7027','233-308-7525','247-831-2224','480-474-2908','665-017-9391','824-597-4269','931-471-6825','825-333-7212','292-015-6816','920-637-3808','558-151-7788','408-037-1304','423-630-3239','894-366-6715','710-155-8882','939-715-1859','587-111-7882','832-805-2372','557-321-3420','612-910-3131','167-635-9975','410-427-5775','384-627-2814','315-637-3038','415-972-8826','351-284-8077','574-813-5260','971-801-0720','644-320-5267','347-897-8835','238-549-9253','681-612-8740','991-317-6178','552-851-1153','931-017-3898','446-395-9728','691-349-8125','778-249-7525','661-113-1181','821-072-2286','727-318-3879','316-758-0546','762-444-0829','770-516-0929','983-443-8051','956-574-1589','237-236-1792','174-270-6578','655-635-0763','253-908-0010','915-462-9808','785-989-5836','355-043-2921','976-191-7874','984-343-6431','119-041-2065','734-990-8529','481-086-5480','520-336-4375','770-312-2979','851-232-6094','813-321-3474','583-594-2607','890-471-3165','924-455-2376','629-606-1686','205-511-0271','419-633-6233','417-677-0376','295-228-2076','749-176-8589','169-967-0317','538-753-0938','347-664-1957','362-396-0173','817-186-9967','201-249-0425','958-848-3983','920-035-7925','161-910-9161','308-903-7072','272-031-1181','125-562-8218','658-648-0653','568-970-5150','347-512-6088','878-156-9553','718-670-9967','987-523-2487','392-666-4010','495-268-3583','538-065-8732','709-391-5976','947-827-4687','449-110-2406','577-648-4216','539-895-8910','812-674-4984','624-662-9128','635-105-7978','809-327-5561','480-320-2461','353-860-6263','242-325-1828','433-401-4162','727-605-2428','983-067-3233','526-539-1772','405-070-3751','636-251-5263','416-629-3184','713-931-6467','403-365-6848','999-707-1822','995-998-8053','550-544-7569','248-357-6830','818-893-5292','575-486-2014','477-138-7410','544-603-8504','587-408-5541','997-798-8540','614-535-5001','764-870-7529','950-196-9287','654-929-5788','923-738-2075','300-014-4051','786-308-0935','707-723-6880','996-577-2904','725-427-1122','123-627-8225','499-785-2179','251-513-9575','712-654-9387','390-269-0565','880-126-0151','460-799-4948','724-129-3263','679-871-9383','135-443-6241','996-958-4369','113-814-2252','730-994-9980','592-774-9106','278-305-2100','248-007-4981','146-148-6502','973-104-7275','250-869-2824','568-075-2014','197-492-2340','320-268-3823','413-511-3234','100-999-1040','626-760-3810','966-649-3975','884-142-2310','284-440-2224','972-978-2086','694-691-0578','853-198-8880','582-469-6231','441-487-9116','744-816-1181','672-509-0865','579-953-0038','404-606-0651','982-086-0675','290-980-0976','759-030-9706','977-946-3378','801-926-1499','908-809-0318','341-666-1880','568-414-2234','240-244-6123','972-154-6049','454-504-3435','330-671-9265','758-088-8645','942-203-0120','436-289-7743','682-623-0706','385-741-7689','436-758-2750','478-502-9773','969-793-3800','523-628-5123','452-967-2681','790-624-2525','742-652-1825','744-572-2314','420-041-0022','812-242-5878','223-777-4177','353-256-7030','836-276-0730','868-640-3738','226-272-2920','899-519-2262','925-653-2655','460-309-0540','210-962-5331','487-412-0561','282-448-6722','161-891-7187','732-151-7931','835-471-8238','860-515-3220','685-534-3123','127-803-2921','107-880-4122','475-353-7300','965-862-7321','173-913-2736','776-783-5463','543-322-8271','945-129-3219','542-080-5273','249-165-4053','887-729-3373','960-614-7887','529-682-5879','609-560-8032','943-857-7076','619-620-3210','490-656-7426','329-319-6778','854-165-0288','173-528-0139','226-868-8214','167-822-3130','432-859-7826','152-092-8422','681-335-1204','305-670-9165','461-246-0259','488-128-6925','801-391-8279','141-766-4678','602-030-0974','693-482-7667','547-930-5580','957-767-2777','379-841-4481','438-013-9534','539-077-0163','685-661-7299','238-247-6730','469-950-8327','236-349-0857','748-404-5871','980-639-9932','689-958-0339','751-842-6078','503-147-3655','774-284-3642','762-945-9830','994-418-2859','581-653-7485','782-267-6673','804-964-9538','712-067-6217','893-943-1571','792-192-1915','540-227-8110','323-135-2608','503-010-8178','624-726-0672','300-358-0623','561-377-6406','750-436-0539','312-603-2902','305-410-7572','775-747-5218','674-287-2869','574-080-7961','475-559-8940','570-707-8613','134-327-2161','513-529-2755','786-835-1977','878-716-5324','412-068-4413','578-135-1099','931-425-5221','730-683-0288','886-308-9123','604-080-0920','911-285-2540','551-082-3824','585-397-1359','232-458-0057','152-179-8467','881-849-6639','738-642-5078','631-256-4121','928-560-4363','269-924-1231','764-875-9584','114-229-9240','254-914-6955','395-637-4951','407-421-9309','199-890-0830','298-295-5018','679-955-8324','462-884-3781','387-553-1716','770-707-5136','783-633-5387','487-713-5470','575-268-7712','314-970-9640','531-226-7533','833-698-7526','801-620-3840','772-745-3125','972-900-7629','306-446-3252','971-939-0487','728-427-4365','261-587-3679','160-780-7083','688-044-6778','960-974-9759','312-791-6838','715-836-0881','476-048-7920','595-717-9216','994-970-1812','652-920-3465','817-423-7869','408-712-5625','317-546-5510','228-847-3087','928-445-4340','797-178-5288','999-146-4092','778-429-0573','695-703-1489','283-643-8606','531-555-1722','203-434-6463','546-061-5481','759-626-8579','855-878-2406','804-060-8453','826-899-7114','776-351-9236','320-717-2026','488-470-6913','924-635-8721','417-545-8017','303-720-7867','252-586-7772','514-677-3610','240-651-1880','890-536-3789','571-857-3598','815-405-6729','470-807-2465','201-405-9227','417-406-3965','265-445-3739','424-308-6823','254-408-3888','386-967-4922','759-170-3673','563-195-4059','250-804-3173','475-031-0289','772-457-8130','185-663-9808','471-172-8838','628-552-1033','456-772-1030','531-379-9538','692-608-8114','987-080-8578','355-243-9777','324-624-9324','770-831-4216','350-768-0835','303-192-0459','747-098-6734','225-779-3949','307-711-0101','876-805-6706','801-868-6210','930-300-7379','422-297-0730','371-736-1430','839-592-1520','778-047-8440','962-585-3163','462-080-5406','100-206-2278','596-952-8165','216-452-2053','339-050-0826','151-372-7067','967-307-6998','159-285-7629','165-851-0828','331-470-4872','894-425-3678','460-437-4804','897-551-4053','689-991-5026','580-956-3120','804-456-9282','147-959-4961','819-030-5469','380-039-3925','655-033-9900','143-761-6129','119-942-8057','926-858-2916','122-692-9985','654-229-3721','776-498-6279','218-975-5334','828-599-0651','405-292-0463','209-556-0920','562-009-3871','968-983-1884','566-535-6194','815-605-5023','656-975-8567','954-011-2121','120-341-3269','161-716-5083','201-247-8006','226-602-9073','147-879-6639','293-433-3839','999-857-2718','511-928-2908','483-771-0208','765-224-7083','721-601-1339','994-923-8427','789-068-2163','294-092-4381','653-261-2440','478-560-1938','877-009-8518','837-134-6512','889-954-9510','882-642-3220','498-016-0250','767-262-0432','343-437-6831','638-463-6131','602-796-2067','668-326-5559','775-594-0489','576-888-4623','746-506-8425','226-178-6710','663-814-9781','198-437-2714','373-482-3840','335-563-1195','950-308-2608','474-847-6557','395-972-1673','865-822-6573','478-561-7136','496-707-1690','289-474-6839','287-864-3230','310-576-2920','167-803-4080','131-708-6759','155-823-4406','630-537-7679','587-541-2963','875-606-4971','172-932-7064','116-511-5238','213-494-4105','894-292-4983','306-272-7602','917-086-1575','779-635-5937','548-266-2930','719-847-9412','669-879-7856','840-680-0937','611-432-3722','897-919-6430','726-898-9714','368-304-2170','421-767-5763','394-067-2739','408-935-5469','502-481-3391','508-782-4223','823-498-1157','109-687-2305','994-621-8738','725-133-0770','303-698-0887','622-572-0531','538-308-1428','650-540-7704','533-831-1210','174-365-4124','768-412-9612','658-158-7436','975-207-3902','259-624-6877','761-857-9380','514-719-3622','751-665-4769','111-815-3884','490-767-7723','726-273-3929','536-699-4040','318-526-8928','683-789-9050','906-836-6790','892-684-7390','641-340-2455','707-400-2640','974-604-7153','166-660-9990','349-196-2177','570-353-0352','958-267-7388','206-841-9020','574-611-0232','902-031-5735','764-521-8039','104-955-6526','722-171-8171','235-553-3785','988-163-9677','437-752-3951','724-039-3620','929-826-4389','858-488-0139','809-644-6590','458-119-5524','523-088-8820','957-319-2108','212-315-8316','197-518-6367','446-861-5432','192-247-1874','811-453-3260','342-749-7634','199-121-8956','673-514-7532','679-820-6872','281-182-7579','931-946-1486','623-471-7075','865-944-0980','834-348-7290','211-082-5223','726-237-8476','469-016-0920','606-255-4136','107-660-0712','927-219-2427','191-971-9016','731-808-6049','234-839-2827','488-380-8318','179-932-0110','627-672-3957','164-661-6732','592-924-8076','669-729-1172','987-704-8482','492-219-9976','288-892-8928','856-886-1970','454-556-5181','190-457-2638','802-986-1856','655-688-0866','590-932-4910','889-361-7106','913-049-0688','284-906-2828','963-892-2933','403-946-2280','611-054-5657','584-417-9367','806-196-9089','167-688-0130','884-735-3451','271-670-2693','502-598-2912','364-983-6634','677-157-4026','733-159-1597','488-444-1080','576-157-1629','701-133-6528','428-496-7078','750-146-8710','487-065-1912','922-379-9161','127-234-8278','776-817-2306','874-094-1620','392-946-3350','812-801-5821','621-840-3750','657-486-5687','718-146-4181','156-106-1408','370-840-1130','183-131-5789','915-386-8383','704-254-3900','739-135-7681','305-461-0933','538-136-3940','985-063-3081','976-130-9890','726-406-4620','531-618-8236','795-776-0608','450-125-1832','356-058-6034','252-465-8335','125-533-6081','754-119-4576','950-441-5918','371-734-2420','377-327-2398','765-052-7904','638-994-8875','718-371-1159','652-269-0449','485-925-2130','490-173-5859','885-309-2025','491-304-5621','216-649-0989','891-419-5856','930-549-5312','559-875-4081','739-005-8274','809-565-5872','754-660-4161','301-893-0306','253-807-2830','405-632-0553','159-888-8175','668-250-1435','655-182-2754','760-491-3067','403-771-7675','330-846-0383','371-912-0355','973-694-0153','998-638-3506','991-211-9602','657-271-7714','407-770-8516','573-463-7934','533-342-6665','773-585-3679','445-446-4180','259-600-1985','364-969-9584','468-173-0873','554-419-5723','854-821-5204','423-183-7578','340-823-6633','940-015-8246','994-857-4586','158-561-9347','379-256-6514','440-578-8107','494-683-7970','225-310-9835','806-033-2326','861-274-3223','334-107-4016','114-040-9098','743-170-3327','289-104-4389','539-672-7140','491-634-1536','546-125-3961','870-911-8810','307-693-0276','196-350-8988','233-938-1858','582-532-9816','803-651-3808','509-212-4269','465-155-9381','339-638-4259','106-094-1583','254-180-3895','832-514-1518','103-469-8473','371-848-1237','648-787-1365','247-145-8608','322-184-0814','174-241-6432','728-724-0781','549-132-3659','860-191-6734','908-478-4150','194-346-5506','366-424-2588','393-758-1875','888-294-1384','866-222-2463','614-788-5504','926-527-2676','123-929-9920','794-120-6218','876-775-1157','225-623-6183','152-827-1812','384-648-3518','908-513-2169','750-245-9819','501-438-0420','937-479-8028','380-995-8014','206-259-3655','243-392-5006','289-926-6121','245-986-6504','254-833-8525','385-175-6821','241-396-2214','953-378-5426','590-874-9248','902-706-0481','934-912-9139','418-857-0002','748-193-2286','642-002-2370','927-805-1925','772-681-8432','334-613-9902','412-105-8283','197-289-4823','200-939-3270','629-406-4220','361-953-0811','540-471-4518','252-523-6118','553-291-7375','279-179-9830','863-509-0318','485-546-1776','307-491-2299','343-999-0304','947-208-8086','224-433-4423','100-248-7190','704-457-7818','184-024-9177','922-998-6047','225-039-1888','449-723-2427','777-265-4008','241-100-6899','184-480-4373','336-224-4189','692-232-0567','674-668-4089','438-251-5125','200-525-2861','426-016-9810','252-917-2812','175-181-1977','551-304-0736','701-741-4514','383-315-3838','416-210-6553','876-713-6437','687-778-8525','262-065-0557','753-765-8579','208-343-7050','554-940-2396','198-781-6032','598-582-7320','539-374-9781','406-432-0923','265-613-2424','780-418-9181','516-551-1567','491-906-7995','503-761-3276','209-510-1067','552-694-3279','111-883-1870','250-206-1523','139-675-2569','197-958-3702','402-665-5829','707-628-0527','586-431-4430','326-163-5181','682-535-7802','972-376-1638','496-457-6681','634-846-8479','160-636-6934','448-693-4665','673-262-8400','306-979-6712','142-739-5080','195-664-4789','334-059-0518','459-906-9429','470-210-0355','782-611-0606','603-223-1857','142-546-0885','750-159-7318','800-107-7375','714-643-9488','980-999-2689','309-466-5988','751-713-1406','569-028-7653','799-938-4755','373-422-7930','747-448-4876','911-427-6688','605-039-8957','766-359-9340','610-242-0131','978-208-2155','682-766-4539','120-563-5006','553-210-3855','797-485-8968','416-965-1122','514-332-8261','878-226-3720','119-693-0574','743-316-2371','147-710-9367','792-854-5832','128-254-1930','734-801-9360','189-659-1951','662-291-7160','474-684-5327','649-416-6961','835-655-2838','578-009-6153','819-570-7165','804-134-7989','358-191-0551','340-720-4665','642-149-6192','574-781-5321','470-892-8620','183-790-2939','456-445-9618','747-760-9418','457-014-7020','784-739-3361','544-077-8508','926-906-3350','407-386-6880','953-638-0438','825-222-1537','284-004-7359','570-166-2357','725-273-8867','345-881-3731','230-126-1926','997-593-9279','200-604-8179','903-601-1431','487-404-3200','293-310-6395','162-223-0151','708-836-9506','140-868-6071','428-841-4378','552-649-8051','116-406-3902','904-545-4351','188-921-3540','615-257-1359','306-681-1171','197-134-0116','687-671-7869','445-260-2168','868-909-9188','346-451-7029','114-586-4670','724-857-8950','526-768-8824','723-792-4377','856-424-0987','390-761-7375','627-062-1543','644-623-1512','914-524-5614','234-430-2672','723-678-5910','315-421-2033','342-075-9539','951-823-3526','848-302-6178','849-298-5056','486-075-9867','398-606-5261','618-017-8225','661-117-5667','274-039-1550','598-898-7108','146-751-8106','346-763-6088','605-938-8930','657-785-9555','549-897-2183','910-819-4620','674-849-7853','402-065-2240','170-368-7871','701-564-8838','191-265-9351','909-703-3809','400-705-5071','388-678-0083','470-475-3340','152-112-0471','104-694-0518','185-838-1874','878-905-5088','716-183-6206','458-470-4877','189-216-4280','791-970-4475','495-615-6469','263-875-1227','137-050-0522','748-637-5983','700-632-9173','922-646-0483','411-585-8006','385-268-0687','239-717-3838','857-425-3108','351-170-2724','322-004-1390','651-910-0261','851-582-4241','865-870-1279','914-580-7071','598-879-0494','338-395-6296','710-166-4380','285-706-4321','646-755-7720','984-353-7537','960-200-9504','842-305-8355','214-196-5437','185-943-7187','773-160-1158','897-266-4424','799-965-2399','904-351-1889','586-005-9553','488-349-9167','710-149-3970','197-402-7932','480-604-7983','652-229-6931','962-156-7402','879-277-5455','308-330-6012','514-472-2238','586-141-1908','771-928-6182','655-696-4435','855-233-0167','311-422-7773','734-318-7463','896-184-6557','330-981-3581','766-212-9653','976-262-4410','519-184-9327','374-689-1140','417-230-0235','706-869-3183','163-566-6485','727-216-1721','317-592-9190','526-246-7636','226-906-6704','369-712-6269','597-122-1280','397-050-0872','990-909-0408','173-183-0280','814-491-7377','737-898-5282','961-853-8458','729-356-1978','281-845-9983','888-425-7625','377-592-8575','919-857-0670','765-187-7660','912-098-3469','317-539-7699','337-282-5681','354-211-0018','532-473-3504','835-239-6683','619-029-4406','254-679-1232','937-826-4178','733-933-7830','479-127-7071','240-790-4734','642-963-6353','261-489-8038','529-801-3677','299-016-1453','175-653-0787','748-173-3676','304-943-0159','791-156-5912','902-875-0267','445-127-5349','323-344-9329','562-108-5040','456-095-8472','327-330-0396','279-426-4951','741-470-1588','481-803-2617','150-849-6504','762-435-6822','610-501-3022','754-718-6404','286-770-7108','722-398-3914','500-367-8767','571-753-9924','173-934-8650','800-496-6979','780-574-1029','992-988-8589','575-776-3278','141-702-1453','559-379-9474','312-658-7235','775-337-3497','381-192-1980','111-289-0061','872-220-7938','643-985-0561','949-789-8277','539-896-8255','867-240-1685','725-618-1402','748-455-7539','636-347-7687','811-996-3221','216-713-8824','251-300-1642','656-582-4782','645-920-9176','984-608-1372','401-558-6289','205-193-1728','872-108-2868','871-116-7198','252-532-5035','725-124-0965','538-845-8581','649-531-0488','249-863-4526','242-425-7107','368-102-0261','729-365-0935','908-778-5677','932-364-0353','215-794-4778','949-158-8046','457-752-9921','193-733-9302','249-840-1628','251-509-3378','120-163-7185','738-546-8955','614-052-4102','288-243-0730','475-038-0261','535-122-3627','140-299-3236','721-291-4429','620-564-8869','171-300-3036','651-211-3732','845-058-1024','744-519-0918','990-400-4559','447-906-5402','122-690-5692','470-858-9876','658-766-2683','639-886-7050','958-850-6520','807-814-7140','878-461-4853','781-962-5057','307-249-7620','783-607-1580','357-968-4514','545-250-0483','367-022-0361','375-051-4951','750-613-0780','889-002-7238','432-965-5380','266-273-4072','117-690-5269','220-750-8230','291-859-6506','485-296-5136','533-499-6225','505-881-7882','904-143-6069','232-744-5532','761-780-8520','955-822-8299','658-924-1125','782-429-4651','623-065-8139','809-335-8975','712-078-6390','133-378-3922','209-192-9380','583-337-3086','673-102-1363','915-943-0814','466-017-6807','639-051-3371','257-400-2824','761-273-0180','698-818-6636','442-114-6012','382-292-6328','881-273-4380','375-962-7674','831-468-7761','108-571-1529','687-217-0237','117-406-9382','782-253-1071','816-397-5128','673-747-2914','455-388-8329','508-077-2077','333-963-6561','989-537-4081','727-529-0953','233-310-4504','764-344-9579','652-085-1772','959-403-6261','180-939-8571','167-510-5034','778-560-7932','141-565-4180','943-302-3865','843-910-3038','672-493-5923','920-001-2935','514-609-4576','263-632-8271','282-788-5869','726-321-5556','712-146-1372','846-216-8823','678-277-9733','826-360-6869','343-370-0361','842-474-6670','186-698-4925','660-073-0422','589-275-8361','827-963-4308','935-422-4408','141-338-9170','410-112-8561','914-608-4110','116-888-9516','599-606-4530','383-995-8253','886-481-3022','940-198-7228','255-902-4810','442-590-8510','847-404-8869','987-395-6740','421-674-0371','584-921-6460','347-932-8625','870-434-5569','211-854-1385','359-418-6824','267-780-9820','385-639-1604','763-100-4029','387-130-4421','204-915-8932','884-207-8402','986-147-9173','635-000-8083','300-143-4078','465-607-5206','334-404-4424','597-499-9040','364-000-0251','939-998-2333','853-583-6184','541-513-2361','755-880-9129','643-664-6572','157-745-7957','468-851-7486','245-016-1428','808-697-0540','364-090-6175','846-450-5796','453-149-4234','325-625-1955','161-633-8336','296-540-6625','971-708-3202','565-286-2321','652-469-1552','278-378-2814','888-631-0618','191-102-1655','141-171-0440','815-944-8357','501-915-4957','439-566-0600','437-232-7171','571-503-9232','868-021-4078','349-433-1172','485-962-1265','513-665-9500','354-768-3037','961-389-9453','255-528-0983','210-078-0965','171-438-2160','604-039-9025','992-360-5077','414-469-1533','574-596-0150','869-898-3624','197-743-4118','374-694-7785','963-836-9798','813-379-4989','190-056-0134','426-892-8023','803-405-2254','818-345-2033','569-496-4183','785-009-3361','747-259-5232','106-280-1859','769-696-0781','107-340-9740','831-990-4124','437-090-0922','500-251-4534','546-980-0457','116-316-6270','953-169-6529','650-338-2821','526-366-0459','141-811-8478','529-128-4239','927-318-6080','490-850-9190','143-172-4279','736-554-3185','615-755-2650','313-212-2444','888-723-7713','182-872-2080','212-076-8580','355-511-2530','949-412-6528','567-285-3718','822-750-1790','969-492-1570','863-962-2119','124-212-1932','618-878-7927','564-067-6233','839-145-7037','876-176-7621','598-477-3818','634-308-0878','405-471-7533','864-831-4740','142-537-9567','396-155-7381','936-153-9438','293-099-8138','164-121-6149','425-510-3839','833-560-3024','423-353-5083','954-248-4280','836-325-2330','506-873-7239','629-564-6614','611-134-9212','155-485-2883','790-536-3918','466-159-9912','790-572-1357','773-069-1387','636-314-8628','563-471-5494','577-174-8457','247-723-3176','346-727-3979','919-830-9522','404-644-4479','604-501-4713','718-592-6075','527-357-3010','105-411-1732','483-616-3808','602-289-6106','922-297-1731','133-499-9980','861-415-2308','913-170-4122','626-211-2922','459-583-4834','783-293-2953','607-272-9926','543-349-9682','205-695-2580','587-510-2929','512-828-6128','278-753-9450','553-094-9462','765-524-1506','281-583-1681','212-250-4873','912-973-0251','433-807-8781','330-987-1064','362-029-1073','351-499-4677','782-928-5392','444-665-7500','164-557-7720','777-433-5382','848-082-3861','400-273-6190','446-228-4072','402-896-3987','605-106-4704','255-447-8051','252-470-1523','651-371-3653','198-010-8567','263-695-7321','301-192-7421','469-699-9253','204-876-7480','638-954-5029','601-720-5780','493-955-7023','615-692-2557','317-990-8404','306-078-6263','323-730-9875','346-977-8986','108-021-2104','408-717-7810','210-320-5667','739-436-4353','408-111-6623','700-224-7320','218-569-6408','614-392-1018','515-730-4953','424-617-0681','756-372-9863','737-611-5970','202-348-1486','840-529-0751','284-295-7495','808-027-2261','108-761-7857','263-228-4738','357-764-3835','982-107-9781','956-883-7881','426-710-9389','379-444-6628','554-607-5657','531-132-0770','582-054-2820','667-791-5538','707-201-0887','801-835-9297','250-475-9557','232-785-5889','848-342-0559','267-377-7951','121-834-3170','427-029-5471','347-610-7627','445-651-2638','546-108-9379','798-339-9421','526-725-3086','773-744-4420','131-165-1733','513-501-7457','209-136-3676','768-604-4577','345-759-5387','514-665-1733','133-912-3470','707-474-5778','731-482-3239','508-440-4820','804-672-8386','586-818-6930','947-445-5040','310-320-1028','426-820-1614','636-419-8473','389-071-1284','276-582-4932','105-740-8540','509-909-1370','539-598-8512','303-251-0651','989-263-6511','743-695-4761','637-068-6726','805-739-9483','987-768-1972','398-920-9871','879-170-3043','447-134-7834','784-686-1232','883-558-0414','697-147-1371','294-380-0129','119-922-2208','379-005-7480','394-136-2021','225-179-2541','955-363-1241','917-881-9880','422-244-1055','459-733-1983','632-311-5272','531-299-2919','462-133-8553','389-952-7838','160-247-0489','421-657-1339','765-763-1292','875-983-7328','894-253-4704','963-067-0670','834-959-8276','940-057-0279','171-725-1835','612-552-1580','455-555-0175','618-607-0245','100-558-3402','379-922-5940','633-557-7861','985-544-0818','670-758-7836','621-319-7145','564-206-8329','530-770-7337','639-689-1183','901-980-6771','638-468-7871','728-264-3828','123-763-8459','722-163-2088','415-758-2336','323-976-4918','621-993-8404','860-808-9470','399-295-0116','352-633-9510','309-661-0161','788-704-5778','328-115-0424','812-463-9651','457-755-5527','110-959-4106','795-967-3567','727-302-9730','100-314-3507','112-921-1933','690-727-8189','764-522-7414','328-024-1521','227-116-6159','173-557-2416','482-231-6059','940-154-6480','963-924-5206','342-459-2338','431-648-0672','112-412-4861','744-774-9806','295-376-8059','748-076-0714','187-669-6482','711-924-7639','178-594-4258','652-209-7498','344-647-8677','423-089-9427','810-939-8988','102-700-5223','234-749-5435','985-056-9565','980-314-4561','321-702-0783','763-528-6233','994-552-1967','449-546-4985','920-197-5140','684-447-4204','908-540-0436','381-796-7141','168-324-9610','418-486-5831','816-721-6029','178-200-4435','320-338-1712','312-372-1520','472-477-6669','145-984-9694','967-772-7962','675-059-3661','917-191-4339','848-706-4543','841-922-6379','327-048-5823','387-670-8393','171-202-8163','211-956-2525']
  if (cid_to_compare_with.indexOf(cid_to_compare) > -1)
  {
    //In the array!
    window.is_error = true;
    $('#cid_error').show();
    $(".lead-form :input").prop("disabled", true);
    $("#cid").prop("disabled", false);
  
    dataLayer.push({ 'event': 'gTrackEvent', 'category': 'Picasso', 'action': 'ineligible', 'label': cid.value});
    $('#formsubmit').prop('disabled', true);
    return false;
  }
  else {
      //Not in the array
    $('#cid_error').hide();
    $(".lead-form :input").prop("disabled", false);
    $('#formsubmit').prop('disabled', false);
    return true;
  }
}