function showTrendReportOption(){
    var value = $('#filter_report_type').val();
    if (value === 'trend_report_program_wise' || value === 'trends_report_for_win_and_total'){
      $(".program").hide();
      $(".code_types").show();
      $(".c_types").hide();
      showButton();
      showTimeLineOption();
      showProgramOption();
      setTimeLineLable('trend');
    }else{
      showButton();
      showTimeLineOption();
      showProgramOption();
      $(".program").show();
      $(".c_types").show();
      setTimeLineLable('lead');

     }
 }

function setTimeLineLable(type){
  if(type == 'lead'){
    $("#label_timeline").text('Timeline');
  }else{
    $("#label_timeline").text('Trend Duration');
  }
}

function showButton(){
    var value = $('#filter_report_type').val();
    if (value === 'trend_report_program_wise' || value === 'trends_report_for_win_and_total'){
      $("#get_report").hide();
      $("#get_trend_report").show();
    }else{
      $("#get_report").show();
      $("#get_trend_report").hide();
     }
 }


function showTimeLineOption(){
  var value = $('#filter_report_type').val();
  if (value === 'trend_report_program_wise' || value === 'trends_report_for_win_and_total'){
    $("#filter_timeline").hide();
    $("#trend_filter_timeline").show();
    $(".filter_quarterly").hide();
    $(".filter_monthly").hide();
    $(".filter_weekly").hide();
    $(".filter_dateRange").hide();
  }else{
    $("#filter_timeline").show();
    $("#trend_filter_timeline").hide();
   }
}


function showProgramOption(){
  var value = $('#filter_report_type').val();
  if (value === 'trends_report_for_win_and_total'){
        $('.team2').show();
        $('.team').hide();
  }else if (value === 'trend_report_program_wise'){
     $('.team2').hide();
     $('.team').show();   
  }else{
    $('.team2').hide();
  }
}

//  function for hideing trend chart
function hideTrendChart(){
  $('#Program_wise_div').hide();
}

function showTrendChart(){
  $('#Program_wise_div').show();
}


// 
// function for geting trends report
function validateFilters(){
    isError = false;
    if ($('#filter_report_type').val() === 'trend_report_program_wise'){
        var trend_timeline = $('#trend_filter_timeline').val()
        if( trend_timeline==='Quarters' || trend_timeline==='Weeks' || trend_timeline==='Months'){
               $('#Program_wise_div').show();
               $('#chart_div').hide();
        }else{
          isError = true;
          alert('please selsect trends duration');
        }           
    }else if ($('#filter_report_type').val() === 'trends_report_for_win_and_total'){
      var trend_timeline = $('#trend_filter_timeline').val()
        if( trend_timeline==='Quarters' || trend_timeline==='Weeks' || trend_timeline==='Months'){
           $('#Program_wise_div').hide();
           $('#chart_div').show();
        }else{
          isError = true;
          alert('please selsect trends duration');
        }
        if (!$('#filter_team2').val()){
          isError = true;
          alert('please selsect Program for trends report');
        }
                 
    }else{
      alert('please select Trends Report type')
      isError = true;
    }
    if(isError){
      return true;
    }
    return false;
}


$('#get_trend_report').click(function(){
    var trendReportType = $('#filter_report_type').val();
    if (trendReportType === 'trends_report_for_win_and_total'){
      var teams = $('#filter_team2').val();
      teams = [teams]
    }else{
      var teams = $('#filter_team').val();
    }
    var codeTypes = $('#filter_code_types').val();
    var trendTimeLine = $('#trend_filter_timeline').val();
    if(validateFilters()){
      return false;
    }else{
        $('.report_display').hide();
        hideTrendChart();
        showAjaxLoader();

        $.ajax({
          url: "/reports/get-trends-reports",
          data: { timeLine: trendTimeLine, teams : teams, code_types: codeTypes, report_type: trendReportType },
          type: 'GET',
          dataType: "json",
          success: function(data){
            clearReports();
            hideAjaxLoader();
            showTrendChart();
            if (trendReportType === 'trend_report_program_wise'){
              // Hide Lead report Charts
              hideCharts();
              drawChart(data['reports']);
              showTrendReports(data);
            }else{
              drawVisualization(data['reports']);
              showTrendReports(data);
              
            }
            
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



function showAjaxLoader(){
  $(".load_page_overlay").show();
}

function hideAjaxLoader(){
  $(".load_page_overlay").hide();
}

/* Lead Trends Report (Win & Total) For a Programs start here*/


google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawVisualization);

function drawVisualization(reports) {
  
  var data = google.visualization.arrayToDataTable(reports);
  var teams = $('#filter_team2').val();

  var options = {
    chartArea:{left:100,width:"88%",backgroundColor: { stroke: '#C0C0C0',strokeWidth: 1}},
    width: 1330,
    title : 'Lead Trends Report (Wins & Total) For a ' + teams,
    vAxis: { 1:{title: "Leads"},2:{title: "conversion"}},
    vAxes : { 0: { minValue : 0, maxValue: 10 , title:"Number Of Leads"}, 1: { minValue: 0 , maxValue :10,format: '#', title:"Conversion Ratio %" } },
    hAxis: {baselineColor: '#FFFFFF',textStyle: {color: '#000',  fontSize: 9},title:"Trends Report Timeline" },
    seriesType: "bars",
    series: {0:{type :"bars",targetAxisIndex: 0} , 2: {type : "line" , targetAxisIndex : 1}},
    legend: { position: 'top' },
    pointSize: 4
  };

  var chart = new google.visualization.ComboChart(document.getElementById('Program_wise_div'));
  chart.draw(data, options);
}
    
/* Lead Trends Report (Win & Total) For a Programs end here*/

/* Lead Trends Report - Program wise start here*/
 google.setOnLoadCallback(drawChart);
 function drawChart(reports) {
   var data = google.visualization.arrayToDataTable(reports);

   var options = {
     chartArea:{left:100,width:"88%",backgroundColor: { stroke: '#C0C0C0',strokeWidth: 1}},
     width: 1330,
     title: 'Lead Trends Report - Program wise',
     vAxes : { 0: { minValue : 0, maxValue: 10 , title:"Number Of Leads"}},
     hAxis: { baselineColor: '#FFFFFF',textStyle: {color: '#000',  fontSize: 9}, title:"Trends Report Timeline"},
     legend: { position: 'top' },
     pointSize: 2
   };

   var chart = new google.visualization.LineChart(document.getElementById('Program_wise_div'));
   chart.draw(data, options);
 }
/* Lead Trends Report - Program wise end here*/


/* Show Reports Starts here */

function showTrendReports(data){

  var codeTypes = data['codeTypes'];
  var programs = data['teams'];
  var timeLine = data['timeline'];
  var reports = data['tableReports'];
  var report_type = data['reportType'];

  drawTable(reports, timeLine);
  createTableTitle(programs, timeLine);
  $('.report_display').show();

}

function createTableTitle(programs, timeLine){
  var tabHeader = "<b>Trend Reports for Program(s): </b>";
  for(i=0; i<programs.length; i++){
    tabHeader += programs[i] + ", ";
  }
  tabHeader += "<b> Trend Duration: </b>"+ timeLine;
  $(".TrendReportTable").before("<p class='tab-header'>" + tabHeader + "</p>");
}

function drawTable(reports, timeLine) {
   $("#trend_report_display").append("<table class='TrendReportTable' width='100%' cellpadding='0' cellspacing='0' border='1'><thead><tr></tr></thead><tbody></tbody></table>");

   var elem = "";
   for(i=0; i<reports[0].length; i++){
      elem += "<th>" + reports[0][i]+ "</th>";
   }
   $("#trend_report_display thead tr").append(elem);

    for(row=1; row<reports.length; row++){
      colElem = "<tr>";
      for(col=0; col<reports[row].length; col++){
        if(col === 0){
          colElem += "<td width='70px'>" + reports[row][col] + "</td>"
        }else{
          colElem += "<td align='right' width='50px'>" + reports[row][col] + "</td>"
        }
        
      }
      colElem += "</tr>";
      $("#trend_report_display tbody").append(colElem);
    }
}

/* Show Reports Ends here */
