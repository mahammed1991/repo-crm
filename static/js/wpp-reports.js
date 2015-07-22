/*========== hide and show filter for changes in report type=========*/
$(document).ready(function() {
  getWppReport({'report_type': 'default_report', 'report_timeline': ['today']})
});

function showFilters(){
  $('#filter_wpp_report_type').show();
  $('#wpp_filter_timeline').show();
}

function showErrorMessage(message){
  alert(message);
}

/*=========== Changes in report type ===============*/
$("#filter_wpp_report_type").change(function() {
  //$("#download").prop('disabled', false);
  $("#wpp_filter_team_members").hide();
  showFilters();
  var report_type = $(this).val();

  if(report_type == 'leadreport_individualRep'){
    $("#wpp_filter_team_members").hide();
    $(".checkbox_select_all").trigger("click");
  }else if(report_type == 'leadreport_teamLead'){
     $("#wpp_filter_team_members").show();
     //$(".checkbox_select_all").trigger("click");
  }
  window.report_type = report_type;

});

/*=================Get Reports by clicking view Reports Button=====================*/
$("#get_wpp_report").click(function(){
  $("#download").prop('disabled', false);
    $('#form_ldap_id').prop("value",window.current_ldap);
    var isError = false;
    var dataString = {}
    var selectedReportType = $("#filter_wpp_report_type").val();
    var selectedTimeline = $("#wpp_filter_timeline").val();
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
    }else{
      dataString['report_timeline'] = [selectedTimeline];
    }

    team_members = [];
    if ($("#wpp_filter_team_members").is(":visible")){
      $("#wpp_filter_team_members label input:checked").each(function(){
        team_members.push($(this).val());
      });  
      if (team_members.length < 1){
          var errMsg = "Please select atleast one member from your team";
          showErrorMessage(errMsg);
          isError = true;
        }  
    }

    dataString['team_members'] = team_members;

     if(isError){
        return false;
    }else{
      // Ajax call for get reports
      getWppReport(dataString);
    }
});

function getWppReport(dataString){
    $('#preloaderOverlay').show();
    $.ajax({
        url: "get-wpp-reports",
        data: dataString,
        type: 'GET',
        dataType: "json",
        success: function(data){
          $('#preloaderOverlay').hide();
          console.log(data)
          $('#wpp_lead_status_table').empty();
          $('#treatment_type_table').empty();
          reports = data['reports'];
          lead_analysis_table(reports['wpp_lead_status_analysis']);
          drawColumnChart(reports['wpp_lead_status_analysis']);
          treatment_type_analysis_table(reports['treatment_type_header'], reports['wpp_treatment_type_analysis']);
          drawPieChart(reports['pie_chart_dict']);
        },
        error: function(jqXHR, textStatus, errorThrown){
            $('#preloaderOverlay').hide();
        }
    })
}


function lead_analysis_table(details){
  var keys = "<tr>"
  var values = "<tr>"
  for(var key in details){
         keys += '<td class="lbl">' + key + '</td>'
         values += '<td class="value">' + details[key] + '</td>'
  }
  keys += '</tr>'
  values += '</tr>'
  $("#wpp_lead_status_table").append(keys+values);

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

    colors = ['#666', '#e57368', '#9933FF', '#acacac', 'orange', '#f6b300', '#77a7fb', '#99CC00', '#34b67a', '#BEC98F', 'purple', '#FF33CC']

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

  var pieChart_datatable = [['Treatment Types', 'Leads per Treatment Type']];

  for(var key in details) pieChart_datatable.push([key, details[key]]);

  pieChartDraw(pieChart_datatable, '', 'piechart')
}

//treatment_type_table
function treatment_type_analysis_table(table_header , table_data){
  var rows = ""
  var lead_status = ""
  var data_row = ""
  var header = "<tr><td> Treatment Type/Lead Status</td>"
  for (ele in table_header){
    header += '<td>'+table_header[ele]+'</td>'
     }
  header += '</tr>'

  for (data in table_data){
      data_row += '<tr><td>'+data+'</td>'
      console.log(table_data[data])
      for(lead in table_data[data]){
        data_row += '<td>'+table_data[data][lead]+'</td>'
      }
      data_row += "</tr>"
  }

  $('#treatment_type_table').append(header+data_row)
}