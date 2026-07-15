async function registerUser(){

    const name =
    document.getElementById("name").value.trim();

    const email =
    document.getElementById("email").value.trim();

    const password =
    document.getElementById("password").value;

    if(!name || !email || !password){

        alert("Please fill all fields.");

        return;

    }

    try{

        const response = await fetch("/auth/register",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                name:name,

                email:email,

                password:password

            })

        });

        const data = await response.json();

        if(response.ok){

            alert("Registration Successful!");

            window.location.href="/login";

        }

        else{

            alert(data.detail);

        }

    }

    catch(err){

        console.log(err);

        alert("Server Error");

    }

}