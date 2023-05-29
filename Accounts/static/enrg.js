function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$("#subm").click(function() {
    $.ajax({
        url:"/api/register/",
        type:"POST",
        headers:{
          'X-CSRFToken': csrftoken
        },
        data:JSON.stringify({
          Email : $("#email").val(),
          Password : $("#password").val(),
          Group : $("#idp").is(":checked") ? "Patient" : "Nurse"
        }),
        dataType:"json",
        contentType: 'application/json; charset=utf-8'
      })
})