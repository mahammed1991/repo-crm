 $(document).ready(function(){
        $(".jquery-filterable-filter").hide()
        $("#form-filter").show()
    })

    $('#all').click(function(){
      $('.open').show()
      $('.onhold').show()
      $('.inmockup').show()
      $('.mockupreview').show()
      $('.deferred').show()
      $('.inuiuxreview').show()
      $('.infiletransfer').show()
      $('.indevelopment').show()
      $('.instage').show()
      $('.implemented').show()
    })

    $('#Open').click(function(){
      $('.open').show()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.inuiuxreview').hide()
      $('.infiletransfer').hide()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.implemented').hide()
    })

    $('#OnHold').click(function(){
      $('.open').hide()
      $('.onhold').show()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.inuiuxreview').hide()
      $('.infiletransfer').hide()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.implemented').hide()
    })

    $('#InMockup').click(function(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').show()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.inuiuxreview').hide()
      $('.infiletransfer').hide()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.implemented').hide()
    })

    $('#MockupReview').click(function(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').show()
      $('.deferred').hide()
      $('.inuiuxreview').hide()
      $('.infiletransfer').hide()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.implemented').hide()
    })

    $('#Deferred').click(function(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').show()
      $('.inuiuxreview').hide()
      $('.infiletransfer').hide()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.implemented').hide()
    })

    $('#InUIUXReview').click(function(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.inuiuxreview').show()
      $('.infiletransfer').hide()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.implemented').hide()
    })
    $('#InFileTransfer').click(function(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.inuiuxreview').hide()
      $('.infiletransfer').show()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.implemented').hide()
    })
    $('#InDevelopment').click(function(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.inuiuxreview').hide()
      $('.indevelopment').show()
      $('.instage').hide()
      $('.implemented').hide()
      $('.infiletransfer').hide()
    })

    $('#InStage').click(function(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.mockupdelivered').hide()
      $('.indevelopment').hide()
      $('.instage').show()
      $('.infiletransfer').hide()
    })

    $('#Implemented').click(function(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.inuiuxreview').hide()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.implemented').show()
      $('.infiletransfer').hide()
    })

    $('#CID').click(function(){
      $('#CIDText').toggle()
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
              7: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              },
          } 
      });
    /*end sorting function*/
    /*comment popup*/
    $('[data-toggle="tooltip"]').tooltip({
          'placement': 'right'
      });
    /*comment popup*/
  })


$('.pingchat').click(function(){
  $('.popup_overlay').show()
})

$('.close').click(function(){
  $('.popup_overlay').hide()
})

$('#habla_panel_div').click(function(){
  $('.popup_overlay').hide()
  $('#habla_panel_div').hide()
})


// sorting function statrt here


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

   $('#Leads thead>tr>th').unbind('click');

/* sorting function end here*/

/* */