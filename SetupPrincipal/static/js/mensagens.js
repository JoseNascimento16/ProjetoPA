$(document).ready(function(){

    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
    
    // SLIDE_UP DAS MENSAGENS
    if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Func_sec'){
        setTimeout(function(){
            // $('.li-mensagens').css("display","none");    
            $('.li-mensagens').slideUp(500);
            $('.ul-mensagens').slideUp(500);
            }, 4000);
    }else if (tipo_de_usuario == 'Escola'){
        setTimeout(function(){
        // $('.li-mensagens').css("display","none");    
        $('.li-mensagens').slideUp(500);
        $('.ul-mensagens').slideUp(500);
        }, 4000);
    }else if (tipo_de_usuario == 'Funcionario'){
        
    }

    
    

})