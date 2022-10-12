$(document).ready(function(){

    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
    
    // PLANOS GERAIS
    if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Func_sec'){
        
    }else if (tipo_de_usuario == 'Diretor_escola'){
        
    }else if (tipo_de_usuario == 'Funcionario'){
        
    }

    
    // PLANOS NECESSITANDO CORREÇÃO

    if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Func_sec'){
        $('.a-clear-href').removeAttr('href');
        $('.remove').remove('.remove');
    }else if (tipo_de_usuario == 'Diretor_escola'){
        
    }else if (tipo_de_usuario == 'Funcionario'){
        $('.a-clear-href').removeAttr('href');
        $('.remove').remove('.remove');
    }

    // PLANOS FINALIZADOS

    // TODOS OS USUARIOS
    

})