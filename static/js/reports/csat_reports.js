$(document).ready(function() {
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
                if (data['comparison'] == 'yes') {
                    $('#displaycolor').show();
                    CSATComparisonReport(data);
                } else {
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

function displayFilters() {
    $("#myselect li").remove();
    for (i = 0; i < window.showFilter.length; i++) {
        $("#myselect").append('<li class="msc18" >' + window.showFilter[i]['val'] + '<span id="we-' + window.showFilter[i]['id'] + '" class="glyphicon glyphicon-remove msc19"></span></li>');
    }
}


function displayReportData(reportData) {
    $('.table').empty();
    header = '<tr >' +
        '<th class="msc24">' + reportData['report_type'] + '</th>' +
        '<th class="msc24">CSAT%</th>' +
        '<th class="msc24">vs Target(95%)</th>' +
        '<th class="msc24">Survey Channel</th>' +
        '<th class="msc24">Response Rate</th>' +
        '<th class="msc24">Transfer Rate</th>' +
        '<th class="msc24">Leads</th>' +
        '<th class="msc24">Wins</th>' +
        '<th class="msc24">Extremely Satisfied</th>' +
        '<th class="msc24">Moderately Satisfied</th>' +
        '<th class="msc24">Slightly Satisfied</th>' +
        '<th class="msc24">Neither Satisfied nor Dissatisfied</th>' +
        '<th class="msc24">Slightly Dissatisfied</th>' +
        '<th class="msc24">Moderately Dissatisfied</th>' +
        '<th class="msc24">Extremely Dissatisfied</th>' +
        '<th class="msc23">Grand Total</th>' +
        '</tr>'
    row = '';

    for (i = 0; i < reportData['report_data'].length; i++) {

        row += '<tr>' +
            '<td>' + reportData['report_data'][i][reportData['report_type'].toString()] + '</td>' +
            '<td>' + reportData['report_data'][i]['Extremely satisfied in pcg'] + '</td>' +
            '<td>' + (reportData['report_data'][i]['Extremely satisfied in pcg'] - 95).toFixed(2) + '</td>' +
            '<td>' + reportData['channel'] + '</td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Grand Total'] + '</div><div class="msc21">' + reportData['report_data'][i]['Response Rate in pcg'] + '%</div></td>';
        if (reportData['channel'] == 'PHONE' || reportData['channel'] == 'EMAIL') {
            channel = '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Transfer Rate'] + '</div><div class="msc21">' + reportData['report_data'][i]['Transfer Rate in pcg'] + '%</div></td>'
        } else {
            channel = '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Wins'] + '</div><div class="msc21">100%</div></td>'
        }

        row_end = '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Leads'] + '</div><div class="msc21">' + reportData['report_data'][i]['Leads in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Wins'] + '</div><div class="msc21">' + reportData['report_data'][i]['Wins in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Extremely satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Extremely satisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Moderately satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Moderately satisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Slightly satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Slightly satisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Neither satisfied nor dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Neither satisfied nor dissatisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Slightly dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Slightly dissatisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Moderately dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Moderately dissatisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Extremely dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Extremely dissatisfied in pcg'] + '%</div></td>' +


            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Grand Total'] + '</div><div class="msc21">100%</div></td>' +
            ' </tr>'

        row += channel + row_end;

    }

    $('.table').append(header + row);
}

function CSATComparisonReport(reportData) {
    $('.table').empty();
    header = '<tr >' +
        '<th class="msc24">' + reportData['report_type'] + '</th>' +
        '<th class="msc24">Survey Channel</th>' +
        '<th class="msc24">CSAT%</th>' +
        '<th class="msc24">vs Target(95%)</th>' +
        '<th class="msc24">Response Rate</th>' +
        '<th class="msc24">Transfer Rate</th>' +
        '<th class="msc24">Leads</th>' +
        '<th class="msc24">Wins</th>' +
        '<th class="msc24">Extremely Satisfied</th>' +
        '<th class="msc24">Moderately Satisfied</th>' +
        '<th class="msc24">Slightly Satisfied</th>' +
        '<th class="msc24">Neither Satisfied nor Dissatisfied</th>' +
        '<th class="msc24">Slightly Dissatisfied</th>' +
        '<th class="msc24">Moderately Dissatisfied</th>' +
        '<th class="msc24">Extremely Dissatisfied</th>' +
        '<th class="msc23">Grand Total</th>' +
        '</tr>'
    row = '';

    for (i = 0; i < reportData['report_data'].length; i++) {
        row += '<tr>' +
            '<td>' + reportData['report_data'][i][reportData['report_type'].toString()] + '</td>' +
            '<td>' + reportData['channel'] + '</td>' +
            '<td style="padding: 0px !important;"><div class="tabletop">' + reportData['report_data'][i]['Extremely satisfied in pcg'] + '</div><div class="prev">' + reportData['previous_report_data'][i]['Extremely satisfied in pcg'] + '</div></td>' +
            '<td style="padding: 0px !important;"><div class="tabletop">' + (reportData['report_data'][i]['Extremely satisfied in pcg'] - 95).toFixed(2) + '</div><div class="prev">' + (reportData['previous_report_data'][i]['Extremely satisfied in pcg'] - 95).toFixed(2) + '</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Grand Total'] + '</div><div class="msc21">' + reportData['report_data'][i]['Response Rate in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Grand Total'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Response Rate in pcg'] + '%</div></td>';
        if (reportData['channel'] == 'PHONE' || reportData['channel'] == 'EMAIL') {
            channel = '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Transfer Rate'] + '</div><div class="msc21">' + reportData['report_data'][i]['Transfer Rate in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Transfer Rate'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Transfer Rate in pcg'] + '%</div></td>'
        } else {
            channel = '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Wins'] + '</div><div class="msc21">100%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Wins'] + '%</div><div class="msc21 previous">100%</div></td>'
        }

        row_end = '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Leads'] + '</div><div class="msc21">' + reportData['report_data'][i]['Leads in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Leads'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Leads in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Wins'] + '</div><div class="msc21">' + reportData['report_data'][i]['Wins in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Wins'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Wins in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Extremely satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Extremely satisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Extremely satisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Extremely satisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Moderately satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Moderately satisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Moderately satisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Moderately satisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Slightly satisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Slightly satisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Slightly satisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Slightly satisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Neither satisfied nor dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Neither satisfied nor dissatisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Neither satisfied nor dissatisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Neither satisfied nor dissatisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Slightly dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Slightly dissatisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Slightly dissatisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Slightly dissatisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Moderately dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Moderately dissatisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Moderately dissatisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Moderately dissatisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Extremely dissatisfied'] + '</div><div class="msc21">' + reportData['report_data'][i]['Extremely dissatisfied in pcg'] + '%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Extremely dissatisfied'] + '</div><div class="msc21 previous">' + reportData['previous_report_data'][i]['Extremely dissatisfied in pcg'] + '%</div></td>' +
            '<td style="padding: 0px !important;"><div class="msc20">' + reportData['report_data'][i]['Grand Total'] + '</div><div class="msc21">100%</div><div class="msc20 previous">' + reportData['previous_report_data'][i]['Grand Total'] + '%</div><div class="msc21 previous">100%</div></td>' +

            ' </tr>'

        row += channel + row_end;

    }

    $('.table').append(header + row);
}