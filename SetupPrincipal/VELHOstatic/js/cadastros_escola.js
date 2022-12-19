$(document).ready(function(){

    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
    
    // PLANOS GERAIS
    if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Func_sec'){
        
    }else if (tipo_de_usuario == 'Diretor_escola'){
        $('.cursor-default').css('cursor', 'default');
    }else if (tipo_de_usuario == 'Funcionario'){
        
    }

})