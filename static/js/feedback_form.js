window.cancel_clicked = false;

    $('.cancel').click(function(event) { 
      window.cancel_clicked = true;
    });

    function validate(frm) {
        $(".error-box").removeClass('error-box');
        if (window.cancel_clicked){
          return false;
        }
        
        if (frm.cid.value == "") {
             $('#feedbackCID').addClass('error-box');
            frm.cid.focus();
            return false;
        }
        
        if (frm.title.value == "") {
             $('#feedbackTitle').addClass('error-box');
            frm.title.focus();
            return false;
        }

        if (frm.location.value == "Location" || frm.location.value == 0) {
             $('#feedbackLocation').addClass('error-box');
            frm.location.focus();
            return false;
        }

        if (frm.description.value == "") {
             $('#description').addClass('error-box');
            frm.description.focus();
            return false;
        }
         if (frm.feedbackType.value == "Feedback Type") {
            $('#feedbackType').addClass('error-box');
            frm.feedbackType.focus();
            return false;
        }

        if (frm.language.value == "Language") {
             $('#feedbackType').addClass('error-box');
            frm.description.focus();
            return false;
        }

        if (frm.program.value == "0") {
             $('#advProgram').addClass('error-box');
            frm.description.focus();
            return false;
        }

    }

    function setSelectValue (id, val) {
        document.getElementById(id).value = val;
    }

    function setLanguages(languages_list){
      $('#advertiserLanguage').html('')
      for(i=0 ;i < languages_list.length; i +=1){
        $('#advertiserLanguage').append('<option value="' + languages_list[i].l_id + '">' + languages_list[i].language_name + '</option>')
      }
    }

    $('input[name=cid]').on('focusout', function(){
        if(!$(this).val()){
            $('input[name=cid], input[name=advertiser], input[id=advertiser], input[name=lead_owner], input[id=lead_owner]').val('')
        }else{
            $.ajax({
                'method': 'GET',
                'dataType': 'json',
                'url': "/leads/get-lead/" + $('input[name=cid]').val(),
                success: function(response){
                    if(response['status'] == 'FAILED'){
                        alert('Lead for Selected CID not available.');
                        $('input[name=cid], input[name=advertiser], input[id=advertiser], input[name=lead_owner], input[id=lead_owner], input[id=lead_owner]' ).val('')
                    }
                    else if(response['status'] == 'MULTIPLE'){
                        alert("Getting multiple leads on this " + $('input[name=cid]').val() + " customer id, please choose advertiser name");
                        multiple_leads(response['details']);
                    }
                    else{
                        $('input[name=lead_owner], input[id=lead_owner]').val(response.details.email);
                        $('input[name=advertiser], input[id=advertiser]').val(response.details.name);
                        $('input[name=code_type], input[id=code_type]').val(response.details.code_type);
                        $('input[name=google_acManager_name], input[id=googleAcManager]').val(response.details.google_rep_email);
                        setSelectValue('advProgram', response.details.team_id);
                        setSelectValue('feedbackLocation', response.details.loc);
                        setSelectValue('googleAcManager', response.details.google_rep_email);
                        setLanguages(response.details.languages_list);
                        
                    }
                },
                error:function(xhr, status, error){
                    alert('Something went wrong!. Please check CID');
                    $('input[name=cid], input[name=advertiser], input[id=advertiser], input[name=lead_owner], input[id=lead_owner]').val('')
                }
            })
        }
    });

function multiple_leads(details){
    $('#feedbackCID').hide();
    $('#advertiserNames').show();
    var html = '<option value>Select Advertiser</option>'
    for(var i=0; i<details.length; i++){
        var obj = details[i];
        var rec = '<option value='+ obj['l_id']+'>'+ obj['name'] +'</option>';
        html += rec
    }
    $('#advertiserNames').append(html);
}

$('#advertiserNames').change(function(){
    var lid = $(this).val();
    if(lid){
        $.ajax({
          url: "/leads/get-lead-by-lid/"+ lid,
          dataType: "json",
          type: 'GET',
          success: function(response) {
             if(response['status'] == 'FAILED'){
                alert('Lead for Selected CID not available.');
                $('input[name=cid], input[name=advertiser], input[id=advertiser], input[name=lead_owner], input[id=lead_owner], input[id=lead_owner], input[name=code_type]').val('')
                }
            else{
                $('input[name=lead_owner], input[id=lead_owner]').val(response.details.email);
                $('input[name=advertiser], input[id=advertiser]').val(response.details.name);
                $('input[name=code_type], input[id=code_type]').val(response.details.code_type);
                $('input[name=google_acManager_name], input[id=googleAcManager]').val(response.details.google_rep_email);
                setSelectValue('advProgram', response.details.team_id);
                setSelectValue('feedbackLocation', response.details.loc);
                setSelectValue('googleAcManager', response.details.google_rep_email);
                setLanguages(response.details.languages_list);

            }
          },
          error: function(errorThrown) {
              alert('Something went wrong!. Please check CID');
                    $('input[name=cid], input[name=advertiser], input[id=advertiser], input[name=lead_owner], input[id=lead_owner]').val('')
          }
    }); 
  }
});