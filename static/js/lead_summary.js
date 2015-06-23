 $(document).ready(function(){
        $(".jquery-filterable-filter").hide()
        $("#form-filter").show()
    })

    $('#all, .all').click(function(){
      $('.implemented').show()
      $('.inactive').show()
      $('.inprogress').show()
      $('.attemptingcontact').show()
      $('.inqueue').show()
    })

    $('#Inactive, .Inactive').click(function(){
      $('.implemented').hide()
      $('.inactive').show()
      $('.inprogress').hide()
      $('.attemptingcontact').hide()
      $('.inqueue').hide()
    })
    $('#InQueue, .InQueue').click(function(){
      $('.implemented').hide()
      $('.inactive').hide()
      $('.inprogress').hide()
      $('.attemptingcontact').hide()
      $('.inqueue').show()
    })
    $('#AttemptingContact, .AttemptingContact').click(function(){
      $('.implemented').hide()
      $('.inactive').hide()
      $('.inprogress').hide()
      $('.attemptingcontact').show()
      $('.inqueue').hide()
    })
    $('#Implemented, .Implemented').click(function(){
      $('.implemented').show()
      $('.inactive').hide()
      $('.inprogress').hide()
      $('.attemptingcontact').hide()
      $('.inqueue').hide()
    })
    $('#InProgress, .InProgress').click(function(){
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

      /* sorting function start here*/
        $("#Leads, #ldapLeads").tablesorter({ 
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
              5: { 
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
              9: { 
                  // disable it by setting the property sorter to false 
                  sorter: false 
              },
              11: { 
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


 $("#statusHeader, .statusHeader").click(function(){

      var txt = $(this).text()
      $('#sortBy, .sortBy').text(txt);
      $("#StatusRow, .StatusRow").trigger("click");
      
   })

   $("#CodeTypeHeader, .CodeTypeHeader").click(function(){
      var txt = $(this).text()
      $('#sortBy, .sortBy').text(txt);
      $("#CodeTypeRow, .CodeTypeRow").trigger("click");

   })

   $("#RecentHeader, .RecentHeader").click(function(){
      var txt = $(this).text()
      $('#sortBy, .sortBy').text(txt);
      $("#RecentRow, .RecentRow").trigger("click");
   })

   $('#Leads thead>tr>th').unbind('click');
   $('#ldapLeads thead>tr>th').unbind('click');

/* sorting function end here*/


/* feed back submit through leads status page start here */

$('#SubmitFeedback').click(function(){
    $(".error-box").removeClass('error-box');
    var feedbackTitle = $('#feedbackTitle').val();
    var feedbackType = $('#feedbackType').val();
    var comments = $('#comments').val();
    if (feedbackTitle === '' ){
      $('#feedbackTitle').addClass('error-box');
    }else if(feedbackType === 'Feedback Type'){
      $('#feedbackType').addClass('error-box');
    }else if(comments === ''){
      $('#comments').addClass('error-box');
    }else{
      dataString = {'title': feedbackTitle, 'type': feedbackType, 'comment': comments, 'lead_id': window.lead_id}
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
$('#closeFeedbcak').click(function(){
  $('#feedbackModal').hide()
  $('#feedbackTitle').val('');
  $('#feedbackType').prop('selectedIndex', 0);
  $('#comments').val('');
})

$('.close').click(function(){
  $('#feedbackModal').hide()
  $('#feedbackTitle').val('');
  $('#feedbackType').prop('selectedIndex', 0);
  $('#comments').val('');
})

/* feed back submit through leads status page end  here */
