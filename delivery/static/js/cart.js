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
        form.html("<div class=\"text-center\">" + msg + "</div>")

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

$(".quantity-input").bind('keyup mouseup', function () {
    let item_input = $(this);
    let itemid = $(this).data("itemid");
    let input_val = $(this).val();
    let payload = {"offer": itemid, "quantity": input_val}
    $.ajax({
        url: "/cart/manage/",
        method: "PUT",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(payload),
    }).done(function (data) {
        let q = data.cart_item.quantity;
        let total = data.cart_item.total;
        let cart_total = data.cart_total;
        console.log(q + " " +  total +  " " +  cart_total);
        item_input.parent().parent().find('.cart_item_price').text(total);
        $('.cart_price').text(cart_total);
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