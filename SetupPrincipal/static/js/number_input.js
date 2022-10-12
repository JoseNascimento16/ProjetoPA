$(document).ready(function(){

var inputBox = document.getElementById("id_codigo_escola");
var inputBox2 = document.getElementById("id_nte");
// coloca os ids dos campos nm array
const var_inputs = [inputBox, inputBox2];
    // varre o array e aplica as restrições em cada campo
    $( var_inputs ).each(function(index,element) {

        var invalidChars = [ "-", "+", "e" ];

        element.addEventListener("keydown", function(e) {
            if (invalidChars.includes(e.key)) {
                e.preventDefault();
            }
        element.addEventListener('change', function(e) {
            if (e.target.value == '') {
                e.target.value = 0
            }
            })
        });

    });

})