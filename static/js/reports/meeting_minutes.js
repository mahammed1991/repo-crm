function validatethis(frm) {
    $(".error-txt").remove();
    $(".lead-form .form-control").removeClass('error-box');
    // var check = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var numericExpression = /^[0-9]+$/;
    window.failedFields = new Array();
    window.is_error = false;

    if(window.is_reset == true){
      window.is_reset = false;
      return false;
    }

    // Subject Name Validation
    subjectElem = document.getElementById('subject');
    validateFiled(subjectElem);

    meetingDateElem = document.getElementById('meeting_date');
    validateFiled(meetingDateElem);
  
    meetingTimeElem = document.getElementById('meeting_time');
    validateFiled(meetingTimeElem);

    googlePocElem = document.getElementById('google_poc');
    validateFiled(googlePocElem);

    regalixPocElem = document.getElementById('regalix_poc');
    validateFiled(regalixPocElem);

    googleTeam = document.getElementById('google_team');
    validateFiled(googleTeam);

    regionElem = document.getElementById('region');
    validateFiled(regionElem);

    attendeesElem = document.getElementById('attendees');
    validateFiled(attendeesElem);

    for( i=1; i <= $(".key-points").length; i++){
      if($("#key_point_" + i).is(":visible")){
        topicElem = document.getElementById("topic_" + i);
        validateFiled(topicElem);
        highlightElem = document.getElementById('highlight_'+i);
        validateFiled(highlightElem);
      }
    }

    for( i=1; i <= $(".action-plans").length; i++){
      if($("#action_plan_" + i).is(":visible")){
        actionItemElem = document.getElementById("action_item_" + i);
        validateFiled(actionItemElem);
        ownerElem = document.getElementById('owner_'+i);
        validateFiled(ownerElem);
        dateElem = document.getElementById('action_date_'+i);
        validateFiled(dateElem);
      }
    }

    nextDateElem = document.getElementById('next_meeting_date');
    validateFiled(nextDateElem);

    nextTimeElem = document.getElementById('next_meeting_time');
    validateFiled(nextTimeElem);

    // Check If Error in Form
    if(window.is_error){
      focusElem = failedFields[0];
      $(focusElem).focus();
      return false;
    }else{
      return true;
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
