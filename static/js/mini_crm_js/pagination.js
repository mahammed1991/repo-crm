// Set the default values to clickedPage, pageStartNum, pageEndNum
var clickedPage = 1;
var pageStartNum = 1;
var pageEndNum = 10;
var defaultStartNum = 1, defaultEndNum = 20, shuffleCount = 10;

// Call reloadPagination on every on event change like Process, result count, status, appointment, selecting page num
var reloadPagination = function(){
    clickedPage = 1;
    pageStartNum = defaultStartNum;
    pageEndNum = defaultEndNum;
}

// Form pagination according to above event changes
var formPagination = function(numOfPages){

    var lmt = parseInt($("#limit").val());
    var from = clickedPage * lmt - lmt + 1
    var to = from + lmt-1;
    var ulEle = $("#pagination");
    ulEle.html('');
    
    // Set Text to show the total No of entries and current range
    if($("#entries").length) $("#entries").html("Showing "+ from +" to "+ to +" of "+ leads_count +" entries");
    else{
      $("#pagination-container").before("<div id='entries' style='margin-left: 2%;margin-right: 2%;margin-bottom: 10px;float: left;display: inline;margin-top: 2%;'></div>");
      $("#entries").html("Showing "+ from +" to "+ to +" of "+ leads_count +" entries");
    }
    /* if the click is on 1st page out of total numOfPages then replace backward arrow to forward 
    arrow else keep the backward arrow as it is */
    if(clickedPage < 2) ulEle.append("<li><a class='paged' href='#'>»</a></li>");
    else ulEle.append("<li><a class='paged' href='#'>«</a></li>");

    //set the pagination numbers according to pageStartNum, pageEndNum, clickedPage and numOfPages
    for(i=pageStartNum; i<= Math.min(pageEndNum, numOfPages); i++){
        if(clickedPage == i) ulEle.append("<li><a class='paged active'href='#' style='background-color: #4CAF50;' data-value=" +i+ ">"+i+"</a></li>");
        else ulEle.append("<li><a class='paged' href='#' data-value=" +i+ ">"+i+"</a></li>");
    }
    // Take all page No. but show only default No. of pages
    if($('#pagination li a').data('value')){
        if(numOfPages > defaultEndNum){
            $('#pagination li a').hide();
            $('#pagination li a:lt('+defaultEndNum+')').show();
        }
    }

    // if the click is on Last page out of total numOfPages then replace forward arrow to backward arrow 
    // else keep the forward arrow as it is
    if(clickedPage == numOfPages) ulEle.append("<li><a class='paged' href='#'>«</a></li>");
    else ulEle.append("<li><a class='paged ' href='#'>»</a></li>");
}

// calling this on every page click
$("body").on('click', '.paged', function(e){
    e.preventDefault();
    clickedPage = $(this).text();
    // get firstPage, lastPage and activePage from the pagination formed
    var firstPage = parseInt($('#pagination li a:eq(1)' ).data('value' ));
    var lastPage = parseInt($('#pagination li a:eq('+defaultEndNum+')' ).data('value' ));
    var activePage = parseInt($('#pagination li a.active' ).data('value' ));
    var reShufflePagination = false;

    if(clickedPage === "«" && activePage > 0){
        // if the click is on forward arrow decrease the pageStartNum and PageEndNum by 1
        if(firstPage == 1){
            pageStartNum = defaultStartNum;
            pageEndNum = defaultEndNum;
            if(activePage == 1) clickedPage = activePage;
            else clickedPage = activePage - 1;
        }else{
            pageStartNum -= 1;
            pageEndNum -= 1;
            clickedPage = activePage - 1;
        }
        reShufflePagination = true;
    }else if(clickedPage === "»" && activePage < numOfPages){
        if(activePage == numOfPages) reShufflePagination = false;
        else{
            // if click is on forward arrow increase the pageStartNum and PageEndNum by 1 if numOfPages > defaultEndNum
            if(numOfPages > defaultEndNum){
                pageStartNum += 1
                pageEndNum += 1
                clickedPage = activePage + 1;
            }else{
                pageStartNum = 1
                pageEndNum = numOfPages
                clickedPage = activePage + 1;
            }
        }
        reShufflePagination = true;
    }else if(parseInt(clickedPage)){
        clickedPage = parseInt(clickedPage);
        //if the click on lastPage then set pageStartNum to pageStartNum + shuffleCount
        if(clickedPage == lastPage){
            pageStartNum += shuffleCount;
            pageEndNum += shuffleCount;
        }else if (clickedPage == firstPage){
            //if the click on firstPage then set pageStartNum to pageStartNum-shuffleCount
            if(activePage - shuffleCount > shuffleCount){
                pageStartNum -= shuffleCount;
                pageEndNum -= shuffleCount;
            }else{
                pageStartNum = defaultStartNum
                pageEndNum = defaultEndNum
            }
        }else clickedPage = clickedPage;

        reShufflePagination = true;
    }
      
    if(is_agent){
        appointment = $('#appointment').val()
        if(reShufflePagination){
          if (appointment != 'Select') call_crm_management(true);
          else call_crm_management(false);
        }
    }else{
          if(reShufflePagination) LoadTheTableContent(false);
    }
});