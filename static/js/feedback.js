$(document).ready(function() 
    { 
	    $("#feedback_table").tablesorter({ 
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
	              
	            9: { 
	                // disable it by setting the property sorter to false 
	                sorter: false 
	            }
	            
	        } 
	    });
    }
     /* filter on document load end*/
     /* on document load feedback filter select option pass*/
    // document.getElementById('FeedbackCat').value = '{{feedback_type}}';
	
     // setSelectValue('FeedbackCat', '{{feedback_type}}')

); 
/* sort by function start here*/
   $("#status_sort").click(function(){
   		$('#SortBy').text($("#status_sort").text());
   		$("#status_header").trigger("click");
   })

   $("#lead_owner_sort").click(function(){
   		$('#SortBy').text($("#lead_owner_sort").text());
   		$("#lead_owner_header").trigger("click");
   })

   $("#recent_sort").click(function(){
   		$('#SortBy').text($("#recent_sort").text());
   		$("#recent_header").trigger("click");
   })


/* sort by function  here*/

/*serch function */ 
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
/*serch function */ 

$('#All').click(function(){
      $('.status-inq').show()
      $('.status-inpro').show()
      $('.status-implemented').show()
      $('.status-fixed').show()
    })
$('#Resolved').click(function(){
      $('.status-inq').hide()
      $('.status-inpro').hide()
      $('.status-implemented').show()
      $('.status-fixed').hide()
    })
$('#InProgress').click(function(){
      $('.status-inq').hide()
      $('.status-inpro').show()
      $('.status-implemented').hide()
      $('.status-fixed').hide()
    })
$('#New').click(function(){
      $('.status-inq').show()
      $('.status-inpro').hide()
      $('.status-implemented').hide()
      $('.status-fixed').hide()
    })
$('#Fixed').click(function(){
	 $('.status-fixed').show()
	 $('.status-inq').hide()
     $('.status-inpro').hide()
     $('.status-implemented').hide()
})


   


/* feedback filter by  team lead*/ 
function setSelectValue (id, val) {
    document.getElementById(id).value = val;
}

  $('#FeedbackCat').click(function(){
    feecdbackcat = $('#FeedbackCat').val();
    if (feecdbackcat === 'TeamFeedback'){
    	$('#EmailId').show()
    }else{
    	$('#EmailId').hide()
    }
  });

