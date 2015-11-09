 $(document).ready(function(){
        $(".jquery-filterable-filter").hide()
        $("#form-filter").show()
        /* sorting function start here*/
        $("#Leads").tablesorter({ 
          // pass the headers argument and assing a object 
          headers: { 
              // assign the secound column (we start counting zero) 
              0: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              }, 
              1: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              }, 
              2: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              },
              4: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              }, 
              6: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              },
              
             
          } 
    })

 $('#all').click(function(){
      showAll();
    })
 $('#InQueue').click(function(){
      hideAll();
      $('.inqueue').show(); 
    })
 $('#Audited').click(function(){
      hideAll();
      $('.audited').show(); 
    })
 $('#AlreadyResponsive').click(function(){
      hideAll();
      $('.alreadyresponsive').show(); 
    })
 $('#Delivered').click(function(){
      hideAll();
      $('.delivered').show(); 
    })
 function showAll(){
      $('.inqueue').show()
      $('.audited').show()
      $('.alreadyresponsive').show()
      $('.delivered').show()
  }

 function hideAll(){
      $('.inqueue').hide()
      $('.audited').hide()
      $('.alreadyresponsive').hide()
      $('.delivered').hide()
  }

$("#statusHeader").click(function(){

      $('#sortBy').text($("#statusHeader").text());
      $("#StatusRow").trigger("click");
      
   })

   $("#CodeTypeHeader").click(function(){
      $('#sortBy').text($("#CodeTypeHeader").text());
      $("#CodeTypeRow").trigger("click");

   })

   $("#RecentHeader").click(function(){
      $('#sortBy').text($("#RecentHeader").text());
      $("#RecentRow").trigger("click");
   })
 });