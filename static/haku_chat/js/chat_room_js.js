/**
 * Created by Kohaku on 5/29/2017.
 */


// socket 消息格式 flag&username&content
// flag 取值为 0|1|2， 0表示新用户加入，1表示用户离开，2表示用户发送消息
// 如果flag 取值为 0或1，content内容为在线用户列表，如果flag 取值为2， content为发送的消息内容

$(document).ready(function () {
    socket = new WebSocket("wss://" + window.location.host + "/chat/");
    //socket = new WebSocket("wss://kohaku.cc/chat/");
    username = $("#username").text();

    socket.onopen = function () {
        var arr = new Array(3);
        arr[0] = "0";
        arr[1] = username;
        arr[2] = "";
        var msg = arr.join("&");
        socket.send(msg);
    };

    socket.onmessage = function (e) {
        decode_msg = e.data.split("&");
        var flag = decode_msg[0];
        if (flag == "0" || flag == "1"){
            //user join or leave
            var users = decode_msg[2].split('#');
            var ul_html_str = "";
            for (var i in users){
                ul_html_str += "<li class='user-list-user'>" + users[i] + "</li>";
                $("#user-list").html(ul_html_str);
            }
        }

        else if (flag == "2"){
            //user message
            new_item = "<div class='message_item'>" + decode_msg[1] + ":" + decode_msg[2] + "</div>";
            $("#message_box").append(new_item);
        }

    };
});

window.onbeforeunload=function(){
    var arr = new Array(3);
    arr[0] = "1";
    arr[1] = username;
    arr[2] = "";
    var msg = arr.join("&");
    socket.send(msg);
};


function send_message() {
    var message_content = $("#message_to_be_sent").val();
    var arr = new Array(3);
    arr[0] = "2";
    arr[1] = username;
    arr[2] = message_content;
    var msg = arr.join("&");
    socket.send(msg);

}