    window.shoppingLeads = {'Dynamic Remarketing - Extension (non retail)': 'Dynamic Remarketing - Extension (non retail)',
                            'Google Shopping Setup': 'Google Shopping Setup',
                            'Dynamic Remarketing - Retail': 'Dynamic Remarketing - Retail'}

    // lead form controls
    $("#appointmentCheck" ).click(function() {
      $( "#tag_appointment" ).animate({
      height: "toggle"
      }, 300, function() {
      });
    });
  
    $("#webmasterCheck" ).click(function() {
      /* this line for uncheck other check box*/ 
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

    });
    

    $("#is_campaign_created1").click(function(){
      if(document.getElementById('is_campaign_created1').checked == false){
          $(this).val(0);
          $("#rbid_campaign1").show();
          $("#rbudget_campaign1").show();
      }else{
          $(this).val(1);
          $("#rbid_campaign1").hide().val('');
          $("#rbudget_campaign1").hide().val('');
      }
    });


    $("#is_campaign_created2").click(function(){
      if(document.getElementById('is_campaign_created2').checked == false){
          $(this).val(0);
          $("#rbid_campaign2").show();
          $("#rbudget_campaign2").show();
      }else{
          $(this).val(1);
          $("#rbid_campaign2").hide().val('');
          $("#rbudget_campaign2").hide().val('');
      }
    });


    $("#is_campaign_created3").click(function(){
      if(document.getElementById('is_campaign_created3').checked == false){
        $(this).val(0);
          $("#rbid_campaign3").show();
          $("#rbudget_campaign3").show();
      }else{
        $(this).val(1);
          $("#rbid_campaign3").hide().val('');
          $("#rbudget_campaign3").hide().val('');
      }
    });
    
  $('#team').change(function(){
    var selectedTeam = $(this).val();
    if (selectedTeam == 'Gem Central America' || selectedTeam == 'Gem Central America'){
      console.log(window.is_loc_changed, "status")
      if(!window.is_loc_changed){
        setLocations(window.new_locations); 
      }
      window.is_loc_changed = true;
    }else if (selectedTeam == 'Services' || selectedTeam == 'Services (Traverwood)' || selectedTeam == 'Services Revenue Program (SRP)'){
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
      $(ths).submit();
  }

  // $("#tag_contact_person_name").change(function(){
  //     var tag_name = $(this).val();
  //     $("#shop_contact_person_name").val(tag_name);
  // });

  // $("#shop_contact_person_name").change(function(){
  //   var shop_name = $(this).val();
  //     $("#tag_contact_person_name").val(shop_name);
  // });

  // $("#tag_primary_role").change(function(){
  //     var tag_role = $(this).val();
  //     $("#shop_primary_role").val(tag_role);
  // });

  // $("#shop_primary_role").change(function(){
  //     var shop_role = $(this).val();
  //     $("#tag_primary_role").val(shop_role);
  // });

  function setLocations(newLocations){
    $("#country option").remove()
    $("#country").append('<option value="0">Program Location</option>');
    for(i=0; i<newLocations.length; i++){
      $("#country").append('<option value="' + newLocations[i]['name'] + '" location_id="' + newLocations[i]['id']+ '">'+ newLocations[i]['name'] +'</option>');
    }
  }
  
   // sshopping check 
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
    $('.shopping-policy').removeClass('error-box');
    $('.web-access').removeClass('error-box');
    // var check = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var check = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var cidFormat = /^\d{3}-\d{3}-\d{4}$/;
    var phoneFormat = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    var numericExpression = /^[0-9]+$/;
    
    var fix_slots = new Array();

    window.is_error = false;

    if(window.is_reset == true){
      window.is_reset = false;
      return false;
    }
    
    // Google Rep Name Validation
    grefElem = document.getElementById('gref');
    validateFiled(grefElem);

    // Google Rep Email Validation
    emailrefElem = document.getElementById('emailref');
    validateFiled(emailrefElem);

    // Programs Validation
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

    if (document.getElementById("manager_name").value == "") {
      //alert("Please Update Google Manager details");
      managerElem = document.getElementById("manager_name");
      validateFiled(managerElem);
    }

    if (document.getElementById("manager_email").value == "") {
      //alert("Please Update Google Manager details");
      emailElem = document.getElementById("manager_email");
      validateFiled(emailElem);
    }

    // Location/Country Validation
    countryElem = document.getElementById('country');
    validateFiled(countryElem);
    

    // Advertiser Info
    // Advertiser Name Validation
    advertiserNameElem = document.getElementById('advertiser_name');
    validateFiled(advertiserNameElem);

    // Advertiser Email Validation
    aemailElem = document.getElementById('aemail');
    validateFiled(aemailElem);

    // Email Validation
    frm.aemail.value = frm.aemail.value.trim();
    if (!frm.aemail.value.trim().match(check)) {
      $(frm.aemail).addClass('error-box');
      frm.aemail.focus();
      window.is_error = true;
    }

    // Advertiser Phone Validation
    phoneElem = document.getElementById('phone');
    validateFiled(phoneElem);

    // Advertiser Company Validation
    companyElem = document.getElementById('company');
    validateFiled(companyElem);
    
    // Customer Id validation
    cidElem = document.getElementById('cid');
    validateFiled(cidElem);

    if(!frm.cid.value.match(cidFormat)){
      //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
      $(frm.cid).addClass('error-box');
      //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
      frm.cid.focus();
      window.is_error = true;
    }

    // Advertiser Location validation
    // advertiserLocationElem = document.getElementById('advertiser_location');
    // validateFiled(advertiserLocationElem);

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
      foptElem = document.getElementById('fopt');
      validateFiled(foptElem);

      // Contact Person Role
      webMasterEmailElem = document.getElementById('web_master_email');
      validateFiled(webMasterEmailElem);

      // Contact Person Name
      poptElem = document.getElementById('popt');
      validateFiled(poptElem);

    }


    // ####################### Bundle Code Types Validations #####################################
    // Code Type / Task 1
    ctype1Elem = document.getElementById('ctype1');
    validateFiled(ctype1Elem);

    // Check all related fields for Code Type 1
    task1 = ctype1Elem.value;
    if(task1){
      if(task1 == 'Google Shopping Setup'){
          
          // Validate Shopping related fields
          rbidElem = document.getElementById('rbid1');
          validateFiled(rbidElem);

          rbidmodifierElem = document.getElementById('rbidmodifier1');
          validateFiled(rbidmodifierElem);

          rbudgetElem = document.getElementById('rbudget1');
          validateFiled(rbudgetElem);

          shoppingUrlElem = document.getElementById('url1');
          validateFiled(shoppingUrlElem);
          
          // Hava an appointment 
          if (document.getElementById("appointmentCheck").checked == true) {
            // Contact Person Name Validation
            contactElem = document.getElementById('shop_contact_person_name1');
            validateFiled(contactElem);

            // Contact Person Role Validation
            roleElem = document.getElementById('shop_primary_role');
            validateFiled(roleElem);

            // Appointments Date and Time Validation
            setupDateElem = document.getElementById('setup_datepick1');
            validateFiled(setupDateElem);

            if(setupDateElem.value){
                var slot = {
                'type' : 'SHOPPING',
                'time' : setupDateElem.value
                }
                fix_slots.push(slot)
              }
            }

      }else{

          if (task1 == 'Dynamic Remarketing - Extension (non retail)' || task1 == 'Dynamic Remarketing - Retail'){
            if(document.getElementById('is_campaign_created1').checked == false){
                rbidElem = document.getElementById('rbid_campaign1');
                validateFiled(rbidElem);

                rbudgetElem = document.getElementById('rbudget_campaign1');
                validateFiled(rbudgetElem);
            }
          }

          // Validate Tag related fields
          tagUrlElem = document.getElementById('url1');
          validateFiled(tagUrlElem);

          // Hava an appointment 
          if (document.getElementById("appointmentCheck").checked == true) {
            // Contact Person Name Validation
            contactElem = document.getElementById('tag_contact_person_name1');
            validateFiled(contactElem);

            // Contact Person Role Validation
            roleElem = document.getElementById('tag_primary_role');
            validateFiled(roleElem);

            // Appointments Date and Time Validation
            tagDateElem = document.getElementById('tag_datepick1');
            validateFiled(tagDateElem);

            if(tagDateElem.value){
                var slot = {
                'type' : 'TAG',
                'time' : tagDateElem.value
                }
                fix_slots.push(slot)
              }
            }
          }
      }

    // Code Type / Task 2
    // Check all related fields for Code Type 1
    ctype2Elem = document.getElementById('ctype2');
    task2 = ctype2Elem.value;
    if(task2){
      if(task2 == 'Google Shopping Setup'){
          
          // Validate Shopping related fields
          rbidElem = document.getElementById('rbid2');
          validateFiled(rbidElem);

          rbidmodifierElem = document.getElementById('rbidmodifier2');
          validateFiled(rbidmodifierElem);

          rbudgetElem = document.getElementById('rbudget2');
          validateFiled(rbudgetElem);

          shoppingUrlElem = document.getElementById('url2');
          validateFiled(shoppingUrlElem);
          
          // // Hava an appointment 
          // if (document.getElementById("appointmentCheck").checked == true && document.getElementById("appointmentCheck_2").checked == true) {
          //   // Contact Person Name Validation
          //   contactElem = document.getElementById('shop_contact_person_name2');
          //   validateFiled(contactElem);

          //   // Appointments Date and Time Validation
          //   setupDateElem = document.getElementById('setup_datepick2');
          //   validateFiled(setupDateElem);

          //   if(setupDateElem.value){
          //       var slot = {
          //       'type' : 'SHOPPING',
          //       'time' : setupDateElem.value
          //       }
          //       fix_slots.push(slot)
          //     }
          // }

      }else{
          // Validate Tag related fields

          if (task2 == 'Dynamic Remarketing - Extension (non retail)' || task2 == 'Dynamic Remarketing - Retail'){
            if(document.getElementById('is_campaign_created2').checked == false){
                rbidElem = document.getElementById('rbid_campaign2');
                validateFiled(rbidElem);

                rbudgetElem = document.getElementById('rbudget_campaign2');
                validateFiled(rbudgetElem);
            }
          }

          tagUrlElem = document.getElementById('url2');
          validateFiled(tagUrlElem);

          // // Hava an appointment 
          // if (document.getElementById("appointmentCheck").checked == true && document.getElementById("appointmentCheck_2").checked == true) {
          //   // Contact Person Name Validation
          //   contactElem = document.getElementById('tag_contact_person_name2');
          //   validateFiled(contactElem);

          //   // Appointments Date and Time Validation
          //   tagDateElem = document.getElementById('tag_datepick2');
          //   validateFiled(tagDateElem);

          //   if(tagDateElem.value){
          //       var slot = {
          //       'type' : 'TAG',
          //       'time' : tagDateElem.value
          //       }
          //       fix_slots.push(slot)
          //     }
          // }
      }
    }

    // Code Type / Task 3
    // Check all related fields for Code Type 3
    ctype3Elem = document.getElementById('ctype3');
    task3 = ctype3Elem.value;
    if(task3){
      if(task3 == 'Google Shopping Setup'){
          
          // Validate Shopping related fields
          rbidElem = document.getElementById('rbid3');
          validateFiled(rbidElem);

          rbidmodifierElem = document.getElementById('rbidmodifier3');
          validateFiled(rbidmodifierElem);

          rbudgetElem = document.getElementById('rbudget3');
          validateFiled(rbudgetElem);

          shoppingUrlElem = document.getElementById('url3');
          validateFiled(shoppingUrlElem);
          
          // Hava an appointment 
          if (document.getElementById("appointmentCheck").checked == true && document.getElementById("appointmentCheck_3").checked == true) {
            // Contact Person Name Validation
            contactElem = document.getElementById('shop_contact_person_name3');
            validateFiled(contactElem);

            // Appointments Date and Time Validation
            setupDateElem = document.getElementById('setup_datepick3');
            validateFiled(setupDateElem);

            if(setupDateElem.value){
                var slot = {
                'type' : 'SHOPPING',
                'time' : setupDateElem.value
                }
                fix_slots.push(slot)
              }

          }
      }else{
          // Validate Tag related fields

          if (task3 == 'Dynamic Remarketing - Extension (non retail)' || task3 == 'Dynamic Remarketing - Retail'){
            if(document.getElementById('is_campaign_created3').checked == false){
                rbidElem = document.getElementById('rbid_campaign3');
                validateFiled(rbidElem);

                rbudgetElem = document.getElementById('rbudget_campaign3');
                validateFiled(rbudgetElem);
            }
          }

          tagUrlElem = document.getElementById('url3');
          validateFiled(tagUrlElem);

          // Hava an appointment 
          // if (document.getElementById("appointmentCheck").checked == true && document.getElementById("appointmentCheck_3").checked == true) {
          //   // Contact Person Name Validation
          //   contactElem = document.getElementById('tag_contact_person_name3');
          //   validateFiled(contactElem);

          //   // Appointments Date and Time Validation
          //   tagDateElem = document.getElementById('tag_datepick3');
          //   validateFiled(tagDateElem);

          //   if(tagDateElem.value){
          //       var slot = {
          //       'type' : 'TAG',
          //       'time' : tagDateElem.value
          //       }
          //       fix_slots.push(slot)
          //     }

          // }
      }

    }

    if($("#is_shopping_policies").is(":visible")){
        if($("#is_shopping_policies").is(":checked")){
          $("#is_shopping_policies").val(1);
          $(".shopping-policy").removeClass('error-box');
        }else{
            $(".shopping-policy").addClass('error-box');
            $("#is_shopping_policies").val(0);
            return false;
        }
    }

      // Check If Error in Form
      if(window.is_error){
        return false;
      }else{
        var status = true;
        if (fix_slots.length) {
          status = check_and_create_appointment(fix_slots);
        }
        if (status) {
          $('form input[type=submit]').attr('disabled', 'disabled');
        }
        return status;  
      }  
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


function validateFiled(elem){
    // Validate Form Field
    if ($(elem).val() == "" || $(elem).val() == "0" || !$(elem).val()) {
      $(elem).addClass('error-box');
      $(elem).focus();
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

$(".ctype").change(function(){
    window.lead_type = '';
    $("#ctype2 option").show();
    $("#ctype3 option").show();

    var selectedId1 = $("#ctype1 option:selected").attr('id');
    if(selectedId1){
        id1 = selectedId1.split('_')[1];

        if($("#ctype2 option:selected").attr('id') && id1 == $("#ctype2 option:selected").attr('id').split('_')[1]){
          $("#ctype2").val('');
        }else{
          $("#ctype2_" + id1).hide();
        }

        if($("#ctype3 option:selected").attr('id') && id1 == $("#ctype3 option:selected").attr('id').split('_')[1]){
          $("#ctype3").val('');
        }else{
          $("#ctype3_" + id1).hide();
        } 

    }

    var selectedId2 = $("#ctype2 option:selected").attr('id');
    
    if(selectedId2){
        id2 = selectedId2.split('_')[1];
        if($("#ctype3 option:selected").attr('id') && id2 == $("#ctype3 option:selected").attr('id').split('_')[1]){
            $("#ctype3").val('');
        }else{
            $("#ctype3_" + id2).hide();
        }
    }

    curId = $(this).attr('id');
    $("#" + curId + '_campaign').hide();
    if($(this).val()){
        $("#" + curId + '_name').text($(this).val());
        $("#" + curId + '_appointment').show();
    }else{
        $("#" + curId + '_name').text('');
        $("#" + curId + '_appointment').hide();
    }
    
    if($(this).val() == 'Google Shopping Setup'){
        $("#" + curId + '_shopping').show();
        window.lead_type = 'SHOPPING';
    }else{
        $("#" + curId + '_shopping').hide();
        window.lead_type = 'TAG';
    }

    if($(this).val() == 'Dynamic Remarketing - Extension (non retail)' || $(this).val() == 'Dynamic Remarketing - Retail'){
        $("#" + curId + '_campaign').show();
    }

    if($("#ctype1").val() == 'Google Shopping Setup'){
        $(".shop_appointment-1").show();
        $(".tag_appointment-1").hide();
      }else{
        $(".tag_appointment-1").show();
        $(".shop_appointment-1").hide();
      }

    showHeadsUp();

});

// $("#appointmentCheck_2").click(function(){
//     var thisElem = document.getElementById("appointmentCheck_2") ;
//     if(thisElem.checked){
//         if($("#ctype2").val() == 'Google Shopping Setup'){
//           $(".shop_appointment-2").show();
//         }else if($("#ctype2").val()){
//           $(".tag_appointment-2").show();
//         }
//     }else{
//         $(".tag_appointment-2").hide();
//         $(".shop_appointment-2").hide();
//     }
// });


// $("#ctype3_appointment label").click(function(){
//   var thisElem = document.getElementById("appointmentCheck_3") ;
//     if(thisElem.checked){
//         if($("#ctype3").val() == 'Google Shopping Setup'){
//           $(".shop_appointment-3").show();
//         }else if($("#ctype3").val()){
//           $(".tag_appointment-3").show();
//         }
//     }else{
//         $(".tag_appointment-3").hide();
//         $(".shop_appointment-3").hide();
//     }
// });


function showHeadsUp(){

  $(".tag-policies").hide();
  $(".shopping-policy").hide();

  type1 = $("#ctype1").val();
  type2 = $("#ctype2").val();
  type3 = $("#ctype3").val();

  if(type1 || type2 || type3){
    // Type 1
    if(type1 && type1 == 'Google Shopping Setup'){
      $("#heads_up").show();
      $(".shopping-policy").show();
    }else if(type1){
      $("#heads_up").show();
      $(".tag-policies").show();
    }

    // Type 2
    if(type2 && type2 == 'Google Shopping Setup'){
      $("#heads_up").show();
      $(".shopping-policy").show();
    }else if(type2){
      $("#heads_up").show();
      $(".tag-policies").show();
    }

    // Type 3
    if(type3 && type3 == 'Google Shopping Setup'){
      $("#heads_up").show();
      $(".shopping-policy").show();
    }else if(type3){
      $("#heads_up").show();
      $(".tag-policies").show();
    }
  }else{
    $("#heads_up").hide();
  }
}