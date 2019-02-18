var addSpan=function(tdata){
	if(univ.theme_toggle){
		tdata=tdata.replace(/[\{]/mg,"<span class='json-braces theme_change dark_theme'>{</span>");
		tdata=tdata.replace(/[\}]/mg,"<span class='json-braces theme_change dark_theme'>}</span>");
		tdata=tdata.replace(/[\[]/mg,"<span class='json-braces theme_change dark_theme'>[</span>");
		tdata=tdata.replace(/[\]]/mg,"<span class='json-braces theme_change dark_theme'>]</span>");
		tdata=tdata.replace(/[:]/mg,"<span class='json-braces theme_change dark_theme'>:</span>");
		tdata=tdata.replace(/[,]/mg,"<span class='json-braces theme_change dark_theme'>,</span>");
	}
	else{
		tdata=tdata.replace(/[\{]/mg,"<span class='json-braces theme_change'>{</span>");
		tdata=tdata.replace(/[\}]/mg,"<span class='json-braces theme_change'>}</span>");
		tdata=tdata.replace(/[\[]/mg,"<span class='json-braces theme_change'>[</span>");
		tdata=tdata.replace(/[\]]/mg,"<span class='json-braces theme_change'>]</span>");
		tdata=tdata.replace(/[:]/mg,"<span class='json-braces theme_change'>:</span>");
		tdata=tdata.replace(/[,]/mg,"<span class='json-braces theme_change'>,</span>");	
	}

	return tdata;
}

var requestAjax=function(options){

	var object = {
		url:"http://35.200.140.248:5000/validate",
		type:"POST",
		datatype:'json',
        crossDomain:true,
	};

	$.extend(object,options);

	$.ajax(object).done(function(data){

		$('.loader').hide();

		if(data==null){
			console.log("No data found!!!");
		}
		else{
			console.log(data);

			$("header").animate({"height":"10em"},1000,function(){
				$(".search_result_cont").toggleClass("search_result_cont_show");

				univ.tags=[];	

				var hits=data['hits']['hits'];

				var stringHits='';
				//console.log(data[0]);
				/*stringHits+='<div class="sub_hits_head">'+addSpan("<span class='json-key'>took: </span>"+prettyPrintJson.toHtml(data['took'])+",<br>");
				stringHits+=addSpan("<span class='json-key'>timed_out: </span>"+prettyPrintJson.toHtml(data['timed_out'])+",<br>");
				stringHits+=addSpan("<span class='json-key'>_shards:  </span>"+prettyPrintJson.toHtml(data['_shards'])+",<br>");
				stringHits+=addSpan("<span class='json-key'>total:  </span>"+prettyPrintJson.toHtml(data['hits']['total'])+",<br>");
				stringHits+=addSpan("<span class='json-key'>max_score:  </span>"+prettyPrintJson.toHtml(data['hits']['max_score'])+",<br>");
				stringHits+='</div>';*/

				for(key in hits){
					var tdata=prettyPrintJson.toHtml(hits[key]);

					univ.tags.push(hits[key]['_source']['name']);

					if(univ.theme_toggle){
						tdata=addSpan(tdata);
						
						stringHits+="<div class='sub_hits theme_change dark_theme'>"+tdata+"</div>";
					}
					else{
						tdata=addSpan(tdata);

						stringHits+="<div class='sub_hits theme_change'>"+tdata+"</div>";
					}
				}

				$('pre').html(stringHits);

				$("#searchtext").autocomplete({
			    	source: univ.tags,
			    	minLength:1,
			    	select: function( event, ui ) {
			    		$("#searchtext").val(ui.item.value);

			    		$("form").trigger("submit");
				    	//console.log( "Selected: " + ui.item.value);
				    }
			    });

			    if(!$(".ui-menu").hasClass("theme_change")){
			    	$(".ui-menu").addClass("theme_change");

			    	if(univ.theme_toggle){
						$(".ui-menu").toggleClass("dark_theme");				    		
			    	}
			    }
			});
		}
	});
}