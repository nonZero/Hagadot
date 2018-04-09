$(function () {
    'use strict';

    const fix = x => x.toFixed(1);

    const createDialog = html => {
        const modal = $("<dialog/>").appendTo($('body')).html(html);
        modal.show().get(0).showModal();
        return modal;
    };

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

    const pageImg = $(".page-img");

    $('.add-an').click(function () {
        pageImg.toggleClass('add');
        $(this).toggleClass('active');
        return false;
    });

    pageImg.on('click', '.an', function () {
        if (posData) {
            return true;
        }
        const el = $(this);
        const modal = createDialog(el.find(".c").html());
        modal.find(".edit-ann").click(function () {
            modal.load($(this).attr('href')).html("Loading...");
            return false;
        });
        modal.on('cancel', (e) => {
            modal.hide().html("").get(0).close();
        });
        modal.on('click', '.close-dialog', () => {
            modal.hide().html("").get(0).close();
            return false;
        });
        modal.on('click', '.delete', () => {
            return confirm("Delete?");
        });
        return false;
    });

    pageImg.parent().on('click', '.add', e => {
        pageImg.removeClass('add');
        $('.add-an').removeClass('active');
        const x = (e.pageX - pageImg.offset().left) / pageImg.innerWidth() * 100;
        const y = (e.pageY - pageImg.offset().top) / pageImg.innerHeight() * 100;

        const marker = $(".marker");

        marker.show().css({
            top: y + "%",
            left: x + "%",
        });
        $.get(marker.data('url'), html => {
            const modal = createDialog(html);
            modal.html(html);
            modal.on('cancel', (e) => {
                modal.hide().get(0).close();
                $(".marker").hide();
            });
            modal.on('click', '.close-dialog', () => {
                modal.hide().get(0).close();
                $(".marker").hide();
                return false;
            });
            modal.find("#id_x").val(fix(x));
            modal.find("#id_y").val(fix(y));
            modal.find(".close").click(() => {
                modal.hide().get(0).close();
                $(".marker").hide();
            });

        });
    });

    let isDragging = false, dragX, dragY, an, pos, posData;

    pageImg.filter('.edit').on('mousedown', '.an', function (e) {
        isDragging = false;
        dragX = e.pageX;
        dragY = e.pageY;
        an = $(this);
        pos = an.position();
        posData = null;
        e.stopPropagation();
        return false;
    }).mousemove(function (e) {
        if (!dragX) {
            return;
        }
        const dx = e.pageX - dragX;
        const dy = e.pageY - dragY;

        // Check drag move threshold:
        isDragging = isDragging | Math.abs(dx) + Math.abs(dy) > 10;
        if (isDragging) {
            const left = Math.min(Math.max(0, pos.left + dx), pageImg.width());
            const top = Math.min(Math.max(0, pos.top + dy), pageImg.height());
            an.css({
                left: left + "px",
                top: top + "px",
            }).addClass('dragging');
            posData = {
                x: fix(left / pageImg.width() * 100),
                y: fix(top / pageImg.height() * 100),
            };
        }

        return false;
    });

    $(document).on('mousemove mouseup', e => {
        if (dragX && e.buttons === 0) {
            an.removeClass('dragging');
            if (posData) {
                $.post(an.data('url'), posData)
                    .fail(() => alert("An error occurred! Please refresh the page"));
            }
            dragX = null;
            dragY = null;
            return false;
        }
    });

});
