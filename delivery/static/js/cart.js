$(".btn-offer").click(function () {
    let form = $(this).parent().parent();
    let id = $(this).data("id");
    let quantity = form.find(".form-control").val();
    let payload = {"offer": id, "quantity": quantity}
    $.ajax({
        url: "/cart/manage/",
        method: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(payload),
    }).done(function () {
        let msg = "Позиция добавлена в корзину";
        $('#cart_toast').find('.toast-body').text(msg);
        $('#cart_toast').toast('show');
        form.empty();
        form.html("<div class=\"text-center\">"+msg+"</div>")

    }).fail(function (jqXHR, exception) {
        // Our error logic here
        var msg = '';
        if (jqXHR.status === 0) {
            msg = 'Not connect.\n Verify Network.';
            alert(msg);
        } else if (jqXHR.status == 400) {
            let response = JSON.parse(jqXHR.responseText);
            $('#cart_toast').find('.toast-body').text(response.msg);
            $('#cart_toast').toast('show');
        } else {
            msg = 'Uncaught Error.\n' + jqXHR.responseText;
            alert(msg);
        }

    });
});

