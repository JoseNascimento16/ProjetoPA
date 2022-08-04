// MANTÉM O SCROLL DA JANELA

$(document).ready(function(){
var pos = localStorage.getItem('my-scroll-pos', 0); // busca o valor da posicao do scrol salva em my-scroll-pos
if (pos)
    $(window).scrollTop(pos) // se houver informação seta a posição do scrol da janela PRINCIPAL
});

$(document).ready(function(){
    $(".sub-menu-item-edicao").click(function(){ localStorage.setItem('my-scroll-pos', $(window).scrollTop()) }); // Ao clicar em ".sub-menu-item-edicao", salva a posição do scroll em um item "my-scroll-pos" no localStorage
  });



// MANTÉM O SCROLL DO MENU EDIÇÃO
$(document).ready(function(){
    var pos = localStorage.getItem('my-scroll-pos2', 0); // busca o valor da posicao do scrol salva em my-scroll-pos2
    if (pos)
        $(".classe-div-menu-lateral-edicao").scrollTop(pos)  // se houver informação seta a posição do scrol da janela de classe ".classe-div-menu-lateral-edicao"
    });
    
    $(document).ready(function(){
        $(".sub-menu-item-edicao").click(function(){ localStorage.setItem('my-scroll-pos2', $(".classe-div-menu-lateral-edicao").scrollTop()) }),
        $(".sub-menu-item-codigos-edicao").click(function(){ localStorage.setItem('my-scroll-pos2', $(".classe-div-menu-lateral-edicao").scrollTop()) });
      });