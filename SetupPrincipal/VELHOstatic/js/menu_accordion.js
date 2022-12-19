// MENU LATERAL
$(document).ready(function(){
  $(".item-principal-menu").click(function(){ $(".sub-menu").slideUp(400) });
});

$(document).ready(function(){
  $(".item-principal-menu").click(function(){ if ($(this).next().is(":visible")){
    $(this).next().slideUp(400)
  }else{ $(this).next().slideDown(400) } })
  });

// MENU EDIÇÃO
// $(document).ready(function(){
//   $(".item-principal-menu-edicao").click(function(){ $(".sub-menu-edicao").slideUp(400) });
// });

// $(document).ready(function(){
//   $(".item-principal-menu-edicao").click(function(){ if ($(this).next().is(":visible")){
//     $(this).next().slideUp(400)
//   }else{ $(this).next().slideDown(400) } })
//   });

$(document).ready(function(){
  $(".item-principal-menu-edicao").click(function(){ $(".sub-menu-edicao").slideUp(400) });
});

$(document).ready(function(){
  $(".ordens-menu").click(function(){
    if ($('.sub-menu-edicao-ordens').is(":visible")){
    $('.sub-menu-edicao-ordens').slideUp(400)
    }else{ 
    $('.sub-menu-edicao-ordens').slideDown(400)
    } 
  })

  $(".codigos-menu").click(function(){
    if ($('.sub-menu-edicao-codigos').is(":visible")){
    $('.sub-menu-edicao-codigos').slideUp(400)
    }else{ 
    $('.sub-menu-edicao-codigos').slideDown(400)
    } 
  })

  $(".turmas-menu").click(function(){
    if ($('.sub-menu-turmas-edicao').is(":visible")){
    $('.sub-menu-turmas-edicao').slideUp(400)
    }else{ 
    $('.sub-menu-turmas-edicao').slideDown(400)
    } 
  })
  
});