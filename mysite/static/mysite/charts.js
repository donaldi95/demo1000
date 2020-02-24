/**********************************

Show hide campaigns based on filter

*********************************/


$('select').on('change', function() {
	var optionValue = $(this).val();
	if (optionValue == 'Start') {
		$('.Start').show();
		$('.Closed').hide();
		$('.Created').hide();
	}else if (optionValue == 'Closed') {
		$('.Start').hide();
		$('.Closed').show();
		$('.Created').hide();
	}else if (optionValue == 'Created') {
		$('.Start').hide();
		$('.Closed').hide();
		$('.Created').show();
	}else{
		$('.Start').show();
		$('.Closed').show();
		$('.Created').show();
	}
});