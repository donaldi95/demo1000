function groupClick(event) {
  
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
        peak = JSON.parse(JSON.stringify(result.peaks));

        $('#peak').html(
             "<p class='peaks'> "+ peak[0]['id']+" </p>"
        );

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
