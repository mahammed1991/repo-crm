 $(document).ready(function(){
        $(".jquery-filterable-filter").hide()
        $("#form-filter").show()
    })
    $('#all').click(function(){
      $('.implemented').show()
      $('.inactive').show()
      $('.inprogress').show()
      $('.attemptingcontact').show()
      $('.inqueue').show()
    })

    $('#Inactive').click(function(){
      $('.implemented').hide()
      $('.inactive').show()
      $('.inprogress').hide()
      $('.attemptingcontact').hide()
      $('.inqueue').hide()
    })
    $('#InQueue').click(function(){
      $('.implemented').hide()
      $('.inactive').hide()
      $('.inprogress').hide()
      $('.attemptingcontact').hide()
      $('.inqueue').show()
    })
    $('#AttemptingContact').click(function(){
      $('.implemented').hide()
      $('.inactive').hide()
      $('.inprogress').hide()
      $('.attemptingcontact').show()
      $('.inqueue').hide()
    })
    $('#Implemented').click(function(){
      $('.implemented').show()
      $('.inactive').hide()
      $('.inprogress').hide()
      $('.attemptingcontact').hide()
      $('.inqueue').hide()
    })
    $('#InProgress').click(function(){
      $('.implemented').hide()
      $('.inactive').hide()
      $('.inprogress').show()
      $('.attemptingcontact').hide()
      $('.inqueue').hide()
    })
    $('#CID').click(function(){
      $('#CIDText').toggle()
    })

    $('#CodeType').click(function(){
      $('#CodeTypeText').toggle()
    })
  
  function filter(phrase, _id){
    var words = phrase.value.toLowerCase().split(" ");
    var _table = document.getElementById(_id);
    var ele;
    for (var r = 1; r < _table.rows.length; r++){
      ele = _table.rows[r].innerHTML.replace(/<[^>]+>/g,"");
            var displayStyle = 'none';
            for (var i = 0; i < words.length; i++) {
          if (ele.toLowerCase().indexOf(words[i])>=0)
        displayStyle = '';
          else {
        displayStyle = 'none';
        break;
          }
            }
      _table.rows[r].style.display = displayStyle;
    }
  }

 $(document).ready(function(){
     $('.pop_up').mouseover(function(){     
        $(this).find('.popover').show();
      })
      $('.pop_up').mouseout(function(){
          $(this).find('.popover').hide();
      })
  })
