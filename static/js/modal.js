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
			$(".div-form-plano").css("display", "none")  });
		});

// MOSTRA MODAL DE EDITAR PLANO
$(document).ready(function(){
	$("#chama-form-edita-plano").click(function(){ 
		$(".modelo-modal-edicao").css("display", "flex"),
		$(".div-form-edita-plano").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal-edicao").css("display", "none"),
			$(".div-form-edita-plano").css("display", "none")});
		});

// MOSTRA MODAL DE CRIAR ORDEM
$(document).ready(function(){
	$("#chama-form-ordem").click(function(){ 
		$(".modelo-modal").css("display", "flex"),
		$(".div-form-ordem").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal").css("display", "none"),
			$(".div-form-ordem").css("display", "none")});
		});		

// MOSTRA MODAL DE CRIAR CODIGO
$(document).ready(function(){
	$("#chama-form-codigo").click(function(){ 
		$(".modelo-modal").css("display", "flex"),
		$(".div-form-codigo").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal").css("display", "none"),
			$(".div-form-codigo").css("display", "none")});
		});		

// MOSTRA MODAL DE CRIAR CADASTROS DE ESCOLAS	
$(document).ready(function(){
	$("#chama-form-cadastro-escolas").click(function(){ 
		$(".modelo-modal").css("display", "flex"),
		$(".div-form-cadastro-escolas").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal").css("display", "none"),
			$(".div-form-cadastro-escolas").css("display", "none")});
		});

// MOSTRA MODAL DE CRIAR CADASTRO DE FUNCIONARIOS
$(document).ready(function(){
	$("#chama-form-cadastro-funcionario").click(function(){ 
		$(".modelo-modal").css("display", "flex"),
		$(".div-form-cadastro-funcionarios").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal").css("display", "none"),
			$(".div-form-cadastro-funcionarios").css("display", "none")});
		});	
		
// MOSTRA MODAL DE CRIAR CADASTRO DE TURMAS
$(document).ready(function(){
	$("#chama-form-cadastro-turmas").click(function(){ 
		$(".modelo-modal").css("display", "flex"),
		$(".div-form-cadastro-turmas").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal").css("display", "none"),
			$(".div-form-cadastro-turmas").css("display", "none")});
		});	

// MOSTRA MODAL DE CONFIRMAÇÃO DE AÇÃO		
$(document).ready(function(){
	$("#chama-confirma-deleta").click(function(){ 
		$(".modelo-modal-confirma").css("display", "flex"),
		$(".div-confirma-deleta").css("display", "block")  });
  });
	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal-confirma").css("display", "none"),
			$(".div-confirma-deleta").css("display", "none")});
		});

// MODAL DE CORRECAO DE AÇÃO		

	$(document).ready(function(){
		$(".fecha-modal").click(function(){ 
			$(".modelo-modal-correcao").css("display", "none"),
			$(".div-form-correcao-acao").css("display", "none")});
		});