$(function () {
    'use strict';

    const fix = x => x.toFixed(1);

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

    const mainDialog = $("#main-dialog");

    mainDialog.on('click', '.close-dialog', () => {
        mainDialog.hide().get(0).close();
        return false;
    });

    const pageImg = $(".page-img");

    let getXY = function (e) {
        const x = (e.pageX - pageImg.offset().left) / pageImg.innerWidth() * 100;
        const y = (e.pageY - pageImg.offset().top) / pageImg.innerHeight() * 100;
        return [x, y];
    };

    let dragX, dragY, an, pos, posData;

    pageImg.on('mousedown', '.an .handle', function (e) {
        dragX = e.pageX;
        dragY = e.pageY;
        an = $(this).closest('.an');
        pos = an.position();
        e.stopPropagation();
        return false;
    });

    // pageImg.on('mousedown mouseup', '.an', function (e) {
    //     return false;
    // });

    pageImg.mousemove(function (e) {
        if (!dragX) {
            return;
        }
        const dx = e.pageX - dragX;
        const dy = e.pageY - dragY;
        const left = Math.min(Math.max(0, pos.left + dx), pageImg.width() - an.width());
        const top = Math.min(Math.max(0, pos.top + dy), pageImg.height() - an.height());
        an.css({
            left: left + "px",
            top: top + "px",
        });
        const x0 = left / pageImg.width() * 100;
        const y0 = top / pageImg.height() * 100;
        posData = {
            x0: fix(x0),
            y0: fix(y0),
            x1: fix(x0 + (an.width() / pageImg.width() * 100)),
            y1: fix(y0 + (an.height() / pageImg.height() * 100))
        };
        return false;
    });

    // pageImg.on('mouseup', '.an .handle', function (e) {
    //     savePos();
    //     dragX = false;
    //     dragY = false;
    //     return false;
    // });

    // pageImg.on('click', '.an .handle', function (e) {
    //     return false;
    // });
    //

    pageImg.on('click', '.an', function () {
        if (dragX) {
            return true;
        }
        const el = $(this);
        mainDialog.html(el.find(".c").html());
        mainDialog.find(".edit-ann").click(function () {
            mainDialog.load($(this).attr('href')).html("Loading...");
            return false;
        });
        mainDialog.show().get(0).showModal();
    });

    let startX, startY;

    pageImg.on('mousedown', e => {
        [startX, startY] = getXY(e);
        return false;
    });

    pageImg.on('mousemove', e => {
        if (!startX) {
            return;
        }
        const [x, y] = getXY(e);

        $(".marker").show().css({
            top: Math.min(startY, y) + "%",
            left: Math.min(startX, x) + "%",
            width: Math.abs(x - startX) + "%",
            height: Math.abs(y - startY) + "%",
        });
    });

    let savePos = function () {
        $.post(an.data('url'), posData)
            .done(() => console.log("OK"))
            .fail(() => alert("FAIL"));
    };
    $(document).on('mousemove mouseup', e => {
        if (startX && e.buttons === 0) {
            startX = null;
            startY = null;
            $(".marker").hide();
            return false;
        }
        if (dragX && e.buttons === 0) {
            savePos();
            dragX = null;
            dragY = null;
            return false;
        }
    });


    pageImg.on('mouseup', e => {
        if (dragX) {
            return true;
        }
        if (!startX) {
            return true;
        }
        const [endX, endY] = getXY(e);
        const x0 = fix(Math.min(startX, endX));
        const y0 = fix(Math.min(startY, endY));
        const x1 = fix(Math.max(startX, endX));
        const y1 = fix(Math.max(startY, endY));
        // Check annotation minimal size
        if (Math.abs(endX - startX) > 8 && Math.abs(endY - startY) > 8) {
            $.get($(".marker").data('url'), html => {
                const modal = $("<dialog/>").appendTo($('body')).html(html);
                modal.find("#id_x0").val(x0);
                modal.find("#id_y0").val(y0);
                modal.find("#id_x1").val(x1);
                modal.find("#id_y1").val(y1);
                modal.find(".close").click(() => {
                    modal.hide().get(0).close();
                    $(".marker").hide();
                });
                modal.get(0).showModal();
            });
        } else {
            $('.marker').hide();
        }
        startX = null;
        startY = null;

        return false;
    });

});
