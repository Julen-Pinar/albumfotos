// JQuery Snippet

$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
}

var rh = rh || {}; // If rh exists dont blow it away just use the old one
rh.mq = rh.mq || {}; // MovieQuote(mq) namespace in RoseHulman(rs) namespace
						// to avoid the not so posible in this project
						// overlapping

rh.mq.enableButtons = function() {
	
}

rh.mq.enableInfo = function() {
	
			
		if  ($.urlParam('success')) {
			$('.info').addClass('bg-success');
			$('.info').removeClass('hidden');
			$('.info').html(unescape($.urlParam('success')));
		} else if ($.urlParam('error')) {
			$('.info').addClass('bg-danger');
			$('.info').removeClass('hidden');
			$('.info').html(unescape($.urlParam('error')));
		}

}

$(document).ready( function() {
	rh.mq.enableButtons();
	rh.mq.enableInfo();
	rh.mq.attachEventHandlers();
});