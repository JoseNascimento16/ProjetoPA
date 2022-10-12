
// TROCA O BACKGROUND DA TABELA AO PASSAR O MOUSE (HOVER)
$(document).ready(function(){

    var lista_de_ordens = JSON.parse(document.getElementById('id-do-json').textContent);
    var lista2_de_ordens = JSON.parse(document.getElementById('id-lista2-ordens').textContent);
    var sugestoes_concluidas = JSON.parse(document.getElementById('id-chave-sugestoes-acoes-concluidas').textContent);
    var plano_devolvido = JSON.parse(document.getElementById('id-chave-devolvido').textContent);
    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
    var situacao_do_plano = JSON.parse(document.getElementById('id-situacao-plano').textContent);
    // var quebra_linha = JSON.parse(document.getElementById('id-q-linha').textContent);
    // var apos_print = JSON.parse(document.getElementById('id-apos-print').textContent);
    
    // var planoString2 = planoString.replace('[', '');
    // var planoString3 = planoString2.replace(']', '');
    // var planoArray = new Array(planoString3)
    // var teste = {"nome":"joao","idade":"20"}
    // var teste2 = teste[0]
    // var testando = ["1","3"]
    // console.log(typeof(planoArray[0]));
    console.log(plano_devolvido);
    // console.log(valor[0]);

    if( sugestoes_concluidas == 0 && plano_devolvido == 0 ){ // ENQUANTO AS SUGESTOES AINDA NAO FORAM CONCLUIDAS E O PLANO NAO ESTIVER EM ESTADO DE DEVOLVIDO

        $( lista_de_ordens ).each(function(index,element) {
            // console.log( element );
    
            // SE A ORDEM/CODIGO POSSUIR CORREÇÕES
            if ( lista2_de_ordens.includes(element) )  { 
                // console.log('Achou a ordem: ' + element)
                
                $('.tr-dinamicos' + element).addClass('background-possui-correcao');

                if (situacao_do_plano == 'Pendente' || situacao_do_plano == 'Corrigido pela escola'){

                    $('.tds-trs-' + element).hover(function(){
                    $('.tds-trs-' + element).addClass('tooltip2-tabela'),
                    $('.tooltiptext2-tabela').css("display","block");
                    })

                    $('.tds-trs-' + element).mouseleave(function(){
                    $('.tds-trs-' + element).removeClass('tooltip2-tabela'),
                    $('.tooltiptext2-tabela').css("display","none");
                    })
                }


            }
            // SE A ORDEM/CODIGO NÃO POSSUIR CORREÇÕES
            else {
                
                if (situacao_do_plano == 'Pendente' || situacao_do_plano == 'Corrigido pela escola'){

                    $('.tds-trs-' + element).hover(function(){
                    $('.tr-dinamicos' + element).addClass('background-tr-acoes'),
                    $('.tds-trs-' + element).addClass('tooltip1-tabela'),
                    $('.tooltiptext1-tabela').css("display","block");
                    }),
                    
                    $('.tds-trs-' + element).mouseleave(function(){
                    $('.tr-dinamicos' + element).removeClass('background-tr-acoes'),
                    $('.tds-trs-' + element).removeClass('tooltip1-tabela'),
                    $('.tooltiptext1-tabela').css("display","none");
                    })
                }
            }

        });
    
    }
    else{ // SE O PLANO JA ESTIVER DEVOLVIDO OU COM SUGESTÕES DE CORRECOES DE AÇÕES CONCLUIDAS

        $( lista_de_ordens ).each(function(index,element) {
        
            if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Funcionario' || tipo_de_usuario == 'Func_sec'){
                // SE A ORDEM/CODIGO POSSUIR CORREÇÕES
                if ( lista2_de_ordens.includes(element) )  { 
                    $('.tr-dinamicos' + element).addClass('background-possui-correcao'),
                    $('.a-clear-acao').removeAttr('href');
                }
                // SE A ORDEM/CODIGO NÃO POSSUIR CORREÇÕES
                else {
                    $('.a-clear-acao').removeAttr('href');
                    $('.a-clear-href').removeAttr('href');

                    $('.tds-trs-' + element).hover(function(){
                    $('.tr-dinamicos' + element).addClass('background-tr-acoes');
                    }),
                    $('.tds-trs-' + element).mouseleave(function(){
                    $('.tr-dinamicos' + element).removeClass('background-tr-acoes');
                    })
                    
                }
            }
            else if (tipo_de_usuario == 'Diretor_escola') {
                // SE A ORDEM/CODIGO POSSUIR CORREÇÕES
                if ( lista2_de_ordens.includes(element) )  { 
                    $('.tr-dinamicos' + element).addClass('background-possui-correcao');
                    
                    $('.tds-trs-' + element).hover(function(){
                    $('.tds-trs-' + element).addClass('tooltip2-tabela'),
                    $('.tooltiptext2-tabela').css("display","block");    
                    }),
                    $('.tds-trs-' + element).mouseleave(function(){
                    $('.tds-trs-' + element).removeClass('tooltip2-tabela'),
                    $('.tooltiptext2-tabela').css("display","none");
                    })
                    // $('.a-clear-acao').removeAttr('href');
                }
                // SE A ORDEM/CODIGO NÃO POSSUIR CORREÇÕES
                else {

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

            if (situacao_do_plano == 'Em desenvolvimento' || situacao_do_plano == 'Publicado' || situacao_do_plano == 'Corrigido' || situacao_do_plano == 'Aprovado' || situacao_do_plano == 'Assinado' || situacao_do_plano == 'Inteiramente assinado' || situacao_do_plano == 'Finalizado' || situacao_do_plano == 'Necessita correção'){
                $(".desabilita-js").removeAttr('href'); // Desabilita alguns links
                $('.display-none').removeClass("display-none"); // Mostra mensagem que o plano nao pode ser alterado
                $('.botao-concluir-js').addClass("display-none"); // Esconde botão
                $('.mensagem-menu-js').addClass("display-none"); // Esconde mensagem
                $('.aviso-verde-menu-edicao-js').addClass("display-none"); // Esconde mensagem
                $('.botao-voltar-menu-edicao-js').addClass("display-none"); // Esconde botao
            }
            
        }else if (tipo_de_usuario == 'Diretor_escola'){

            if (situacao_do_plano == 'Pendente' || situacao_do_plano == 'Corrigido pela escola' || situacao_do_plano == 'Aprovado' || situacao_do_plano == 'Assinado' || situacao_do_plano == 'Finalizado'){
                $(".desabilita-js").removeAttr('href'); // Desabilita alguns links
                $('.display-none').removeClass("display-none"); // Mostra mensagens
            }

        }else if (tipo_de_usuario == 'Funcionario'){
            
        }

    // SITUAÇÕES EXTRAS

    if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Func_sec'){
            
    }else if (tipo_de_usuario == 'Diretor_escola'){

        if (situacao_do_plano == 'Em desenvolvimento' || situacao_do_plano == 'Publicado' || situacao_do_plano == 'Necessita correção'){
            // TOOLTIP MENU CRIAR ORDENS.
            showContext = $('.sinal-ordens-js').hover(function() {
                var e = window.event;
            
                var posX = e.clientX - 15;
                var posY = e.clientY - 39;
                var context = document.getElementById("id-tooltip5-menu")
                context.style.top = posY + "px";
                context.style.left = posX + "px";
                context.style.display = "block";

                $('.sinal-ordens-js').mouseleave(function(){
                $('.sinal-ordens-js').removeClass('tooltip5-menu');
                $('.tooltiptext5-tabela').css("display","none");
                })
            })

            // TOOLTIP MENU CRIAR CODIGOS
            $( lista_de_ordens ).each(function(index,element) {
                showContext = $('.sinal-codigos-js-' + element).hover(function() {
                    var e = window.event;
                
                    var posX = e.clientX - 15;
                    var posY = e.clientY - 39;
                    var context = document.getElementById("id-tooltip6-menu")
                    context.style.top = posY + "px";
                    context.style.left = posX + "px";
                    context.style.display = "block";
        
                    $('.sinal-codigos-js-'+ element).mouseleave(function(){
                    $('.sinal-codigos-js-'+ element).removeClass('tooltip6-menu'),
                    $('.tooltiptext6-tabela').css("display","none");
                    })
                })
            })
            
        }

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

    }else if (tipo_de_usuario == 'Funcionario'){
        
    }

    
})