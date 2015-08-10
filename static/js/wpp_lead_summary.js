 $(document).ready(function(){
        $(".jquery-filterable-filter").hide()
        $("#form-filter").show()
    })

    $('#all').click(function(){
      showAll();
    })

    $('#Open').click(function(){
      hideAll();
      $('.open').show(); 
    })

    $('#OnHold').click(function(){
      hideAll();
      $('.onhold').show();
    })

    $('#InMockup').click(function(){
      hideAll();
      $('.inmockup').show();
    })

    $('#MockupReview').click(function(){
      hideAll();
      $('.mockupreview').show();
    })

    $('#Deferred').click(function(){
      hideAll();
      $('.deferred').show();
    })

    $('#InUIUXReview').click(function(){
      hideAll();
      $('.inuiuxreview').show()
    })

    $('#InFileTransfer').click(function(){
      hideAll();
      $('.infiletransfer').show()
    })
    $('#InDevelopment').click(function(){
      hideAll();
      $('.indevelopment').show()
    })

    $('#InStage').click(function(){
      hideAll();
      $('.instage').show()
    })
    $('#ABTesting').click(function(){
      hideAll();
      $('.ab-testing').show()
    })
    $('#Implemented').click(function(){
      hideAll();
      $('.impl').show()
    })

    function showAll(){
      $('.open').show()
      $('.onhold').show()
      $('.inmockup').show()
      $('.mockupreview').show()
      $('.deferred').show()
      $('.inuiuxreview').show()
      $('.infiletransfer').show()
      $('.indevelopment').show()
      $('.instage').show()
      $('.ab-testing').show()
      $('.impl').show()
    }

    function hideAll(){
      $('.open').hide()
      $('.onhold').hide()
      $('.inmockup').hide()
      $('.mockupreview').hide()
      $('.deferred').hide()
      $('.inuiuxreview').hide()
      $('.infiletransfer').hide()
      $('.indevelopment').hide()
      $('.instage').hide()
      $('.ab-testing').hide()
      $('.impl').hide()
    }



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
              3: { 
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
              8: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              },
              10: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              }
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

$('#SubmitFeedback').click(function(){
    $(".error-box").removeClass('error-box');
    var feedbackTitle = $('#feedbackTitle').val();
    var feedbackType = $('#feedbackType').val();
    var comments = $('#comments').val();
    var lead_type = 'wpp'
    if (feedbackTitle === '' ){
      $('#feedbackTitle').addClass('error-box');
    }else if(feedbackType === 'Feedback Type'){
      $('#feedbackType').addClass('error-box');
    }else if(comments === ''){
      $('#comments').addClass('error-box');
    }else{
      dataString = {'title': feedbackTitle, 'type': feedbackType, 'comment': comments, 'lead_id': window.lead_id, 'lead_type': lead_type}
      $.ajax({
          url: "/main/create-feedback-from-lead-status",
          data: dataString,
          type: 'GET',
          dataType: "json",
          success: function(data) {
            if(data === 'SUCCESS'){
              alert('feedback succesfully created ')
              $('#closeFeedbcak').trigger('click');
              $('#feedbackTitle').val('');
              $('#feedbackType').prop('selectedIndex', 0);
              $('#comments').val('');
            }
          },
          error: function(jqXHR, textStatus, errorThrown) {
              alert('failure');
          }
        }); 
    }
    
    })