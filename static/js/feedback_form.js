window.cancel_clicked = false;

    $('.cancel').click(function(event) { 
      window.cancel_clicked = true;
    });

    function validate(frm) {
        var res = validateFields(frm)
        if(!res){
           $("#preloaderOverlay").hide();
        }
        return res;  
    }

    function validateFields(frm){
        window.is_error = false;
        $(".error-box").removeClass('error-box');
        if (window.cancel_clicked){
          return false;
        }
        validateField(frm.cid);
        validateField(frm.title);
        validateField(frm.location);
        validateField(frm.location);
        validateField(frm.description);
        validateField(frm.feedbackType);
        validateField(frm.language);
        validateField(frm.program);
        validateField(frm.description);
        
        if(window.is_error){
            return false;
        }else{
            return true;    
        }
        
    }

    function validateField(elem){
        // Validate Form Field
        if ($(elem).val() == "" || $(elem).val() == "0" || !$(elem).val()) {
          $(elem).addClass('error-box');
          $(elem).focus();
          window.is_error = true;
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
                'url': "/leads/get-lead/" + $('input[name=cid]').val() +'/'+ $('input[name=feedback_type]').val(),
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
                        $("#advertiserNames").append("<option value=" + response.details.l_id + ">"+ response.details.l_id +"</option>")
                        
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
          url: "/leads/get-lead-by-lid/"+ lid + '/' + $('input[name=feedback_type]').val(),
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
                $("#advertiserNames").append("<option value=" + response.details.l_id + ">"+ response.details.l_id +"</option>")

            }
          },
          error: function(errorThrown) {
              alert('Something went wrong!. Please check CID');
                    $('input[name=cid], input[name=advertiser], input[id=advertiser], input[name=lead_owner], input[id=lead_owner]').val('')
          }
    }); 
  }
});