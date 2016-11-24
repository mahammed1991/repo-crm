var clickedPage = 1;
var pageStartNum = 1;
var pageEndNum = 10;
var defaultStartNum = 1, defaultEndNum = 20, shaffelCount = 10;

var reloadPagination = function(){
  clickedPage = 1;
  pageStartNum = defaultStartNum;
  pageEndNum = defaultEndNum;
}
var formPagination = function(numOfPages){

  var lmt = parseInt($("#limit").val());
  var from = clickedPage * lmt - lmt + 1
  var to = from + lmt-1;
 
  if($("#entries").length){
    $("#entries").html("Showing "+ from +" to "+ to +" of "+ leads_count +" entries");
  }else{
      $("#pagination-container").before("<div id='entries' style='margin-left: 2%;margin-right: 2%;margin-bottom: 10px;float: left;display: inline;margin-top: 2%;'></div>");
      $("#entries").html("Showing "+ from +" to "+ to +" of "+ leads_count +" entries");
  }

  var ulEle = $("#pagination");
  ulEle.html('');
  if(clickedPage < 2)
    ulEle.append("<li><a class='paged' href='#'>»</a></li>");
  else
    ulEle.append("<li><a class='paged' href='#'>«</a></li>");

  for(i=pageStartNum; i<= Math.min(pageEndNum, numOfPages); i++){
      if(clickedPage == i)
        ulEle.append("<li><a class='paged active'href='#' style='background-color: #4CAF50;' data-value=" +i+ ">"+i+"</a></li>");
      else{
        ulEle.append("<li><a class='paged' href='#' data-value=" +i+ ">"+i+"</a></li>");
      }
  }
  if($( '#pagination li a' ).data( 'value' ) )
  if(numOfPages > defaultEndNum){
    $('#pagination li a').hide();
    $('#pagination li a:lt('+defaultEndNum+')').show();
  }
  if(clickedPage == numOfPages)
    ulEle.append("<li><a class='paged' href='#'>«</a></li>");
  else
    ulEle.append("<li><a class='paged ' href='#'>»</a></li>");

}
$("body").on('click', '.paged', function(e){
      e.preventDefault();

      clickedPage = $(this).text();
      var firstPage = parseInt($('#pagination li a:eq(1)' ).data('value' ));
      var lastPage = parseInt($('#pagination li a:eq('+defaultEndNum+')' ).data('value' ));
      var activePage = parseInt($('#pagination li a.active' ).data('value' ));
      var reShuffelPagination = false;
      if(clickedPage === "«" && activePage > 0){
        if(firstPage == 1){
          pageStartNum = defaultStartNum
          pageEndNum = defaultEndNum
          if(activePage == 1)
            clickedPage = activePage
          else
            clickedPage = activePage - 1
        }else{
          pageStartNum -= 1
          pageEndNum -= 1
          clickedPage = activePage - 1;
        }
        reShuffelPagination = true;
      }else if(clickedPage === "»" && activePage < numOfPages){
        if(activePage == numOfPages)
            reShuffelPagination = false;
        else{
          if(numOfPages > defaultEndNum){
             pageStartNum += 1
             pageEndNum += 1
             clickedPage = activePage + 1;
          }
          else{
             pageStartNum = 1
             pageEndNum = numOfPages
             clickedPage = activePage + 1;

          }
         
        }
        reShuffelPagination = true;
        
      }else if(parseInt(clickedPage)) {
        clickedPage = parseInt(clickedPage);
        if(clickedPage == lastPage){
          pageStartNum += shaffelCount;
          pageEndNum += shaffelCount;
        }else if (clickedPage == firstPage){
          if(activePage - shaffelCount > shaffelCount){
            pageStartNum -= shaffelCount;
            pageEndNum -= shaffelCount; 
          }else{
              pageStartNum = defaultStartNum
              pageEndNum = defaultEndNum
          }
        }else{
          clickedPage = clickedPage;
        }
        reShuffelPagination = true;
      }
      
      if(is_agent){
        appointment = $('#appointment').val()
        if(reShuffelPagination){
          if (appointment != 'Select'){
            call_crm_management(true);
          }
          else{
            call_crm_management(false);
          }
        }
      }
      else{
          if(reShuffelPagination){
          LoadTheTableContent(false);
        }
      }
      
      
  });