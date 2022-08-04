// RE-ABILITA OS CAMPOS DISABLED ANTES DO SUBMIT DO FORM, PARA EVITAR ERROS DE VALIDAÇÃO
$(document).ready(function(){

    $('#form_correcao_acao').submit(function(){
        $("#form_correcao_acao :disabled").removeAttr('disabled');
    });

    $('#form_correcao_despesa').submit(function(){
        $("#form_correcao_despesa :disabled").removeAttr('disabled');
    });

    $('#form_corrigindo_acao').submit(function(){
        $("#form_corrigindo_acao :disabled").removeAttr('disabled');
    });

    $('#form_corrigindo_despesa').submit(function(){
        $("#form_corrigindo_despesa :disabled").removeAttr('disabled');
    });

    // $('#form_corrigindo_acao').submit(function(){
    //     $("#form_corrigindo_acao").prop('disabled', false);
    // });

});