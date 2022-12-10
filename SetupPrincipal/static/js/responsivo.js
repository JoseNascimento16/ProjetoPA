$(document).ready(function(){

    $('.wrapper i').each(function() {
        var $this = $(this);
        var text = $this.text();
        var newText = text.slice(0,45);
        
        $this.html(newText);
        
    });

    $('.titulo-wrapper i').each(function() {
        var $this = $(this);
        var text = $this.text();
        var newText = text.slice(0,45);
        
        $this.html(newText);
        
    });

})