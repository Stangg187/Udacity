$(document).ready(function() {
	$('.hover-image').each(function() {
		$(this).wrap('<div class="tint"></div>');
	});
});