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


/*=========== Changes in report type ===============*/
$("#filter_wpp_report_type").change(function() {
  //$("#download").prop('disabled', false);
  $(".checkbox_select_all").trigger("click");
  $(".checkbox_select_all").trigger("click");
  $('#wpp_filter_timeline').val('')
  $("#wpp_filter_team_members").hide();
  showFilters();
  var report_type = $(this).val();

  if(report_type == 'leadreport_individualRep'){
    $("#wpp_filter_team_members").hide();
    //$(".checkbox_select_all").trigger("click");
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
          $('#wpp_treatment_lead_status_table').empty()
          reports = data['reports'];
          treatment_type_and_lead_status_analysis_table(reports['treatment_type_header'], reports['wpp_treatment_type_analysis'], reports['wpp_lead_status_analysis'])
          barChartDraw(reports['bar_chart_data'], '', 'barchart');
        },
        error: function(jqXHR, textStatus, errorThrown){
            $('#preloaderOverlay').hide();
        }
    })
}


function treatment_type_and_lead_status_analysis_table(table_header , table_data, total_data){

  var rows = ""
  var lead_status = ""
  var data_row = ""
  var header = "<tr><td> Treatment Type/Lead Status</td>"
  for (ele in table_header){
    header += '<td>'+table_header[ele].replace(/[0-9\.]/g,'')+'</td>'
     }
  header += '</tr>'

  for (data in table_data){
      data_row += '<tr><td>'+data+'</td>'
      for(lead in table_data[data]){
        data_row += '<td>'+table_data[data][lead]+'</td>'
      }
      data_row += "</tr>"
  }

  var values = "<tr><td>Total</td>"
  for(var key in total_data){
        if (key == 'TAT'){

         values += '<td> Avg TAT=' + total_data[key] + '</td>'
        }
        else{
          values += '<td>' + total_data[key] + '</td>'
        }
        
  }
  values += '</tr>'

  $('#wpp_treatment_lead_status_table').append(header+data_row+values)
}
