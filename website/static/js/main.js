function ajax_call(option_number){
	event.preventDefault();

	var question_id = $('#question-id').text()
	
	$.ajax({
		data: {
			question_id : question_id,
			selected: option_number
		},
		success: function(data){
			// Success
			console.log("Successfully received updated recommendations");

			// Update the question
			$("#user-input-div").fadeOut(300, function(){	
				// Update question here
				$("#question-id").text(data.question.id);
				$("#user-question").text(data.question.question);
				for(var i=0; i<5; i++){
					var elem = $('#option-'+(i+1));
					$(elem).hide();
				}				
				for(var i=0; i<data.question.options.length; i++){
					var elem = $('#option-'+(i+1));
					$(elem).find("img").attr("src", data.question.options[i].image);
					$(elem).find("h3").text(data.question.options[i].text);
					$(elem).show();
				}				
			}).fadeIn(300);				
			
			
			
			// Update the recommendations
			$("#recos").fadeOut(300, function(){	
				for(var i=0; i<data.recos.length;i++){
					// Get the element from the html
					var elem = $('#reco-dog-'+i);						
					$(elem).find("a").attr("href", data.recos[i].url)
					$(elem).find("img").attr("src", data.recos[i].image)
					$(elem).find("h4").text(data.recos[i].name+" ("+data.recos[i].score+")")
				}
			}).fadeIn(300);

			// Update the recommendations
			$("#not-recos").fadeOut(300, function(){	
				for(var i=0; i<data.skip.length;i++){
					// Get the element from the html
					var elem = $('#not-reco-dog-'+i);						
					$(elem).find("a").attr("href", data.skip[i].url)
					$(elem).find("img").attr("src", data.skip[i].image)
					$(elem).find("h4").text(data.skip[i].name+" ("+data.skip[i].score+")")
				}
			}).fadeIn(300);	
		},
		error: function(){
			console.log("nooo :(");
		},
		type: 'GET'
	});		
};	
