$(document).ready(function(){
    $(".item-principal-menu").click(function(){ $(".sub-menu").slideUp(400) });
  });
  
  $(document).ready(function(){
    $(".item-principal-menu").click(function(){ if ($(this).next().is(":visible")){
      $(this).next().slideUp(400)
    }else{ $(this).next().slideDown(400) } })
    });