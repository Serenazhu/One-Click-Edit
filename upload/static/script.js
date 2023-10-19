const LogInOption = document.getElementsByClassName('log-in-option')[0];
const SignInOption = document.getElementsByClassName('sign-up-option')[0];

const LogInOptionUsername = document.getElementsByClassName('username')[0];
const SignUpOptionUsername = document.getElementsByClassName('unique-username')[0];
const SignUpOptionEmail = document.getElementsByClassName('email')[0];

const SignIn = document.getElementsByClassName('signin')[0];
const LogIn = document.getElementsByClassName('login')[0];

const warningMessage = document.getElementById('warning');
const warningMessage2 = document.getElementById('warning2');

LogInOption.addEventListener('click', ()=>{
    LogInOptionUsername.style.display = 'block';
    SignUpOptionUsername.style.display = 'none';
    SignUpOptionEmail.style.display = 'none';
    LogInOption.classList.remove('not-selected-login');
    SignInOption.classList.add('not-selected-signup');
    SignInOption.classList.remove("sign-up-option");
    SignIn.style.display = 'none';
    LogIn.style.display = 'block';
});

SignInOption.addEventListener('click', ()=>{
    LogInOptionUsername.style.display = 'none';
    SignUpOptionUsername.style.display = 'block';
    SignUpOptionEmail.style.display = 'block';
    LogInOption.classList.add('not-selected-login')
    SignInOption.classList.add("sign-up-option");
    SignInOption.classList.remove('not-selected-signup');
    SignIn.style.display = 'block';
});

let isStyled = false;
//default option
document.addEventListener('DOMContentLoaded', ()=>{

    SignInOption.click();
    LogInOption.classList.add('not-selected-login');
    
});

//Handle form submission for signin
document.addEventListener('DOMContentLoaded', ()=>{
    const signinButton = document.getElementById("signin");

    const signinUsername = document.getElementById("unique-username-form");
    const signinEmail = document.getElementById("email-form");

    //signin
    signinButton.addEventListener('click', () =>{
        const signinUsernameData = new FormData(signinUsername); // key:Form field names  values:actual info
        const signinEmailData = new FormData(signinEmail);
        //combine data from both forms
        const combinedData = new FormData(); // create an instance of FormData
        for (const [key, value] of signinUsernameData.entries()) {
            combinedData.append(key, value);
        }
        for (const [key, value] of signinEmailData.entries()) {
            combinedData.append(key, value);
        }

        fetch('/Authentication', {
            method: 'POST',
            body: combinedData

        })
        

        .then(response => response.json()) // parses the response body as JSON 
        .then(data =>{  //data is the parsed JSON data that is returned as the response from the server
            if (data.status === "username_exists") {
                warningMessage.style.display = 'block';
            }
            if(data.status === 'user_created'){
                window.location.href = '/upload';
            }

        
        })

     });
});


//Handle form submission for Login
document.addEventListener('DOMContentLoaded', ()=>{

const loginButton = document.getElementById("login");
const loginUsername = document.getElementById("username-form");

loginButton.addEventListener('click', () =>{
    const loginUsernameData = new FormData(loginUsername)
    fetch('/Authentication',{
        method: 'POST',
        body: loginUsernameData
    })
    .then(response2=>{
        console.log('Response received:', response2);
        return response2.json(); //parse the JSON data
    })
    .then(data=>{
        console.log(data.status);
        //'data' now contains the parsed JSON response
        if (data.status === 'user_does_not_exist'){
            warningMessage2.style.display = 'block';
            console.log('ff');
        };
    
        if (data.status === 'user_does_exist'){
            window.location.href = '/upload';
        };
    });

});

});



