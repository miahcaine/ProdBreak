$(".task").find("a").css("visibility", "hidden");

$(".task").mouseover(function (){
    $(this).find("a").css("visibility", "visible");
});

$(".task").mouseout(function (){
    $(this).find("a").css("visibility", "hidden");
});