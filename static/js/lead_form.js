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

    // Programs Validation
    if (frm.team.value == "0" || frm.team.value == "") {
      //alert("Please Select the Team");
      frm.team.addClass('error-box');
      frm.team.after('<span class="error-txt">Please Select the Team</span>')
      frm.team.focus();
      return false;
    }

    // Service Segment Validation
    if ($("#"+frm.service_segment.id).is(":visible")) {
      if(frm.service_segment.value == "0" || frm.service_segment.value == ""){
        //alert("Please Select the Service Segment");
        $(frm.service_segment).addClass('error-box');
        $(frm.service_segment).after('<span class="error-txt">Please Select the Service Segment</span>')
        frm.service_segment.focus();
        return false;
      }
    }

    // Google Manager details validation
    if (document.getElementById("00Nd00000075Crj").value == "") {
      //alert("Please Update Google Manager details");
      elem = document.getElementById("00Nd00000075Crj");
      $(elem).addClass('error-box');
      $(elem).after('<span class="error-txt">Please Update Google Manager details</span>')
      $(elem).focus();
      return false;
    }
    if (document.getElementById("00Nd00000077r3s").value == "") {
      //alert("Please Update Google Manager details");
      elem = document.getElementById("00Nd00000077r3s");
      $(elem).addClass('error-box');
      $(elem).after('<span class="error-txt">Please Update Google Manager details</span>')
      $(elem).focus();
      //document.getElementById("addPm").focus();
      return false;
    }

    // Location/Country Validation
    if (frm.country.value == "0") {
      // alert("Please Select Your Country");
      $(frm.country).addClass('error-box');
      $(frm.country).after('<span class="error-txt">Please Select Your Country</span>')
      frm.country.focus();
      return false;
    }

    // Advertiser Info
    // Advertiser Name Validation
    if (frm.advertiser_name.value == "") {
      // alert("Please Enter First Name");
      $(frm.advertiser_name).addClass('error-box');
      $(frm.advertiser_name).after('<span class="error-txt">Please Enter Advertizer Name</span>')
      frm.advertiser_name.focus();
      return false;
    }

    // Advertiser Email Validation
    if (frm.aemail.value == "") {
      // alert("Please Enter Email Address");
      $(frm.aemail).addClass('error-box');
      $(frm.aemail).after('<span class="error-txt">Please Enter Email Address</span>')
      frm.aemail.focus();
      return false;
    }
    frm.aemail.value = frm.aemail.value.trim();
    if (!frm.aemail.value.trim().match(check)) {
      // alert("Invalid E-mail ID !");
      $(frm.aemail).addClass('error-box');
      $(frm.aemail).after('<span class="error-txt">Invalid E-mail ID !</span>')
      frm.aemail.focus();
      return false;
    }

    // Advertiser Phone Validation
    if (frm.phone.value == "") {
      //alert("Please Enter Phone Number");
      $(frm.phone).addClass('error-box');
      $(frm.phone).after('<span class="error-txt">Please Enter Phone Number</span>');
      frm.phone.focus();
      return false;
    }
    
    // Advertiser Company Validation
    if (frm.company.value == "") {
      //alert("Please Enter Company Name");
      $(frm.company).addClass('error-box');
      $(frm.company).after('<span class="error-txt">Please Enter Company Name</span>')
      frm.company.focus();
      return false;
    }

    // Customer Id validation
    if (frm.cid.value == "") {
      //alert("Please Enter Customer ID");
      $(frm.cid).addClass('error-box');
      $(frm.cid).after('<span class="error-txt">Please Enter Customer ID</span>')
      frm.cid.focus();
      return false;
    }else if(!frm.cid.value.match(cidFormat)){
      //alert("Please enter a valid Customer ID (nnn-nnn-nnnn)");
      $(frm.cid).addClass('error-box');
      $(frm.cid).after('<span class="error-txt">Please enter a valid Customer ID (nnn-nnn-nnnn)</span>')
      frm.cid.focus();
      return false;
    }

    // Advertiser Location validation
    if (frm.advertiser_location.value == "") {
      //alert("Please Enter Customer ID");
      $(frm.advertiser_location).addClass('error-box');
      $(frm.advertiser_location).after('<span class="error-txt">Please Enter Advertiser location</span>')
      frm.advertiser_location.focus();
      return false;
    }
    
    // Language validation
    if (frm.language.value == "") {
      //alert("Please Enter Customer ID");
      $(frm.language).addClass('error-box');
      $(frm.language).after('<span class="error-txt">Please Choose Language</span>')
      frm.language.focus();
      return false;
    }

    // Timezone Validation
    if (frm.tzone.value == 0 || frm.tzone.value == "") {
      // alert("Please Select Advertiser Time Zone.");
      $(frm.tzone).addClass('error-box');
      $(frm.tzone).after('<span class="error-txt">Please Select Advertiser Time Zone.</span>')
      frm.tzone.focus();
      return false;
    }

    // Hava an appointment 
    if (document.getElementById("appointmentCheck").checked == false) {

      // Contact Person Name Validation 
      if (frm.contact_person_name.value == "") {
        // alert("Please Select Advertiser Time Zone.");
        $(frm.contact_person_name).addClass('error-box');
        $(frm.contact_person_name).after('<span class="error-txt">Please Enter Contact Person Name.</span>')
        frm.contact_person_name.focus();
        return false;
      }

      // Contact Person Role Validation 
      if (frm.contact_person_role.value == "") {
        // alert("Please Select Advertiser Time Zone.");
        $(frm.contact_person_role).addClass('error-box');
        $(frm.contact_person_role).after('<span class="error-txt">Please Enter Contact Person Role.</span>')
        frm.contact_person_role.focus();
        return false;
      }

      // Appointments Date and Time Validation
      if (frm.tag_datepick.value == "") {
        //alert("'Date and Time' is Mandatory for Appointments, else select 'Not Applicable' check box to continue.");
        $(frm.tag_datepick).addClass('error-box');
        $(frm.tag_datepick).after('<span class="error-txt">Date and Time is Mandatory for Appointments, else select Don’t have an appointment check box to continue.</span>')
        frm.tag_datepick.focus();
        return false;
      }
      var slot = {
        'type' : 'TAG',
        'time' : frm.tag_datepick.value
      }
      fix_slots.push(slot)
    } else {
      frm.tag_datepick.value = "";
    }


    // Webmaster Validation
    if(document.getElementById("webmasterCheck").checked == false){

      // Contact Person Name
      if (frm.fopt.value == "") {
        $(frm.fopt).addClass('error-box');
        $(frm.fopt).after('<span class="error-txt">Please Enter Contact Person Name.</span>')
        frm.fopt.focus();
        return false;
      }

      // Contact Person Role
      if (document.getElementById("00Nd0000005WayW").value == "") {
        var elem = document.getElementById("00Nd0000005WayW");
        $(elem).addClass('error-box');
        $(elem).after('<span class="error-txt">Please Enter Contact Person Role.</span>')
        $(elem).focus();
        return false;
        }

    // Contact Person Name
      if (frm.popt.value == "") {
        $(frm.popt).addClass('error-box');
        $(frm.popt).after('<span class="error-txt">Please Enter Phone Number.</span>')
        frm.popt.focus();
        return false;
      }
    }

    // Tag Implementation lead form related Validation
    // validate Tag Implementation fields
    if($("#tagImplementationBtn").is(":visible")){

      // Code Type Validation
      if (frm.ctype1.value == "") {
        // alert("Please Select Code Type");
        $(frm.ctype1).addClass('error-box');
        $(frm.ctype1).after('<span class="error-txt">Please Select Code Type</span>')
        frm.ctype1.focus();
        return false;
      }

      // Code Validation
      if (frm.code1.value == "") {
        //alert("Please Enter Code");
        $(frm.code1).addClass('error-box');
        $(frm.code1).after('<span class="error-txt">Please Enter Code</span>')
        frm.code1.focus();
        return false;
      }

      // URL Validation
      var domain = document.getElementById('url1');
      if (domain.value == "") {
        // alert("Please enter a URL");
        $(domain).addClass('error-box');
        $(domain).after('<span class="error-txt">Please enter a URL</span>')
        domain.focus();
        return false;
      }

    }
    
    // Check If Shopping related lead fields
    if ($('#shoppingSetupBtn').is(':visible')) {

      if (frm.rbid.value == "") {
        // alert("Please Enter Recommended Bid Value");
        $(frm.rbid).addClass('error-box');
        $(frm.rbid).after('<span class="error-txt">Please Enter Recommended Bid Value</span>')
        frm.rbid.focus();
        return false;
      }
      if (frm.rbidmodifier.value == "") {
        // alert("Please Enter Recommended Mobile Bid Modifier Value");
        $(frm.rbidmodifier).addClass('error-box');
        $(frm.rbidmodifier).after('<span class="error-txt">Please Enter Recommended Mobile Bid Modifier Value</span>')
        frm.rbidmodifier.focus();
        return false;
      }
      if (frm.rbudget.value == "") {
        // alert("Please Enter Recommended Budget Value");
        $(frm.rbudget).addClass('error-box');
        $(frm.rbudget).after('<span class="error-txt">Please Enter Recommended Budget Value</span>')
        frm.rbudget.focus();
        return false;
      }
      if (document.getElementById("setup_datepick_nApplicable").checked == false) {
        if (frm.setup_datepick.value == "") {
          //alert("'Date and Time' is Mandatory for Appointments, else select 'Not Applicable' check box to continue.");
          $(frm.setup_datepick).addClass('error-box');
          $(frm.setup_datepick).after('<span class="error-txt">Date and Time is Mandatory for Appointments, else select Not Applicable check box to continue.</span>')
          frm.setup_datepick.focus();
          return false;
        }
        var slot = {
          'type' : 'SHOPPING',
          'time' : frm.setup_datepick.value
        }
        fix_slots.push(slot)
      } else {
        frm.setup_datepick.value = "";
      }
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