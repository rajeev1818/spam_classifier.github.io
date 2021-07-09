let data=document.getElementById("data");
let button=document.getElementById("submitButton");
let result=document.getElementById("result");
let errMsg=document.getElementById("errMsg");

function showResult(data){
    result.textContent="";
    result.classList.remove("result");
    if(data==="1.0"){
        result.textContent="It's a Spam";
        result.classList.add("result");
    }
    else{
        result.classList.add("result");
        result.textContent="It's not a Spam";
    }
    
}


button.addEventListener("click",(event)=>{
    event.preventDefault();
    result.textContent="";
    result.classList.remove("result");
    let url="https://beware-spammers.herokuapp.com/predict/";
    if(data.value===""){
        errMsg.textContent="Required*";
    }
    else{
        errMsg.textContent="";
        let obj={
            "data":data.value,
        }
        data.value="";
        let options = {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body:JSON.stringify(obj),
        };
    
        fetch(url,options)
        .then((response)=>{
            return response.json();
        })
        .then((final)=>{
            showResult(final["prediction"]);
        });
    }
    
});