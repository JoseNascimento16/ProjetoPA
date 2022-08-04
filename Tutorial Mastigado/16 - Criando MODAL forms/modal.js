// To set multiple properties values: .css({ "display":"flex" , "display":"flex" , ... });

// MOSTRA MODAL DE CRIAR PLANO
$(document).ready(function(){
	$("#chama-form-plano").click(function(){ 
		$(".modelo-modal").css("display", "flex"),
		$(".div-form-plano").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal").css("display", "none"),
			$(".div-form-plano").css("display", "none")});
		});

// MOSTRA MODAL DE CRIAR CADASTROS		
$(document).ready(function(){
	$("#chama-form-cadastro").click(function(){ 
		$(".modelo-modal").css("display", "flex"),
		$(".div-form-cadastro").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal").css("display", "none"),
			$(".div-form-cadastro").css("display", "none")});
		});