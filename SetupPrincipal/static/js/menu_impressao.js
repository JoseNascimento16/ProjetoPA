$(document).ready(function(){

    var lista_de_ordens = JSON.parse(document.getElementById('id-do-json').textContent);

    $( lista_de_ordens ).each(function(index,element) {

        // $("#mais-ordem-"+ element).click(function(){
        //     num = parseInt($("#figure-ordem-"+ element).text());
        //     if (num < 10){
        //         $("#figure-ordem-"+ element).text(num+1);
        //     }
        // })

        // $("#menos-ordem-"+ element).click(function(){
        //     num = parseInt($("#figure-ordem-"+ element).text());
        //     if (num > 0){
        //         $("#figure-ordem-"+ element).text(num-1);
        //     }
        // })

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

    

})