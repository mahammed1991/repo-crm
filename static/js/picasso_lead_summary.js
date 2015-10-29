 $(document).ready(function(){
        $(".jquery-filterable-filter").hide()
        $("#form-filter").show()
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