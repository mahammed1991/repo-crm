$(document).ready(function() {

  $('#dropdown_container_location').hide();
/* ===================== Default Report Starts Here ============= */
  // Get default report while loading template
  callAjax({'report_type': 'default_report', 'report_timeline': ['today']})
/* ===================== Default Report Ends Here ============= */

// date picker
  $(function() {
    $( "#datepickerFrom, #datepickerTo" ).datepicker();
  });
});

/*=========== Changes in report type ===============*/
$("#filter_report_type").change(function() {
  var report_type = $(this).val();
  setDefaultDropdown();
  showFilters();

  if (report_type == 'leadreport_programview'){
    $("#filter_team").show();
    $("#filter_region").hide();
    $("#filter_country").hide();
  }else if (report_type == 'leadreport_regionview'){
    $("#filter_team").hide();
    $("#filter_region").show();
    $("#filter_country").hide();
  }else if(report_type == 'leadreport_individualRep'){
    hideFilters();
    $("#filter_region").show();
  }else if(report_type == 'leadreport_teamLead'){
    hideFilters();
    $("#filter_region").show();
  }

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
$('#filter_region').change(function(){
    $("#filter_country").hide();
    var region = $(this).val();
    if(region){
      //$("#filter_country").show();
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
      var from_date = $("#from").val();
      var to_date = $("#to").val();

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


    if($('#filter_region').is(':visible')){
      var selectedRegion = $('#filter_region').val();

      if(!selectedRegion){
      var errMsg = "Please select Region from dropdown list";
        showErrorMessage(errMsg);
        isError = true;

    }else{
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
    
    // selectedCountries = $("#filter_country:visible").val();
    // if (window.locationFlag){
    //   if(!include(selectedCountries, 'all')){
    //     selectedCountries.push('all');  
    //   }
    //   window.locationFlag = false;
    // }
    dataString['countries'] = selectedCountries;

    var selectedTeam = [];

    if ($("#filter_team:visible")){
      $("#filter_team .checkbox input:checked").each(function(){
          selectedTeam.push($(this).val());
      });  
    }

    // selectedTeam = $("#filter_team:visible").val();
    // if (window.teamFlag){
    //   if(!include(selectedTeam, 'all')){
    //     selectedTeam.push('all');
    //   }
    //   window.teamFlag = false;
    // }
    dataString['team'] = selectedTeam;

     console.log(dataString);

    if(isError){
        return false;
    }else{
      // Ajax call for get reports
      callAjax(dataString);
    }
});


function callAjax(dataString){

  $.ajax({
        url: "/reports/get_new_reports",
        data: dataString,
        type: 'GET',
        dataType: "json",
        success: function(data) {
            console.log(data);
            report = data['reports'];
            window.code_type = data['code_types'];
            window.report_type = data['report_type'];
            showReport(report);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('failure');
        }
      }); 

}



/*========== hide and show filter for changes in report type=========*/
function hideFilters(){
   $('#dropdown_container_region').hide();
   $('#dropdown_container_team').hide();
}

function showFilters(){
   $('#dropdown_container_region').show();
   $('#dropdown_container_team').show();
}

function showErrorMessage(message){
  alert(message);
}

function setDefaultDropdown(){
  $("#filter_region").val('');
  $("#filter_team").val('all');
  //$('#dropdown_container_location').hide();
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

  for( i=0; i<countries.length; i++){
      var id = countries[i]['id'];
      var name = countries[i]['name'];
      //$("#filter_country").append('<option value="'+ id+ '">' + name +'</option>');
      $("#filter_country .checkbox").append('<label><input type="checkbox" value="' + id + '">' + name + '</label>');
  }
  $("#filter_country").show();
}

function showReport(reports){

  console.log(reports);

  if(window.report_type == 'default_report'){
    draw_and_display_table(reports);
  }
  else if(window.report_type == 'leadreport_individualRep'){
    draw_and_display_table(reports);
  }
  else if(window.report_type == 'leadreport_teamLead'){
    draw_and_display_table(reports);
  }
  else if(window.report_type == 'leadreport_programview'){
    clearTables()
    drawColumnChart(reports['lead_status_summary']);
    displayLeadStatusTable(reports['lead_status_summary']);
    drawPieChart(reports['piechart']);
    //drawStatusCodeTypeTable(reports['piechart'], reports['lead_code_type_analysis'])
    newTable(reports['table_header'], reports['lead_code_type_analysis'])
    drawLineChart(reports['week_on_week_details_in_qtd'])
    displayLineChartTable(reports['week_on_week_details_in_qtd'])
  }

   else if(window.report_type == 'leadreport_regionview'){
    clearTables()
    drawColumnChart(reports['lead_status_summary']);
    displayLeadStatusTable(reports['lead_status_summary']);
    drawPieChart(reports['piechart']);
    //drawStatusCodeTypeTable(reports['piechart'], reports['lead_code_type_analysis'])
    newTable(reports['table_header'], reports['lead_code_type_analysis'])
    drawLineChart(reports['week_on_week_details_in_qtd'])
    displayLineChartTable(reports['week_on_week_details_in_qtd'])
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
  console.log(details)

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


/*function drawStatusCodeTypeTable(firstrow, details){

    $("#code_type_table").empty();

    firt_row = '<tr><td>Lead Status/Code Types</td>'
    second_row = '<tr><td>Total Leads</td>'

    for(key in firstrow){
      firt_row += '<td>'+key+'</td>'
      second_row += '<td>'+firstrow[key]+'</td>'
    }

    firt_row += '</tr>';
    second_row += '</tr>';
    var each_row;

    for(i = 0; i < details.length; i++){

        dict_obj = details[i];
        dict_row = '<tr><td>'
        var value_dict;  

        for(key in dict_obj){
          dict_row += key +'</td>'
          value_dict = dict_obj[key]
        }

        for(key in value_dict){
          dict_row += '<td>'+value_dict[key]+'</td>'
          console.log(dict_row)
        }

        dict_row += '</tr>';
        each_row += dict_row;
    }

    console.log(dict_row)
    $("#code_type_table").append(firt_row+second_row+each_row);
}*/

function clearTables(){
  $('#lead_status_table').empty();
  $('#code_type_table').empty();
  $('#line_chart_table').empty();
}

function draw_and_display_table(reports){
    clearTables()
    drawColumnChart(reports['lead_status_summary']);
    displayLeadStatusTable(reports['lead_status_summary']);
    drawPieChart(reports['lead_code_type_analysis']);
    displayCodeTypeTable(reports['lead_code_type_analysis']);
    drawLineChart(reports['week_on_week_details_in_qtd']);
    displayLineChartTable(reports['week_on_week_details_in_qtd']);
}

function newTable(firstrow, details){
  console.log(firstrow);
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

