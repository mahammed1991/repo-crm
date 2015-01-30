$(document).ready(function() {
  $("#split_program").hide();
  $("#split_location").hide();
/* ===================== Default Report Starts Here ============= */
  // Get default report while loading template
  callAjax({'report_type': 'default_report', 'report_timeline': ['today'], 'teams': ['all'], 'countries': ['all']})
/* ===================== Default Report Ends Here ============= */

// date picker
  /*$(function() {
    $("#datepickerFrom, #datepickerTo").datepicker();
  });*/

 $(function() {
    $("#datepickerFrom").datepicker({
      defaultDate : "+1w",
      changeMonth : true,
      numberOfMonths : 1,
      dateFormat: "M dd, yy",
      onClose : function(selectedDate) {
        $("#to").datepicker("option", "minDate", selectedDate);
      }
    });
    $("#datepickerTo").datepicker({
      defaultDate : "+1w",
      changeMonth : true,
      numberOfMonths : 1,
      dateFormat: "M dd, yy",
      onClose : function(selectedDate) {
        $("#from").datepicker("option", "maxDate", selectedDate);
      }
    });
  });


  $(document).on('click', '.checkbox_select_all', function(e) {
      is_checked = $(this).is(":checked");
      id = $(this).closest('.checkbox').attr('id');
      $("#"+id+" label input").each(function(){
        if(is_checked){
          $(this).prop('checked', 'checked');  
        }else{
          $(this).prop('checked', false);
        }
      });
    });

});

/*=========== Changes in report type ===============*/
$("#filter_report_type").change(function() {

  var report_type = $(this).val();

  setDefaultDropdown();
  showFilters();

  $("#filter_country").hide();
  $("#split_location").hide();
  $("#filter_team_members").hide();

  if (report_type == 'leadreport_programview'){
    $("#filter_team").show();
    $("#filter_region").show();
    $("#filter_team_members").hide();
    $("#auth_user_info").hide();
    $("#split_program").show();

  }else if (report_type == 'leadreport_regionview'){
    $("#filter_team").show();
    $("#filter_region").show();
     $("#filter_country").hide();
     $("#split_location").hide();
     $("#auth_user_info").hide();
     $("#split_program").hide();
  }else if(report_type == 'leadreport_individualRep'){
      hideFilters();
    $("#filter_report_type").show();
    $("#auth_user_info").show();
    $("#filter_team_members").hide();
    $("#split_program").hide();
    $(".checkbox_select_all").trigger("click");
  }else if(report_type == 'leadreport_teamLead'){
      //callTeamMembers();
      hideFilters();
     $("#filter_region").hide();
     $("#auth_user_info").hide();
     $("#filter_team_members").show();
     $("#split_program").hide();
     $(".checkbox_select_all").trigger("click");
  }
  else if(report_type == ''){
    $('#filter_team').hide();
    $("#split_program").hide();
    $("#filter_region").hide();
    $("#auth_user_info").hide();
  }
  window.report_type = report_type;

});

/*=========== Changes in report timeline ===============*/
$('#filter_timeline').change(function(){
    var value = $(this).val();
    $('#filter_dateRange').hide();

    if(value == 'dateRange'){
      $('#filter_dateRange').show();
    }else{
      $('#filter_dateRange').hide();
    }
});

/*=========== Gettin Countries for selected Region ===============*/
$('#filter_region select').change(function(){
    $("#filter_country").hide();
    $("#split_location").hide();
    var region = $(this).val();
    if(region){
      if(window.report_type == 'leadreport_regionview' && region != 'all'){
        $("#split_location").show();
      }else{
        $("#split_location").hide();
      }
      get_countries(region);
    }
});



/*=================Get Reports by clicking view Reports Button=====================*/
$("#get_report").click(function(){
    var isError = false;
    var dataString = {}
    var selectedReportType = $("#filter_report_type").val();
    var selectedTimeline = $("#filter_timeline").val();
    //var selectedRegion = $('#filter_region').val();

    // Get report type details
    if(!selectedReportType){
        var errMsg = "Please select report type";
          showErrorMessage(errMsg);
          isError = true;
    }else{
        dataString['report_type'] = selectedReportType;
    }
    // Get timeline details
    if(!selectedTimeline){
        var errMsg = "Please select timeline from dropdown list";
        showErrorMessage(errMsg);
        isError = true;
    }
    else if (selectedTimeline == 'dateRange'){
      var from_date = $("#datepickerFrom").val();
      var to_date = $("#datepickerTo").val();

      // Validate from and to date
      if(from_date == "" || to_date == ""){
        var errMsg = "Please select from and to date";
        showErrorMessage(errMsg);
        isError = true;
      }

      dataString['report_timeline'] = [from_date, to_date];
    }
    else{
      dataString['report_timeline'] = [selectedTimeline];
    }


    team_members = [];
    if ($("#filter_team_members").is(":visible")){
      $("#filter_team_members label input:checked").each(function(){
        team_members.push($(this).val());
      });    
    }

    dataString['team_members'] = team_members;
    
    if($('#filter_region').is(':visible')){
      var selectedRegion = $('#filter_region select').val();

      if(!selectedRegion){
      var errMsg = "Please select Region from dropdown list";
        showErrorMessage(errMsg);
        isError = true;

      }
    else{
      dataString['region'] = selectedRegion;
      }
    }

     // Get location and team details 
    var selectedCountries = [];
    if ($("#filter_country:visible")){
      $("#filter_country .checkbox input:checked").each(function(){
          selectedCountries.push($(this).val());
      });  
    }
    
    dataString['countries'] = selectedCountries;

    var selectedTeam = [];

    if ($("#filter_team:visible")){
      $("#filter_team .checkbox input:checked").each(function(){
          selectedTeam.push($(this).val());
      });  
    }

    dataString['team'] = selectedTeam;

    if($('#program_split').is(":checked")){
      dataString['program_split'] = $('#program_split').prop('checked');;
    }
    else{
      dataString['program_split'] = $('#program_split').prop('unchecked');
    }

  if($('#location_split').is(":checked")){
        dataString['location_split'] = $('#location_split').prop('checked');
      }
      else{
        dataString['location_split'] = $('#location_split').prop('unchecked');
      }

     console.log(dataString);

     if(window.current_ldap){
      dataString['ldap_id'] = window.current_ldap;
     }

    if(isError){
        return false;
    }else{
      // Ajax call for get reports
      callAjax(dataString);
    }
});


function callAjax(dataString){
  $('#preloaderOverlay').show()
  $.ajax({
        url: "/reports/get_new_reports",
        data: dataString,
        type: 'GET',
        dataType: "json",
        success: function(data) {
            console.log(data);
            report = data['reports'];
            if (data['report_type'] == 'leadreport_programview'){
              $('#view_reports').empty();
              window.report_type = 'leadreport_programview';
              if(report['program_report']){
                createProgramByCountry(report['program_report']);
              }
            }
            else if(data['report_type'] == 'leadreport_regionview'){
              $('#view_reports').empty();
              window.report_type = 'leadreport_regionview';
              if(report['region_report']){
                createCountryByProgram(report['region_report']);
              }
            }
            window.code_type = data['code_types'];
            window.report_type = data['report_type'];
            showReport(report);
        $('#preloaderOverlay').hide()
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('failure');
        }
      }); 

}

/*========== hide and show filter for changes in report type=========*/
function hideFilters(){
  $('#filter_region').hide();
  $('#filter_team').hide();
  $('#filter_country').hide();
  $("#split_location").hide();

}

function showFilters(){
  $('#filter_report_type').show();
  $('#filter_region').show();
  $('#filter_timeline').show();
  $('#filter_team').show();
}

function showErrorMessage(message){
  alert(message);
}

function setDefaultDropdown(){
  $("#filter_region select").val('');
  $("#filter_team").val('all');
}

function get_countries(id){
  if(id=='all'){
    console.log(id);
  }else{
     $.ajax({
          url: "/reports/get-countries",
          dataType: "json",
          type: 'GET',
          data: {'team_id': id},
          success: function(data) {
              console.log(data);
              displayCountry(data);
          },
          error: function(errorThrown) {
              console.log('failure');
          }
        }); 
   }
}

function displayCountry(countries){
  $("#filter_country input").remove();
  $("#filter_country label").remove();
  $("#filter_country .checkbox").append('<label><input type="checkbox" value="all" class="checkbox_select_all"> Select All </label>')
  for( i=0; i<countries.length; i++){
      var id = countries[i]['id'];
      var name = countries[i]['name'];
      $("#filter_country .checkbox").append('<label><input type="checkbox" value="' + id + '">' + name + '</label>');
  }
  $("#filter_country").show();
  //$("#split_location").show();
}

function showReport(reports){

  if(window.report_type == 'default_report'){
    draw_and_display_tables(reports);
  }
  else if(window.report_type == 'leadreport_individualRep'){
    draw_and_display_tables(reports);
  }
  else if(window.report_type == 'leadreport_teamLead'){
   draw_and_display_tables(reports);
  }
  else if(window.report_type == 'leadreport_programview'){
   draw_and_display_tables(reports);
  }
   else if(window.report_type == 'leadreport_regionview'){
    draw_and_display_tables(reports);
  }

}

function drawColumnChart(details){
  var keys = [];
  var values = [];

  for(var key in details){
    if (key =='total_leads'){
      keys.splice(0, 0, "Total Leads");
    }
    else{
      keys.push(key)
    }
  } 

  for(var key in details) {
     if (key =='total_leads'){
      values.splice(0, 0, details[key]);
    }else{
      values.push(details[key])
    }
  }

  var columnChart_datatable = [keys, values];

  columnChartDraw(columnChart_datatable, '', 'columnchart')
}


function drawPieChart(details){

  var pieChart_datatable = [['Code Types', 'Leads per Code Type']];

  for(var key in details) pieChart_datatable.push([key, details[key]]);

  pieChartDraw(pieChart_datatable, '', 'piechart')
}

function drawLineChart(details){

  var lineChart_datatable = [['Weeks', 'Leads Won', 'Leads Submitted']]

  for(var key in details){
      var record = []
      var val = 'Week '+ key.toString()
      record.push(val)
      week_dict = details[key]

      for(key in week_dict){
        record.push(week_dict[key])
      }
      lineChart_datatable.push(record)
  }
  lineChartDraw(lineChart_datatable, '', 'linechart')
}

function displayLeadStatusTable(details){
  var rows = ""

  for(var key in details){
    if(key == 'total_leads'){
        total = '<tr><td class="lbl">Total Leads</td><td class="value">' + details[key] + '</td></tr>'
    }else if (key == 'TAT'){
      end = '<tr><td class="lbl"> Average ' + key + '</td><td class="value">' + details[key] + ' days</td></tr>'
    }else{
      rows += '<tr><td class="lbl">' + key + '</td><td class="value">' + details[key] + '</td></tr>'
    }
  }
    $("#lead_status_table").append(total+rows+end);
}

function displayCodeTypeTable(details){
  var rows = ""

  for(key in details){

      rows += '<tr><td class="lbl">' + key + '</td><td class="value">' + details[key] + '</td></tr>'
  }
  $("#code_type_table").append(rows);
}

function displayLineChartTable(details){
  var rows = '<tr><th class="lbl">Weeks</th><th class="value">Leads Won</th><th class="value">Leads Submitted</th></tr>'
  var row = ''

  for(key in details){

      row += '<tr><td class="lbl">Week '+ key +'</td>'
      var week_dict = details[key]

      for (key in week_dict){

      row += '<td class="value">' + week_dict[key] + '</td>'
   
      }
      row +='</tr>'

   }
  $("#line_chart_table").append(rows+row)
}

function clearTables(){
  $('#lead_status_table').empty();
  $('#code_type_table').empty();
  $('#line_chart_table').empty();
}

function draw_and_display_tables(reports){
    clearTables()
    drawColumnChart(reports['lead_status_summary']);
    displayLeadStatusTable(reports['lead_status_summary']);
    drawPieChart(reports['piechart']);
    newTable(reports['table_header'], reports['lead_code_type_analysis'])
    drawLineChart(reports['week_on_week_details_in_qtd'])
    displayLineChartTable(reports['week_on_week_details_in_qtd'])
}

function newTable(firstrow, details){
  $("#code_type_table").empty();

  header = '<tr><td>Code Types/Lead Status</td>'
  for(key in firstrow){
    header += '<td>'+ key + '</td>'
  }
  header = header+'<td>Total</td></tr>'

  var each_row;

    for(i = 0; i < details.length; i++){

        dict_obj = details[i];
        dict_row = '<tr><td>'
        var value_dict;  
        end = '';

        for(key in dict_obj){
          dict_row += key +'</td>'
          value_dict = dict_obj[key]
        }

        for(key in value_dict){

          if(key=='Total'){

            end = '<td>'+value_dict[key]+'</td>'
          }
          else{

            dict_row += '<td>'+value_dict[key]+'</td>'
          }
        }

        each_row += dict_row+end;
  }
 $("#code_type_table").append(header+each_row);
}


function createProgramByCountry(programs){
  createTableHeader();

  total_rows  = "";
  rows = "";
  for(i=0; i<programs.length; i++){
      rows += '<tr><td colspan="8" class="no-pad no-bor">' +
              '<table cellpadding="0" cellspacing="0" border="0" width="100%" class="main-row">'+
              '<tr class="clickable" data-toggle="collapse" data-target="'+ '#accordion'+ i +'">'+
                      '<td class="lbl relative">'+ programs[i]['program_name']+ '<span class="row-expand">+</span> <span class="row-collapse">_</span></td>' +
                      '<td class="value">'+ programs[i]['week_total'] +'</td>'+
                      '<td class="value">' + programs[i]['week_win'] + '</td>'+
                      '<td class="value">'+ programs[i]['qtd_total'] +'</td>'+
                      '<td class="value">' + programs[i]['qtd_win'] + '</td>'+
                  '</tr>'

      inner_rows = '<tr id="'+ 'accordion'+ i +'" class="collapse">'+
                      '<td colspan="8" class="no-pad no-bor">'+
                          '<table cellpadding="0" cellspacing="0" border="0" width="100%" class="sub-row">'

      for(j=0; j<programs[i]['locations'].length; j++){
        loc = programs[i]['locations']
        inner_rows += '<tr>'+
                        '<td class="lbl">' + loc[j]['location_name'] +'</td>'+
                        '<td class="value">' + loc[j]['week_total'] +'</td>'+
                        '<td class="value">' + loc[j]['week_win'] +'</td>'+
                        '<td class="value">' + loc[j]['qtd_total'] +'</td>' +
                        '<td class="value">' + loc[j]['qtd_win'] +'</td>'+
                    '</tr>'
      }
      inner_rows += "</table></td></tr>";
      rows += inner_rows;
  }
  total_rows += rows + "</table></td></tr>";
  $("#view_reports").append(total_rows);
}

function createCountryByProgram(programs){
  createTableHeader();

  total_rows  = "";
  rows = "";
  for(i=0; i<programs.length; i++){
      rows += '<tr><td colspan="8" class="no-pad no-bor">' +
              '<table cellpadding="0" cellspacing="0" border="0" width="100%" class="main-row">'+
              '<tr class="clickable" data-toggle="collapse" data-target="'+ '#accordion'+ i +'">'+
                      '<td class="lbl relative">'+ programs[i]['location_name']+ '<span class="row-expand">+</span> <span class="row-collapse">_</span></td>' +
                      '<td class="value">'+ programs[i]['week_total'] +'</td>'+
                      '<td class="value">' + programs[i]['week_win'] + '</td>'+
                      '<td class="value">'+ programs[i]['qtd_total'] +'</td>'+
                      '<td class="value">' + programs[i]['qtd_win'] + '</td>'+
                  '</tr>'

      inner_rows = '<tr id="'+ 'accordion'+ i +'" class="collapse">'+
                      '<td colspan="8" class="no-pad no-bor">'+
                          '<table cellpadding="0" cellspacing="0" border="0" width="100%" class="sub-row">'

      for(j=0; j<programs[i]['programs'].length; j++){
        loc = programs[i]['programs']
        inner_rows += '<tr>'+
                        '<td class="lbl">' + loc[j]['team_name'] +'</td>'+
                        '<td class="value">' + loc[j]['week_total'] +'</td>'+
                        '<td class="value">' + loc[j]['week_win'] +'</td>'+
                        '<td class="value">' + loc[j]['qtd_total'] +'</td>' +
                        '<td class="value">' + loc[j]['qtd_win'] +'</td>'+
                    '</tr>'
      }
      inner_rows += "</table></td></tr>";
      rows += inner_rows;
  }
  total_rows += rows + "</table></td></tr>";
  $("#view_reports").append(total_rows);
}



function createTableHeader(){

  header = '<tr class="top-head">'+
              '<th></th>'+
                '<th colspan="2">Current Week</th>'+
                '<th colspan="2">QTD</th>'+
            '</tr>'+
            '<tr>'+
              '<th>Program</th>'+
                '<th>Leads</th>'+
                '<th>Wins</th>'+
                '<th>Leads</th>'+
                '<th>Wins</th>'+
            '</tr>'

  $("#view_reports").append(header);

}

$('#download').click(function(){
    var isError = false;
    var dataString = {}
    var selectedReportType = $("#filter_report_type").val();
    var selectedTimeline = $("#filter_timeline").val();
    //var selectedRegion = $('#filter_region').val();

    // Get report type details
    if(!selectedReportType){
        var errMsg = "Please select report type";
          showErrorMessage(errMsg);
          isError = true;
    }else{
        dataString['report_type'] = selectedReportType;
        $("#download_report_type").val(selectedReportType);
    }

    // Get timeline details
    if(!selectedTimeline){
        var errMsg = "Please select timeline from dropdown list";
        showErrorMessage(errMsg);
        isError = true;
    }
    else if (selectedTimeline == 'dateRange'){
      var from_date = $("#datepickerFrom").val();
      var to_date = $("#datepickerTo").val();

      // Validate from and to date
      if(from_date == "" || to_date == ""){
        var errMsg = "Please select from and to date";
        showErrorMessage(errMsg);
        isError = true;
      }

      dataString['report_timeline'] = [from_date, to_date];
      $("#download_report_timeline").val(dataString['report_timeline']);
    }
    else{
      dataString['report_timeline'] = [selectedTimeline];
      $("#download_report_timeline").val([selectedTimeline]);
    }


    team_members = [];
    if ($("#filter_team_members").is(":visible")){
      $("#filter_team_members label input:checked").each(function(){
        team_members.push($(this).val());
      });    
    }

    dataString['team_members'] = team_members;
    $("#download_team_members").val(team_members);
    
    if($('#filter_region').is(':visible')){
      var selectedRegion = $('#filter_region select').val();

      if(!selectedRegion){
      var errMsg = "Please select Region from dropdown list";
        showErrorMessage(errMsg);
        isError = true;

      }
    else{
      dataString['region'] = selectedRegion;
      $("#download_region").val(selectedRegion);
      }
    }

     // Get location and team details 
    var selectedCountries = [];
    if ($("#filter_country:visible")){
      $("#filter_country .checkbox input:checked").each(function(){
          selectedCountries.push($(this).val());
      });  
    }
    
    dataString['countries'] = selectedCountries;
    $("#download_countries").val(selectedCountries);

    var selectedTeam = [];

    if ($("#filter_team:visible")){
      $("#filter_team .checkbox input:checked").each(function(){
          selectedTeam.push($(this).val());
      });  
    }

    dataString['team'] = selectedTeam;
    $("#download_team").val(selectedTeam);

    var selectedFields = [];

     if ($("#download_fields:visible")){

      $("#download_fields .checkbox input:checked").each(function(){
          selectedFields.push($(this).val());
      });  
    }

    dataString['selectedFields'] = selectedFields;
    $("#download_selectedFields").val(selectedFields);

    console.log(dataString);

    if(isError){
        return false;
    }else{
     $("#download_reports").submit();
    }
}); 
 
    

//{'report_type': 'default_report', 'report_timeline': ['today'], 'teams': ['all'], 'countries': ['all']}

function downloadReport(dataString){
   //$('#preloaderOverlay').show();
  $.ajax({
        url: "/reports/get-download-report",
        data: dataString,
        type: 'GET',
        dataType: "json",
        success: function(data) {
            console.log(data);
            },
        error: function(data) {
            console.log('failure');
        },
      }); 

}

$('.ldap').focus(function() {
  return $(this).autocomplete({
    source: "/reports/get-user-name",
    minLength: 2,
    close: function(event) {
    },
    select: function(event, ui) {
      if ($("#ldap").val() !== "") {
        $("#ldap").val(ui.item.id + "-" + ui.item.username);
        window.current_ldap = ui.item.id;
         $("#ldap_manager").text(ui.item.manager);
         $("#ldap_program").text(ui.item.program);
         $("#ldap_region").text(ui.item.region);
        //$("label[for=id_employee]").css("display", "none");

      }
    }
  });
});