
const canvas = document.getElementById('canvas'),
coord = document.getElementById('coord'),
ctx = canvas.getContext('2d'); // get 2D context

// desenha linha de referencia
ctx.beginPath();
ctx.strokeStyle = 'rgb(9, 66, 172, 0.200)';
ctx.lineWidth = 0.5;
ctx.moveTo(0, 40);
ctx.lineTo(400, 40);
ctx.stroke();

// CÓDIGO PARA PEGAR POSIÇÃO DO MOSUE DENTRO DO CANVAS

function fixPosition(event, canvas) {
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    // console.log("x: " + x + " y: " + y)

    return {x: x, y:y};
}

// USA POSIÇÃO DO MOUSE PARA PINTAR O CANVAS
var mousedown = false;
ctx.strokeStyle = 'rgb(9, 66, 172)';
ctx.lineWidth = 0.1;
ctx.lineCap = 'round'
canvas.onmousedown = function(e) {
    var pos = fixPosition(e, canvas);
    mousedown = true;
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    return false;
};

canvas.onmousemove = function(e) {
    var pos = fixPosition(e, canvas);
    // coord.innerHTML = '(' + pos.x + ',' + pos.y + ')';
    if(mousedown){
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();
    }
};

canvas.onmouseup = function(e) {
    mousedown = false;
};

// LIMPA O CANVAS
$(".clear-canvas").click(function(){
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);

    // desenha linha de referencia
    ctx.beginPath();
    ctx.strokeStyle = 'rgb(9, 66, 172, 0.200)';
    ctx.lineWidth = 0.5;
    ctx.moveTo(0, 40);
    ctx.lineTo(400, 40);
    ctx.stroke();
    ctx.closePath();
});

function save_canvas(){
    var canvas = document.getElementById('canvas');
    document.getElementById('input_hidden_canvas').value = canvas.toDataURL('assinatura/png');
    document.forms["form-canvas"].submit();
}

// function save_canvas(){
//     var canvas = document.getElementById('canvas');
//     const file = dataURLtoBlob( canvas.toDataURL() );
//     document.getElementById('input_hidden_canvas').value = file
//     document.forms["form-canvas"].submit();
// }

// function dataURLtoBlob(dataURL) {
//     let array, binary, i, len;
//     binary = atob(dataURL.split(',')[1]);
//     array = [];
//     i = 0;
//     len = binary.length;
//     while (i < len) {
//       array.push(binary.charCodeAt(i));
//       i++;
//     }
//     return new Blob([new Uint8Array(array)], {
//       type: 'image/png'
//     });
//   };

