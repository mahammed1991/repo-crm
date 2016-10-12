// lead form controls
var argos = false
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
           $("#smart_goal_messsage_1").hide();
           $("#code_type_avg_time_1").hide();
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

      showHideArgos();
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
      // Clearing current div values
      argos = false;
      $(".shopping-policies").show();
      $('#is_shopping_policies').attr('checked', false);
      $('#issues_description').val('');
      $('#mcIdCheck').prop('checked', true);
      $('#shopping_trobleshooting_url').val('');
      $('#rbid, #rbidmodifier, #rbudget, #shopping_url, #mc_id, #description').val('');
      $('#shoppping_argos_categories').val('Business Type');
      $('#auth_case_id, #products_count, #sheets_link, #area, #additional_description, #mc_id').val('');

      // Uncheck checked option
      $('#Shopping_Trobleshoot').prop('checked', false);
      $('#Shopping_argos').prop('checked', false);

      // Hide other divs
      $( "#shopping_trobleshooting" ).hide();
      $("#shopping_feed_optimisation" ).hide();

      // Show Appointment Timing
      $(".appointment").show();
      //$("#appointmentCheck2").attr('checked', true);

      $( ".shoppingInfo" ).animate({
      height: "toggle"
      }, 300, function() {
      });
    });

    $('#Shopping_Trobleshoot').click(function(){
      // Clearing all divs values
      argos = false;
      $(".shopping-policies").show();
      $('#is_shopping_policies').attr('checked', false);
      $('#issues_description').val('');
      $('#mcIdCheck').prop('checked', true);
      $('#shopping_trobleshooting_url').val('');
      $('#rbid, #rbidmodifier, #rbudget, #shopping_url, #mc_id, #description').val('');
      $('#shoppping_argos_categories').val('Business Type');
      $('#auth_case_id, #products_count, #sheets_link, #area, #additional_description, #mc_id').val('');

      // Uncheck checked option
      $('#Shopping_Campaign_Setup').prop('checked', false);
      $('#Shopping_argos').prop('checked', false);

      //Hide other divs
      $(".shoppingInfo" ).hide();
      $("#shopping_feed_optimisation" ).hide();

      // Show Appointment Timing
      $(".appointment").show();
      //$("#appointmentCheck2").attr('checked', true);
      // $("#appointment_check_shopping").show();
      // $("#shopping_appointment").show();

      $( "#shopping_trobleshooting" ).animate({
          height: "toggle"
          }, 300, function() {
      });
    });

     $('#Shopping_argos').click(function(){
      // Clearing current div values
      argos = true;
      $(".shopping-policies").hide();
      $('#is_shopping_policies').attr('checked', false);
      $('#issues_description').val('');
      $('#mcIdCheck').prop('checked', true);
      $('#shopping_trobleshooting_url').val('');
      $('#rbid, #rbidmodifier, #rbudget, #shopping_url, #mc_id, #description').val('');
      $('#shopping_argos_categories').val('Business Type');
      $('#auth_case_id, #argos_mc_id, #products_count, #sheets_link, #area, #additional_description, #mc_id').val('');
      $("#tat-msg-block").hide();
      // Uncheck checked option
      $('#Shopping_Trobleshoot').prop('checked', false);
      $('#Shopping_Campaign_Setup').prop('checked', false);

      // Hiding other divs
      $( ".shoppingInfo" ).hide();
      $( "#shopping_trobleshooting" ).hide();

      // Hide Appointment Timing
      $(".appointment").hide();
      // $("#appointment_check_shopping").hide();
      // $("#shopping_appointment").hide();

      $( "#shopping_feed_optimisation" ).animate({
        height: "toggle"
      }, 300, function() {
      });

      // Hide Appointment date

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
       $('#smart_goal_messsage_'+indx).hide('');
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
    showHideArgos();
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
        if(!argos){
            $( "#shoppingTerms" ).animate({
                height: "toggle"
                }, 300, function() {
            });
        }

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

        if($('#shopping_feed_optimisation').is(':visible')){
            // Mandatory Fields - #shoppping_argos_categories, #mc_id, #auth_case_id, #products_count,
            // #sheets_link, #area
            //Validate Business Type Validation
            var argos_category = document.getElementById('shopping_argos_categories');
            var mc_id = document.getElementById('argos_mc_id');
            var auth_case_id = document.getElementById('auth_case_id');
            var products_count = document.getElementById('products_count');
            var sheets_link = document.getElementById('sheets_link');
            var area = document.getElementById('area');

            validateShoppingFeedOptimisationFields(argos_category, true)
            validateShoppingFeedOptimisationFields(mc_id, false)
            validateShoppingFeedOptimisationFields(auth_case_id, false)
            validateShoppingFeedOptimisationFields(products_count, false)
            validateShoppingFeedOptimisationFields(sheets_link, false)
            validateShoppingFeedOptimisationFields(area, false)

        }

    if(!$('#shopping_feed_optimisation').is(':visible')){
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
    }
    if(!argos){
          if($("#is_shopping_policies").is(":checked")){
              $("#is_shopping_policies").val(1);
              $(".shopping-policy").removeClass('error-box');
          }else{
              $(".shopping-policy").addClass('error-box');
              window.failedFields.push($("#is_shopping_policies"));
              window.is_error = true;
              $("#is_shopping_policies").val(0);
          }
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
    var status = true;
    if(window.is_error){
      focusElem = failedFields[0];
      $(focusElem).focus();
      status = false;
    }else{

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
    //$('.lead-form').delay(15000).submit();
    }
    return status;
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

    $('#smart_goal_messsage_'+selectedindex).show();   
  }
  if(['GA Smart Goals'].indexOf(selectedCodeType) == -1){
 
    $('#smart_goal_messsage_'+selectedindex).hide(); 
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

  $.ajax({
    url: "/leads/get-picasso-bolt-lead/?cid="+cid_to_compare,
    type: "GET",
    dataType: 'JSON',
    success:function(data){
      if(data['status'] === 'success') {
        isBoth = 'both';
      }
    },
    failure:function(error) {
      // body...
    }
  });
}

$('#country').change(function(){
    showHideArgos();
});

function showHideArgos(){
    // Teams allowed for Feed Optimisation Argos
    var allowedTeams = ['MMS One', 'MMS One Apollo', 'MMS Two', 'MMS Two Apollo'];
    var allowedCountries = ['AU/NZ','United States', 'Canada'];

    // Allow Feed optimisation argos only for the below teams
    var allowed = allowedTeams.indexOf($('#team').val());
    if(allowed >= 0)
        allowed = allowedCountries.indexOf($("#country").val());

    if(allowed >= 0){
        $("#shopping_argos_option").show();
    }else{
        if($("#Shopping_argos").is(":checked")){
            $("#Shopping_Campaign_Setup").trigger('click')
        }
        $("#shopping_argos_option").hide();
        //$('#Shopping_Campaign_Setup').trigger("click");
    }
}

function validateShoppingFeedOptimisationFields(elem, isDropdown){
      var err = false;
      if(isDropdown){
           if($(elem).val() === "Business Type")
                err = true;
      }else{
           if ($(elem).val() === "" || $(elem).val() == 0 || !$(elem).val())
                 err = true;

      }
      if(err){
            $(elem).addClass('error-box');
            window.failedFields.push(elem);
            window.is_error = true;
            return false;
      }
}

function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
}

$("#products_count").focusout(function(e){
    productsCount = $(this).val();
    if(productsCount !== ""){
        $.ajax({
          'url': "/leads/tag/argos-tat/",
          'dataType': "json",
          'type': 'GET',
          'data': {'products': productsCount},
          success: function(resp) {
                if(resp.success){
                       estimated_date = localTime(resp.estimated_date);
                       total_inqueue_products = resp.products_in_queue;
                       $(".estimated-date").text('');
                       $(".estimated-date").text(estimated_date)
                       $("#tat-msg-block").show();
                }
          },
          error: function(errorThrown) {
              alert('Something went wrong!. please try after some time');
          }
        });
    }else{
        $("#tat-msg-block").hide();
        $(".estimated-date").text('');
    }
});

function localTime(unixTimestamp){
    var localTime  = moment.unix(unixTimestamp);
    localTime = moment(localTime).format('DD-MM-YYYY');
    return localTime;
}