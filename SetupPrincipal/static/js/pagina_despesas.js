// TROCA O BACKGROUND DA TABELA AO PASSAR O MOUSE (HOVER)
$(document).ready(function(){

    var lista_ordens_codigos = JSON.parse(document.getElementById('id-lista-todos-codigos').textContent);
    var lista_codigos_correcao = JSON.parse(document.getElementById('id-lista-codigos-correcao').textContent);
    var sugestoes_despesas_concluidas = JSON.parse(document.getElementById('id-chave-sugestoes-despesas-concluidas').textContent);
    var plano_devolvido = JSON.parse(document.getElementById('id-chave-devolvido').textContent);
    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
    var situacao_do_plano = JSON.parse(document.getElementById('id-situacao-plano').textContent);
        // console.log(lista_ordens_codigos);
        // console.log(lista_codigos_correcao);
    
    if( sugestoes_despesas_concluidas == 0 && plano_devolvido == 0 ){

        $( lista_ordens_codigos ).each(function(index,element) {
    
            // SE A ORDEM/CODIGO POSSUIR CORREÇÕES
            if ( lista_codigos_correcao.includes(element) )  { 
                // console.log('Achou a ordem: ' + element)
                
                $('.tr-dinamicos' + element).addClass('background-possui-correcao');

                if (situacao_do_plano == 'Pendente' || situacao_do_plano == 'Corrigido pela escola'){

                    $('.tr-dinamicos' + element).hover(function(){
                    $('.tds-trs-' + element).addClass('tooltip3-tabela'),
                    $('.tooltiptext3-tabela').css("display","block");
                    })

                    $('.tr-dinamicos' + element).mouseleave(function(){
                    $('.tds-trs-' + element).removeClass('tooltip3-tabela'),
                    $('.tooltiptext3-tabela').css("display","none");
                    })
                }
            }
            // SE A ORDEM/CODIGO NÃO POSSUIR CORREÇÕES
            else {

                if (situacao_do_plano == 'Pendente' || situacao_do_plano == 'Corrigido pela escola'){

                    $('.tr-dinamicos' + element).hover(function(){
                    $('.tr-dinamicos' + element).addClass('background-tr-acoes'),
                    $('.tds-trs-' + element).addClass('tooltip4-tabela'),
                    $('.tooltiptext4-tabela').css("display","block");
                    }),
                    
                    $('.tr-dinamicos' + element).mouseleave(function(){
                    $('.tr-dinamicos' + element).removeClass('background-tr-acoes'),
                    $('.tds-trs-' + element).removeClass('tooltip4-tabela'),
                    $('.tooltiptext4-tabela').css("display","none");
                    })
                }
            }

        }); 

    }           
    else { // SE O PLANO JA ESTIVER DEVOLVIDO OU COM SUGESTÕES DE CORRECOES DE DESPESAS CONCLUIDAS

        $( lista_ordens_codigos ).each(function(index,element) {

            if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Funcionario' || tipo_de_usuario == 'Func_sec' ){
                // SE A ORDEM/CODIGO POSSUIR CORREÇÕES
                if ( lista_codigos_correcao.includes(element) )  { 
                    $('.tr-dinamicos' + element).addClass('background-possui-correcao'),
                    $('.a-clear-acao').removeAttr('href');
                }
                // SE A ORDEM/CODIGO NÃO POSSUIR CORREÇÕES
                else{
                    $('.tds-trs-' + element).hover(function(){
                    $('.tr-dinamicos' + element).addClass('background-tr-acoes');
                    }),
                    $('.tds-trs-' + element).mouseleave(function(){
                    $('.tr-dinamicos' + element).removeClass('background-tr-acoes'),
                    $('.a-clear-acao').removeAttr("href");
                    })

                }
            }
            else if (tipo_de_usuario == 'Escola') {
                // SE A ORDEM/CODIGO POSSUIR CORREÇÕES
                if ( lista_codigos_correcao.includes(element) )  { 
                    $('.tr-dinamicos' + element).addClass('background-possui-correcao');
                    
                    $('.tds-trs-' + element).hover(function(){
                    $('.tds-trs-' + element).addClass('tooltip3-tabela'),
                    $('.tooltiptext3-tabela').css("display","block");    
                    }),
                    $('.tds-trs-' + element).mouseleave(function(){
                    $('.tds-trs-' + element).removeClass('tooltip3-tabela'),
                    $('.tooltiptext3-tabela').css("display","none");
                    })
                }
                // SE A ORDEM/CODIGO NÃO POSSUIR CORREÇÕES
                else{
                    $('.tds-trs-' + element).hover(function(){
                    $('.tr-dinamicos' + element).addClass('background-tr-acoes');
                    }),
                    $('.tds-trs-' + element).mouseleave(function(){
                    $('.tr-dinamicos' + element).removeClass('background-tr-acoes');
                    // $('.a-clear-acao').removeAttr("href");
                    })

                }
            }
        });

    }


    // DESABILITA MODIFICAR PLANOS EM ESTADOS EM QUE ELES NAO PODEM SER ALTERADOS


    if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Func_sec'){

        if (situacao_do_plano == 'Em desenvolvimento' || situacao_do_plano == 'Publicado' || situacao_do_plano == 'Corrigido' || situacao_do_plano == 'Aprovado' || situacao_do_plano == 'Assinado' || situacao_do_plano == 'Finalizado'){
            $(".desabilita-js").removeAttr('href'); // Desabilita alguns links
            $('.display-none').removeClass("display-none"); // Mostra mensagem que o plano nao pode ser alterado
            $('.botao-concluir-js').addClass("display-none"); // Esconde botão
            $('.mensagem-menu-js').addClass("display-none"); // Esconde mensagem
        }
        
    }else if (tipo_de_usuario == 'Escola'){

        if (situacao_do_plano == 'Pendente' || situacao_do_plano == 'Corrigido pela escola' || situacao_do_plano == 'Pronto' || situacao_do_plano == 'Aprovado' || situacao_do_plano == 'Assinado' || situacao_do_plano == 'Finalizado'){
            $(".desabilita-js").removeAttr('href');
        }
        
    }else if (tipo_de_usuario == 'Funcionario'){
        
    }

})