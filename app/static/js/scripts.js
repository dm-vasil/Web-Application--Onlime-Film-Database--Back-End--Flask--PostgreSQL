    $( ".target" ).change(function() {
  $('#ttt').val("petyx");
});




function myFunction() {
      document.getElementById("myDropdown").classList.toggle("show");
    }

    function submitFilmData(){
        $.ajax({
          type : 'POST',
          url : "/add_film",
          data : $('#form1,#form2, #form3, #form4').serialize(),
          success:function(response){ document.write(response); }
         });
    }

     function scoreAndReview(id){
        $('#temp').slideToggle("slow");
        /*if ($('#temp').prop('hidden')==true)
            $('#temp').prop("hidden", false);
         else
            $('#temp').prop("hidden", true);*/
    }

    function submitFilmSearch(){
        $.ajax({
          type : 'POST',
          url : "/search_film",
          data : $('#form_filters,#form_film_name').serialize(),
          success:function(response){ document.open(); document.write(response);}
         });
    }

    function showOptions(id){ //начинает показ вариантов только от 4 букв
        if ($('#'+id).val().length>2)
            $('.film_option').prop("disabled", false);
        else
            $('.film_option').prop("disabled", true);

    }

    function appendActor()
    {
        var data = $('#actors_choice').val();
        if (data)
        {
            var id = $('option[value="'+data+'"]').attr('id');
            $('#chosen_actors').append("<div class='variants_list' id='actor"+id+"'><label class='inputs'>"+data+"</label>" +
                "  <button type='button' class='button_delete' value='"+id+"' onclick='deleteActor(this.value)'>" +
                "<i class=\"fa fa-times-circle\"></i></button>" +
                "<input type='hidden' name='actors_list_ids "+data+"' value='"+id+"'><br></div>");
            $('#actors_choice').val("");
        }
    }

    function appendDirector()
    {
        var data = $('#directors_choice').val()
        if (data)
        {
            var id = $('option[value="'+data+'"]').attr('id');
            $('#chosen_directors').append("<div class='variants_list' id='director"+id+"'><label class='inputs'>"+data+"</label>" +
                "  <button type='button' class='button_delete' value='"+id+"' onclick='deleteDirector(this.value)'>" +
                "<i class=\"fa fa-times-circle\"></i></button>" +
                "<input type='hidden' name='directors_list_ids "+data+"' value='"+id+"'><br></div>");
            $('#directors_choice').val("");
        }
    }

    function appendGenre()
    {
        var data = $('#genres_choice').val()
        if (data)
        {
            $('#chosen_genres').append("<div class='variants_list' id='genre"+data+"' style='display: inline-block;'><label class='inputs'>"+data+"</label>" +
                "  <button type='button' class='button_delete' value='"+data+"' onclick='deleteGenre(this.value)'>" +
                "<i class=\"fa fa-times-circle\"></i></button>" +
                "<input type='hidden' name='genres_list_ids "+data+"' value='"+data+"' class='inputs'></div>  ");
            $('#genres_choice').val("");
        }
    }

    function appendCountry()
    {
        var data = $('#countries_choice').val()
        if (data)
        {
            $('#chosen_countries').append("<div class='variants_list' id='country"+data+"' style='display: inline-block;'><label class='inputs'>"+data+"</label>" +
                "  <button type='button' class='button_delete' value='"+data+"' onclick='deleteCountry(this.value)'>" +
                "<i class=\"fa fa-times-circle\"></i></button>" +
                "<input type='hidden' name='countries_list_ids "+data+"' value='"+data+"' class='inputs'></div>  ");
            $('#countries_choice').val("");
        }
    }

    function deleteActor(id)
    {
        $("div").remove('#actor'+id);
    }

    function deleteDirector(id)
    {
        $("div").remove('#director'+id);
    }

    function deleteGenre(id)
    {
        $("div").remove('#genre'+id);
    }

    function deleteCountry(id)
    {
        $("div").remove('#country'+id);
    }

    window.onclick = function(e) {
      if (!e.target.matches('.dropbtn')) {
      var myDropdown = document.getElementById("myDropdown");
        if (myDropdown.classList.contains('show')) {
          myDropdown.classList.remove('show');
        }
      }
    }