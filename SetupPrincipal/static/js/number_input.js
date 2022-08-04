$(document).ready(function(){

var inputBox = document.getElementById("id_codigo_escola");

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

})