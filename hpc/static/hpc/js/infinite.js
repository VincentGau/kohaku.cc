/**
 * Created by Kohaku on 3/17/2017.
 */

//get more articles from server
var page = 2;
var all_loaded = false;
function displayMore(){
    if(!all_loaded){
        $("article:last").after("<div class='row infinite-loading'><img class='loading-gif' src='static/hpc/img/loading-gif.gif' >");
        var url = "/infinite/?page=" + page;
        $.getJSON(url, function(data){
            //setTimeout(function(){
            //    if(data.end == 'true'){
            //        if(data.html != 'false'){
            //            $(data.html).insertAfter("article:last");
            //            $("div").remove(".infinite-loading");
            //        }
            //        var all_loaded_info = "<h4 style='text-align:center;margin-top:20px;'>No more articles.</h4>";
            //        $("article:last").after(all_loaded_info);
            //        all_loaded = true;
            //    }
            //    else{
            //        $(data.html).insertAfter("article:last");
            //        $("div").remove(".infinite-loading");
            //        //alert(data.page);
            //        page += 1;
            //        loading = false;
            //    }
            //},1000);

            if(data.end == 'true'){
                //indicate that all articles were displayed if data.end == 'true'
                if (data.html != 'false') {
                    //less than or equal pagesize articles this time, at least 1.
                    $(data.html).insertAfter("article:last");

                }
                $("div").remove(".infinite-loading");

                var all_loaded_info = "<h4 style='text-align:center;margin-top:20px;'>No more articles.</h4>";
                $("article:last").after(all_loaded_info);
                all_loaded = true;
            }
            else {
                $(data.html).insertAfter("article:last");
                $("div").remove(".infinite-loading");
                page += 1;
                loading = false;
            }
        });

    }
}

//ignore the scroll action when loading new articles
var loading = false;

//Scroll to top function, hide the icon if the scroll bar is less than 100px to top
$(function () {
    $(window).scroll(function () {
        if ($(window).scrollTop() > 100) {
            $("#scroll-to-top").fadeIn(200);
        }
        else {
            $("#scroll-to-top").fadeOut(200);
        }

        //display more articles when scroll to bottom(if not all articles were loaded)
        if (!all_loaded && $(this).scrollTop() + $(window).height() > $("#main-content").height() + $("#header-navigator").height() + $("#main-footer").height() - 10 && !loading) {
            loading = true;
            displayMore();
        }
    });
});