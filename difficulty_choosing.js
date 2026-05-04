const birds = document.querySelectorAll(".bird")

for (let bird of birds){
    bird.addEventListener("click", function(){
        let info = bird.value
        console.log(info)
    })
}