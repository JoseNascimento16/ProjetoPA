// INFO EXTRA PLANOS



$(document).ready(function(){
    
    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);
    // var icone_seta = document.getElementById('icone-accordion');
    
    //if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Func_sec'){
        
        $(".icone-accordion").click(function(){ 
            
            $('.accordion-planos').slideUp(550),
            $('.cards-planos').removeClass('background-accordion-planos')
            if ($(".icone-accordion").hasClass('rotate-90')){
                $(".icone-accordion").removeClass('rotate-90')
            }
            // $(".icone-accordion").removeClass('rotate-90')
            // $(this).removeClass('rotate-90')
        });

        $(".icone-accordion").click(function(){ 

            $(this).closest("div").click(function(){
                if ($(this).next().is(":hidden")){
                    $(this).next().slideDown(550),
                    $(this).next().css('display','flex'),
                    $(this).removeClass('background-accordion-planos')
                    // sessionStorage.setItem("variable",1)
                }else{  } 
            })

            // let var1 = sessionStorage.getItem("variable");
            if ($(this).next().is(":visible") && $(this).not('.rotate-90')){
                $(this).addClass('rotate-90') // rotate-90 estao em avulsos.css
                // sessionStorage.setItem("variable",0)
                // $(this).querySelector('.icone-accordion').style.transform = "rotate(90deg)";
                // sessionStorage.setItem("variable",1)
            }
        });
        // $(this).addClass('rotate-90') // rotate-90 estao em avulsos.css

        

    // }else if (tipo_de_usuario == 'Escola'){
        
    // }else if (tipo_de_usuario == 'Funcionario'){
        
    //}
    
});

    