function getCookie(name) {
    // this gets the csrf token from the page
    // https://docs.djangoproject.com/en/3.0/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    // adds the csrf token to the headers of each AJAX request
    // https://docs.djangoproject.com/en/3.0/ref/csrf/#setting-the-token-on-the-ajax-request
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$('.like-button').on("click", function(event){
    event.preventDefault();
    var answerBtn = $(this);
    var likeUrl = answerBtn.attr("href");
    var answerID = answerBtn.attr("answer-id");
    var currentLikeNumber = parseInt(answerBtn.children('span').text());
    $.ajax({
        url: likeUrl,
        method: "POST",
        data: {
            "answer_id": answerID
        },
        success: function(data){
            console.log('success');
            if (data.liked) {
                answerBtn.children('span').text(currentLikeNumber + 1);
                //answerBtn.activate('toggle');
            }
            else {
                answerBtn.children('span').text(currentLikeNumber - 1);
                //answerBtn.activate('off')
            }
        },
        error: function(error){
            console.log('error');
            console.log(error);
        }
    })
 });
