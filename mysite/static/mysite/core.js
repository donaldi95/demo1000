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
        console.log(peak);
       //console.log( 'this is peak '+peak);
        $('#peak').html(
             "<p class='peaks'> Peak Name : "+ peak[0]['name'] + "<br><span> Localize Name is :"+  peak[0]['localize_names'] +" </span> <br> Lat : "+ peak[0]['lat'] + " Lon : "+ peak[0]['lon']+"<br> Date Posted : "+ peak[0]['date_posted'] +" </p>" 
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
          $("#submitAnnotation").show();
        }else{
          $("#submitAnnotation").hide();
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

/* counter */


(function ($) {
  $.fn.countTo = function (options) {
    options = options || {};
    
    return $(this).each(function () {
      // set options for current element
      var settings = $.extend({}, $.fn.countTo.defaults, {
        from:            $(this).data('from'),
        to:              $(this).data('to'),
        speed:           $(this).data('speed'),
        refreshInterval: $(this).data('refresh-interval'),
        decimals:        $(this).data('decimals')
      }, options);
      
      // how many times to update the value, and how much to increment the value on each update
      var loops = Math.ceil(settings.speed / settings.refreshInterval),
        increment = (settings.to - settings.from) / loops;
      
      // references & variables that will change with each update
      var self = this,
        $self = $(this),
        loopCount = 0,
        value = settings.from,
        data = $self.data('countTo') || {};
      
      $self.data('countTo', data);
      
      // if an existing interval can be found, clear it first
      if (data.interval) {
        clearInterval(data.interval);
      }
      data.interval = setInterval(updateTimer, settings.refreshInterval);
      
      // initialize the element with the starting value
      render(value);
      
      function updateTimer() {
        value += increment;
        loopCount++;
        
        render(value);
        
        if (typeof(settings.onUpdate) == 'function') {
          settings.onUpdate.call(self, value);
        }
        
        if (loopCount >= loops) {
          // remove the interval
          $self.removeData('countTo');
          clearInterval(data.interval);
          value = settings.to;
          
          if (typeof(settings.onComplete) == 'function') {
            settings.onComplete.call(self, value);
          }
        }
      }
      
      function render(value) {
        var formattedValue = settings.formatter.call(self, value, settings);
        $self.html(formattedValue);
      }
    });
  };
  
  $.fn.countTo.defaults = {
    from: 0,               // the number the element should start at
    to: 0,                 // the number the element should end at
    speed: 1000,           // how long it should take to count between the target numbers
    refreshInterval: 100,  // how often the element should be updated
    decimals: 0,           // the number of decimal places to show
    formatter: formatter,  // handler for formatting the value before rendering
    onUpdate: null,        // callback method for every time the element is updated
    onComplete: null       // callback method for when the element finishes updating
  };
  
  function formatter(value, settings) {
    return value.toFixed(settings.decimals);
  }
}(jQuery));

jQuery(function ($) {
  // custom formatting example
  $('.count-number').data('countToOptions', {
  formatter: function (value, options) {
    return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
  }
  });
  
  // start all the timers
  $('.timer').each(count);  
  
  function count(options) {
  var $this = $(this);
  options = $.extend({}, options || {}, $this.data('countToOptions') || {});
  $this.countTo(options);
  }
});