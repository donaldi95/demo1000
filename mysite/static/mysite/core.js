function groupClick(event) {
  console.log("hey");
  var csrftoken     = jQuery("[name=csrfmiddlewaretoken]").val();
  const id          = this.options.id;
  //console.log(id);
  function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
  $.ajax({
    url     :            window.location.pathname,
    type    :           'POST',
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    data:          JSON.stringify( {
      csrfmiddlewaretoken     : csrftoken,
      peak_id                 : id, 
      action                  : 'getPeakData',
    }),
    contentType:    'application/json; charset=utf-8',
    dataType:       'json',
    success:        function (result) {
      $('#annotation').html("<p></p>");
        //console.log(result.peaks);
        peak = JSON.parse(JSON.stringify(result.peaks['peaks_json']));
       //console.log( 'this is peak '+peak);
        $('#peak').html(
             "<p class='peaks'> "+ peak[0]['id'] + "<span> Status is : </span>"+  peak[0]['status'] +" </p>"
        );

        annotation = JSON.parse(JSON.stringify(result.peaks['annotations']));
       // console.log(annotation.length);
        for (var i = 0; i <= annotation.length-1; i++) {
          //console.log(i);
          $('#annotation').append(
             "<p class='annotaion'> Annotation name : "+ annotation[i]['w_name'] + " <br> <span> Status is : </span>"+  annotation[i]['status'] +" </p>"
          );
        }

        /*
        *check if status is to annotate or not to annotate, 
        *than we can show the form of annotation 
        *on click to each peak
        */
        if(peak[0]['status']){
          $("#submitAnnotation").hide();
        }else{
          $("#submitAnnotation").show();
        }
        var mydiv = $('#peak .peaks');
        if(mydiv.length > 1){
            $('#peak .peaks:last').remove();
        }
        $('#hidden_id').val(peak[0]['id']);
    },
    error: function(result) {
        $("#message-div").html("Something went wrong!");
    } 
  });

}

$(function() {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
});
