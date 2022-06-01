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
        $('#cart_toast').toast('show');
    }).fail(function (jqXHR, exception) {
        // Our error logic here
        var msg = '';
        if (jqXHR.status === 0) {
            msg = 'Not connect.\n Verify Network.';
        } else if (jqXHR.status == 404) {
            msg = 'Requested page not found. [404]';
        } else if (jqXHR.status == 500) {
            msg = 'Internal Server Error [500].';
        } else if (exception === 'parsererror') {
            msg = 'Requested JSON parse failed.';
        } else if (exception === 'timeout') {
            msg = 'Time out error.';
        } else if (exception === 'abort') {
            msg = 'Ajax request aborted.';
        } else {
            msg = 'Uncaught Error.\n' + jqXHR.responseText;
        }
        alert(msg);
    });
});