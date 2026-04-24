const buttons = document.getElementsByClassName("login");
buttons.addEventListener('click', function(){
    value = buttons.valueOf();

    function sendData() {
        $.ajax({
            url: '/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'value': value}),
            success: function(response) {
                document.getElementById('output').innerHTML = response.result;
            },
            error: function(error){
                console.log(error);
            }
        });
    }
})