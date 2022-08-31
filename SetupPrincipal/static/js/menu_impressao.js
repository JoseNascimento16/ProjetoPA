// PAGINA AÇÕES
$(document).ready(function(){
    
    var quebra_linha = JSON.parse(document.getElementById('id-q-linha').textContent);
    var apos_print = JSON.parse(document.getElementById('id-apos-print').textContent);

    var lista_de_ordens = JSON.parse(document.getElementById('id-do-json').textContent);
    $( lista_de_ordens ).each(function(index,element) {

        var inputBox = document.getElementById("figure-ordem-" + element);

        var invalidChars = [ "-", "+", "e" ];

        inputBox.addEventListener("keydown", function(e) {
            if (invalidChars.includes(e.key)) {
                e.preventDefault();
            }
        inputBox.addEventListener('change', function(e) {
            if (e.target.value == '') {
                e.target.value = 0
            }
            })
        });
    });
    // *******************

    // ALTERNANCIA ENTRE MENUS EDIÇÃO/IMPRESSAO

    $(".icone-alternancia").click(function(){ 
        if ($(".menu-edicao").is(":visible")){
            $(".menu-edicao").addClass("display_none"),
            $(".menu-impressao-js").removeClass("display_none")
        }else{ 
            $(".menu-edicao").removeClass("display_none"),
            $(".menu-impressao-js").addClass("display_none")
        } 
    });
        // mantém menu impressão a mostra caso inseriu quebra de linha
    if (quebra_linha || apos_print){
        $(".menu-edicao").addClass("display_none"),
        $(".menu-impressao-js").removeClass("display_none")
    }
    // recarrega a página com um parametro adicionado à url 
    window.onafterprint = function(){
        window.location.href += "?postprint=conf";
    }

})

// PAGINA DESPESAS
$(document).ready(function(){
    
    var quebra_linha = JSON.parse(document.getElementById('id-q-linha').textContent);
    var apos_print = JSON.parse(document.getElementById('id-apos-print').textContent);

    var lista_de_codigos = JSON.parse(document.getElementById('id-lista-todos-codigos').textContent);
        $( lista_de_codigos ).each(function(index,element) {

            var inputBox = document.getElementById("figure-codigo-" + element);

            var invalidChars = [ "-", "+", "e" ];

            inputBox.addEventListener("keydown", function(e) {
                if (invalidChars.includes(e.key)) {
                    e.preventDefault();
                }
            inputBox.addEventListener('change', function(e) {
                if (e.target.value == '') {
                    e.target.value = 0
                }
                })
            });
        });
    // *******************

    // ALTERNANCIA ENTRE MENUS EDIÇÃO/IMPRESSAO

    $(".icone-alternancia").click(function(){ 
        if ($(".menu-edicao").is(":visible")){
            $(".menu-edicao").addClass("display_none"),
            $(".menu-impressao-js").removeClass("display_none")
        }else{ 
            $(".menu-edicao").removeClass("display_none"),
            $(".menu-impressao-js").addClass("display_none")
        } 
    });
        // mantém menu impressão a mostra caso inseriu quebra de linha
    if (quebra_linha || apos_print){
        $(".menu-edicao").addClass("display_none"),
        $(".menu-impressao-js").removeClass("display_none")
    }
    // recarrega a página com um parametro adicionado à url 
    window.onafterprint = function(){
        window.location.href += "?postprint=conf";
    }
})

// PAGINA FIA
$(document).ready(function(){
    
    var quebra_linha = JSON.parse(document.getElementById('id-q-linha').textContent);
    var apos_print = JSON.parse(document.getElementById('id-apos-print').textContent);

    var lista_de_ordens_extra = JSON.parse(document.getElementById('id-todas-ordens').textContent);
        $( lista_de_ordens_extra ).each(function(index,element) {

            var inputBox = document.getElementById("figure-ordem-fia-" + element);

            var invalidChars = [ "-", "+", "e" ];

            inputBox.addEventListener("keydown", function(e) {
                if (invalidChars.includes(e.key)) {
                    e.preventDefault();
                }
            inputBox.addEventListener('change', function(e) {
                if (e.target.value == '') {
                    e.target.value = 0
                }
                })
            });
        });
    // *******************

    // ALTERNANCIA ENTRE MENUS EDIÇÃO/IMPRESSAO

    $(".icone-alternancia").click(function(){ 
        if ($(".menu-edicao").is(":visible")){
            $(".menu-edicao").addClass("display_none"),
            $(".menu-impressao-js").removeClass("display_none")
        }else{ 
            $(".menu-edicao").removeClass("display_none"),
            $(".menu-impressao-js").addClass("display_none")
        } 
    });
        // mantém menu impressão a mostra caso inseriu quebra de linha
    if (quebra_linha || apos_print){
        $(".menu-edicao").addClass("display_none"),
        $(".menu-impressao-js").removeClass("display_none")
    }
    // recarrega a página com um parametro adicionado à url 
    window.onafterprint = function(){
        window.location.href += "?postprint=conf";
    }
})