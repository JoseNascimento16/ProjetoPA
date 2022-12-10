$(document).ready(function(){

    $('.wrapper p').each(function() {
        var $this = $(this);
        var text = $this.text();
        var newText = text.slice(0,45);
        
        $this.html(newText);
        
    });

    $('.wrapper p').css("color","red");
    $('.fa-cog').css("color","red");
})