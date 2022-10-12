$(document).ready(function(){

    //var plano_devolvido = JSON.parse(document.getElementById('id-chave-devolvido').textContent);
    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
    var situacao_do_plano = JSON.parse(document.getElementById('id-situacao-plano').textContent);
    var alterabilidade_plano = JSON.parse(document.getElementById('id-alterabilidade-plano').textContent);
    var sugestoes_fia_concluidas = JSON.parse(document.getElementById('id-sugestoes-fia-concluidas').textContent);
    var todas_ordens = JSON.parse(document.getElementById('id-todas-ordens').textContent);
    var ordens_com_correcao = JSON.parse(document.getElementById('id-ordens-com-correcao').textContent);
    var assinatura_tecnico = JSON.parse(document.getElementById('id-assinatura-tecnico').textContent);
    

    if (alterabilidade_plano == 'Escola' && tipo_de_usuario == 'Diretor_escola' ){

        
    }else if(alterabilidade_plano == 'Secretaria' && tipo_de_usuario == 'Func_sec' ){
        if (!sugestoes_fia_concluidas){
        
        //SE O PLANO TIVER COM SUGESTÕES DE CORREÇÃO CONCLUIDAS OU 
        }else{ 
            $(".desabilita-js").removeAttr('href'),
            $('.tooltiptext3-tabela').css("display","none"),
            $('.tooltiptext4-tabela').css("display","none");
        }
        
    }else if(alterabilidade_plano == 'Desativada' || tipo_de_usuario == 'Funcionario' ){
        if(assinatura_tecnico){
            $(".desabilita-js").removeAttr('href'),
            $('.tooltiptext3-tabela').css("display","none"),
            $('.tooltiptext4-tabela').css("display","none");
            $('.mensagem-cinza').removeClass('display-none');
            $('.sinal-ordens-js').css("display","none");
        }else{
            $('.icone-tecnico').removeClass('desabilita-js'),
            $('.icone-tecnico').removeClass('sinal-ordens-js'),
            $('.tooltiptext3-tabela').css("display","none"),
            $('.tooltiptext4-tabela').css("display","none"),
            $('.mensagem-cinza').removeClass('display-none'),
            $(".desabilita-js").removeAttr('href'),
            $('.sinal-ordens-js').css("display","none");
        }
        
    }else{ // Se for escola ou func_sec e plano estiver com alterabilidade oposta
        $(".desabilita-js").removeAttr('href'),
        $('.tooltiptext3-tabela').css("display","none"),
        $('.tooltiptext4-tabela').css("display","none");
        $('.mensagem-cinza').removeClass('display-none');
        $('.sinal-ordens-js').css("display","none")
    }

    if (alterabilidade_plano == 'Desativada'){
        $('.background-hover').removeClass('background-hover'); // Remove hover background para nao atrapalhar impressao
    }

    // ADICIONA FUNDO LARANJA
    $( todas_ordens ).each(function(index,element) {
        // SE A ORDEM-FIA POSSUIR CORREÇÕES
        if ( ordens_com_correcao.includes(element) )  { 
            $('.tr-dinamico-fia-' + element).addClass('background-possui-correcao');
        }
    })

    // TOOLTIP QUESTION MARK DE IMPRESSÃO
            
    showContext = $('.question-menu-impressao').hover(function() {
        var e = window.event;
    
        var posX = e.clientX - 15;
        var posY = e.clientY - 39;
        var context = document.getElementById("id-tooltip7-menu")
        context.style.top = posY + "px";
        context.style.left = posX + "px";
        context.style.display = "block";

        $('.question-menu-impressao').mouseleave(function(){
        $('.question-menu-impressao').removeClass('tooltip7-menu'),
        $('.tooltiptext7-tabela').css("display","none");
        })
    })

})