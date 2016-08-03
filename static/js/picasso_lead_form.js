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
    var emailFormat = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i; 
    window.failedFields = new Array();
    var fix_slots = new Array();
    $('#display_url_has_space').hide();
    $('#display_url_has_comma').hide();
    $('#display_invalid_url').hide();
    window.is_error = false;

    if(window.is_reset == true){
      window.is_reset = false;
      return false;
    }


    if($('#language_selector').val().trim()=='Simplified Chinese' && $('#market_selector option:selected').val().trim()=='Select Market')
    {
      $('#market_selector').addClass('error-box');
      $('#display_error_for_other_fields').show();
      window.is_error = true;
    }
    else{
       $('#display_error_for_other_fields').hide();
      $('#market_selector').removeClass('error-box');
    }
    // Google Rep Name Validation
    // grefElem = document.getElementById('gref');
    // validateFiled(grefElem);

   
    validateCheckBox();
    validateCasesAliasInput();
    removeCasesErrorClass();
    removeAdvertiserErrorClass();
    validateAvertiserEmailInput();

    validateCasesEmailField($('#cases_alias'));
    validateEmailField($('#advertiser_email'));


/*    if($('#cid').val() && $('#picasso_pod').val() && $('#team').val())
    {
      $('#display_error_for_other_fields').show();
      window.failedFields.push(elem);
      return false;
    }*/



    if(!$('#cid').val().trim().match(cidFormat)){
      $('#display_error_for_enter_valid_cid_format').show();
      $('#cid').addClass('error-box');
      /*frm.cid.focus();*/
      window.is_error = true;
    }
    else{
      $('#display_error_for_enter_valid_cid_format').hide();
    }

    objectiveValidation();

/*    if($('#bolt').hasClass('active') == false){
      objectiveValidation();
    }*/
    
    var comp_url1 = $('#comp_url_1').val().trim();
    var comp_url2 = $('#comp_url_2').val().trim();
    var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;


    competitorValidation();
 
    uniqueCompetitor()
    
    
    ValidateUrlField();
    validateCorpNCaseField();
    validatePodField();
    validateCidField();
    validateTeamField();
    /*podElem = document.getElementById('picasso_pod');
    validateFiled(podElem);


    teamElem = document.getElementById('team');
    validateFiled(teamElem);


    cidElem = document.getElementById('cid');
    validateFiled(cidElem);*/

    // Check If Error in Form
    if(window.is_error){
      focusElem = failedFields[0];
      $(focusElem).focus();
      return false;
    }else{
      $('#display_error_for_other_fields').hide();
      $('.error_list').css({'padding-top':'0px','padding-bottom':'0px'});
      $('#company').val($('#url').val().trim());
      $('#preloaderOverlay').show();
      return true;
    }  
  }


var nbs_team = ['NBS'];
  $('#team').change(function(){
  if(prevaluedict['cid']){
      $('#cid').val(prevaluedict['cid']);
  }
  else{
    if(nbs_team.indexOf($('#team option:selected').val().trim()) != -1){
      $('#cid').val('000-000-0000');
    }
    else{
      if($('#cid').val() === '000-000-0000'){
            $('#cid').val('');
      }
    }
  }
    $('#adv_mail').attr('hidden',false);
    $("#advertiser_email").val('').attr('hidden',false);
    $('#checkbox33').attr('hidden',false);
    $("#advertiser_email").attr("readonly",false);
    $('#language_selector').prop('selectedIndex',0);
    $('#Picasso input[type="checkbox"]').attr('disabled', false);
    var gettingAorC = $(this).find('option:selected').attr("class") == 'A' || $(this).find('option:selected').attr("class") == 'C';
    if (gettingAorC ){
      $('#checkbox3').attr('disabled', true);
      $('#checkbox33').addClass('is-checked');
      $('#checkbox33').find('span.mdl-checkbox__tick-outline').addClass('add_bg');
      $('.add_bg').css('background-color','grey');
      $('#checkbox33').find('span.mdl-checkbox__box-outline').addClass('add_border');
      $('.add_border').css('border','grey');
    }

    else{
      var removingStyle1 = $('#checkbox33').find('span.mdl-checkbox__tick-outline');
      removingStyle1.removeAttr('style');
      var removingStyle2 = $('#checkbox33').find('span.mdl-checkbox__box-outline');
      removingStyle2.removeAttr('style');
      //$('#checkbox33').removeClass('is-checked');
      //$('#checkbox3').attr('disabled', false);
    }
  if(prevaluedict['aemail']){
    $('#advertiser_email').val(prevaluedict['aemail']);
  }

  });


  function validateCidField(){
    // Validate Form Field
    if ($('#cid').val().trim() == "" || $('#cid').val().trim() == "0" || !$('#cid').val().trim()) {
    $('#cid').addClass('error-box');
    $('#display_error_for_other_fields').show();
    window.failedFields.push(elem);
    window.is_error = true;
    return false;
  }
}

function validatePodField(){
    // Validate Form Field
    if ($('#picasso_pod').val().trim() == "" || $('#picasso_pod').val().trim() == "0" || !$('#picasso_pod').val().trim()) {
    $('#picasso_pod').addClass('error-box');
    $('#display_error_for_other_fields').show();
    window.failedFields.push(elem);
    window.is_error = true;
    return false;
  }
}

function validateTeamField(){
    // Validate Form Field
    if ($('#team').val().trim() == "" || $('#team').val().trim() == "0" || !$('#team').val().trim()) {
    $('#team').addClass('error-box');
    $('#display_error_for_other_fields').show();
    window.failedFields.push(elem);
    window.is_error = true;
    return false;
  }
}

function ValidateUrlField() {
  var regexp = new RegExp("^http(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?$");
    var url = document.getElementById("url").value.toLowerCase();
    var Elementurl = document.getElementById("url");
    if (!regexp.test(url)) {
      var expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&/=]*)?/
      var regex = new RegExp(expression);
      var check_one_more = url;
        if (check_one_more.match(regex) )
          {   var inValid = /\s/;
              var value = url;
              var check = inValid.test(value);
              if(check){
                        // alert("URL contains space");
                        $('#display_url_has_space').show(); 
                        window.failedFields.push(Elementurl);
                        $("#url").addClass('error-box');
                        window.is_error = true;
                        return false;}
              if(!check){/*alert("valid with no space url");*/
                          string = url
                          re = new RegExp(/,\s*/);
                          var check_coma = re.test(string);
                          if (check_coma){
                                  $('#display_url_has_comma').show();
                                  // alert("URL contains comma");
                                  window.failedFields.push(Elementurl);
                                  $("#url").addClass('error-box');
                                  window.is_error = true;
                                  return false;
                                  }
                          $("#url").removeClass('error-box');
                          return true} 
          }
        else {
               $('#display_invalid_url').show();
               $("#url").addClass('error-box'); 
                window.is_error = true;
                window.failedFields.push(Elementurl);
                return false;}
  } else {  /*alert("Valid Url!");*/
            string = url
            re = new RegExp(/,\s*/);
            var check_coma = re.test(string);
            if (check_coma){
                    $('#display_url_has_comma').show();
                    // alert("URL contains comma");
                    window.failedFields.push(Elementurl);
                    $("#url").addClass('error-box');
                    window.is_error = true;
                    return false;
                    }
            $("#url").removeClass('error-box');
            return true; }
}

function validateOnlyCasesField()
{
   if ($('#cases_alias').val().trim() == "" || $('#cases_alias').val().trim() == "0" || !$('#cases_alias').val().trim()) {
    $('#cases_alias').addClass('error-box');
    $('#display_error_for_cases_mail').show();
    window.failedFields.push(elem);
    window.is_error = true;
    return false;
  }
  else{
    $('#display_error_for_cases_mail').hide();
    return true;
  }
}

function validateOnlyAdv(){
   if ($('#advertiser_email').val().trim() == "" || $('#advertiser_email').val().trim() == "0" || !$('#advertiser_email').val().trim()) {
    $('#advertiser_email').addClass('error-box');
    $('#display_error_for_adv_mail').show();
    window.failedFields.push(elem);
    window.is_error = true;
    return false;
  }
  else{
    $('#display_error_for_adv_mail').hide();
    return true;
  }
}

function validateEmailField(elem) {
  var check = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  // Validate Email Field
  if($(elem).val().trim()){
    if (!$(elem).val().trim().match(check)) {
      /*$(elem).focus();*/
      window.is_error = true;
      $(elem).addClass('error-box');
      $('#display_error_for_email_fields').show();
      return false;
    }
    else{
      $('#display_error_for_email_fields').hide();
      return true;
    }

  }
   else{
      $('#display_error_for_email_fields').hide();
      return true;
    }
}

function validateCasesEmailField(elem) {
  if ($(elem).val().trim()){
    var domain = $(elem).val().trim();
    domain = domain.split("@");
    if(domain[1] != 'google.com')
    {
    $(elem).addClass('error-box');
    /*$(elem).focus();*/
    window.is_error = true;
    $('#display_error_for_cases_alias').show();
    return false;
    }
    else{
    $('#display_error_for_cases_alias').hide();
    return true;
  }
  }
}

function resetBtn(elem){
  elemId = $(elem).attr('id');
  if(elemId == 'formReset'){
    window.is_reset = true;
    window.location.reload();
  }
}


function validateCheckBox()
{
  var cases_alias_checkbox = $('#checkbox22').attr('class');
  var advertiser_email_checkbox = $('#checkbox33').attr('class');
  if(cases_alias_checkbox.search('is-checked') != -1){
      var cases_alias = document.getElementById('cases_alias');
      validateOnlyCasesField(cases_alias);
  }
  if(advertiser_email_checkbox.search('is-checked') != -1){
      var advertiser_email = document.getElementById('advertiser_email');
      validateOnlyAdv(advertiser_email);
  }
  else{
    $('#display_error_for_adv_mail').hide();
  }
}


function validateCasesAliasInput()
{
  if($('#cases_alias').val().trim()){
    var cases_alias_checkbox = $('#checkbox22').attr('class');
    if(cases_alias_checkbox.search('is-checked') == -1){
        $('#checkbox22 .mdl-checkbox__ripple-container').addClass('error-box');
        window.is_error = true;
        return false;
    }
  }
  else{
    $('#checkbox22 .mdl-checkbox__ripple-container').removeClass('error-box');
      return true;
  }
}

function validateAvertiserEmailInput()
{
  if($('#advertiser_email').val().trim()){
    var advertiser_email_checkbox = $('#checkbox33').attr('class');
    if(advertiser_email_checkbox.search('is-checked') == -1){
        $('#checkbox33 .mdl-checkbox__ripple-container').addClass('error-box');
        window.is_error = true;
        return false;
    }
  }
  else{
      $('#checkbox33 .mdl-checkbox__ripple-container').removeClass('error-box');
      return true;
  }
}


function removeCasesErrorClass()
{
  var cases_alias_checkbox = $('#checkbox22').attr('class');
  if($('#cases_alias').val().trim() && cases_alias_checkbox.search('is-checked') != -1){
     $('#checkbox22 .mdl-checkbox__ripple-container').removeClass('error-box');
      return true;
  }
}

function removeAdvertiserErrorClass()
{
  var advertiser_email_checkbox = $('#checkbox33').attr('class');
  if($('#advertiser_email').val().trim() && advertiser_email_checkbox.search('is-checked') != -1){
     $('#checkbox33 .mdl-checkbox__ripple-container').removeClass('error-box');
      return true;
  }
}

var nbs_team = ['NBS'];
var pgName = "{{user.profile.team}}";
$('#bolt').click(function(){
  if(nbs_team.indexOf(pgName) == $('#team option:selected').val()){
    $('#cid').val('000-000-0000');
    $('#team').val(pgName);
  }

  if(prevaluedict['cid']){
    $('#cid').val(prevaluedict['cid']);
  }
  if(prevaluedict['team']){
    $("#team > option").each(function() {
      if(this.text == prevaluedict['team']){
        $('#team').val(prevaluedict['team']);
      }
    });
  }

  $('#ctype1').val('BOLT');
  $('.tab-content').css("background-color","#F9FAFC");
  $('.for-bolt').show();
});

$('#picasso').click(function(){
  if(nbs_team.indexOf(pgName) == $('#team option:selected').val()){
    $('#cid').val('000-000-0000');
    $('#team').val(pgName);
  }
  
  if(prevaluedict['cid']){
      $('#cid').val(prevaluedict['cid']);
  }

  if(prevaluedict['team']){
    $("#team > option").each(function() {
      if(this.text == prevaluedict['team']){
        $('#team').val(prevaluedict['team']);
      }
    });
  }
  
  $('#ctype1').val('PICASSO');
  $('.tab-content').css("background-color","#F9FAFC");
  $('.for-bolt').hide();
});


function resetPicasso() {
  $('#cases_alias').val('');
  $('#checkbox22').removeClass('is-checked');
  $('#checkbox2').removeProp("checked");

  $('#checkbox11').removeClass('is-checked');
  $('#checkbox1').removeProp("checked");
 /* 
  $('#team').prop('selectedIndex',0);*/
  $('#language_selector').prop('selectedIndex',0);
  $('#adv_mail').attr('hidden',false);
  $("#advertiser_email").val('').attr('hidden',false);
  $("#advertiser_email").attr("readonly",false);

  //$('#checkbox33').removeClass('is-checked');
  $('#checkbox33').find('span.mdl-checkbox__tick-outline').addClass('add_bg');
  $('.add_bg').css('background-color','');
  $('#checkbox33').find('span.mdl-checkbox__box-outline').addClass('add_border');
  $('.add_border').css({"border-color": "grey", "border-width":"2px", "border-style":"solid"});
  $('#checkbox33').attr('hidden',false);
  $('#checkbox3').attr("disabled",false);
  
  $('.checkvalid').removeClass('is-checked');
  $('.picasso_objective').removeProp("checked");
  $('.checkboxvalidation').find('input').val('');
  $('#additional_notes').val('');
  $('#comp_url_1').val('');
  $('#comp_url_2').val('');

          $("#language_selector").html('');
          $("#language_selector").append('<option value="English">English</option>');
          $("#language_selector").append('<option value="German">German</option>');
          $("#language_selector").append('<option value="French">French</option>');

  $("#advertiser_email").removeAttr("disabled");
    if(prevaluedict['aemail']){
      $('#advertiser_email').val(prevaluedict['aemail']);
  }
  $("#checkbox3").removeAttr("disabled");
  $('#checkbox33').addClass('is-checked');
  $("#checkbox3").show();
  $("#checkbox33").show();
  $('#advertiser_email').show();
  $('#adv_mail').show();
  $("#remove-check").show();
  
}

function resetBolt() {
  $('#cases_alias').val('');
  $('#checkbox22').removeClass('is-checked');
  $('#checkbox2').removeProp("checked");

  $('#checkbox11').removeClass('is-checked');
  $('#checkbox1').removeProp("checked");
/*
  $('#team').prop('selectedIndex',0);*/
  $('#language_selector').prop('selectedIndex',0);
  $('#adv_mail').attr('hidden',false);
  $("#advertiser_email").val('').attr('hidden',false);
  $("#advertiser_email").attr("readonly",false);

  //$('#checkbox33').removeClass('is-checked');
  $('#checkbox33').find('span.mdl-checkbox__tick-outline').addClass('add_bg');
  $('.add_bg').css('background-color','');
  $('#checkbox33').find('span.mdl-checkbox__box-outline').addClass('add_border');
  $('.add_border').css({"border-color": "grey", "border-width":"2px", "border-style":"solid"});
  $('#checkbox33').attr('hidden',false);
  $('#checkbox3').attr("disabled",false);
  
  $('.checkvalid').removeClass('is-checked');
  $('.picasso_objective').removeProp("checked");
  $('.checkboxvalidation').find('input').val('');
  $('#additional_notes').val('');
  $('#comp_url_1').val('');
  $('#comp_url_2').val('');

    $("#language_selector").html('');
    $("#language_selector").append('<option value="English">English</option>'+
    '<option value="French">French</option>'+
    '<option value="German">German</option>'+
    '<option value="Japanese">Japanese</option>'+
    '<option value="Simplified Chinese">Simplified Chinese</option>'+
    '<option value="Spanish (EMEA)">Spanish (EMEA)</option>'+
    '<option value="Spanish (LATAM)">Spanish (LATAM)</option>');

  $("#advertiser_email").removeAttr("disabled");
    if(prevaluedict['aemail']){
      $('#advertiser_email').val(prevaluedict['aemail']);
  }
  $("#checkbox3").removeAttr("disabled");
  $('#checkbox33').addClass('is-checked');
  $("#checkbox3").show();
  $("#checkbox33").show();
  $('#advertiser_email').show();
  $('#adv_mail').show();
  $("#remove-check").show();

}
/// code for restricted CID's
function checkID()
{
  var cid_to_compare = $('#cid').val().trim();
  if(cid_to_compare != '000-000-0000') {
    $.ajax({
      url: "/leads/get-picasso-bolt-lead/?cid="+cid_to_compare,
      type: "GET",
      dataType: 'JSON',
      success:function(data){
        if(data['status'] === 'success') {
          window.is_error = true;
          $('#cid_error').show();
          $(".lead-form :input").prop("disabled", true);
          $("#cid").prop("disabled", false);
          dataLayer.push({ 'event': 'gTrackEvent', 'category': 'Picasso', 'action': 'ineligible', 'label': cid.value});
          $('#formsubmit').prop('disabled', true);
          return false;
        }else{
            //Not in the array
          $('#cid_error').hide();
          $(".lead-form :input").prop("disabled", false);
          $('#formsubmit').prop('disabled', false);
          return true;
        }
      },
      failure:function(error) {
        // body...
      }
    });
  }
  else{
    $('#formsubmit').prop('disabled', false);
  }
}

function validateCorpNCaseField()
{
  var corp_email_checkbox = $('#checkbox11').attr('class').search('is-checked');
  var cases_alias_checkbox = $('#checkbox22').attr('class').search('is-checked');
  if((corp_email_checkbox == -1) && (cases_alias_checkbox == -1))
  {
    window.is_error = true;
    $('#checkbox11 .mdl-checkbox__ripple-container').addClass('error-box');
    $('#checkbox22 .mdl-checkbox__ripple-container').addClass('error-box');
    $('#display_error_for_contact_mail').show();
  }
  else
  {
    $('#checkbox11 .mdl-checkbox__ripple-container').removeClass('error-box');
    $('#display_error_for_contact_mail').hide();
  }
}

function optSelect(event) {
    if($('#team').find('option:selected').attr("class") == 'A' || $('#team').find('option:selected').attr("class") == 'C'){
      if(this.options[this.selectedIndex].text != 'English'){
        $('#checkbox33').removeClass('is-checked');
        $('#checkbox33').find('span.mdl-checkbox__tick-outline').addClass('add_bg');
        $('.add_bg').css('background-color','');
        $('#checkbox33').find('span.mdl-checkbox__box-outline').addClass('add_border');
        $('.add_border').css({"border-color": "grey", "border-width":"2px", "border-style":"solid"});
        $("#advertiser_email").val('').attr("readonly",true).attr('hidden',true);
        $('#display_error_for_adv_mail').hide();
        $('#adv_mail').attr('hidden',true);
        $('#checkbox3').attr('disabled',true);
        $('#checkbox33').attr('hidden',true);
      }
      else{
        $('#adv_mail').attr('hidden',false);
        $("#advertiser_email").attr("readonly",false).attr('hidden',false);
        $('#checkbox3').attr('disabled', false);
        $('#checkbox33').attr('hidden',false);
        $('#checkbox33').addClass('is-checked');
        $('#checkbox33').find('span.mdl-checkbox__tick-outline').addClass('add_bg');
        $('.add_bg').css('background-color','grey');
        
      }
    }
    if($('#team').find('option:selected').attr("class") == 'B'){
      if(this.options[this.selectedIndex].text != 'English'){
        $('#display_error_for_adv_mail').hide();
        $('#adv_mail').attr('hidden',true);
        $("#advertiser_email").val('').attr("readonly",true).attr('hidden',true);
        $('#checkbox3').attr('disabled', true);
        $('#checkbox33').attr('hidden',true);
      }
      else{
        $('#adv_mail').attr('hidden',false);
        $("#advertiser_email").attr("readonly",false).attr('hidden',false);
        $('#checkbox3').attr('disabled', false);
        $('#checkbox33').attr('hidden',false);
      }
    }
}

function uniqueCompetitor(){
  var curl1 = $('#comp_url_1').val().trim();
  var curl2 = $('#comp_url_2').val().trim();
  if(curl1 && curl2)
    {
      if(curl1 == curl2)
      {
      $('#comp_url_1').addClass('error-box');
      $('#comp_url_2').addClass('error-box');
      $('#display_error_for_same_competitor_url').show();
      window.is_error = true;
      return false;
      }
      else
      {
        $('#comp_url_1').removeClass('error-box');
        $('#comp_url_2').removeClass('error-box');
        $('#display_error_for_same_competitor_url').hide();
        return true;
      }
    }
}

/*function validateCompURL(){
  var curl1 = $('#comp_url_1').val();
  var curl2 = $('#comp_url_2').val();
  var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
  if(curl1 || curl2)
  {
    if(!re.test(curl1)){
      $('#comp_url_1').addClass('error-box');
      $('#invalid_competitor_url').show();
      window.is_error = true;
      return false;
    }

  else if(!re.test(curl2)){
    $('#comp_url_2').addClass('error-box');
    $('#invalid_competitor_url').show();
    window.is_error = true;
    return false;
    }
  }
}*/


function competitorValidation(){
  var curl1 = $('#comp_url_1').val().trim();
  var curl2 = $('#comp_url_2').val().trim();
  if($('#bolt').hasClass('active')){ 
    if(!curl1 && !curl2){
      $('#comp_url_1').addClass('error-box');
      $('#comp_url_2').addClass('error-box');
      $('#display_error_for_enter_comp_url').show();
      window.is_error = true;
      return false;
    }
    else if(curl1 && !curl2){
      $('#comp_url_2').addClass('error-box');
      $('#display_error_for_enter_comp_url').show();
      window.is_error = true;
      return false;
    }
    else if(curl2 && !curl1){
      $('#comp_url_1').addClass('error-box');
       $('#display_error_for_enter_comp_url').show();
      window.is_error = true;
      return false;
    }
    else{
       $('#display_error_for_enter_comp_url').hide();
       return true;
    }
  }
   else{
       $('#display_error_for_enter_comp_url').hide();
       return true;
  }
}


function objectiveValidation(){
    if($('#install_mobile_app').prop("checked") || $('#drive_foot_traffic').prop("checked") || $('#buy_online').prop("checked") || $('#form_entry').prop("checked") || $('#call_your_business').prop("checked") || $('#engage_with_your_content').prop("checked") || $('#become_a_fan').prop("checked")){
        $('.checkboxvalidation').removeClass('error-box');
        $('#display_error_for_objective').hide();
        return true;

      }else{
        $('#display_error_for_objective').show();
        $('.checkboxvalidation').addClass('error-box');
        if($('#bolt').hasClass('active')){
          $('#display_error_for_objective').hide();
          return true;
        }
        window.is_error = true;
        return false;
      }
}

