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

$(document).ready(function() 
    { 

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
    } 
); 

 $("#statusHeader").click(function(){
      $("#StatusRow").trigger("click");
   })

   $("#CodeTypeHeader").click(function(){
      $("#CodeTypeRow").trigger("click");
   })

   $("#RecentHeader").click(function(){
      $("#RecentRow").trigger("click");
   })

   $('#Leads thead>tr>th').unbind('click');

/* sorting function end here*/

 $(document).ready(function(){
         $('[data-toggle="tooltip"]').tooltip({
          'placement': 'right'
      });
    }) 

/* feed back submit through leads status page start here */

$('#SubmitFeedback').click(function(){
    var feedbackTitle = $('#feedbackTitle').val();
    var feedbackType = $('#feedbackType').val();
    var comments = $('#comments').val();
    dataString = {'title': feedbackTitle, 'type': feedbackType, 'comment': comments, 'lead_id': window.lead_id}
    $.ajax({
        url: "/main/create-feedback-from-lead-status",
        data: dataString,
        type: 'GET',
        dataType: "json",
        success: function(data) {
          if(data === 'SUCCESS'){
            alert('feedback succesfully created ')
            $('#feedbackModal').hide()
          }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            alert('failure');
        }
      }); 
    })


/* feed back submit through leads status page end  here */

/* pin chat */
var lead_owner_email = ''
var lead_owner_name = ''
var weekday = new Array("Sun","Mon","Tue","Wed","Thu","Fri","Sat")
var currentTime = new Date();
var day = currentTime.getDay()
var hour = currentTime.getHours()
var min = currentTime.getMinutes()
currentDayTime=''
if (hour >= 12){
  hour = hour - 12
  currentDayTime = weekday[day]+ ', ' + ' ' + hour + ' : ' + min + ' PM'
}else{
  currentDayTime = weekday[day]+ ', ' + ' ' + hour + ' : ' + min + ' AM'
}

function chat(lead_owner_email, lead_owner_name){
    lead_owner_email = lead_owner_email;
    lead_owner_name = lead_owner_name 
}

var counter = true;
$('#submitmsg').click(function(){
  msg = $('#message').val()
  $('#message').val('')
  if (counter){
    $('.modal-body').append(  '<div class=" ping-copy out-msg">' +
                            '<img src="{{request.session.profile_image}}?sz=32" class="chatter-img">'+
                            '<div class="chat-msg">'+
                            '<img src="{%static 'images/chat-out-img.png' %}">'+
                            '<p>'+ msg +' </p><div class="chat-date">'+ currentDayTime +'</div></div></div>')
    counter = false;
    $(".modal-body").animate({
        scrollTop: $(".modal-body").scrollHeight()
    }, 300);
  }else{
    $('.modal-body').append(  '<div class=" ping-copy in-msg">' +
                            '<img src="{%static 'images/testimonial-pic.jpg' %}" class="chatter-img">'+
                            '<div class="chat-msg">'+
                            '<img src="{%static 'images/chat-in-img.png' %}">'+
                            '<p>'+ msg +' </p><div class="chat-date">'+ currentDayTime +'</div></div></div>')
    counter = true;
    $(".modal-body").animate({
        scrollTop: $(".modal-body").scrollHeight()
    }, 300);
  }
  
})

$("#message").keypress(function(event) {
    if (event.which == 13) {
        event.preventDefault();

        $("#submitmsg").trigger("click");
    }
});
/* */