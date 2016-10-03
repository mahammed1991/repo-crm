$(document).ready(function() {
    UncheckAll();
    window.reportType = '';
    window.filters = new Array();
    window.timeline = new Array();
    $(function() {
        $("#datepickerFrom").datepicker({
            defaultDate: "+1w",
            changeMonth: true,
            numberOfMonths: 1,
            dateFormat: "M dd, yy",
            onClose: function(selectedDate) {
                $("#to").datepicker("option", "minDate", selectedDate);
            },
            onSelect: function(selected) {
                var dt = new Date(selected);
                dt.setDate(dt.getDate() + 1);
                $("#datepickerTo").datepicker("option", "minDate", dt);
            }
        });
        $("#datepickerTo").datepicker({
            defaultDate: "+1w",
            changeMonth: true,
            numberOfMonths: 1,
            dateFormat: "M dd, yy",
            onClose: function(selectedDate) {
                $("#from").datepicker("option", "maxDate", selectedDate);
            },
            onSelect: function(selected) {
                var dt = new Date(selected);
                dt.setDate(dt.getDate() - 1);
                $("#datepickerFrom").datepicker("option", "maxDate", dt);
            }
        });


    });

});
function UncheckAll(){ 
    var getinputelements = document.getElementsByTagName('input'); 
    for(var i = 0; i < getinputelements.length; i++){ 
        if(getinputelements[i].type=='checkbox'){ 
        getinputelements[i].checked = false; 
        }
    }
}

$(document).on('click', '.msc19', function() {
    $('#sel_all').prop('checked', false);
    var iim = $(this).attr('id');
    var arr1 = iim.split('-');
    var arr2 = "#" + arr1[1];
    $(arr2).attr('checked', false);
    $(this).parent().remove();
});

$(document).on('click', '.report-type li', function() {
    window.reportType = '';
    window.reportType = $(this).text();
    var thischeck = $(this).find('.mcico');
    $('.mm1 .mcico').css('display', 'none');
    $('.mm1 .report-type li').css('background', '#fff');
    $('.mm1 .report-type li a').css('color', '#474747');
    $(this).css('background', '#1e66c6', 'color', '#fff');
    $(this).find('a').css('color', '#fff');
    $(thischeck).css('display', 'inline-block');

});

$(document).on('click', '.timeline li', function() {
    $('#prev_comp').show();
    window.timeline = []
    window.timeline.push($(this).attr('id'));
    $("#datepickerFrom").val('');
    $("#datepickerTo").val('');
    if ($(this).text() == "Custom Date Range") {
        $('#custome_date').show();
        $('#prev_comp').hide();
    }
    if ($(this).text().indexOf('This') != -1) {
        $('#custome_date').hide();
    }
    var thischeck = $(this).find('.mcico');
    $('.mm2 .mcico').css('display', 'none');
    $('.mm2 .timeline li').css('background', '#fff');
    $('.mm2 .timeline li a').css('color', '#474747');
    $(this).css('background', '#1e66c6', 'color', '#fff');
    $(this).find('a').css('color', '#fff');
    $(thischeck).css('display', 'inline-block');

});

$('#viewButton').on('click', function() {

    var isError = false;
    var data = {}
    if (window.filters.length == 0) {
        isError = true;
        alert("Please Select Any One Filter From Choose Filter Section!")
    } else {
        data['filter'] = window.filters;
    }

    if (window.reportType == '') {
        isError = true;
        alert("Please Choose Report Type Report Section!")
    } else {
        data['report_type'] = window.reportType;
    }

    if (window.timeline.length == 0) {
        isError = true;
        alert("Please Choose Timeline Section!")
    } else {
        if (window.timeline[0] == 'custom_date') {
            data['comparison'] = '';
            $('#comparison').prop('checked', false);
            fromDate = $("#datepickerFrom").val();
            toDate = $("#datepickerTo").val();
            if (fromDate && toDate) {
                data['timeline'] = [fromDate, toDate]
            } else {
                isError = true;
                alert("Please Custome Date Range From Calendar")
            }

        } else {
            data['timeline'] = [window.timeline[0]];
        }
    }

    if ($('#comparison').prop('checked') == true) {
        data['comparison'] = 'yes';
    } else {
        data['comparison'] = '';
    }

    if (isError) {
        alert('Failure!');
        return false;
    } else {
        $('#preloaderOverlay').show();
        $.ajax({
            method: 'GET',
            url: '/reports/csat-reports',
            data: data,
            dataType: "json",
            success: function(data) {
                console.log('Success Response From Ajax');
                $('#preloaderOverlay').hide();
                console.log(data);
                if(data['survey_for_unmapped'] != null){
                    displayUnmappedData(data);
                }else if(data['comparison'] == 'yes'){
                    $('#displaycolor').show();
                    CSATComparisonReport(data);
                }else{
                    $('#displaycolor').hide();
                    displayReportData(data);
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Failure');
            }
        }) 
    }
});

$("input:checkbox").on('click', function() {
    // in the handler, 'this' refers to the box clicked on
    var $box = $(this);
    var se = $(this).attr('id');
    var val1 = $(this).val();

    if ($(this).attr('id') == "sel_all") {
        window.filters = [];
        $('.msc13').prop('checked', false);
        $('.msc18').remove();
        if ($('#sel_all').prop('checked') == true) {
            $('.msc13 ').trigger("click");
        } else {
            $('.msc13 ').attr('checked', false)
            $('.msc18').remove();
        }
    }

    if ($box.is(":checked")) {
        var group = "input:checkbox[name='" + $box.attr("name") + "']";
        $(group).prop("checked", false);
        $box.prop("checked", true);
        customFilter()
    } else {
        $box.prop("checked", false);
        customFilter()
    }

});

function customFilter() {
    window.filters = [];
    window.showFilter = [];
    updateFilter('survey_category');
    updateFilter('survey_channel');
    updateFilter('language');
    updateFilter('process');
    updateFilter('tag_location');
    displayFilters();

}

function updateFilter(name) {
    var group = "input:checkbox[name='" + name + "']";
    $(group).each(function() {
        var grp = $(this).attr('id');
        var val = $(this).val();
        if ($(this).is(":checked")) {
            window.filters.push(grp);
            window.showFilter.push({
                'val': val,
                'id': grp
            });
        }
    });

}

$(document).on('click', '#myselect li', function() {
    customFilter();
});

function displayFilters() {
    $("#myselect li").remove();
    for (i = 0; i < window.showFilter.length; i++) {
        $("#myselect").append('<li class="msc18" >' + window.showFilter[i]['val'] + '<span id="we-' + window.showFilter[i]['id'] + '" class="glyphicon glyphicon-remove msc19"></span></li>');
    }
}

function displayUnmappedData(reportData){
    $('.csatreport').empty();
    header = '<tr >' +
        '<th class="msc23">Channel</th>' +
        '<th class="msc23">No Response</th>' +
        '<th class="msc23">Extremely Satisfied</th>' +
        '<th class="msc23">Moderately Satisfied</th>' +
        '<th class="msc23">Slightly Satisfied</th>' +
        '<th class="msc23">Neither Satisfied/Dissatisfied</th>' +
        '<th class="msc23">Slightly Dissatisfied</th>' +
        '<th class="msc23">Moderately Dissatisfied</th>' +
        '<th class="msc23">Extremely Dissatisfied</th>' +
        '<th class="msc23">Grand Total</th>' +
        '</tr>'
    row = '';
    row += '<tr>' +
        '<td>' + reportData['channel'] + '</td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['No Response'] + '</div><div class="msc21">' + reportData['survey_for_unmapped']['No Response in pcg'] + '%</div></td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['Extremely satisfied'] + '</div><div class="msc21">' + reportData['survey_for_unmapped']['Extremely satisfied in pcg'] + '%</div></td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['Moderately satisfied'] + '</div><div class="msc21">' + reportData['survey_for_unmapped']['Moderately satisfied in pcg'] + '%</div></td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['Slightly satisfied'] + '</div><div class="msc21">' + reportData['survey_for_unmapped']['Slightly satisfied in pcg'] + '%</div></td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['Neither satisfied nor dissatisfied'] + '</div><div class="msc21">' + reportData['survey_for_unmapped']['Neither satisfied nor dissatisfied in pcg'] + '%</div></td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['Slightly dissatisfied'] + '</div><div class="msc21">' + reportData['survey_for_unmapped']['Slightly dissatisfied in pcg'] + '%</div></td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['Moderately dissatisfied'] + '</div><div class="msc21">' + reportData['survey_for_unmapped']['Moderately dissatisfied in pcg'] + '%</div></td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['Extremely dissatisfied'] + '</div><div class="msc21">' + reportData['survey_for_unmapped']['Extremely dissatisfied in pcg'] + '%</div></td>' +
        '<td style="padding: 0px !important;"><div class="msc20">' + reportData['survey_for_unmapped']['Grand Total'] + '</div></td>' +
        ' </tr>'
    $('.csatreport').append(header + row);
}



function displayReportData(reportData) {
    $('.csatreport').empty();

    header = '<tr class="nav-head">' +
        '<th class="msc24 header1" style="width:245px;">' + reportData['report_type'] + '</th>' +
        '<th class="msc24 header14" style="width:55px;">CSAT%</th>' +
        '<th class="msc24 header15" style="width:65px;">vs Target<br>(95%)</th>' +
        '<th class="msc24 header2" style="width:62px;">Process</th>' +
        '<th style="width:56px;"  data-toggle="tooltip" title="Transfer Rate"class="msc24 header3">TR<sup>[?]</sup></th>' +   
        /*'<th class="msc24">Transfer Rate1</th>' +*/
        '<th class="msc24 header4" style="width:56px;">Leads</th>' +
        '<th class="msc24 header5" style="width:59px;">Wins</th>' +
        '<th title="Extremely Satisfied" data-toggle="tooltip" data-placement="top" class="msc24 header6" style="width:45px;">ES<sup>[?]</sup></th>' +
        '<th title="Moderately Satisfied" data-toggle="tooltip" data-placement="top" class="msc24 header7" style="width: 45px;padding: 8px 4px!important;">MS<sup>[?]</sup></th>' +
        '<th title="Slightly Satisfied" class="msc24 header8" style="width:45px;">SS<sup>[?]</sup></th>' +
        '<th title="Neither Satisfied/Dissatisfied" class="msc24 header9" style="width:50px;">NS/D<sup>[?]</sup></th>' +
        '<th title="Slightly Dissatisfied" class="msc24 header10" style="width:41px;">SD<sup>[?]</sup></th>' +
        '<th title="Moderately Dissatisfied" class="msc24 header11" style="width:44px;">MD<sup>[?]</sup></th>' +
        '<th title="Extremely Dissatisfied" class="msc24 header12" style="width:45px;">ED<sup>[?]</sup></th>' +
        '<th title="Grand Total" class="msc23 header13" style="width:52px;">GT<sup>[?]</sup></th>' +
        '</tr>'


    row = '';
    for (i = 0; i < reportData['report_data'].length; i++) {



        total_row = ''
        if(reportData['report_data'][i]['report_type'] == 'Total'){
            console.log(reportData['report_data'][i]['TotalLeads'])
            total_row += '<tr>' +
            '<td class="data1">' + reportData['report_data'][i]['report_type'] + '</td>' +
            '<td class="data2">' + '-' + '</td>' +
            '<td class="data3">' + '-' + '</td>' +
            '<td class="data4">' + reportData['process'] + '</td>' +
            '<td class="data5" style="padding: 10px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalGrand Total'] + 

           '<td class="data6" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalLeads'] + 
            '<td class="data7" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalWins'] + 
            '<td class="data8" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalExtremely satisfied'] + 
            '<td class="data9" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalModerately satisfied'] + 
            '<td class="data10" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalSlightly satisfied'] + 
            '<td class="data11" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalNeither satisfied nor dissatisfied'] + 
            '<td class="data12" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalSlightly dissatisfied'] + 
            '<td class="data13" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalModerately dissatisfied'] + 
            '<td class="data14" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalExtremely dissatisfied'] + 


            '<td id="data15" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['TotalGrand Total'] + 
            ' </tr></div>';
        }else{
        row += '<tr>' +
            '<td class="data1" style="">' + reportData['report_data'][i][reportData['report_type'].toString()] + '</td>' +
            '<td class="data2" style="">' + reportData['report_data'][i]['Extremely satisfied in pcg'] + '%</td>' +
            '<td class="data3" style="">' + (reportData['report_data'][i]['Extremely satisfied in pcg'] - 95).toFixed(2) + '%</td>' +
            '<td class="data4" style="">' + reportData['process'] + '</td>' +
            '<td class="data5" style="" ><div class="msc20">' + reportData['report_data'][i]['Grand Total'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Response Rate in pcg'] + '%</div></td>';
       /* if (reportData['channel'] == 'PHONE' || reportData['channel'] == 'EMAIL') {
            channel = '<td style=""><div class="msc20">' + reportData['report_data'][i]['Transfer Rate'] + '</div><div class="msc21">' + reportData['report_data'][i]['Transfer Rate in pcg'] + '%</div></td>'
        } else {
            channel = '<td style=""><div class="msc20">' + reportData['report_data'][i]['Wins'] + '</div><div class="msc21">100%</div></td>'
        }*/

        row_end = '<td class="data6" style=""><div class="msc20">' + reportData['report_data'][i]['Leads'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Leads in pcg'] + '%</div></td>' +
            '<td class="data7" style=""><div class="msc20">' + reportData['report_data'][i]['Wins'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Wins in pcg'] + '%</div></td>' +
            '<td class="data8" style=""><div class="msc20">' + reportData['report_data'][i]['Extremely satisfied'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Extremely satisfied in pcg'] + '%</div></td>' +
            '<td class="data9" style=""><div class="msc20">' + reportData['report_data'][i]['Moderately satisfied'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Moderately satisfied in pcg'] + '%</div></td>' +
            '<td class="data10" style=""><div class="msc20">' + reportData['report_data'][i]['Slightly satisfied'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Slightly satisfied in pcg'] + '%</div></td>' +
            '<td class="data11" style=""><div class="msc20">' + reportData['report_data'][i]['Neither satisfied nor dissatisfied'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Neither satisfied nor dissatisfied in pcg'] + '%</div></td>' +
            '<td class="data12" style=""><div class="msc20">' + reportData['report_data'][i]['Slightly dissatisfied'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Slightly dissatisfied in pcg'] + '%</div></td>' +
            '<td class="data13" style=""><div class="msc20">' + reportData['report_data'][i]['Moderately dissatisfied'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Moderately dissatisfied in pcg'] + '%</div></td>' +
            '<td class="data14" style=""><div class="msc20">' + reportData['report_data'][i]['Extremely dissatisfied'] + '</div><div class="msc21 previous">' + reportData['report_data'][i]['Extremely dissatisfied in pcg'] + '%</div></td>' +


            '<td class="data15" style=""><div class="msc20">' + reportData['report_data'][i]['Grand Total'] + '</div></td>' +
            ' </tr>'

        row +=  row_end;

    }

    }

    $('.csatreport').append(header + row + total_row);
}

function CSATComparisonReport(reportData) {
    $('.csatreport').empty();

    header = '<tr class="nav-head">' +
        '<th class="msc24 header1" style="width:245px;">' + reportData['report_type'] + '</th>' +
        '<th class="msc24 header2" style="width:62px;">Process</th>' +
        '<th class="msc24 header14" style="width:55px;">CSAT%</th>' +
        '<th class="msc24 header15" style="width:65px;">vs Target<br>(95%)</th>' +
        '<th style="width:56px;"  data-toggle="tooltip" title="Transfer Rate"class="msc24 header3">TR<sup>[?]</sup></th>' +   
        /*'<th class="msc24">Transfer Rate1</th>' +*/
        '<th class="msc24 header4" style="width:56px;">Leads</th>' +
        '<th class="msc24 header5" style="width:59px;">Wins</th>' +
        '<th title="Extremely Satisfied" data-toggle="tooltip" data-placement="top" class="msc24 header6" style="width:45px;">ES<sup>[?]</sup></th>' +
        '<th title="Moderately Satisfied" data-toggle="tooltip" data-placement="top" class="msc24 header7" style="width: 45px;padding: 8px 4px!important;">MS<sup>[?]</sup></th>' +
        '<th title="Slightly Satisfied" class="msc24 header8" style="width:45px;">SS<sup>[?]</sup></th>' +
        '<th title="Neither Satisfied/Dissatisfied" class="msc24 header9" style="width:46px;">NS/D<sup>[?]</sup></th>' +
        '<th title="Slightly Dissatisfied" class="msc24 header10" style="width:41px;">SD<sup>[?]</sup></th>' +
        '<th title="Moderately Dissatisfied" class="msc24 header11" style="width:44px;">MD<sup>[?]</sup></th>' +
        '<th title="Extremely Dissatisfied" class="msc24 header12" style="width:45px;">ED<sup>[?]</sup></th>' +
        '<th title="Grand Total" class="msc23 header13" style="width:52px;">GT<sup>[?]</sup></th>' +
        '</tr>'

    row = '';

    for (i = 0; i < reportData['report_data'].length; i++) {
        row += '<tr>' +
            '<td class="data1" id="comp_report" style="max-width:287px;">' + reportData['report_data'][i][reportData['report_type'].toString()] + '</td>' +
            '<td class="data4" id="comp_report_header">' + reportData['process'] + '</td>' +
            '<td class="data2" style="padding: 0px !important;"><div class="tabletop">' + reportData['report_data'][i]['Extremely satisfied in pcg'] + '%</div><div class="prev">' + reportData['previous_report_data'][i]['Extremely satisfied in pcg'] + '%</div></td>' +
            '<td class="data3" style="padding: 0px !important;"><div class="tabletop">' + (reportData['report_data'][i]['Extremely satisfied in pcg'] - 95).toFixed(2) + '%</div><div class="prev">' + (reportData['previous_report_data'][i]['Extremely satisfied in pcg'] - 95).toFixed(2) + '%</div></td>' +
            '<td class="data5" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Grand Total'] + '</div><div class="msc21">' + reportData['report_data'][i]['Response Rate in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Grand Total'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Response Rate in pcg'] + '%</div></td>';
        /*if (repclass="data1" ortData['channel'] == 'PHONE' || reportData['channel'] == 'EMAIL') {
            channel = '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Transfer Rate'] + '</div><div class="msc21">' + reportData['report_data'][i]['Transfer Rate in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Transfer Rate'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Transfer Rate in pcg'] + '%</div></td>'
        } else {
            channel = '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Wins'] + '</div><div class="msc21">100%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Wins'] + '%</div><div class="msc21 previous">100%</div></td>'
        }*/

        row_end = '<td class="data6" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Leads'] + '</div><div class="msc21">' + reportData['report_data'][i]['Leads in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Leads'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Leads in pcg'] + '%</div></td>' +
            '<td class="data7" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Wins'] + '</div><div class="msc21">' + reportData['report_data'][i]['Wins in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Wins'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Wins in pcg'] + '%</div></td>' +
            '<td class="data8" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Extremely satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Extremely satisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Extremely satisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Extremely satisfied in pcg'] + '%</div></td>' +
            '<td class="data9" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Moderately satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Moderately satisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Moderately satisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Moderately satisfied in pcg'] + '%</div></td>' +
            '<td class="data10" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Slightly satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Slightly satisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Slightly satisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Slightly satisfied in pcg'] + '%</div></td>' +
            '<td class="data11" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Neither satisfied nor dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Neither satisfied nor dissatisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Neither satisfied nor dissatisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Neither satisfied nor dissatisfied in pcg'] + '%</div></td>' +
            '<td class="data12" style="padding: 0px !important; width:32px;"><div class="msc20">' + reportData['report_data'][i]['Slightly dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Slightly dissatisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Slightly dissatisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Slightly dissatisfied in pcg'] + '%</div></td>' +
            '<td class="data13" style="padding: 0px !important; width:32px;"><div class="msc20">' + reportData['report_data'][i]['Moderately dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Moderately dissatisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Moderately dissatisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Moderately dissatisfied in pcg'] + '%</div></td>' +
            '<td class="data14" style="padding: 0px !important; width:32px;"><div class="msc20">' + reportData['report_data'][i]['Extremely dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Extremely dissatisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Extremely dissatisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Extremely dissatisfied in pcg'] + '%</div></td>' +
            '<td class="data15" style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Grand Total'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Grand Total'] + '</div></td>' +

            ' </tr>'

        row +=  row_end;

    }

    $('.csatreport').append(header + row);
    

}



$(window).scroll(function () {
    if( $(window).scrollTop() > 613 && $(window).scrollTop() < 6000){
        $('.nav-head').css('position','fixed');
        $('.nav-head').css('top','61px');
        $('.nav-head').css('background','#CCC');
        $(".data1").css('width','245px');
        $(".data2").css('width','55px');
        $(".data3").css('width','65px');
        $(".data4").css('width','62px');
        $(".data5").css('width','57px');
        $(".data6").css('width','57px');
        $(".data7").css('width','57px');
        $(".data8").css('width','45px');
        $(".data9").css('width','45px');
        $(".data10").css('width','45px');
        $(".data11").css('width','52px');
        $(".data12").css('width','45px');
        $(".data13").css('width','45px');
        $(".data14").css('width','45px');
        $(".data15").css('width','52px');
    }
    else
    {
        $('.nav-head').css('position','relative');
        $('.nav-head').css('top','0');
        $('.nav-head').css('background','none');
    }
  
});


$(document).ready(function () {
    //$("th").tooltip({container:'body'});
        $('[data-toggle="tooltip"]').tooltip();   


});