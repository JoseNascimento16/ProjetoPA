// INFO EXTRA PLANOS



$(document).ready(function(){
    
    var tipo_de_usuario = JSON.parse(document.getElementById('id-tipo-usuario').textContent);

    if (tipo_de_usuario == 'Secretaria' || tipo_de_usuario == 'Func_sec'){
        
        

    }else if (tipo_de_usuario == 'Diretor_escola'){
        
    }else if (tipo_de_usuario == 'Funcionario'){
        
    }

    $(".icone-accordion").click(function(){ 
        $('.accordion-planos').slideUp(550),
        $('.cards-planos').removeClass('background-accordion-planos') 
    });
    
    });
  
    $(document).ready(function(){
        $(".icone-accordion").click(function(){ 
            $(this).closest("div").click(function(){
                if ($(this).next().is(":hidden")){
                    $(this).next().slideDown(550),
                    $(this).addClass('background-accordion-planos') 
                }else{ 
                    // $(this).next().slideDown(550)
                } 
        
        })

    })

});

    