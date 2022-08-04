function printDiv(imprimir) {
    var printContents = document.getElementById('imprimir').innerHTML;
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;
    $('#impressao').addClass("display-none");
    $('.a-impressao').addClass("a-black").css("text-decoration","none");
    $('.impressao-none').addClass("display-none");
    $('.tr-extra').removeClass("display-none");
    window.print();

    document.body.innerHTML = originalContents;
}

// $(document).ready(function(){
//     $("#impressao").click(function(){
//     $('.noprint').addClass("display-none");

//       window.print();

//     })
    
//   });

// $(document).ready(function printData(){
//    var divToPrint=document.getElementById("imprimir");
//    newWin= window.open("");
//    newWin.document.write(divToPrint.innerHTML);
//    newWin.print();
//    newWin.close();

// });
// $('.impressao').on('click',function(){
//     printData();
//     })

// function printDiv(imprimir) {
//     //Get the HTML of div
//     var divElements = document.getElementById(imprimir).innerHTML;
//     //Get the HTML of whole page
//     var oldPage = document.body.innerHTML;
//     //Reset the page's HTML with div's HTML only
//     document.body.innerHTML = 
//       "<html><head><title></title></head><body>" + 
//       divElements + "</body>";
//     //Print Page
//     $('#impressao').addClass("display-none");
//     window.print();
//     //Restore orignal HTML
//     document.body.innerHTML = oldPage;

// }