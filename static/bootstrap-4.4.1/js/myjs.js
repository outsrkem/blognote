function doSendMail(obj) {
    var email = $.trim($("#regname").val());
    // 使用正则表达式验证邮箱地址格式是否正确
    if (!email.match(/.+@.+\..+/)) {
        bootbox.alert({title:"错误提示", message:"邮箱地址格式不正确."});
        $("#regname").focus();
        return false;
    }
    $(obj).attr('disabled', true);     // 发送邮件按钮变成不可用
    $.post('/ecode', 'email=' + email, function (data) {
        if (data == 'send-pass') {
            bootbox.alert({title:"信息提示", message:"邮箱验证码已成功发送，请查收."});
            $("#regname").attr('disabled', true);   // 验证码发送完成后禁止修改注册邮箱
            $(obj).attr('disabled', true);
            return false;
        }
        else {
            bootbox.alert({title:"错误提示", message:"邮箱验证码发送失败."});
            return false;
        }
    });
}