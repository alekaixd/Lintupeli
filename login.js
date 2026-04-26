const button = document.getElementsById("send");
button.addEventListener('click', function(){
    value = button.valueOf();

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