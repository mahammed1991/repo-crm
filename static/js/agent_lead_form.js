$('#team').change(function(){
    var selectedTeam = $(this).val();
    if (selectedTeam.indexOf('Services') != -1){
      // if(selectedTeam == 'Services/GCE'){
      //   alert("Only Pinnacle and HiPo Newbie customers are eligible for Regalix support");
      // }
      //$(".tr_service_segment").show();
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
      //$(".tr_service_segment").show();
      $('#g_cases_id').hide();

      $('label[for="g_cases_id"]').hide();
      $('label[for="service_segment"]').show();
    }else{
      if (window.is_loc_changed){
        setLocations(window.locations);
        window.is_loc_changed = false;
      }
      //$(".tr_service_segment").hide();
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

    // Google Rep Email Validation
    emailrefElem = document.getElementById('emailref');
    validateFiled(emailrefElem);

    validateEmailField(emailrefElem)

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
    emailElem = document.getElementById("manager_email");
    validateEmailField(emailElem)

    // Location/Country Validation
    countryElem = document.getElementById('country');
    validateFiled(countryElem);
    

    shopAppointmentElem = document.getElementById('setup_datepick');
    if($(shopAppointmentElem).is(":visible")){
      validateFiled(shopAppointmentElem);
    }

    agencyInfoElem = document.getElementById('agency_info')
    if($(agencyInfoElem).is(":visible")){

      // Advertiser Email Validation

      agencyNameElem = document.getElementById('agency_name');
      validateFiled(agencyNameElem);

      
      // Advertiser Email Validation
      agencyEmailElem = document.getElementById('agency_email');
      validateFiled(agencyEmailElem);

      // Email Validation
      validateEmailField(agencyEmailElem)
      $("#aemail").val(agencyEmailElem.value);

      // Advertiser Phone Validation
      phoneElem = document.getElementById('agency_phone');
      validateFiled(phoneElem);
     

    }

    companyElem = document.getElementById('company');
    validateFiled(companyElem);

    // Timezone Validation
    tzoneElem = document.getElementById('tzone');
    validateFiled(tzoneElem);

    var isTagLeads = false;
    var isShopLeads = false;
    // Check Agency fields
    if(document.getElementById('agency').checked){
        if(document.getElementById('same_task').checked){
            var sameTagTask = $(".tag:visible").length;
            $("#agency_same_tag_count").val(sameTagTask);
            // Code Type Validation
            codeTypeElem = document.getElementById('same_task_ctype');
            validateFiled(codeTypeElem)
            if(sameTagTask){
                if($("#tag_datepick").val() != ''){
                    var slot = {
                      'type' : 'TAG',
                      'time' : $("#tag_datepick").val()
                    }
                  fix_slots.push(slot);
                  isTagLeads = true; 
                }else{
                  tagAppointmentElem = document.getElementById('tag_datepick');
                    if($(tagAppointmentElem).is(":visible")){
                      validateFiled(tagAppointmentElem);
                    }
                }
            }else{
              isTagLeads = false;
            }

            for (i=1; i<=sameTagTask; i++){
                if($("#same_tag_" + i).is(":visible")){
                    // CID Validation
                    cidElem = document.getElementById('cid' + i);
                    validateFiled(cidElem);

                    if(!cidElem.value.match(cidFormat)){
                      //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
                      $(cidElem).addClass('error-box');
                      //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
                      window.failedFields.push(cidElem);
                      window.is_error = true;
                    }

                    // URL Validation
                    urlElem = document.getElementById('url' + i);
                    validateFiled(urlElem);

                    validateDynamicFields($('#is_campaign_created'+i))
                    validateDynamicFields($('#product_expectations'+i))
                    validateDynamicFields($('#campaign_implemented'+i))

                    analyticsCodeElem = document.getElementById('analytics_code' + i);
                    if($(analyticsCodeElem).is(":visible")){
                      validateFiled(analyticsCodeElem);  
                    }

                    if($('#rlsa_bulk' + i).is(":visible")){

                          rlsaUserListEle = document.getElementById('user_list_id' + i);
                          validateFiled(rlsaUserListEle);

                          rlsaBidAdjustment = document.getElementById('rsla_bid_adjustment' + i);
                          validateFiled(rlsaBidAdjustment);

                          campaignIds = document.getElementById('campaign_ids' + i);
                          validateFiled(campaignIds);

                          existingBid = document.getElementById('overwrite_existing_bid_modifiers' + i);
                          validateFiled(existingBid);

                          newBid = document.getElementById('create_new_bid_modifiers' + i);
                          validateFiled(newBid);

                          rlsaPolicies = document.getElementById('rsla_policies' + i);
                          if(!$(rlsaPolicies).is(":checked")){
                             $(rlsaPolicies).parent().addClass('error-box');
                              window.failedFields.push(rlsaPolicies);
                              window.is_error = true;
                              return false;
                          }
                      }
                }
            }
              var sameShopTask = $(".shop:visible").length;
              $("#agency_same_shop_count").val(sameShopTask);
              if(sameShopTask){
                if($("#setup_datepick").val() != ''){
                    var slot = {
                      'type' : 'SHOPPING',
                      'time' : $("#setup_datepick").val()
                    }
                  fix_slots.push(slot);
                  isShopLeads = true;
                }else{
                  isShopLeads = false;
                }
              }
                for (i=1; i<=sameShopTask; i++){
                    if($("#same_shop_" + i).is(":visible")){
                        // CID Validation
                        cidElem = document.getElementById('cid' + i);
                        validateFiled(cidElem);

                        if(!cidElem.value.match(cidFormat)){
                          //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
                          $(cidElem).addClass('error-box');
                          //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
                          window.failedFields.push(cidElem);
                          window.is_error = true;
                        }

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

                        // MCID Validation
                        shoppingMCIDElem = document.getElementById('is-mc_id' + i);
                        if(shoppingMCIDElem.checked == true){
                            shoppingMCElem = document.getElementById('mc_id' + i);
                            validateFiled(shoppingMCElem);
                        }

                    }
              }
        }else if(document.getElementById('diff_task').checked){
            var diffTagTask = $(".tagFields:visible").length;
            $("#agency_diff_tag_count").val($(".tagFields:visible").length);
            var diffShopTask = $(".shopFields:visible").length;
            $("#agency_diff_shop_count").val($(".shopFields:visible").length);
            var totalDiffTasks = diffTagTask + diffShopTask;
            if($(".tagFields:visible").length){
                if($("#tag_datepick").val() != ''){
                    var slot = {
                      'type' : 'TAG',
                      'time' : $("#tag_datepick").val()
                    }
                  fix_slots.push(slot);
                  isTagLeads = true;
                }else{
                  tagAppointmentElem = document.getElementById('tag_datepick');
                    if($(tagAppointmentElem).is(":visible")){
                      validateFiled(tagAppointmentElem);
                    }
                }
            }else{
              isTagLeads = false;
            }

            if(diffShopTask){
                if($("#setup_datepick").val() != ''){
                    var slot = {
                      'type' : 'SHOPPING',
                      'time' : $("#setup_datepick").val()
                    }
                  fix_slots.push(slot);
                  isShopLeads = true;
                }else{
                  isShopLeads = false;
                }
            }
            // CodeType Validation
            ctypeElem = document.getElementById('diff_ctype-1');
            validateFiled(ctypeElem);

            for (i=1; i<=totalDiffTasks; i++){
              // CodeType Validation
              ctypeElem = document.getElementById('diff_ctype-' + i);
              validateFiled(ctypeElem);

                if($("#tagFields" + i).is(":visible")){

                    // CID Validation
                    cidElem = document.getElementById('cid' + i);
                    validateFiled(cidElem);

                    if(!cidElem.value.match(cidFormat)){
                      //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
                      $(cidElem).addClass('error-box');
                      //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
                      window.failedFields.push(cidElem);
                      window.is_error = true;
                    }

                    // URL Validation
                    urlElem = document.getElementById('url' + i);
                    validateFiled(urlElem);

                     validateDynamicFields($('#is_campaign_created'+i))
                     validateDynamicFields($('#product_expectations'+i))
                     validateDynamicFields($('#campaign_implemented'+i))
                    
                    // Analytics 
                    analyticsCodeElem = document.getElementById('analytics_code' + i);
                    if($(analyticsCodeElem).is(":visible")){
                      validateFiled(analyticsCodeElem);  
                    }

                   if($('#rlsa_bulk' + i).is(":visible")){

                          rlsaUserListEle = document.getElementById('user_list_id' + i);
                          validateFiled(rlsaUserListEle);

                          rlsaBidAdjustment = document.getElementById('rsla_bid_adjustment' + i);
                          validateFiled(rlsaBidAdjustment);

                          campaignIds = document.getElementById('campaign_ids' + i);
                          validateFiled(campaignIds);

                          existingBid = document.getElementById('overwrite_existing_bid_modifiers' + i);
                          validateFiled(existingBid);

                          newBid = document.getElementById('create_new_bid_modifiers' + i);
                          validateFiled(newBid);

                          rlsaPolicies = document.getElementById('rsla_policies' + i);
                          if(!$(rlsaPolicies).is(":checked")){
                             $(rlsaPolicies).parent().addClass('error-box');
                              window.failedFields.push(rlsaPolicies);
                              window.is_error = true;
                              return false;
                          }
                      }

                }else{
                    if($("#shopFields" + i).is(":visible")){
                        // CID Validation
                        cidElem = document.getElementById('cid' + i);
                        validateFiled(cidElem);

                        if(!cidElem.value.match(cidFormat)){
                          //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
                          $(cidElem).addClass('error-box');
                          //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
                          window.failedFields.push(cidElem);
                          window.is_error = true;
                        }

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

                         // MCID Validation
                        shoppingMCIDElem = document.getElementById('is-mc_id' + i);
                        if(shoppingMCIDElem.checked == true){
                            shoppingMCElem = document.getElementById('mc_id' + i);
                            validateFiled(shoppingMCElem);
                        }

                    }

                }
            }
        }
      }

      // Check Agency fields
    if(document.getElementById('end_customer').checked){
        if(document.getElementById('same_task').checked){
            var sameTagTask = $(".tag:visible").length;
            $("#customer_same_tag_count").val(sameTagTask);

            codeTypeElem = document.getElementById('same_task_cust_type');
            validateFiled(codeTypeElem)

            if(sameTagTask){
                if($("#tag_datepick").val() != ''){
                    var slot = {
                      'type' : 'TAG',
                      'time' : $("#tag_datepick").val()
                    }
                  fix_slots.push(slot);
                  isTagLeads = true;
                }else{
                  tagAppointmentElem = document.getElementById('tag_datepick');
                    if($(tagAppointmentElem).is(":visible")){
                      validateFiled(tagAppointmentElem);
                    }
                }
            }else{
              isTagLeads = false;
            }

            for (i=1; i<=sameTagTask; i++){
                if($("#same_cust_tag_" + i).is(":visible")){

                    // Customer Name Validation
                    cnameElem = document.getElementById('advertiser_name' + i);
                    validateFiled(cnameElem);

                    // Customer Email Validation
                    cemailElem = document.getElementById('aemail' + i);
                    validateFiled(cemailElem);
                    validateEmailField(cemailElem)

                    // Customer Telephone Validation
                    cphoneElem = document.getElementById('phone' + i);
                    validateFiled(cphoneElem);

                    // CID Validation
                    cidElem = document.getElementById('cid' + i);
                    validateFiled(cidElem);

                    if(!cidElem.value.match(cidFormat)){
                      //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
                      $(cidElem).addClass('error-box');
                      //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
                      window.failedFields.push(cidElem);
                      window.is_error = true;
                    }

                    // URL Validation
                    urlElem = document.getElementById('url' + i);
                    validateFiled(urlElem);

                    // Comment Validation
                   /* commentElem = document.getElementById('comment' + i);
                    validateFiled(commentElem);*/

                    validateDynamicFields($('#is_campaign_created'+i))
                    validateDynamicFields($('#product_expectations'+i))
                    validateDynamicFields($('#campaign_implemented'+i))

                    // Analytics 
                    analyticsCodeElem = document.getElementById('analytics_code' + i);
                    if($(analyticsCodeElem).is(":visible")){
                      validateFiled(analyticsCodeElem);  
                    }

                    if($('#rlsa_bulk' + i).is(":visible")){

                          rlsaUserListEle = document.getElementById('user_list_id' + i);
                          validateFiled(rlsaUserListEle);

                          rlsaBidAdjustment = document.getElementById('rsla_bid_adjustment' + i);
                          validateFiled(rlsaBidAdjustment);

                          campaignIds = document.getElementById('campaign_ids' + i);
                          validateFiled(campaignIds);

                          existingBid = document.getElementById('overwrite_existing_bid_modifiers' + i);
                          validateFiled(existingBid);

                          newBid = document.getElementById('create_new_bid_modifiers' + i);
                          validateFiled(newBid);

                          rlsaPolicies = document.getElementById('rsla_policies' + i);
                          if(!$(rlsaPolicies).is(":checked")){
                             $(rlsaPolicies).parent().addClass('error-box');
                              window.failedFields.push(rlsaPolicies);
                              window.is_error = true;
                              return false;
                          }
                      }
                }
            }

              var sameShopTask = $(".shop:visible").length;
              $("#customer_same_shop_count").val(sameShopTask);

              if(sameShopTask){
                if($("#setup_datepick").val() != ''){
                    var slot = {
                      'type' : 'SHOPPING',
                      'time' : $("#setup_datepick").val()
                    }
                  fix_slots.push(slot);
                  isShopLeads = true;
                }else{
                  isShopLeads = false;
                }
              }
                for (i=1; i<=sameShopTask; i++){
                    if($("#same_cust_shop_" + i).is(":visible")){

                        // Customer Name Validation
                        cnameElem = document.getElementById('advertiser_name' + i);
                        validateFiled(cnameElem);

                        // Customer Email Validation
                        cemailElem = document.getElementById('aemail' + i);
                        validateFiled(cemailElem);
                        validateEmailField(cemailElem)

                        // Customer Telephone Validation
                        cphoneElem = document.getElementById('phone' + i);
                        validateFiled(cphoneElem);

                        // CID Validation
                        cidElem = document.getElementById('cid' + i);
                        validateFiled(cidElem);

                        if(!cidElem.value.match(cidFormat)){
                          //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
                          $(cidElem).addClass('error-box');
                          //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
                          window.failedFields.push(cidElem);
                          window.is_error = true;
                        }

                        // URL Validation
                        urlElem = document.getElementById('url' + i);
                        validateFiled(urlElem);

                        validateDynamicFields($('#is_campaign_created'+i))
                        validateDynamicFields($('#product_expectations'+i))
                        validateDynamicFields($('#campaign_implemented'+i))

                        // URL Validation
                        modifierElem = document.getElementById('rbidmodifier' + i);
                        validateFiled(modifierElem);

                        // MCID Validation
                        shoppingMCIDElem = document.getElementById('is-mc_id' + i);
                        if(shoppingMCIDElem.checked == true){
                            shoppingMCElem = document.getElementById('mc_id' + i);
                            validateFiled(shoppingMCElem);
                        }
                        
                    }

            }
        }else if(document.getElementById('diff_task').checked){
            var diffTagTask = $(".tagFields:visible").length;
            $("#customer_diff_tag_count").val($(".tagFields:visible").length);
            var diffShopTask = $(".shopFields:visible").length;
            $("#customer_diff_shop_count").val($(".shopFields:visible").length);
            var totalCustDiffTasks = diffTagTask + diffShopTask;

            if($(".tagFields:visible").length){
                if($("#tag_datepick").val() != ''){
                    var slot = {
                      'type' : 'TAG',
                      'time' : $("#tag_datepick").val()
                    }
                  fix_slots.push(slot);
                  isTagLeads = true; 
                }else{
                  tagAppointmentElem = document.getElementById('tag_datepick');
                    if($(tagAppointmentElem).is(":visible")){
                      validateFiled(tagAppointmentElem);
                    }
                }
            }else{
              isTagLeads = false;
            }

            if(diffShopTask){
                if($("#setup_datepick").val() != ''){
                    var slot = {
                      'type' : 'SHOPPING',
                      'time' : $("#setup_datepick").val()
                    }
                  fix_slots.push(slot);
                  isShopLeads = true;
                }else{
                  isShopLeads = false;
                }
            }
            // CodeType Validation
            ctypeElem = document.getElementById('diff_cust_type-1');
            validateFiled(ctypeElem);

            for (i=1; i<=totalCustDiffTasks; i++){
                // CodeType Validation
                ctypeElem = document.getElementById('diff_cust_type-' + i);
                validateFiled(ctypeElem);

                if($("#tagFields" + i).is(":visible")){

                    // CID Validation
                    cidElem = document.getElementById('cid' + i);
                    validateFiled(cidElem);

                    if(!cidElem.value.match(cidFormat)){
                      //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
                      $(cidElem).addClass('error-box');
                      //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
                      window.failedFields.push(cidElem);
                      window.is_error = true;
                    }

                    // URL Validation
                    urlElem = document.getElementById('url' + i);
                    validateFiled(urlElem);

                    // Comment Validation
                   /* commentElem = document.getElementById('comment' + i);
                    validateFiled(commentElem);*/

                    bidElem = document.getElementById('rbid' + i);
                    if($(bidElem).is(":visible")){
                      validateFiled(bidElem);  
                    }

                    // URL Validation
                    budgetElem = document.getElementById('rbudget' + i);
                    if($(budgetElem).is(":visible")){
                      validateFiled(budgetElem);  
                    }

                    // Analytics 
                    analyticsCodeElem = document.getElementById('analytics_code' + i);
                    if($(analyticsCodeElem).is(":visible")){
                      validateFiled(analyticsCodeElem);  
                    }

                    if($('#rlsa_bulk' + i).is(":visible")){

                          rlsaUserListEle = document.getElementById('user_list_id' + i);
                          validateFiled(rlsaUserListEle);

                          rlsaBidAdjustment = document.getElementById('rsla_bid_adjustment' + i);
                          validateFiled(rlsaBidAdjustment);

                          campaignIds = document.getElementById('campaign_ids' + i);
                          validateFiled(campaignIds);

                          existingBid = document.getElementById('overwrite_existing_bid_modifiers' + i);
                          validateFiled(existingBid);

                          newBid = document.getElementById('create_new_bid_modifiers' + i);
                          validateFiled(newBid);

                          rlsaPolicies = document.getElementById('rsla_policies' + i);
                          if(!$(rlsaPolicies).is(":checked")){
                             $(rlsaPolicies).parent().addClass('error-box');
                              window.failedFields.push(rlsaPolicies);
                              window.is_error = true;
                              return false;
                          }
                      }

                     cnameElem = document.getElementById('advertiser_name' + i);
                      validateFiled(cnameElem);

                      // Customer Email Validation
                      cemailElem = document.getElementById('aemail' + i);
                      validateFiled(cemailElem);
                      validateEmailField(cemailElem)

                      // Customer Telephone Validation
                      cphoneElem = document.getElementById('phone' + i);
                      validateFiled(cphoneElem);
                }else{
                    if($("#shopFields" + i).is(":visible")){

                        // CID Validation
                        cidElem = document.getElementById('cid' + i);
                        validateFiled(cidElem);

                        if(!cidElem.value.match(cidFormat)){
                          //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
                          $(cidElem).addClass('error-box');
                          //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
                          window.failedFields.push(cidElem);
                          window.is_error = true;
                        }

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

                        cnameElem = document.getElementById('advertiser_name' + i);
                        validateFiled(cnameElem);

                        // Customer Email Validation
                        cemailElem = document.getElementById('aemail' + i);
                        validateFiled(cemailElem);
                        validateEmailField(cemailElem)

                        // Customer Telephone Validation
                        cphoneElem = document.getElementById('phone' + i);
                        validateFiled(cphoneElem);

                         // MCID Validation
                        shoppingMCIDElem = document.getElementById('is-mc_id' + i);
                        if(shoppingMCIDElem.checked == true){
                            shoppingMCElem = document.getElementById('mc_id' + i);
                            validateFiled(shoppingMCElem);
                        }
                    }

                }

            }
        }
      }

      // Advertiser Info
      // Advertiser Name Validation
      advertiserNameElem = document.getElementById('contact_person_name');
      validateFiled(advertiserNameElem);

      // Analytics setup check box
      $('.is_ga_setup').each(function(){
        if(!$(this).is(":visible")){
          $(this).val(0);
        }
      });

      // Check If Error in Form
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
          if(!isTagLeads){
            $("#tag_datepick").val('');
          }
          if(!isShopLeads){
            $("#setup_datepick").val('');
          }
          if(window.tz_name){
            console.log(window.tz_name);
            $("#tzone").append("<option value=" + window.tz_name + "></option>").val(window.tz_name)
          }
          $('#preloaderOverlay').show();
          $('form input[type=submit]').attr('disabled', true);
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
      $(elem).focus();
      window.failedFields.push(elem);
      window.is_error = true;
      return false;
    }
}

$(document).on('click', '.is_campaign_created', function() {
    thisId = $(this).attr('id');
    if($(this).is(":checked")){
        $("."+ thisId).hide().val('');
    }else{
      $("."+ thisId).show().val('');
    }
    
});

function resetBtn(elem){
  elemId = $(elem).attr('id');
  if(elemId == 'formReset'){
    window.is_reset = true;
    window.location.reload();
  }
}

$(document).on('click', '.is_mc_id', function() {
  var thisId = $(this).attr('id');
  elem = thisId.split('-')[1];
  if($(this).is(':checked')){
      $("#" + elem).show();
  }else{
      $("#" + elem).hide().val('');
  }
})

$('#region').change(function(){
  var regionId = $('option:selected', this).attr('region_id');
  countryList = regionWiseLocations[regionId];
  console.log(countryList);
  setLocationsForRegion(window.locations, countryList);
});

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

$(document).on('click', '.is_ga_setup', function() {
    if($(this).is(":checked")){
      $(this).val(1);
    }else{
      $(this).val(0);
    }
});

$(document).on('change', '.end-customer-same, .agency-same', function() {
    var codeType = $(this).val();
    if (codeType != ''){
      if(codeType == 'Google Shopping Setup'){
        $(".setup_datepick").show();
        $(".tag_datepick").hide();
      }else{
        $(".tag_datepick").show();
        $(".setup_datepick").hide();
      }
    }
});

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