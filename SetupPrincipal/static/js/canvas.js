
const canvas = document.getElementById('canvas'),
coord = document.getElementById('coord'),
ctx = canvas.getContext('2d'); // get 2D context

// desenha linha de referencia
ctx.beginPath();
ctx.strokeStyle = 'rgb(9, 66, 172)';
ctx.lineWidth = 0.5;
ctx.moveTo(0, 57.5);
ctx.lineTo(400, 57.5);
ctx.stroke();

/*********** handle mouse events on canvas **************/
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

/********** utils ******************/
// Thanks to http://stackoverflow.com/questions/55677/how-do-i-get-the-coordinates-of-a-mouse-click-on-a-canvas-element/4430498#4430498
// function fixPosition(e, gCanvasElement) {
//     var x;
//     var y;
//     if (e.pageX || e.pageY) { 
//       x = e.pageX;
//       y = e.pageY;
//     }
//     else { 
//       x = e.clientX + document.body.scrollLeft +
//           document.documentElement.scrollLeft;
//       y = e.clientY + document.body.scrollTop +
//           document.documentElement.scrollTop;
//     } 
//     x -= gCanvasElement.offsetLeft;
//     y -= gCanvasElement.offsetTop;
//     // x -= 256;
//     // y -= 311;
//     // x -= 332;
//     // y -= 135;
//     return {x: x, y:y};
// }

// OUTRA SOLUÇÃO PARA PEGAR POSIÇÃO

function fixPosition(event, canvas) {
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    // console.log("x: " + x + " y: " + y)

    return {x: x, y:y};
}

// LIMPA O CANVAS
$(".clear-canvas").click(function(){
    const context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);

    // desenha linha de referencia
    ctx.beginPath();
    ctx.strokeStyle = 'rgb(9, 66, 172)';
    ctx.lineWidth = 0.5;
    ctx.moveTo(0, 57.5);
    ctx.lineTo(400, 57.5);
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

