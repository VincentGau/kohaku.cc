/**
 * Created by Kohaku on 3/8/2017.
 */

//search function, called when Enter pressed
$("input").keydown(function (e) {
    if (e.keyCode == 13) {
        var content = document.getElementById("search-text").value;
        window.location.href = '/search/?q=' + content;
    }
});

//search function, called when search-btn clicked
$("#search-btn").click(function () {
    var content = document.getElementById("search-text").value;
    window.location.href = '/search/?q=' + content;

});

//toggle icon style when mouse hover
$("#scroll-to-top").click(function () {
    $('body,html').animate({scrollTop: 0}, 500);
}).hover(function () {
    $("#scroll-to-top").toggleClass("scroll-top-dark");
});

//Scroll to top function, hide the icon if the scroll bar is less than 100px to top
$(function () {
    $(window).scroll(function () {
        if ($(window).scrollTop() > 100) {
            $("#scroll-to-top").fadeIn(200);
        }
        else {
            $("#scroll-to-top").fadeOut(200);
        }


    });
});

function validate_form() {
    email_field = document.getElementById("id_email").value;
    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;

    if (reg.test(email_field) == true) {
        //alert("TRUE");
        return true;
    }
    else {
        $("#id_email").focus();
        //alert("False");
        return false;
    }
}

function show_reply_form(event) {
    var $this = $(this);
    var comment_id = $this.data('comment-id');
    $('#id_parent').val(comment_id);
    //$('#id_comment').val("Re: ");
    $('#id_comment').attr('placeholder',"Re: ");
    $('#form-comment').insertAfter($this.closest('.comment'));
}
function cancel_reply_form(event) {
    $('#id_comment').val('');
    $('#id_parent').val('');
    $('#id_comment').val('');
    $('#form-comment').appendTo($('#wrap_write_comment'));
}
$.fn.ready(function () {
    $('.comment_reply_link').click(show_reply_form);
    $('#cancel_reply').click(cancel_reply_form);
});


