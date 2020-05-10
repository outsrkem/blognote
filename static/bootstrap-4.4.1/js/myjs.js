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
       if (data == 'email-invalid'){
            bootbox.alert({title:"错误提示", message:"邮箱地址格式不正确."});
            return false;
        }
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


// 用户注册
function doReg(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    regname = $.trim($("#regname").val());
    regpass = $.trim($("#regpass").val());
    regcode = $.trim($("#regcode").val());
    if (!regname.match(/.+@.+\..+/) || regpass.length < 6) {
        bootbox.alert({title:"错误提示", message:"注册邮箱不正确或密码少于5位."});
        return false;
    }
    else {
        // 构建POST请求的正文数据
        param = "username=" + regname;
        param += "&password=" + regpass;
        param += "&ecode=" + regcode;
        // 利用jQuery框架发送POST请求，并获取到后台注册接口的响应内容
        $.post('/user/reg', param, function (data) {
            if (data == "ecode-error") {
                bootbox.alert({title:"错误提示", message:"验证码无效."});
                $("#regcode").val('');  // 清除验证码框的值
                $("#regcode").focus();   // 让验证码框获取到焦点供用户输入
            }
            else if (data == "user-repeated") {
                bootbox.alert({title:"错误提示", message:"该用户名已经被注册."});
                $("#regname").focus();
            }
            else if (data == "reg-pass") {
                bootbox.alert({title:"信息提示", message:"恭喜你，注册成功."});
                // 注册成功后，延迟1秒钟重新刷新当前页面即可
                setTimeout('location.reload();', 1000);
            }
            else if (data == "reg-fail") {
                bootbox.alert({title:"错误提示", message:"注册失败，请联系管理员."});
            }
            else {
                // 如果是其他信息，则极有可能是验证器响应的内容
                bootbox.alert({title:"错误提示", message: data});
            }
        });
    }
}


// 显示模态框中的登录面板
function showLogin(e) {
    if (e!=null && e.keyCode !=13){
        return false;
    }
    $("#login").addClass("active");
    $("#reg").removeClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").addClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").removeClass("active");
    $('#mymodal').modal('show');
}

//  显示模态框中的注册面板
function showReg() {
    $("#login").removeClass("active");
    $("#reg").addClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").addClass("active");
    $("#findpanel").removeClass("active");
    $('#mymodal').modal('show');
}

//  显示模态框中的找回密码面板
function showReset() {
    $("#login").removeClass("active");
    $("#reg").removeClass("active");
    $("#find").addClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").addClass("active");
    $('#mymodal').modal('show');
}
