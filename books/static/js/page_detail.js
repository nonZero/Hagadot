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
        console.log('refresh');
        refresh();
    });

    // $(".save-page").on('submit', function () {
    //     console.log($(this));
    //     const start = $(this).find(".radio-start:checked");
    //     const end = $(this).find(".radio-end:checked");
    //     return false;
    // });


});
