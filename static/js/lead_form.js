function validatethis(frm) {
    $(".error-txt").remove();
    $(".lead-form .form-control").removeClass('error-box');
    var check = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var cidFormat = /^\d{3}-\d{3}-\d{4}$/;
    var phoneFormat = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    var numericExpression = /^[0-9]+$/;
    var ct = 0;
    var rc = 0;
    var fix_slots = new Array();

    
    // Google Rep Name Validation
    if (frm.gref.value == "0" || frm.gref.value == "") {
      //alert("Please Select the Team");
      $(frm.gref).addClass('error-box');
      // $(frm.gref).after('<span class="error-txt">Please Enter Google Rep Name</span>')
      frm.gref.focus();
      return false;
    }

    // Google Rep Email Validation
    if (frm.emailref.value == "0" || frm.emailref.value == "") {
      //alert("Please Select the Team");
      $(frm.emailref).addClass('error-box');
      // $(frm.emailref).after('<span class="error-txt">Please Enter Google Rep Email</span>')
      frm.emailref.focus();
      return false;
    }


    // Programs Validation
    if (frm.team.value == "0" || frm.team.value == "") {
      //alert("Please Select the Team");
      $(frm.team).addClass('error-box');
      // $(frm.team).after('<span class="error-txt">Please Select the Team</span>')
      frm.team.focus();
      return false;
    }

    // Service Segment Validation
    if ($(frm.service_segment).is(":visible")) {
      if(frm.service_segment.value == "0" || frm.service_segment.value == ""){
        //alert("Please Select the Service Segment");
        $(frm.service_segment).addClass('error-box');
        // $(frm.service_segment).after('<span class="error-txt">Please Select the Service Segment</span>')
        frm.service_segment.focus();
        return false;
      }
    }

    // Google Manager details validation
    if (document.getElementById("manager_name").value == "") {
      //alert("Please Update Google Manager details");
      elem = document.getElementById("manager_name");
      $(elem).addClass('error-box');
      // $(elem).after('<span class="error-txt">Please Update Google Manager details</span>')
      $(elem).focus();
      return false;
    }
    if (document.getElementById("manager_email").value == "") {
      //alert("Please Update Google Manager details");
      elem = document.getElementById("manager_email");
      $(elem).addClass('error-box');
      //$(elem).after('<span class="error-txt">Please Update Google Manager details</span>')
      $(elem).focus();
      //document.getElementById("addPm").focus();
      return false;
    }

    // Location/Country Validation
    if (frm.country.value == "0" || frm.country.value == "") {
      // alert("Please Select Your Country");
      $(frm.country).addClass('error-box');
      //$(frm.country).after('<span class="error-txt">Please Select Your Country</span>')
      frm.country.focus();
      return false;
    }

    // Advertiser Info
    // Advertiser Name Validation
    if (frm.advertiser_name.value == "") {
      // alert("Please Enter First Name");
      $(frm.advertiser_name).addClass('error-box');
      //$(frm.advertiser_name).after('<span class="error-txt">Please Enter Advertiser Name</span>')
      frm.advertiser_name.focus();
      return false;
    }

    // Advertiser Email Validation
    if (frm.aemail.value == "") {
      // alert("Please Enter Email Address");
      $(frm.aemail).addClass('error-box');
      //$(frm.aemail).after('<span class="error-txt">Please Enter Email Address</span>')
      frm.aemail.focus();
      return false;
    }

    frm.aemail.value = frm.aemail.value.trim();
    if (!frm.aemail.value.trim().match(check)) {
      // alert("Invalid E-mail ID !");
      $(frm.aemail).addClass('error-box');
      //$(frm.aemail).after('<span class="error-txt">Invalid E-mail ID !</span>')
      frm.aemail.focus();
      return false;
    }

    // Advertiser Phone Validation
    if (frm.phone.value == "") {
      //alert("Please Enter Phone Number");
      $(frm.phone).addClass('error-box');
      //$(frm.phone).after('<span class="error-txt">Please Enter Phone Number</span>');
      frm.phone.focus();
      return false;
    }
    
    // Advertiser Company Validation
    if (frm.company.value == "") {
      //alert("Please Enter Company Name");
      $(frm.company).addClass('error-box');
      //$(frm.company).after('<span class="error-txt">Please Enter Company Name</span>')
      frm.company.focus();
      return false;
    }

    // Customer Id validation
    if (frm.cid.value == "") {
      //alert("Please Enter Customer ID");
      $(frm.cid).addClass('error-box');
      //$(frm.cid).after('<span class="error-txt">Please Enter Customer ID</span>')
      frm.cid.focus();
      return false;
    }else if(!frm.cid.value.match(cidFormat)){
      //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
      $(frm.cid).addClass('error-box');
      //$(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
      frm.cid.focus();
      return false;
    }

    // Advertiser Location validation
    if (frm.advertiser_location.value == "") {
      //alert("Please Enter Customer ID");
      $(frm.advertiser_location).addClass('error-box');
      //$(frm.advertiser_location).after('<span class="error-txt">Please Enter Advertiser location</span>')
      frm.advertiser_location.focus();
      return false;
    }
    
    // Language validation
    if (frm.language.value == "") {
      //alert("Please Enter Customer ID");
      $(frm.language).addClass('error-box');
      //$(frm.language).after('<span class="error-txt">Please Choose Language</span>')
      frm.language.focus();
      return false;
    }

    // Timezone Validation
    if (frm.tzone.value == 0 || frm.tzone.value == "") {
      // alert("Please Select Advertiser Time Zone.");
      $(frm.tzone).addClass('error-box');
      //$(frm.tzone).after('<span class="error-txt">Please Select Advertiser Time Zone.</span>')
      frm.tzone.focus();
      return false;
    }

    // Hava an appointment 
    if (document.getElementById("appointmentCheck").checked == false) {

      // Contact Person Name Validation 
      if (frm.contact_person_name.value == "") {
        // alert("Please Select Advertiser Time Zone.");
        $(frm.contact_person_name).addClass('error-box');
        //$(frm.contact_person_name).after('<span class="error-txt">Please Enter Contact Person Name.</span>')
        frm.contact_person_name.focus();
        return false;
      }

      // Contact Person Role Validation 
      if (frm.primary_role.value == "") {
        // alert("Please Select Advertiser Time Zone.");
        $(frm.primary_role).addClass('error-box');
        //$(frm.contact_person_role).after('<span class="error-txt">Please Enter Contact Person Role.</span>')
        frm.primary_role.focus();
        return false;
      }

      // Appointments Date and Time Validation
      if (frm.tag_datepick.value == "") {
        //alert("'Date and Time' is Mandatory for Appointments, else select 'Not Applicable' check box to continue.");
        $(frm.tag_datepick).addClass('error-box');
        //$(frm.tag_datepick).after('<span class="error-txt">Date and Time is Mandatory for Appointments, else select Don’t have an appointment check box to continue.</span>')
        frm.tag_datepick.focus();
        return false;
      }
    }

    // Webmaster Validation
    if(document.getElementById("webmasterCheck").checked == true){

      // Contact Person Name
      if (frm.fopt.value == "") {
        $(frm.fopt).addClass('error-box');
        //$(frm.fopt).after('<span class="error-txt">Please Enter Contact Person Name.</span>')
        frm.fopt.focus();
        return false;
      }

      // Contact Person Role
      if (frm.web_master_email.value == "") {
        // var elem = document.getElementById("00Nd0000005WayW");
        $(frm.web_master_email).addClass('error-box');
        //$(elem).after('<span class="error-txt">Please Enter Contact Person Role.</span>')
        $(frm.web_master_email).focus();
        return false;
        }

      // Contact Person Name
      if (frm.popt.value == "") {
        $(frm.popt).addClass('error-box');
        //$(frm.popt).after('<span class="error-txt">Please Enter Phone Number.</span>')
        frm.popt.focus();
        return false;
      }
    }

    

    // Tag Implementation lead form related Validation
    // validate Tag Implementation fields
    if($("#tagImplementationBtn").is(":visible")){

      var slot = {
        'type' : 'TAG',
        'time' : frm.tag_datepick.value
      }
      fix_slots.push(slot)

      
      if($("#task_1").is(":visible")){
        ctypeElem = frm.ctype1;
        if(!validateCtype(ctypeElem)){
          return false;
        }

        codeElem = frm.code1;
        if(!validateCode(codeElem)){
          return false;
        }

        urlElem = frm.url1;
        if(!validateUrl(urlElem)){
          return false;
        }
      }
      
      if($("#task_2").is(":visible")){
        ctypeElem2 = frm.ctype2;
        if(!validateCtype(ctypeElem2)){
          return false;
        }

        codeElem2 = frm.code2;
        if(!validateCode(codeElem2)){
          return false;
        }

        urlElem2 = frm.url2;
        if(!validateUrl(urlElem2)){
          return false;
        }
      }

      if($("#task_3").is(":visible")){
        ctypeElem3 = frm.ctype3;
        if(!validateCtype(ctypeElem3)){
          return false;
        }

        codeElem3 = frm.code3;
        if(!validateCode(codeElem3)){
          return false;
        }

        urlElem3 = frm.url3;
        if(!validateUrl(urlElem3)){
          return false;
        }
      }

      if($("#task_4").is(":visible")){
        ctypeElem4 = frm.ctype4;
        if(!validateCtype(ctypeElem4)){
          return false;
        }

        codeElem4 = frm.code4;
        if(!validateCode(codeElem4)){
          return false;
        }

        urlElem4 = frm.url4;
        if(!validateUrl(urlElem4)){
          return false;
        }
      }

      if($("#task_5").is(":visible")){
        ctypeElem5 = frm.ctype5;
        if(!validateCtype(ctypeElem5)){
          return false;
        }

        codeElem5 = frm.code5;
        if(!validateCode(codeElem5)){
          return false;
        }

        urlElem5 = frm.url5;
        if(!validateUrl(urlElem5)){
          return false;
        } 
      }
    }else{
      frm.tag_datepick.value = '';
    }
    
    // Check If Shopping related lead fields
    if ($('#shoppingSetupBtn').is(':visible')) {
      
      if (frm.rbid.value == "") {
        // alert("Please Enter Recommended Bid Value");
        $(frm.rbid).addClass('error-box');
        //$(frm.rbid).after('<span class="error-txt">Please Enter Recommended Bid Value</span>')
        frm.rbid.focus();
        return false;
      }
      if (frm.rbidmodifier.value == "") {
        // alert("Please Enter Recommended Mobile Bid Modifier Value");
        $(frm.rbidmodifier).addClass('error-box');
        //$(frm.rbidmodifier).after('<span class="error-txt">Please Enter Recommended Mobile Bid Modifier Value</span>')
        frm.rbidmodifier.focus();
        return false;
      }

      if (frm.rbudget.value == "") {
        // alert("Please Enter Recommended Budget Value");
        $(frm.rbudget).addClass('error-box');
        //$(frm.rbudget).after('<span class="error-txt">Please Enter Recommended Budget Value</span>')
        frm.rbudget.focus();
        return false;
      }

      if (frm.shopping_url.value == "") {
        // alert("Please Enter Recommended Budget Value");
        $(frm.shopping_url).addClass('error-box');
        //$(frm.rbudget).after('<span class="error-txt">Please Enter Recommended Budget Value</span>')
        frm.shopping_url.focus();
        return false;
      }

      if (frm.setup_datepick.value == "") {
          //alert("'Date and Time' is Mandatory for Appointments, else select 'Not Applicable' check box to continue.");
          $(frm.setup_datepick).addClass('error-box');
          //$(frm.setup_datepick).after('<span class="error-txt">Date and Time is Mandatory for Appointments, else select Not Applicable check box to continue.</span>')
          frm.setup_datepick.focus();
          return false;
        }

      var slot = {
          'type' : 'SHOPPING',
          'time' : frm.setup_datepick.value
        }
      fix_slots.push(slot)
      }else{
        frm.setup_datepick.value = "";
      }

    var status = true;
    if (fix_slots.length) {
      status = check_and_create_appointment(fix_slots);
    }
    
    if (status) {
      $('form input[type=submit]').attr('disabled', 'disabled');
    }
    return status;
  }


  function validateCtype(ctypeElem){
    // Code Type Validation
    if (ctypeElem.value == "" || ctypeElem.value == "") {
      // alert("Please Select Code Type");
      $(ctypeElem).addClass('error-box');
      //$(ctypeElem).after('<span class="error-txt">Please Select Code Type</span>')
      ctypeElem.focus();
      return false;
    }else{
      return true;
    }
  }

  function validateCode(codeElem){
    // Code Type Validation
    if (codeElem.value == "0" || codeElem.value == "") {
      // alert("Please Select Code Type");
      $(codeElem).addClass('error-box');
      //$(codeElem).after('<span class="error-txt">Please Select Code </span>')
      codeElem.focus();
      return false;
    }else{
      return true;
    }
  }


  function validateUrl(urlElem){
    // Code Type Validation
    if (urlElem.value == "0" || urlElem.value == "") {
      // alert("Please Select Code Type");
      $(urlElem).addClass('error-box');
      //$(urlElem).after('<span class="error-txt">Please Select URL</span>')
      urlElem.focus();
      return false;
    }else{
      return true;
    }
  }
    
function resetBtn(elem){
  elemId = $(elem).attr('id');
  if(elemId == 'formReset'){
    window.location.reload();
  }
}