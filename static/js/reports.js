$(document).ready(function() {
  $("#split_program").hide();
  $("#split_location").hide();
/* ===================== Default Report Starts Here ============= */
  // Get default report while loading template
  callAjax({'report_type': 'default_report', 'report_timeline': ['today'], 'team': ['all'], 'countries': ['all']})
/* ===================== Default Report Ends Here ============= */

 $(function() {
    $("#datepickerFrom").datepicker({
      defaultDate : "+1w",
      changeMonth : true,
      numberOfMonths : 1,
      minDate:  dateLimitToPrevQuarter(), 
      dateFormat: "M dd, yy",
      onClose : function(selectedDate) {
        $("#to").datepicker("option", "minDate", selectedDate);
      },
      onSelect: function (selected) {
            var dt = new Date(selected);
            dt.setDate(dt.getDate() + 1);
            $("#datepickerTo").datepicker("option", "minDate", dt);
        }
    });
    $("#datepickerTo").datepicker({
      defaultDate : "+1w",
      changeMonth : true,
      numberOfMonths : 1,
      minDate:  dateLimitToPrevQuarter(),
      dateFormat: "M dd, yy",
      onClose : function(selectedDate) {
        $("#from").datepicker("option", "maxDate", selectedDate);
      },
      onSelect: function (selected) {
            var dt = new Date(selected);
            dt.setDate(dt.getDate() - 1);
            $("#datepickerFrom").datepicker("option", "maxDate", dt);
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
  $("#filter_team input[type=checkbox]").attr('checked', false)
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
    var from_date = $("#datepickerFrom").val('');
    var to_date = $("#datepickerTo").val('');

    if(value == 'dateRange'){
      $('#filter_dateRange').show();
    }else{
      $('#filter_dateRange').hide();
    }
});

/*=========== Gettin Countries for selected Region ===============*/
$('#filter_region select').change(function(){
    $("#filter_country input[type=checkbox]").attr('checked', false)
    $("#filter_country").hide();
    $("#split_location").hide();
    var region = $(this).val();
    if(region){
      if(window.report_type == 'leadreport_regionview' && region == 'all'){
        $("#split_location").show();
      }
      else if (window.report_type == 'leadreport_regionview' && region != ''){
        $("#split_location").show();
      }
      else{
      $("#split_location").hide();
    }
      get_countries(region);
    }
});

/*=================Get Reports by clicking view Reports Button=====================*/
$("#get_report").click(function(){
    $('#form_ldap_id').prop("value",window.current_ldap);
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
      if (team_members.length < 1){
          var errMsg = "Please select atleast one member from your team";
          showErrorMessage(errMsg);
          isError = true;
        }  
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
    if ($("#filter_country").is(":visible")){
      $("#filter_country .checkbox input:checked").each(function(){
          selectedCountries.push($(this).val());
      }); 
      console.log(dataString['region'])
      if (dataString['region'] != 'all' && selectedCountries.length < 1){
        var errMsg = "Please select Countries from Countries list";
        showErrorMessage(errMsg);
        isError = true;
      }
    }
    
    dataString['countries'] = selectedCountries;

    var selectedTeam = [];

    if ($("#filter_team").is(":visible")){

      $("#filter_team .checkbox input:checked").each(function(){
          selectedTeam.push($(this).val());
      }); 
      if (selectedTeam.length < 1){
        var errMsg = "Please select Program from programs list";
        showErrorMessage(errMsg);
        isError = true;
      }
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
  console.log(dataString);
  $('#preloaderOverlay').show();
  $.ajax({
        url: "/reports/get_new_reports",
        data: dataString,
        type: 'GET',
        dataType: "json",
        success: function(data) {
          /*if(dataString['program_split'] || dataString['location_split']){
            program_vs_location(dataString);
            $('#preloaderOverlay').show();
          }*/
            console.log(data);
            report = data['reports'];
            if (data['report_type'] == 'leadreport_programview'){
              $('#view_reports').empty();
              window.report_type = 'leadreport_programview';
              if(report['program_report']){
                programViewReport(report['program_report']);
              }
            }
            else if(data['report_type'] == 'leadreport_regionview'){
              $('#view_reports').empty();
              window.report_type = 'leadreport_regionview';
              if(report['region_report']){
                regionViewReport(report['region_report'])
              }
            }
            window.code_type = data['code_types'];
            window.report_type = data['report_type'];
            window.report_timeline = data['report_timeline']
            $('#tag').text(data['tag']);
            showReport(report);
            if(window.current_ldap == window.user_id){
              $("#profile_div").show();
            }else{
              $("#profile_div").hide();
            }
        $('#preloaderOverlay').hide()
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('failure');
            $('#preloaderOverlay').hide()
        }
      }); 

}

/*function program_vs_location(dataString){
  $('#preloaderOverlay').show();
  $.ajax({
        url: "/reports/get-program-location",
        data: dataString,
        type: 'GET',
        dataType: "json",
        success: function(data) {
            console.log(data);
            $('#preloaderOverlay').hide();
            report = data['reports'];
             if (data['report_type'] == 'leadreport_programview'){
              $('#view_reports').empty();
              window.report_type = 'leadreport_programview';
              if(report['program_report']){
                programViewReport(report['program_report']);
              }
            }
            else if(data['report_type'] == 'leadreport_regionview'){
              $('#view_reports').empty();
              window.report_type = 'leadreport_regionview';
              if(report['region_report']){
                regionViewReport(report['region_report'])
              }
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('failure');
            $('#preloaderOverlay').hide()
        }
  });
}*/

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
  $("#filter_timeline").val('')
  $("#filter_dateRange").hide()
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
    }else{
      if(key != 'TAT')
        keys.push(key)
    }
  } 

  for(var key in details) {
     if (key =='total_leads'){
      values.splice(0, 0, details[key]);
    }else{
        if (key != 'TAT')
          values.push(details[key])
    }
  }

  var columnChart_datatable = [keys, values];

  colors = ['#000099', '#FF0000', '#FFCC00', '#00CC00', '#660066', '#006699']

  res = [['Lead Status', 'No Of Leads', { role: 'style' }]]
  for(var i=0; i<keys.length; i++){
    temp = []
    temp.push(keys[i]);
    temp.push(values[i]);
    temp.push(colors[i]);
    res.push(temp);
  }
  columnChartDraw(res, '', 'columnchart')
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
        if(key != 'date_range'){
          record.push(week_dict[key])
        }
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
      if(details[key] != null){
        end = '<tr><td class="lbl"> Average ' + key + '</td><td class="value">' + details[key] + ' days</td></tr>'
      }else{
        end = '<tr><td class="lbl"> Average ' + key + '</td><td class="value">' + 0 + ' days</td></tr>'
      }
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
  var rows = '<tr><th class="lbl">Weeks</th><th class="lbl">Leads Won</th><th class="lbl">Leads Submitted</th></tr>'
  var row = ''

  for(key in details){

      var week_dict = details[key]
      row += '<tr><td class="lbl" data-toggle="tooltip" data-placement="top" title="'+week_dict['date_range']+'">Week '+ key +'</td>'
      for (key in week_dict){
        if(key != 'date_range')
      {row += '<td class="value">' + week_dict[key] + '</td>'}
   
      }
      row +='</tr>'

   }
  $("#line_chart_table").append(rows+row)
}

function customeTimeLineChartTable(details, s_keys, timeline){
  customDrawLineChart(details, s_keys, timeline);
  var rows = '<tr><th class="lbl">'+ timeline +'</th><th class="lbl">Leads Won</th><th class="lbl">Leads Submitted</th></tr>'
  var row = ''

  for(var i = 0;  i < s_keys.length; i++){

      row += '<tr><td class="lbl">'+ s_keys[i] +'</td>'
      var week_dict = details[s_keys[i]]

      for (s_keys[i] in week_dict){

      row += '<td class="value">' + week_dict[s_keys[i]] + '</td>'
   
      }
      row +='</tr>'

   }
  $("#line_chart_table").append(rows+row)
}

function customDrawLineChart(details, s_keys, timeline){

  var lineChart_datatable = [[timeline, 'Leads Won', 'Leads Submitted']]

  for(var indx=0; indx<s_keys.length; indx++){
      var record = [];
      record.push(s_keys[indx]);
      week_dict = details[s_keys[indx]];

      for(key in week_dict){
        record.push(week_dict[key]);
      }

      lineChart_datatable.push(record);
  }
  lineChartDraw(lineChart_datatable, '', 'linechart')


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
    newTable(reports['table_header'], reports['lead_code_type_analysis']);
    drawLineChart(reports['timeline_chart_details']);
    //displayLineChartTable(reports['week_on_week_details_in_qtd']);
    if (window.report_timeline[0] == "this_quarter"){
      customeTimeLineChartTable(reports['timeline_chart_details'], reports['sort_keys'], 'Months');
      
    }
    else if(window.report_timeline.length > 1){
      displayLineChartTable(reports['timeline_chart_details']);
    }
    else{
      customeTimeLineChartTable(reports['timeline_chart_details'], reports['sort_keys'], 'Weeks');
    }
    
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


function programViewReport(programs){
  createTableHeader("Program");
  rows = "";
  i = 1;
  for(key in programs){

     var colRow = ''
      if((programs[key]['out_vs_trgt']).toFixed(2) >= 100){
            colRow = '<td class="value green">' + (programs[key]['out_vs_trgt']).toFixed(2) + '% </td>'
          }
      else if(((programs[key]['out_vs_trgt']).toFixed(2) < 100) && (programs[key]['out_vs_trgt'].toFixed(2) > 0)){
        colRow = '<td class="value red">' + (programs[key]['out_vs_trgt']).toFixed(2) + '% </td>'
          }
      else{
        colRow = '<td class="value"> N/A </td>'
          }

  if (key === ''){
    pgm  = '<td class="lbl relative" style="font-size:11px !important;"> Other <span class="row-expand"></span> <span class="row-collapse"></span></td>' 
  }
  else{
    pgm = '<td class="lbl relative" style="font-size:11px !important;">'+ key + '<span class="row-expand"></span> <span class="row-collapse"></span></td>' 
  }

    
    i = i + 1;
    rows += '<tr><td colspan="8" class="no-pad no-bor">' +
                '<table cellpadding="0" cellspacing="0" border="0" width="100%" class="main-row">'+
                '<tr class="clickable collapsed" data-toggle="collapse" data-target="'+ '#accordion'+ i +'">'+
                        pgm +
                        '<td class="value">'+ programs[key]['week_total'] +'</td>'+
                        '<td class="value">' + programs[key]['week_win'] + '</td>'+
                        '<td class="value">' + programs[key]['qtd_total'] +'</td>'+
                        '<td class="value">' + programs[key]['qtd_win'] + '</td>'+
                        '<td class="value">' + programs[key]['end_qtr_total'] + '</td>'+
                        '<td class="value">' + programs[key]['end_qtr_target'] + '</td>'+
                        colRow +
                 '</tr>'

    locations = programs[key]['locations']

    inner_rows = '<tr id="'+ 'accordion'+ i +'" class="collapse">'+
                  '<td colspan="8" class="no-pad no-bor">'+
                      '<table cellpadding="0" cellspacing="0" border="0" width="100%" class="sub-row">'

    for (key in locations){

      var rowCol = ''
      if((locations[key]['out_vs_trgt']).toFixed(2) >= 100){
            rowCol = '<td class="value green">' + (locations[key]['out_vs_trgt']).toFixed(2) + '% </td>'
          }
      else if(((locations[key]['out_vs_trgt']).toFixed(2) < 100) && (locations[key]['out_vs_trgt'].toFixed(2) > 0)){
        rowCol = '<td class="value red">' + (locations[key]['out_vs_trgt']).toFixed(2) + '% </td>'
          }
      else{
        rowCol = '<td class="value"> N/A </td>'
          }

    inner_rows += '<tr>'+
                        '<td class="lbl">' + key +'</td>'+
                        '<td class="value">' + locations[key]['week_total'] +'</td>'+
                        '<td class="value">' + locations[key]['week_win'] +'</td>'+
                        '<td class="value">' + locations[key]['qtd_total'] +'</td>' +
                        '<td class="value">' + locations[key]['qtd_win'] +'</td>'+
                        '<td class="value">' + locations[key]['end_qtr_total'] + '</td>'+
                        '<td class="value">' + locations[key]['end_qtr_target'] + '</td>'+
                        rowCol +
                   '</tr>'

    }
  
  inner_rows += "</table></td></tr>";
  rows += inner_rows;
  rows += "</table></td></tr>";
}
 $("#view_reports").append(rows);
}

function regionViewReport(locations){
  createTableHeader("Region");
  rows = "";
  i = 1;
  for(key in locations){
    i = i + 1;

    var rowCol = ''
      if((locations[key]['out_vs_trgt']).toFixed(2) >= 100){
            rowCol = '<td class="value green">' + (locations[key]['out_vs_trgt']).toFixed(2) + '% </td>'
          }
      else if(((locations[key]['out_vs_trgt']).toFixed(2) < 100) && (locations[key]['out_vs_trgt'].toFixed(2) > 0)){
        rowCol = '<td class="value red">' + (locations[key]['out_vs_trgt']).toFixed(2) + '% </td>'
          }
      else{
        rowCol = '<td class="value"> N/A </td>'
          }

    rows += '<tr><td colspan="8" class="no-pad no-bor">' +
                '<table cellpadding="0" cellspacing="0" border="0" width="100%" class="main-row">'+
                '<tr class="clickable collapsed" data-toggle="collapse" data-target="'+ '#accordion'+ i +'">'+
                        '<td class="lbl relative">'+ key + '<span class="row-expand"></span> <span class="row-collapse"></span></td>' +
                        '<td class="value">'+ locations[key]['week_total'] +'</td>'+
                        '<td class="value">' + locations[key]['week_win'] + '</td>'+
                        '<td class="value">' + locations[key]['qtd_total'] +'</td>'+
                        '<td class="value">' + locations[key]['qtd_win'] + '</td>'+
                        '<td class="value">' + locations[key]['end_qtr_total'] + '</td>'+
                        '<td class="value">' + locations[key]['end_qtr_target'] + '</td>'+
                        rowCol +
                 '</tr>'

    programs = locations[key]['programs']

    inner_rows = '<tr id="'+ 'accordion'+ i +'" class="collapse">'+
                  '<td colspan="8" class="no-pad no-bor">'+
                      '<table cellpadding="0" cellspacing="0" border="0" width="100%" class="sub-row">'

    for (key in programs){

      var colRow = ''
      if((programs[key]['out_vs_trgt']).toFixed(2) >= 100){
            colRow = '<td class="value green">' + (programs[key]['out_vs_trgt']).toFixed(2) + '% </td>'
          }
      else if(((programs[key]['out_vs_trgt']).toFixed(2) < 100) && (programs[key]['out_vs_trgt'].toFixed(2) > 0)){
        colRow = '<td class="value red">' + (programs[key]['out_vs_trgt']).toFixed(2) + '% </td>'
          }
      else{
        colRow = '<td class="value"> N/A </td>'
          }

    if (key === ''){
    pgm  = '<td class="lbl"> Other </td>'
  }
  else{
    pgm = '<td class="lbl">' + key +'</td>'
  }


    inner_rows += '<tr>'+
                        pgm + 
                        '<td class="value">' + programs[key]['week_total'] +'</td>'+
                        '<td class="value">' + programs[key]['week_win'] +'</td>'+
                        '<td class="value">' + programs[key]['qtd_total'] +'</td>' +
                        '<td class="value">' + programs[key]['qtd_win'] +'</td>'+
                        '<td class="value">' + programs[key]['end_qtr_total'] + '</td>'+
                        '<td class="value">' + programs[key]['end_qtr_target'] + '</td>'+
                        colRow +
                        
                   '</tr>'

    }
  
  inner_rows += "</table></td></tr>";
  rows += inner_rows;
  rows += "</table></td></tr>";
}
 $("#view_reports").append(rows);
}

function createTableHeader(param){

  header = '<tr class="top-head">'+
              '<th></th>'+
                '<th colspan="2">Current Week</th>'+
                '<th colspan="2">QTD</th>'+
                '<th colspan="3">End of Quarter Outlook</th>'+
            '</tr>'+
            '<tr>'+
              '<th>'+ param +'</th>'+
                '<th>Leads</th>'+
                '<th>Wins</th>'+
                '<th>Leads</th>'+
                '<th>Wins</th>'+
                '<th>Leads</th>'+
                '<th>Target Leads</th>'+
                '<th>Outlook vs Target</th>'+
            '</tr>'

  $("#view_reports").append(header);

}

$('#download').click(function(){

  if($('#drp_autogen0').is(':visible')){

      var isError = false;
      if($("#historical_filter_timeline").daterangepicker("getRange") == null ){
        alert('Please choose date range to download the historical data');
        var isError = true;
      }else{
        alert("Selected range is: " + $("#historical_filter_timeline").val())
       $("#download_report_type").val('historical_report');
       $("#download_report_timeline").val($("#historical_filter_timeline").val());
       $("#download_team").val(['all']);
       $("#download_countries").val(['all']);

       var selectedFields = [];
        if ($("#download_fields:visible")){

          $("#download_fields .checkbox input:checked").each(function(){
              selectedFields.push($(this).val());
          });

        $("#download_selectedFields").val(selectedFields);
        }
          var isError = false;
      }
  }
  else{

    var isError = false;
    var dataString = {}
    var selectedReportType = $("#filter_report_type").val();
    var selectedTimeline = $("#filter_timeline").val();
    //var selectedRegion = $('#filter_region').val();
    var condn = ($("#filter_team_members").is(":visible") || $('#filter_region').is(':visible') || $("#filter_country").is(":visible"))
    if((!selectedReportType && !selectedTimeline) && (!condn)){

          //dataString = {'download_report_type': 'default_report', 'download_report_timeline': ['today'], 'download_team': ['all'], 'download_countries': ['all']};
          $("#download_report_type").val('default_report');
          $("#download_report_timeline").val(['today']);
          $("#download_team").val(['all']);
          $("#download_countries").val(['all']);
          var selectedFields = [];
          if ($("#download_fields:visible")){
            $("#download_fields .checkbox input:checked").each(function(){
                selectedFields.push($(this).val());
            });  
          dataString['selectedFields'] = selectedFields;
          $("#download_selectedFields").val(selectedFields);
          }

          
        }
    else{
     if(!selectedReportType){
                var errMsg = "Please select report type";
                  showErrorMessage(errMsg);
                  isError = true;
                }else{
                    dataString['report_type'] = 'default_report';
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
                from_date = from_date.replace(',', '-');
                to_date = to_date.replace(',', '-');

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
                if (team_members.length < 1){
                    var errMsg = "Please select atleast one member from your team";
                    showErrorMessage(errMsg);
                    isError = true;
                  }
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

              if ($("#filter_country").is(":visible")){
                $("#filter_country .checkbox input:checked").each(function(){
                    selectedCountries.push($(this).val());
                }); 

                if (dataString['region'] != 'all' && selectedCountries.length < 1){
                    var errMsg = "Please select Countries from Countries list";
                    showErrorMessage(errMsg);
                    isError = true;
                  } 
                }
                  dataString['countries'] = selectedCountries;
                  $("#download_countries").val(selectedCountries);
             

              var selectedTeam = [];

              if ($("#filter_team").is(":visible")){
                $("#filter_team .checkbox input:checked").each(function(){
                    selectedTeam.push($(this).val());
                }); 
                if (selectedTeam.length < 1){
                    var errMsg = "Please select Program from programs list";
                    showErrorMessage(errMsg);
                    isError = true;
                  } 
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
    }

    // Get report type details
    

    //console.log(dataString, 'dataString');

    
  }

  if(isError){
        return false;
    }else{
     $("#download_reports").submit();
    }

    
}); 
 
    
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

$('.ldap').on("keyup", function() {
  // $("#profile_div").hide();
  return $(this).autocomplete({
    source: "/reports/get-user-name",
    minLength: 2,
    close: function(event) {
    },
    select: function(event, ui) {
      if ($("#ldap").val() !== "") {
        $("#ldap").val(ui.item.id + "-" + ui.item.username);
          window.current_ldap = ui.item.id;
        if(ui.item.manager){
          $("#ldap_manager").text(ui.item.manager);
        }
        else{
          $("#ldap_manager").text('N/A');
        }
        if(ui.item.team){
          $("#ldap_program").text(ui.item.team);
        }
        else{
          $("#ldap_program").text('N/A');
        }
         if(ui.item.region){
          $("#ldap_region").text(ui.item.region);
         }
         else{
          $("#ldap_region").text('N/A');
         }
         if (window.user_id == ui.item.id){
          $("#profile_div").show();
         }
         else{
          $("#profile_div").hide();
         }
        //$("label[for=id_employee]").css("display", "none");

      }
    }
  });
});

function dateLimitToPrevQuarter(){
    month = new Date().getMonth()
    curMonth = month + 1
    if(curMonth < 3){
       return (new Date(new Date().getFullYear(), 0, 1))
    }
    else if (curMonth > 3 && curMonth <= 6){
        return (new Date(new Date().getFullYear(), 3, 1))
    }

    else if(curMonth > 6 && curMonth <= 9){
        return (new Date(new Date().getFullYear(), 6, 1))
    }
    else {
        return (new Date(new Date().getFullYear(), 9, 1))
    }
}
