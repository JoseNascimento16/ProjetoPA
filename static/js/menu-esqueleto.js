$("#teste > a").click(function(e) {
    $(".sub-menu").slideUp(), $(this).next().is(":visible") || $(this).next().slideDown(),
    e.stopPropagation()
  })