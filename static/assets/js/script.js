$(document).ready(function() {
    $('.answer-text').click(function(e) {
        var $currentElement = $(this);
        console.log($currentElement.attr("answer"));
        $('#id_answer').val($currentElement.attr("answer"));
        $('.answer-text').css("background-color", ""); // Oldingi hamma divlarni rangsiz qilamiz
        $('.answer-text').css("color", ""); // Oldingi hamma divlarni rangsiz qilamiz
        $currentElement.css("background-color", "#FCC822");
        $currentElement.css("color", "white");
    });
});