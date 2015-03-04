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


function setLocations(newLocations){
    $("#country option").remove()
    $("#country").append('<option value="0">Program Location</option>');
    for(i=0; i<newLocations.length; i++){
      $("#country").append('<option value="' + newLocations[i]['name'] + '" location_id="' + newLocations[i]['id']+ '">'+ newLocations[i]['name'] +'</option>');
    }
  }


  function validatethis(frm) {
    $(".error-txt").remove();
    $(".lead-form .form-control").removeClass('error-box');
    // $('.shopping-policy').removeClass('error-box');
    // $('.web-access').removeClass('error-box');
    var check = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
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
    

    // Timezone Validation
    tzoneElem = document.getElementById('tzone');
    validateFiled(tzoneElem);

    // Advertiser Info
    // Advertiser Name Validation
    advertiserNameElem = document.getElementById('contact_person_name');
    validateFiled(advertiserNameElem);

    tagAppointmentElem = document.getElementById('tag_datepick');
    if($(tagAppointmentElem).is(":visible")){
      validateFiled(tagAppointmentElem);
    }

    shopAppointmentElem = document.getElementById('setup_datepick');
    if($(shopAppointmentElem).is(":visible")){
      validateFiled(shopAppointmentElem);
    }

    // Advertiser Email Validation
    agencyNameElem = document.getElementById('agency_name');
    validateFiled(agencyNameElem);

    // Advertiser Email Validation
    pocElem = document.getElementById('poc');
    validateFiled(pocElem);
    
    // Advertiser Email Validation
    agencyEmailElem = document.getElementById('agency_email');
    validateFiled(agencyEmailElem);

    // Email Validation
    agencyEmailElem.value = agencyEmailElem.value.trim();
    if (!agencyEmailElem.value.trim().match(check)) {
      $(agencyEmailElem).addClass('error-box');
      agencyEmailElem.focus();
      window.is_error = true;
    }

    // Advertiser Phone Validation
    phoneElem = document.getElementById('agency_phone');
    validateFiled(phoneElem);


    // Check Agency fields
    if(document.getElementById('agency').checked){
        if(document.getElementById('same_task').checked){
            var sameTagTask = $(".tag:visible").length;
            $("#agency_same_tag_count").val(sameTagTask);
            for (i=1; i<=sameTagTask; i++){
                if($("#same_tag_" + i).is(":visible")){
                    // CID Validation
                    cidElem = document.getElementById('cid' + i);
                    validateFiled(cidElem);

                    // URL Validation
                    urlElem = document.getElementById('url' + i);
                    validateFiled(urlElem);

                    // Comment Validation
                    commentElem = document.getElementById('comment' + i);
                    validateFiled(commentElem);
                }
            }
              var sameShopTask = $(".shop:visible").length;
              $("#agency_same_shop_count").val(sameShopTask);
                for (i=1; i<=sameShopTask; i++){
                    if($("#same_shop_" + i).is(":visible")){
                        // CID Validation
                        cidElem = document.getElementById('cid' + i);
                        validateFiled(cidElem);

                        // URL Validation
                        urlElem = document.getElementById('url' + i);
                        validateFiled(urlElem);

                        // URL Validation
                        bidElem = document.getElementById('rbid' + i);
                        validateFiled(bidElem);

                        // URL Validation
                        budgetElem = document.getElementById('rbudget' + i);
                        validateFiled(budgetElem);

                        // URL Validation
                        modifierElem = document.getElementById('rbidmodifier' + i);
                        validateFiled(modifierElem);

                        // Comment Validation
                        commentElem = document.getElementById('comment' + i);
                        validateFiled(commentElem);
                    }

            }
        }else if(document.getElementById('diff_task').checked){
            var diffTagTask = 5;
            $("#agency_diff_tag_count").val($(".tagFields:visible").length);
            for (i=1; i<=diffTagTask; i++){
                if($("#tagFields" + i).is(":visible")){
                    // CID Validation
                    cidElem = document.getElementById('cid' + i);
                    validateFiled(cidElem);

                    // URL Validation
                    urlElem = document.getElementById('url' + i);
                    validateFiled(urlElem);

                    // Comment Validation
                    commentElem = document.getElementById('comment' + i);
                    validateFiled(commentElem);
                }
            }

              var diffShopTask = 5;
              $("#agency_diff_shop_count").val($(".shopFields:visible").length);
                for (i=1; i<=diffShopTask; i++){
                    if($("#shopFields" + i).is(":visible")){
                        // CID Validation
                        cidElem = document.getElementById('cid' + i);
                        validateFiled(cidElem);

                        // URL Validation
                        urlElem = document.getElementById('url' + i);
                        validateFiled(urlElem);

                        // URL Validation
                        bidElem = document.getElementById('rbid' + i);
                        validateFiled(bidElem);

                        // URL Validation
                        budgetElem = document.getElementById('rbudget' + i);
                        validateFiled(budgetElem);

                        // URL Validation
                        modifierElem = document.getElementById('rbidmodifier' + i);
                        validateFiled(modifierElem);

                        // Comment Validation
                        commentElem = document.getElementById('comment' + i);
                        validateFiled(commentElem);
                    }
            }
        }
      }

      // Check Agency fields
    if(document.getElementById('end_customer').checked){
        if(document.getElementById('same_task').checked){
            var sameTagTask = $(".tag:visible").length;
            $("#customer_same_tag_count").val(sameTagTask);
            for (i=1; i<=sameTagTask; i++){
                if($("#same_cust_tag_" + i).is(":visible")){

                    // Customer Name Validation
                    cnameElem = document.getElementById('advertiser_name' + i);
                    validateFiled(cnameElem);

                    // Customer Email Validation
                    cemailElem = document.getElementById('aemail' + i);
                    validateFiled(cemailElem);

                    // Customer Telephone Validation
                    cphoneElem = document.getElementById('phone' + i);
                    validateFiled(cphoneElem);

                    // CID Validation
                    cidElem = document.getElementById('cid' + i);
                    validateFiled(cidElem);

                    // URL Validation
                    urlElem = document.getElementById('url' + i);
                    validateFiled(urlElem);

                    // Comment Validation
                    commentElem = document.getElementById('comment' + i);
                    validateFiled(commentElem);
                }
            }

              var sameShopTask = $(".shop:visible").length;
              $("#customer_same_shop_count").val(sameShopTask);
                for (i=1; i<=sameShopTask; i++){
                    if($("#same_cust_shop_" + i).is(":visible")){

                        // Customer Name Validation
                        cnameElem = document.getElementById('advertiser_name' + i);
                        validateFiled(cnameElem);

                        // Customer Email Validation
                        cemailElem = document.getElementById('aemail' + i);
                        validateFiled(cemailElem);

                        // Customer Telephone Validation
                        cphoneElem = document.getElementById('phone' + i);
                        validateFiled(cphoneElem);

                        // CID Validation
                        cidElem = document.getElementById('cid' + i);
                        validateFiled(cidElem);

                        // URL Validation
                        urlElem = document.getElementById('url' + i);
                        validateFiled(urlElem);

                        // URL Validation
                        bidElem = document.getElementById('rbid' + i);
                        validateFiled(bidElem);

                        // URL Validation
                        budgetElem = document.getElementById('rbudget' + i);
                        validateFiled(budgetElem);

                        // URL Validation
                        modifierElem = document.getElementById('rbidmodifier' + i);
                        validateFiled(modifierElem);

                        // Comment Validation
                        commentElem = document.getElementById('comment' + i);
                        validateFiled(commentElem);
                    }

            }
        }else if(document.getElementById('diff_task').checked){
            var diffTagTask = 5;
            $("#customer_diff_tag_count").val($(".tagFields:visible").length);
            for (i=1; i<=diffTagTask; i++){
                if($("#tagFields" + i).is(":visible")){
                    // CID Validation
                    cidElem = document.getElementById('cid' + i);
                    validateFiled(cidElem);

                    // URL Validation
                    urlElem = document.getElementById('url' + i);
                    validateFiled(urlElem);

                    // Comment Validation
                    commentElem = document.getElementById('comment' + i);
                    validateFiled(commentElem);
                }
            }

              var diffShopTask = 5;
              $("#customer_diff_shop_count").val($(".shopFields:visible").length);
                for (i=1; i<=diffShopTask; i++){
                    if($("#shopFields" + i).is(":visible")){
                        // CID Validation
                        cidElem = document.getElementById('cid' + i);
                        validateFiled(cidElem);

                        // URL Validation
                        urlElem = document.getElementById('url' + i);
                        validateFiled(urlElem);

                        // URL Validation
                        bidElem = document.getElementById('rbid' + i);
                        validateFiled(bidElem);

                        // URL Validation
                        budgetElem = document.getElementById('rbudget' + i);
                        validateFiled(budgetElem);

                        // URL Validation
                        modifierElem = document.getElementById('rbidmodifier' + i);
                        validateFiled(modifierElem);

                        // Comment Validation
                        commentElem = document.getElementById('comment' + i);
                        validateFiled(commentElem);
                    }
            }
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


function validateFiled(elem){
    // Validate Form Field
    if ($(elem).val() == "" || $(elem).val() == "0" || !$(elem).val()) {
      $(elem).addClass('error-box');
      $(elem).focus();
      window.is_error = true;
      return false;
    }
}