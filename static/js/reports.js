$(document).ready(function() {
/* ===================== Date Picker function Starts Here ============= */
  $(function() {
    $("#from").datepicker({
      defaultDate : "+1w",
      changeMonth : true,
      numberOfMonths : 1,
      dateFormat: "M dd, yy",
      onClose : function(selectedDate) {
        $("#to").datepicker("option", "minDate", selectedDate);
      }
    });
    $("#to").datepicker({
      defaultDate : "+1w",
      changeMonth : true,
      numberOfMonths : 1,
      dateFormat: "M dd, yy",
      onClose : function(selectedDate) {
        $("#from").datepicker("option", "maxDate", selectedDate);
      }
    });
  });
/* ===================== Date Picker function Ends Here ============= */
  hideCharts();
});

// Dropdown box select
$("#filter_timeline").change(function(){
  $("#filter_quarterly, #filter_monthly, #filter_weekly, #dateRange").hide();
  $("").hide();

  var timeline_name = $(this).val();
  $('#filter_'+timeline_name).show();
})

function include(arr, obj) {
    for(var i=0; i<arr.length; i++) {
        if (arr[i] == obj) {return true;}
    }
}

$("#filter_timeline").change(function() {
    $(".popup_select").hide();
    $("#filter_dateRange").hide();
    var value = $(this).val();
    $(".filter_" + value).show();
  });


// List of Reports filter
$("#filter_report_type").change(function() {
    var value = $(this).val();
    hideAllFilters();
    // show stage filter for TAT
    if(value == 'leadreport_quarter'){
        showTrendReportOption();
        setDefaultDropdown();
        setDefaultCheckbox();
    }else if(value == 'leadreport_program'){
      $(".team").show();
      $("#filter_team").val('all');
      $('.program').show();
      setDefaultCheckbox();
      showTrendReportOption();
    }else if(value == 'leadreport_location'){
      $(".location").show();
      $("#filter_location").val('all');
      $('.loc').show();
      setDefaultCheckbox();
      showTrendReportOption();
    }else if(value == 'leadreport_custome'){
      showAllFilters();
      setDefaultCheckbox();
      showTrendReportOption();
    }else if(value === 'trend_report_program_wise' || value === 'trends_report_for_win_and_total'){
      showTrendReportOption();
    }
  });

function showAllFilters(){
  $(".team").show();
  $(".location").show();
  $(".lead_status").show();
  $(".code_types").show();
  $(".check_box").show();

  setDefaultDropdown();

  $("#program_split").attr('checked', false);
  $("#loc_split").attr('checked', false);
}

function hideAllFilters(){
  $(".team").hide();
  $(".location").hide();
  $(".lead_status").hide();
  $(".code_types").hide();
  $(".check_box").hide();

  setDefaultDropdown();
}

function setDefaultDropdown(){
  $("#filter_team").val('all');
  $("#filter_location").val('all');
  $("#filter_lead_status").val('all');
  $("#filter_code_types").val('all');
}

function setDefaultCheckbox(){
  $("#program_split").attr('checked', false);
  $("#loc_split").attr('checked', false);

  // By default Lead and Code types reports should be split wise
  $("#lead_split").attr('checked', true);
  $("#code_split").attr('checked', true);
}

function clearReports(){
  // Clear all report tables
  $(".TrendReportTable").remove();
  $(".tab-header, .main-header").remove();
  $(".error-empty").remove();
  $(".ReportTable").remove();
  $(".tab-header, .main-header").remove();
  $(".tab-italic, .main-italic").remove();
  $(".mainTable").remove();
  $(".error-empty").remove();
}

function hideReports(){
  // Hide all report tables, Before progress blast
  $(".ReportTable").hide();
  $(".tab-header").hide();
  $(".tab-italic").hide();

  // Show Main Report table
  $(".mainTable").show();
  $(".main-header").show();
  $(".main-italic").show();
}

function showReports(){
  // Show all report tables, After progress blast
  $(".ReportTable").show();
  $(".tab-header").show();
  $(".tab-italic").show();

  // Hide main report table
  $(".mainTable").hide();
  $(".main-header").hide();
  $(".main-italic").hide();

  $("table tbody tr:even").css("background-color", "#ffffff");
  $("table tbody tr:odd").css("background-color", "#ededed");
}

function hideCharts(){
  $("#reports").hide();
  $('.note').hide();
}

function showCharts(){
  $("#reports").show();
  $('.note').show();
}

// Click on Go Button
// Get Reports and show
$("#get_report").click(function(){
    var isError = false;
    var selectedTimeline = $("#filter_timeline").val();
    var dataString = {}

    // Get report type details
    var selectedReportType = $("#filter_report_type").val();
    if(!selectedReportType){
        var errMsg = "Please select report type";
          showErrorMessage(errMsg);
          isError = true;
    }else if(selectedReportType == 'leadreport_quarter'){
        dataString['report_type'] = 'lead_report';
    }

    if(!selectedTimeline){
        var errMsg = "Please choose timeline";
        showErrorMessage(errMsg);
        isError = true;
    }

    // Get timeline details
    if(selectedTimeline == 'quarterly'){
      if(!$("#filter_quarterly").val()){
        var errMsg = "Please select quarter from dropdown list";
        showErrorMessage(errMsg);
        isError = true;
      }
      dataString['quarterly'] = $("#filter_quarterly").val();
    }
    else if(selectedTimeline == 'monthly'){
      if(!$("#filter_monthly").val()){
        var errMsg = "Please select month from dropdown list";
        showErrorMessage(errMsg);
        isError = true;
      }
      dataString['monthly'] = $("#filter_monthly").val();
    }
    else if (selectedTimeline == 'weekly'){
      // Validate week
      if(!$("#filter_weekly").val()){
        var errMsg = "Please select week from dropdown list";
        showErrorMessage(errMsg);
        isError = true;
      }
      dataString['weekly'] = $("#filter_weekly").val();
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

      dataString['date_range'] = [from_date, to_date];
    }

    // Get location and team details
    var selectedLocations = [];
    selectedLocations = $("#filter_location:visible").val();
    if (window.locationFlag){
      if(!include(selectedLocations, 'all')){
        selectedLocations.push('all');  
      }
      window.locationFlag = false;
    }
    dataString['location'] = selectedLocations;

    var selectedTeam = [];
    selectedTeam = $("#filter_team:visible").val();
    if (window.teamFlag){
      if(!include(selectedTeam, 'all')){
        selectedTeam.push('all');
      }
      window.teamFlag = false;
    }
    dataString['team'] = selectedTeam;

    // Get Lead status and code type details
    if($("#filter_lead_status").is(':visible')){
        dataString['lead_status'] = $("#filter_lead_status").val();  
    }else{
      dataString['lead_status'] = ['all'];
    }
    
    if($("#filter_code_types").is(':visible')){
        dataString['code_types'] = $("#filter_code_types").val();  
    }else{
      dataString['code_types'] = ['all'];
    }
    
    dataString['team_split'] = $(".program_filter:visible:checked").val();
    dataString['location_split'] = $(".location_filter:visible:checked").val();
    dataString['status_split'] = $(".status_filter:checked").val();
    dataString['code_split'] = $(".code_filter:checked").val();
    
    // Get report type location/team wise report
    if($(".report_filter").is(":visible")){
       var report_filter = $(".report_filter:checked").val();
       if(selectedLocations.length == 1 && 'all' in selectedLocations && selectedTeams.length == 1 && 'all' in selectedTeams){
          if(!report_filter){
            var errMsg = "Please select type of report team/location wise";
            showErrorMessage(errMsg);
            isError = true;
         }
        }
    }else{
      report_filter = 'none';
    }
    dataString['report_filter'] = report_filter;
    console.log(dataString);
    if(isError){
        return false;
    }else{
      showAjaxLoader();
      // Ajax call for get reports
      $.ajax({
        url: "/reports/get-reports",
        data: dataString,
        type: 'GET',
        dataType: "json",
        success: function(data) {
          hideTrendChart();
          hideAjaxLoader();
          console.log(data);
          // Clear all tables with data
          clearReports();
          if(data['report_summary'] != ''){
            showReportSummary(data);
            showCharts();
          }else{
            hideCharts();
            //showMessage();
          }
          displayReports(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          hideAjaxLoader();
          if(textStatus == 'parsererror'){
            // User Session out, Redirect to login page
            alert("Session out, Please login");
            window.location.reload();
            return console.log(textStatus, errorThrown);
          }else if(textStatus == 'error'){
            // Report error, show error message
            hideCharts();
            clearReports();
            $("#report_display").append('<div class="error-empty">Oops! Something went wrong.</div>');
            return console.log(textStatus, errorThrown);
          }else{
            return console.log(textStatus, errorThrown);
          }
        }
      }); 
    }
});

function displayReports(data){

    // Report initial Data
    var reports = data['reports'];
    var start_date = data['start_date'];
    var end_date = data['end_date'];
    var report_filter = data['report_filter'];
    var timeline = data['timeline'];
    var report_type = data['report_type'];
    var stage = data['stage'];

    // Set Global values
    window.report_stage = stage;
    window.code_types = data['code_types'];
    window.lead_status = data['lead_status'];
    window.locations = data['locations'];
    window.teams = data['teams'];
    if(window.teams.indexOf('')){
      window.teams[window.teams.indexOf('')] = 'Other'
    }
    window.year = data['year'];
    window.month = data['month'];
    window.report_filter = report_filter;
    window.standerd_leads = data['leads'];
    window.status_split = data['status_split'];
    window.code_split = data['code_split'];

    // Display Leads report tables
    if (report_filter == 'normal'){
        // Leads Tables
        var tabId = "leadTable-0";
        createTableWithHeader(tabId);
        createTableBody(tabId, reports[0], timeline);
        createHeading(tabId, timeline, start_date, end_date, reports[0]);
    }else{
        // Leads Tables
        for(locIndx=0; locIndx<reports.length; locIndx++){
          var tabId = "leadTable-"+locIndx;
          var locationReport = reports[locIndx];
          createTableWithHeader(tabId);
          createTableBody(tabId, locationReport, timeline);
          createHeading(tabId, timeline, start_date, end_date, locationReport);
        }
    }
    $("table tbody tr:even").css("background-color", "#ffffff");
    $("table tbody tr:odd").css("background-color", "#ededed");
    $("#report_title").html(createChartTitle(timeline, start_date, end_date));
}

/* ##################### Leads Reports Starts ###################################### */
function createTableWithHeader(tabId){
    // Create table with header/tbody  
    $("#report_display").append("<table class='ReportTable' width='100%' cellpadding='0' cellspacing='0' border='1'><thead><tr></tr></thead><tbody></tbody></table>");
    $("#report_display table:last").attr("id", tabId)
    $("#report_display table:last").addClass(tabId.split('-')[0])
    tableHead = $("#" +tabId+ " thead tr");
    tableHead.append("<th>Lead Status</th>");  
    if(window.code_split){
        for(indx=0; indx<window.code_types.length; indx++){
          tableHead.append("<th>" + code_types[indx] + "</th>");
        }  
    }
    tableHead.append("<th> Total </th>");
}

function createTableBody(tabId, report, timeline){
    // create table body/tbody
    tableBody = $("#" +tabId+ " tbody");

    reports = report['report'];
    total = report['total'];
    if(reports.length){
      for(i=0; i<reports.length; i++){
        if(i==0){
            var collums = window.code_types.length + 2;
            var elem = "<tr><td class='row-header' colspan='" + collums + "'>Number of Leads</td></tr><tr>";
            if(window.lead_status.indexOf('Implemented') == -1){
              var rowSpan = window.lead_status.length + 5;  
            }else{
              var rowSpan = window.lead_status.length + 6;
            }

            if(!window.status_split){
              rowSpan = rowSpan - window.lead_status.length;
              var lStatus = [];
            }else{
              var lStatus = window.lead_status;
            }
            if(!window.code_split){
              var cTypes = [];
            }else{
              var cTypes = window.code_types;
            }
        }
        else{
          if(reports[i]['lead_status_name'] == 'TAT (First Contact Made)' || reports[i]['lead_status_name'] == 'TAT (Implemented)'){
            elem = "<tr class='row-tat'>";
          }else{
            elem = "<tr>";  
          }
        }
        if(lStatus.length && cTypes.length){
            if(reports[i]['lead_status_name'] == 'Dead Lead'){
                elem += "<td>Dead</td>";  
            }
            else{
                elem += "<td>" + reports[i]['lead_status_name'] + "</td>";
            }

            // If code_split not selected
            for(codeIndx=0; codeIndx<window.code_types.length; codeIndx++){
              var code_type = window.code_types[codeIndx];
              if (reports[i]['lead_status_name'] == 'Conversion Ratio'){
                elem += "<td>" + reports[i][code_type] + "%</td>" 
              }else{
                elem += "<td>" + reports[i][code_type] + "</td>"
              }
            }

            if (reports[i]['lead_status_name'] == 'Conversion Ratio'){
              elem += "<td>" +reports[i]['total']+ "%</td></tr>"
            }else{
              if(reports[i]['lead_status_name'] == 'Total'){
                elem += "<td>" +reports[i]['total']+ "</td></tr><tr><td class='row-header' colspan='" + collums + "'>Average Turn Around Time in days</td></tr>"
              }else if(reports[i]['lead_status_name'] == 'TAT (Implemented)'){
                elem += "<td>" +reports[i]['total']+ "</td></tr><tr><td class='row-header' colspan='" + collums + "'>Missed Appointments <span class='hint'>(This data is being tracked from Sep 1, 2014)</span></td></tr>" 
              }else if(reports[i]['lead_status_name'] == 'Regalix Missed appointments'){
                elem += "<td>" +reports[i]['total']+ "</td></tr><tr><td class='row-header' colspan='" + collums + "'>Number of Calls</td></tr>" 
              }else{
                elem += "<td>" +reports[i]['total']+ "</td>"
              }
            }

            tableBody.append(elem);
        }else if(lStatus.length && !cTypes.length){
          if(reports[i]['lead_status_name'] == 'Dead Lead'){
                elem += "<td>Dead</td>";  
            }else{
                elem += "<td>" + reports[i]['lead_status_name'] + "</td>";
            }

            if (reports[i]['lead_status_name'] == 'Conversion Ratio'){
              elem += "<td>" +reports[i]['total']+ "%</td></tr>"
            }else{
              if(reports[i]['lead_status_name'] == 'Total'){
                elem += "<td>" +reports[i]['total']+ "</td></tr><tr><td class='row-header' colspan='" + collums + "'>Average Turn Around Time in days</td></tr>"
              }else if(reports[i]['lead_status_name'] == 'TAT (Implemented)'){
                elem += "<td>" +reports[i]['total']+ "</td></tr><tr><td class='row-header' colspan='" + collums + "'>Missed Appointments <span class='hint'>(This data is being tracked from Sep 1, 2014)</span></td></tr>" 
              }else if(reports[i]['lead_status_name'] == 'Number of Calls'){
                elem += "<td>" +reports[i]['total']+ "</td></tr><tr><td class='row-header' colspan='" + collums + "'>Number of Calls</td></tr>" 
              }else{
                elem += "<td>" +reports[i]['total']+ "</td></tr>"  
              }
            }
            tableBody.append(elem);
        }else if(cTypes.length && !lStatus.length){
          if(i == reports.length - 6){
            elem += "<td class='row-header' colspan='" + collums + "'>Number of Leads</td></tr><tr><td>Total</td>";  
            // If status_split not selected
            for(codeIndx=0; codeIndx<window.code_types.length; codeIndx++){
                var code_type = window.code_types[codeIndx];
                elem += "<td>" + reports[i][code_type] + "</td>"
              }
            elem += "<td>" +reports[i]['total']+ "</td></tr><tr><td class='row-header' colspan='" + collums + "'>Average Turn Around Time in days</td></tr>"
            tableBody.append(elem);
          }else if(i == reports.length - 5){
            elem += "<td>TAT (First Contact Made)</td>";
            // If status_split not selected
            for(codeIndx=0; codeIndx<window.code_types.length; codeIndx++){
                var code_type = window.code_types[codeIndx];
                elem += "<td>" + reports[i][code_type] + "</td>"
              }
            elem += "<td>" +reports[i]['total']+ "</td></tr>"
            tableBody.append(elem);
          }else if(i == reports.length - 4){
             elem += "<td>TAT (Implemented)</td>";
            // If status_split not selected
            for(codeIndx=0; codeIndx<window.code_types.length; codeIndx++){
                var code_type = window.code_types[codeIndx];
                elem += "<td>" + reports[i][code_type] + "</td>"
              }
            elem += "<td>" +reports[i]['total']+ "</td></tr>"
            tableBody.append(elem);
          }else if(i == reports.length - 3){
             elem += "<td class='row-header' colspan='" + collums + "'>Missed Appointments <span class='hint'>(This data is being tracked from Sep 1, 2014)</span></td></tr><tr><td>" + reports[i]['lead_status_name']+ "</td>";
            // If status_split not selected
            for(codeIndx=0; codeIndx<window.code_types.length; codeIndx++){
                var code_type = window.code_types[codeIndx];
                elem += "<td>" + reports[i][code_type] + "</td>"
              }
            elem += "<td>" +reports[i]['total']+ "</td></tr>"
            tableBody.append(elem);
          }else if(i == reports.length - 2){
             elem += "<td>" + reports[i]['lead_status_name'] + "</td>";
            // If status_split not selected
            for(codeIndx=0; codeIndx<window.code_types.length; codeIndx++){
                var code_type = window.code_types[codeIndx];
                elem += "<td>" + reports[i][code_type] + "</td>"
              }
            elem += "<td>" +reports[i]['total']+ "</td></tr>"
            tableBody.append(elem);
          }else if(i == reports.length - 1){
            elem += "<td class='row-header' colspan='" + collums + "'>Number of Calls</td></tr><tr><td>" + reports[i]['lead_status_name']+ "</td>";
            // If status_split not selected
            for(codeIndx=0; codeIndx<window.code_types.length; codeIndx++){
                var code_type = window.code_types[codeIndx];
                elem += "<td>" + reports[i][code_type] + "</td>"
              }
            elem += "<td>" +reports[i]['total']+ "</td></tr>"
            tableBody.append(elem);
          }
        }else{
          if(i == reports.length - 6){
            elem = "<tr><td class='row-header' colspan='" + collums + "'>Number of Leads</td></tr><tr><td>Total</td><td>"+ total['total']+"</td></tr><tr><td class='row-header' colspan='" + collums + "'>Average Turn Around Time in days</td></tr>";
            tableBody.append(elem);
          }
          if(i == reports.length - 5){
              elem += "<tr><td>TAT (First Contact Made)</td><td>"+ reports[i]['total']+"</td></tr>";  
            tableBody.append(elem);
          }
          if(i == reports.length - 4){
             elem += "<tr><td>TAT (Implemented)</td><td>"+ reports[i]['total']+"</td></tr>";
            tableBody.append(elem);
          }
          if(i == reports.length - 3){
            elem += "<tr><td class='row-header' colspan='" + collums + "'>Missed Appointments <span class='hint'>(This data is being tracked from Sep 1, 2014)</span></td></tr><tr><td>" + reports[i]['lead_status_name']+ "</td><td>"+ reports[i]['total']+"</td></tr>";
            tableBody.append(elem);
          }
          if(i == reports.length - 2){
            elem += "<tr><td>" + reports[i]['lead_status_name']+ "</td><td>"+ reports[i]['total']+"</td></tr>";
            tableBody.append(elem);
          }
          if(i == reports.length - 1){
            elem += "<tr><td class='row-header' colspan='" + collums + "'>Number of Calls</td></tr><tr><td>" + reports[i]['lead_status_name']+ "</td><td>"+ reports[i]['total']+"</td></tr>";
            tableBody.append(elem);
          }
        }
        }
    }else{
      var collSpan = window.code_types.length + 2;
          tableBody.append("<tr><td colspan='"+ collSpan + "'> Oops! there are no leads for the selected reports</td></tr>")
    }
}

function createHeading(tabId, timeline, start_date, end_date, name){

    if(window.report_filter == 'normal'){
      msg = createChartTitle(timeline, start_date, end_date)
      $("#"+ tabId).before("<p class='tab-header'></p>");
      $("#"+ tabId).prev('.tab-header').html(msg);
    }else{
      var msg = "<b>Lead report for </b>";
      if(start_date && end_date){
        var duration = getDuration(timeline, start_date, end_date);
        var lc = "";
        var tm = "";
          report = name;
          if ('location' in report){
              if(typeof(report['location']) == 'object'){
                lc += getLocationName(report['location']);
              }else{
                lc += "<b>Location(s):</b> ";
                lc += report['location'] + ', ';
              }
            }
            if('team' in report){
              if(typeof(report['team']) == 'object'){
                tm += getTeamsName(report['team']);
              }else{
                tm += "<b>Program(s):</b> ";
                tm += report['team'] + ', ';
              }
          }
        if(tm && lc){
          msg += tm + " " + lc + " <b>Duration:</b> "+ duration
        }else if(tm){
          msg += tm + " <b>Duration:</b> "+ duration
        }else if(lc){
          msg += lc + " <b>Duration:</b> "+ duration
        }else{
          msg += "<b>Duration:</b> "+ duration
        }
      }
      $("#"+ tabId).before("<p class='tab-header'></p>");
      $("#"+ tabId).prev('.tab-header').html(msg);

    }
  }

/* ##################### Leads Reports Ends ###################################### */

function showErrorMessage(message){
  alert(message);
}

function getDuration(timeline, start_date, end_date){
  var fromMon = start_date.split('/')[0];
  var fromDay = start_date.split('/')[1];
  var fromYear = start_date.split('/')[2];

  var toMon = end_date.split('/')[0];
  var toDay = end_date.split('/')[1];
  var toYear = end_date.split('/')[2];
  if(timeline['monthly']){
          var duration = $('#filter_monthly option:selected').text();
    }else if(timeline['weekly']){
        var duration = $('#filter_weekly option:selected').text();
    }else if(timeline['quarterly']){
        var duration = $('#filter_quarterly option:selected').text();
    }else{
      var duration = fromMon + " " + fromDay + ", " + fromYear + " to " + toMon + " " + toDay + ", " + toYear;
    }
    return duration;
}

function createChartTitle(timeline, start_date, end_date){
  return "<b>Lead report for </b> " + getTeamsName(window.teams) + " " + getLocationName(window.locations) + " <b>Duration:</b> " +  getDuration(timeline, start_date, end_date)
}

function getTeamsName(tem){
  var teamName = "";
  if(tem.length){
    var teamName = "<b>Program(s):</b> ";
    for(t=0; t<tem.length; t++){
      teamName += teams[t] + ', ';
    }  
  }
  return teamName;
}

function getLocationName(loc){
  var locName = "";
  if(loc.length){
    var locName = "<b>Location(s):</b> ";
    for(t=0; t<loc.length; t++){
      locName += loc[t] + ', ';
    }  
  }
  return locName;
}

function showMessage(){
  $("#report_display").append('<div class="error-empty">There are NO leads for the selected report criteria.</div>');
}

function showAjaxLoader(){
  $(".load_page_overlay").show();
}

function hideAjaxLoader(){
  $(".load_page_overlay").hide();
}

