var thesislist=[];

function onFormSubmit(event){
	var data = $(event.target).serializeArray();
	var thesis={};

	for (var i=0;i<data.length;i++){
		thesis[data[i].name] = data[i].value;
	}

	var list_element=$('<li id="item"' +'class="' + thesis.year + thesis.title1 + '">');
	var item = list_element.html(thesis.year + ' ' + thesis.title1);

	var thesis_create_api = '/api/thesis';
	$.post(thesis_create_api, thesis, function(response){
		if(response.status = 'OK') {
			var full_thesis = response.data.year + ' ' + response.data.title1;
			$('.thesis-list').append('<li>' + full_thesis)
		}
		else {
			// prompt("Error.")
		}
	});
	return false;
}(jQuery)

function loadAllThesis(){
	var thesis_list_api = '/api/thesis';
	$.get(thesis_list_api, {}, function(response){
		console.log('thesis list', response)
		response.data.forEach(function(thesis) {
			var full_thesis = thesis.year + ' ' + thesis.title1;	
			$('.thesis-list').append('<li>' + full_thesis + '</li>' )
		});
	});
}

$('.create-form').submit(onFormSubmit);
loadAllThesis();
