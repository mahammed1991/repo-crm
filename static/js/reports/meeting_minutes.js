function validatethis() {
    $(".error-txt").remove();
    $(".lead-form .form-control").removeClass('error-box');
    // var check = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var numericExpression = /^[0-9]+$/;
    window.is_error = false;
    window.failedFields = new Array();

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

    locationElem = document.getElementById('country');
    validateFiled(locationElem);

    programElem = document.getElementById('program');
    validateFiled(programElem);

    attendeesElem = document.getElementById('attendees');
    validateFiled(attendeesElem);

    if(document.getElementById('internal_meeting').checked == false && document.getElementById('external_meeting').checked == false){
      $('.meeting_audience').addClass('error-box');
      window.is_error = true;
    }else{
      $('.meeting_audience').removeClass('error-box');
      window.is_error = false;
    }

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

    var show_time_date = $('.next-row').is(":checked");
    if(show_time_date)
    {
       nextDateElem = document.getElementById('next_meeting_date');
    validateFiled(nextDateElem);

    nextTimeElem = document.getElementById('next_meeting_time');
    validateFiled(nextTimeElem);
    }


    // Check If Error in Form
    if(window.is_error){
      focusElem = failedFields[0];
      $(focusElem).focus();
      return false;
    }else{
      $(".modal").modal('show');
      return true;
    }  
  }

  function validateFiled(elem){
  // Validate Form Field
  if ($(elem).val() == "" || $(elem).val() == "0" || !$(elem).val()) {
  $(elem).addClass('error-box');
  window.failedFields.push(elem);
  window.is_error = true;
  return false;
  }else{
    $(elem).removeClass('error-box');
  }
}

function setLocationsForRegion(newLocations, countryIds){
    $("#country option").remove()
    $("#country").append('<option value="0">Location</option>');
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

$('#preview_btn').click(function(){
  
    $('#preview_selected_program').text($('#selected_program').text());
    $('#preview_selected_project').text($('#selected_project').text());
    $('#preview_selected_subject').text($('#selected_subject').text());
    $('#preview_selected_product_name').text($('#selected_product_name').text());
    $('#preview_selected_date').text($('#selected_date').text());

    if($('#internal_meeting').prop("checked")){
      $('#preview_internal_meeting').prop('checked', true);
    }else{
      $('#preview_internal_meeting').prop('checked', false);
    }

    if($('#external_meeting').prop("checked")){
      $('#preview_external_meeting').prop('checked', true);
    }else{
      $('#preview_external_meeting').prop('checked', false);
    }

    $('#preview_subject').val($('#subject').val());
    $('#preview_subject').prop('disabled', true);

    var subject_val = $("#preview_subject").val();
    if(subject_val == "Others" || subject_val == "New Program Launch" || subject_val == "New Product Launch")
    {
      $("#preview_others").show();
      $('#preview_others').val($('#others').val());
    }
    else
    {
      $("#preview_others").hide();
    }

    $('#preview_meeting_date').val($('#meeting_date').val());

    $('#preview_meeting_time').val($('#meeting_time').val());

    $('#preview_google_poc').val($('#google_poc').val());

    $('#preview_regalix_poc').val($('#regalix_poc').val());

    $('#preview_google_team').val($('#google_team').val());

    $('#preview_region').val($('#region').val());

    $('#preview_country').val($('#country').val());

    $('#preview_program').val($('#program').val());

    var program_val = $('#preview_program').val();

    if(program_val == 'TAG Team'){
      $('.preview_program_type').show();
      $('#preview_program_type').val($('#program_type').val());
    }

    $('#preview_attendees').val($('#attendees').val());

    $('#preview_bcc').val($('#bcc').val());


    /***************************adding action plans*********************************/
    $('.preview-add-task').html('');
    var preview_add_task = $('.key-points');
    var add_tasks = new Array();

    for(var i=1;i<=preview_add_task.length;i++)
    {
        add_tasks.push($('#no_'+i).val());
        add_tasks.push($('#topic_'+i).val());
        add_tasks.push($('#highlight_'+i).val());
    }
    var actual_length = add_tasks.length;
     for(var j=1;j<=((actual_length/3));j++)
    {
      $('.preview-add-task').append('<tr id="preview_key_point_'+j+'" class="preview-key-points"></tr>');
      $('#preview_key_point_'+j).append('<td id="preview_no_'+j+'">'+add_tasks[0]+'</td>');
      $('#preview_key_point_'+j).append('<td id="preview_topic_'+j+'">'+add_tasks[1]+'</td>');
      $('#preview_key_point_'+j).append('<td id="preview_highlight_'+j+'">'+add_tasks[2]+'</td>');
      add_tasks = add_tasks.splice(3);
    }

    /***************************adding action plans*********************************/
    $('.preview-action-plan').html('');
    var preview_add_task = $('.action-plans');
    var add_action_points = new Array();

    for(var i=1;i<=preview_add_task.length;i++)
    {
        add_action_points.push($('#ano_'+i).val());
        add_action_points.push($('#action_item_'+i).val());
        add_action_points.push($('#owner_'+i).val());
        add_action_points.push($('#action_date_'+i).val());
    }
    var actual_action_length = add_action_points.length;
     for(var j=1;j<=((actual_action_length/4));j++)
    {
      $('.preview-action-plan').append('<tr id="preview_action_point'+j+'" class="preview-action-points"></tr>');
      $('#preview_action_point'+j).append('<td id="preview_ano_'+j+'">'+add_action_points[0]+'</td>');
      $('#preview_action_point'+j).append('<td id="action_item_'+j+'">'+add_action_points[1]+'</td>');
      $('#preview_action_point'+j).append('<td id="owner_'+j+'">'+add_action_points[2]+'</td>');
      $('#preview_action_point'+j).append('<td id="action_date_'+j+'">'+add_action_points[3]+'</td>');
      add_action_points = add_action_points.splice(4);
    }
    
    /***************************adding tenantive agenda*********************************/
    $('.preview-extra').html('');
    var preview_agenda = $('.tenantive_agendas');
    var tentative_agenda = new Array();

    for(var i=1;i<=preview_agenda.length;i++)
    {
        tentative_agenda.push($('#agenda_text_'+i).val());
    }
    var actual_agenda_length = tentative_agenda.length;

    for(var j=1;j<=(actual_agenda_length);j++)
    {
      $('.preview-extra').append('<tr id="preview_tentative_agenda'+j+'" class="preview-action-points"></tr>');
      $('#preview_tentative_agenda'+j).append('<td id="preview_agenda">Tenanative Agenda :</td>');
      $('#preview_tentative_agenda'+j).append('<td id="preview_agenda_text_'+j+'" class="preview-agenda-item">'+tentative_agenda[0]+'</td>');
      tentative_agenda = tentative_agenda.splice(1);
    }



    $('#preview_next_meeting_date').val($('#next_meeting_date').val());

    $('#preview_next_meeting_time').val($('#next_meeting_time').val());

    $('.attach-link-file').html('');
    var preview_attachments = $('.file-append');
    var attachments = new Array();

    for(var i=1; i<= preview_attachments.length; i++){
      attachments.push($('#file_info_text_'+i).val());
    }

    var attachments_length = preview_attachments.length;

    for(var j=1; j<=(attachments_length);j++){
      $('.attach-link-file').append('<tr id="attachment_link'+j+'" class="attachment-link-file"></tr>');
      $('#attachment_link'+j).append('<td id="preview_file_info_text_'+j+'" class="preview-attach">'+attachments[0]+'</td>');
      attachments = attachments.splice(1);
    }

    $('#preview_internal_meeting').prop('disabled', true);
    $('#preview_external_meeting').prop('disabled', true);
});

$('#subject').change(function(){
  $('.new_link').hide();
  $('#nodatafound').hide();
  $('#generate_link').show();
});

$('#program').change(function(){
  $('.new_link').hide();
  $('#nodatafound').hide();
  $('#generate_link').show();
});

$('#generate_link').click(function(event){
  event.preventDefault();
  window.has_error = false;
  var dataString = {}
  if($('#program').val() == '' || $('#program').val() == '0'){
    alert('Please select progarm');
    window.has_error = true;
  }else{
    dataString['program'] = $('#program').val();
    if($('#program').val() == 'TAG Team'){
      dataString['program_type'] = $('#program_type').val();
    }
  }
  if($('#subject').val() == '' || $('#subject').val() == '0'){
    alert('Please select subject timeline');
    window.has_error = true;
  }else{
    dataString['subject'] = $('#subject').val();
  }

  if(window.has_error){
        return false;
      }else{
        var status = true;
        if (status) {
          $.ajax({
            url: '/reports/generate-link',
            type: 'GET',
            data: dataString,
            dataType: 'JSON',
            success: function(data){
              generate_link(data);
            },
            failure: function(jqXHR, textStatus, errorThrown){
              $('#generate_link').show();
              alert('No data!');
            }

          });
        }
        return status;
      }
});

function generate_link(data){
  $('#generate_link').hide();
  if(data == "No Data"){
    $('#nodatafound').show();
  }else{
    $('#prev_meeting_link').append('<a class="new_link" target="_blank" href='+data+' style="margin-left: 20%;">Click Again to access link</a>');
  }
}


/*  ----------------------------------------------
    start file upload and multiple append
  ----------------------------------------------*/
  $('.remove-upload').hide();

  $('.add-upload-btn').click(function () {
      id = $(this).attr('id');
      indx = id.split('_')[1];
      next_id = parseInt(indx) + 1
      if(next_id < 6 )
      {
          $(".remove-upload").show();
          $new_row = $("#file_upload_row_1").clone().attr('id', 'file_upload_row_'+next_id).show();
          $(".file-info-text", $new_row).attr('id', 'file_info_text_'+next_id);
          $(".file-info", $new_row).attr('id', 'file_info_'+next_id);
          $(".file-info-text", $new_row).attr('name', 'file_info_text_'+next_id);
          $(".file-info", $new_row).attr('name', 'file_info_'+next_id);
          $new_row.appendTo(".browse-files");
          $('.remove-upload').attr('id',"removefileUpload_" + next_id);
          $('.add-upload-btn').attr('id',"addfileUpload_" + next_id);
          $("#file_info_text_"+next_id).val('');
        }
        if(next_id == 5 )
        {
          $(".add-upload-btn").hide();
        }
  });

  $('.remove-upload').click(function () {
    id = $(this).attr('id');
    indx = id.split('_')[1];
    if(("#removefileUpload_"+indx) != "#removefileUpload_1" )
    {
        $(".add-upload-btn").show();
        $("#file_upload_row_"+indx).remove();
        $('.remove-upload').attr('id',"#removefileUpload_" + (indx-1));
        $('.add-upload-btn').attr('id',"#addfileUpload_" + (indx-1));
    }
    if(("#removefileUpload_"+(indx-1)) == "#removefileUpload_1" )
    {
      $('.remove-upload').hide();
    }
  });

/*
  --------------------------------------------------
  end
  -------------------------------------------------*/

$('#internal_meeting').click(function(){
  if($('#internal_meeting').prop("checked")){
    var not_available = 'NA';
    $('#google_poc').val(not_available);
    $('#google_team').val(not_available);
    $('#region').val('APAC');
    $('#country').val('India');
  }else{
    $('#google_poc').val('');
    $('#google_team').val('');
    $('#region option').eq(0).prop('selected', true);
    $('#country option').eq(0).prop('selected', true);
    $('#region').prop('disabled', false);
    $('#country').prop('disabled', false);
  }

});

$('#external_meeting').click(function(){
  $('#region').prop('disabled', false);
  $('#country').prop('disabled', false);
  $('#google_poc').val('');
  $('#google_team').val('');
  $('#region option').eq(0).prop('selected', true);
  $('#country option').eq(0).prop('selected', true);
});