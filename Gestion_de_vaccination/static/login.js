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

$("#diverror").hide()
$("#submit_b").click(function() {
  $.ajax({
    url:"/api/login/",
    type:"POST",
    headers:{
      'X-CSRFToken': csrftoken
    },
    data:JSON.stringify({
      Email : $("#email").val(),
      Password : $("#password").val()
    }),
    contentType: 'application/json; charset=utf-8',
    dataType:"json",
    success: function() {document.location.href = "/"},
    error: function(xhr) {
      $("#error").html(JSON.parse(xhr.responseText)["message"])
      $("#diverror").show()
    }
  })
})