$(document).ready(function(){

    // $(".engrenagem").click(function(){ 
    //     $(".dash-inicio").css("display","flex")
    // });

    $(".engrenagem").click(function(){ if ($(this).next().is(":visible")){
        $('.dash-inicio').slideUp(400)
        $('.dash-sair').slideUp(400)
        $('.engrenagem').slideUp(400)
      }else{ 
        $('.dash-inicio').slideDown(400)
        $('.dash-sair').slideDown(400)
        $('.engrenagem').slideUp(400)
      }
    })

});