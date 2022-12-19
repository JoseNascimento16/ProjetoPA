// INFO EXTRA PLANOS

$(document).ready(function(){
    
    // var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
        
        $(".icone-accordion").click(function(){ 

            // EXECUTA O ACCORDION
            $('.accordion-planos').slideUp(550),
            $('.cards-planos').removeClass('background-accordion-planos')

            if ($(this).closest(".cards-planos").next().is(":hidden")){
                $(this).closest(".cards-planos").next().slideDown(550)
            }
            // ----------------------------------

            // ROTACIONA AS SETINHAS
            if($(this).hasClass('rotate-90')){
                $(this).removeClass('rotate-90')
            }else{
                $('.rotate-90').removeClass('rotate-90')
                $(this).addClass('rotate-90')
            }
            // -----------------------------
            
        });
            
            // if ($(this).next().is(":visible") && $(this).not('.rotate-90')){
            //     $(this).addClass('rotate-90') // rotate-90 estao em avulsos.css
            // }

            // if ($(this).closest(".cards-planos").next().is(":visible")){
            //     $(this).addClass('rotate-90')
            // }

});

    