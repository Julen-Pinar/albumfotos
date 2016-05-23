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
	$('.delete-album').click ( function() {
		entityKey = $(this).find(".entity-key").html();
		$("#delete-album-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});
	
	$('.delete-image').click ( function() {
		entityKey = $(this).find(".entity-key").html();
		$("#delete-image-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});
	
	$('.edit-album').click ( function() {
	   $('#nombre').val($(this).find(".albumNombre").html());
	   $('#descripcion').val($(this).find(".albumDesc").html());
	   $("#insert-album-modal button[type=submit]").html("Modificar Album");
	   $("#insert-album-modal #myModalLabel").html("Modificar Album");
	   entityKey = $(this).find(".entity-key").html();
	   $("#insert-album-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});
	
	$('.add-album').click ( function() {
	   $('#nombre').val("");
       $('#descripcion').val("");
       $("#insert-album-modal button[type=submit]").html("Insertar Album");
       $("#insert-album-modal #myModalLabel").html("Insertar un Album");
       $("#insert-album-modal input[name=entity_key]").val("").prop("disabled", true);
    });
	
	$('.activate-user').click ( function() {
			entityKey = $(this).find(".entity-key").html();
	       $("#activate-user-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});
	
	$('.deactivate-user').click ( function() {
			entityKey = $(this).find(".entity-key").html();
	       $("#deactivate-user-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
	});
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