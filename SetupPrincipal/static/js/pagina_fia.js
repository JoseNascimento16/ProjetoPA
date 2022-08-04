$(document).ready(function(){

    var plano_devolvido = JSON.parse(document.getElementById('id-chave-devolvido').textContent);
    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
    // var situacao_do_plano = JSON.parse(document.getElementById('id-situacao-plano').textContent);
    var alterabilidade_plano = JSON.parse(document.getElementById('id-alterabilidade-plano').textContent);
    var sugestoes_fia_concluidas = JSON.parse(document.getElementById('id-sugestoes-fia-concluidas').textContent);
    var todas_ordens = JSON.parse(document.getElementById('id-todas-ordens').textContent);
    var ordens_com_correcao = JSON.parse(document.getElementById('id-ordens-com-correcao').textContent);
    

    if (alterabilidade_plano == 'Escola' && tipo_de_usuario == 'Escola' ){

        
    }else if(alterabilidade_plano == 'Secretaria' && tipo_de_usuario == 'Func_sec' ){
        if (!sugestoes_fia_concluidas){
        
        //SE O PLANO TIVER COM SUGESTÕES DE CORREÇÃO CONCLUIDAS OU 
        }else{ 
            $(".desabilita-js").removeAttr('href'),
            $('.tooltiptext3-tabela').css("display","none"),
            $('.tooltiptext4-tabela').css("display","none");
        }
        
    }else if(alterabilidade_plano == 'Desativada' || tipo_de_usuario == 'Funcionario' ){
        $(".desabilita-js").removeAttr('href'),
        $('.tooltiptext3-tabela').css("display","none"),
        $('.tooltiptext4-tabela').css("display","none");
        $('.mensagem-cinza').removeClass('display-none');
        $('.sinal-ordens-js').css("display","none")
        
    }else{ // Se for escola ou func_sec e plano estiver com alterabilidade oposta
        $(".desabilita-js").removeAttr('href'),
        $('.tooltiptext3-tabela').css("display","none"),
        $('.tooltiptext4-tabela').css("display","none");
        $('.mensagem-cinza').removeClass('display-none');
        $('.sinal-ordens-js').css("display","none")
    }

    // ADICIONA FUNDO LARANJA
    $( todas_ordens ).each(function(index,element) {
        // SE A ORDEM-FIA POSSUIR CORREÇÕES
        if ( ordens_com_correcao.includes(element) )  { 
            $('.tr-dinamico-fia-' + element).addClass('background-possui-correcao');
        }
    })

})