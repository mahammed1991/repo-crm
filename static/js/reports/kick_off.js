$('.show-testimony').change(function(){
        var show_testimony = $('.show-testimony').is(":checked");
        if(show_testimony)
        {
          $('.testimony').show();
        }
        else
        {
          $('.testimony').hide();
        }
    });

 $('.add-testimony').click(function () {
      id = $(this).attr('id');
      indx = id.split('_')[1];
      next_id = parseInt(indx) + 1
      if(next_id <= 5 )
      {
          $(".remove-testimony").show();
          $new_row = $("#testimony_1").clone().attr('id', 'testimony_'+next_id).show();
          $(".testimony-reciecved-from", $new_row).attr('id', 'testimony_reciecved_from_name_'+next_id);        
          $(".testimony-reciecved-date", $new_row).attr('id', 'testimony_reciecved_date_'+next_id);  
          $(".testimony-reciecved-for-name", $new_row).attr('id', 'testimony_reciecved_for_name_'+next_id);  
          $(".testimony-reciecved-cid", $new_row).attr('id', 'testimony_reciecved_cid_'+next_id);  
          $(".testimony-text", $new_row).attr('id', 'testimony_text_'+next_id);  
          $(".testimony-reciecved-from", $new_row).attr('name', 'testimony_reciecved_from_name_'+next_id);        
          $(".testimony-reciecved-date", $new_row).attr('name', 'testimony_reciecved_date_'+next_id);  
          $(".testimony-reciecved-for-name", $new_row).attr('name', 'testimony_reciecved_for_name_'+next_id);  
          $(".testimony-reciecved-cid", $new_row).attr('name', 'testimony_reciecved_cid_'+next_id);  
          $(".testimony-text", $new_row).attr('name', 'testimony_text_'+next_id); 
          $new_row.appendTo(".testimonies");
          $('.remove-testimony').attr('id',"#removeTestimony_" + next_id);
          $('.add-testimony').attr('id',"#addTestimony_" + next_id);
          $(".datepickerFrom_a").datetimepicker({
              timepicker:false,
              format:'d.m.Y',
              scrollInput:false,
          });
        }
        if(next_id == 5 )
        {
          $(".add-testimony").hide();
        }
  });

  $('.remove-testimony').click(function () {
    id = $(this).attr('id');
    indx = id.split('_')[1];
    if(("#removeTestimony_"+indx) != "#removeTestimony_1" )
    {
        $(".add-testimony").show();
        $("#testimony_"+indx).remove();
        $('.remove-testimony').attr('id',"#removeTestimony_" + (indx-1));
        $('.add-testimony').attr('id',"#addTestimony_" + (indx-1));
    }
    if(("#removeTestimony_"+(indx-1)) == "#removeTestimony_1" )
    {
      $('.remove-testimony').hide();
    }
  });


 $('.add-succes').click(function () {
      id = $(this).attr('id');
      indx = id.split('_')[1];
      next_id = parseInt(indx) + 1
      if(next_id <= 5 )
      {
          $(".remove-succes").show();
          $new_row = $("#succes_row_1").clone().attr('id', 'succes_row_'+next_id).show();
          $(".succes-mat-onebox", $new_row).attr('id', 'succes_metrices_one_'+next_id);        
          $(".succes-mat-twobox", $new_row).attr('id', 'succes_metrices_two_'+next_id);  
          $(".succes-mat-threebox", $new_row).attr('id', 'succes_metrices_three_'+next_id);  
            
           
          $(".succes-mat-onebox", $new_row).attr('name', 'succes_metrices_one_'+next_id);        
          $(".succes-mat-twobox", $new_row).attr('name', 'succes_metrices_two_'+next_id);  
          $(".succes-mat-threebox", $new_row).attr('name', 'succes_metrices_three_'+next_id);  
          
          $new_row.appendTo(".succes-matrics");
          $('.remove-succes').attr('id',"#removeSuccesMat_" + next_id);
          $('.add-succes').attr('id',"#addSuccesMat_" + next_id);
         
        }
        if(next_id == 5 )
        {
          $(".add-succes").hide();
        }
  });

  $('.remove-succes').click(function () {
    id = $(this).attr('id');
    indx = id.split('_')[1];
    if(("#removeSuccesMat_"+indx) != "#removeTestimony_1" )
    {
        $(".add-succes").show();
        $("#succes_row_"+indx).remove();
        $('.remove-succes').attr('id',"#removeSuccesMat_" + (indx-1));
        $('.add-succes').attr('id',"#addSuccesMat_" + (indx-1));
    }
    if(("#removeSuccesMat_"+(indx-1)) == "#removeSuccesMat_1" )
    {
      $('.remove-succes').hide();
    }
  });

 /* start bootsrap selector plugg in fetching multiple selected values id's*/

    $('.region-ul').children().on('click', function(){
        selectProcessPopulateTeamData(this);
    });

    $('#locationTypeBtn').on('click', function(){
        $(".location-ul").html('');
        var elements = $('.region-ul li a .tickMarkShow');
        if(elements.length > 0)
        {
            for (var i=0;i<elements.length;i++)
            {
                var element_id = $(elements[i]).parent().parent().attr('id');
                for (var j=0;j<window.regionWiseLocations[element_id].length;j++)
                {
                    $(".location-ul").append('<li id="'+ window.regionWiseLocations[element_id][j]+'">'+
                                                 '<a href="#" class="smallLoc">'+
                                                 '<input type="checkbox" class="hiddenCheckbox"/>'+
                                                 '<span class="glyphicon glyphicon-ok tickMark">'+
                                                 '</span>&nbsp;'+ window.regionWiseLocations[element_id][j]+'</a></li>')
                }
                $(".location-ul").css('height','auto');
                $(".location-ul").css('overflow','scroll');
            }
            $('.location-ul').children().on('click', function(){
                selectTeams(this.className, this);
            });
        }
        else
        {
            $(".location-ul").append('<li id=""><a href="#" class="smallLoc"></span>&nbsp;Please Select Region</a></li>')
        }
    });

    function selectProcessPopulateTeamData(regionElement){
        var OptionElement = "<option value='"+$(regionElement).attr('id')+"' selected></option>";
        var selectedProcessElement = $(regionElement).children("a").children('span');
        // UnSelect Process Items.
        if(selectedProcessElement.hasClass('tickMarkShow')){
            selectedProcessElement.removeClass('tickMarkShow');     // UnSelect the Process Element.
        }
        else{
            selectedProcessElement.addClass('tickMarkShow')  
        }
    }

    function selectTeams(parentElementId, selectedElement){
        var selectedTeamsElement = $(selectedElement).children("a").children('span');
        var optionElement = "<option class ='"+parentElementId+"' value='"+ $(selectedElement).attr('idValue')+"' selected></option>";
        if(selectedTeamsElement.hasClass('tickMarkShow')){
            selectedTeamsElement.removeClass('tickMarkShow');
        }
        else{
            selectedTeamsElement.addClass('tickMarkShow');
        }
    }


/* To select multiple code type selector plugg in fetching multiple selected values id*/
$('.code-type-ul').children().on('click', function(){
        selectProcessPopulateCodeType(this);
    });

    $('#locationTypeBtn').on('click', function(){
        var elements = $('.code-type-ul li a .tickMarkShow');
        if(elements.length > 0)
        {
            /*for (var i=0;i<elements.length;i++)
            {
                var element_id = $(elements[i]).parent().parent().attr('id');
                for (var j=0;j<window.regionWiseLocations[element_id].length;j++)
                {
                    
                }
            }*/
            $('.code-type-ul').children().on('click', function(){
                selectCodetype(this.className, this);
            });
        }
    });

    function selectProcessPopulateCodeType(codeTypeElement){
        var OptionElement = "<option value='"+$(codeTypeElement).attr('id')+"' selected></option>";
        var selectedProcessElement = $(codeTypeElement).children("a").children('span');
        // UnSelect Process Items.
        if(selectedProcessElement.hasClass('tickMarkShow')){
            selectedProcessElement.removeClass('tickMarkShow');     // UnSelect the Process Element.
        }
        else{
            selectedProcessElement.addClass('tickMarkShow')
        }
    }
    function selectCodetype(selectedElement){
        var selectedCodeTypeElement = $(selectedElement).children("a").children('span');
        var optionElement = "<option class ='' value='"+ $(selectedCodeTypeElement).attr('')+"' selected></option>";
        if(selectedCodeTypeElement.hasClass('tickMarkShow')){
            selectedCodeTypeElement.removeClass('tickMarkShow');
        }
        else{
            selectedCodeTypeElement.addClass('tickMarkShow');
        }
    }
