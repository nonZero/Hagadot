$(function () {
    'use strict';

    const isValid = () => {
        const startEl = $(this).find(".radio-start:checked");
        const endEl = $(this).find(".radio-end:checked");
        if (!startEl.length || !endEl.length) {
            return false;
        }
        return startEl.val() <= endEl.val();
    };

    const refresh = () => {
        $(".save-page button").attr('disabled', !isValid());
    };

    refresh();

    $(".save-page").on('change', 'input', function () {
        refresh();
    });

    const mainDialog = $("#main-dialog").click(() => mainDialog.hide().get(0).close());

    $(".page-img").on('click', '.an', function () {
        const el = $(this);
        mainDialog.html(el.find(".c").html());
        mainDialog.show().get(0).showModal();
    })

});
