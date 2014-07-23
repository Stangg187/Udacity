//like button function for blog posts
function like() {
    alert("Glad you liked it!");
}

//function to show/hide blog post content
$(function () {
	$('div.content').on('click', function() { 
  		$('div.content-body', this).toggleClass('show-content');
  	});
});

//Robot laser eyes function
$(function () {
	$(".flash").click(function() {
	  $(".brain").toggleClass('laser');
	});
});

// Robot background function
$(function () {
	$(".color").click(function() {
	  // assign each named color a random number 0-255
	  var red = Math.floor(Math.random() * 255);
	  var green = Math.floor(Math.random() * 255);
	  var blue = Math.floor(Math.random() * 255);
	  
	  var randomRGBA = 'rgba('+red+','+green+','+blue+',1)';
	  
	  $("body").css("background", randomRGBA);
	});
});