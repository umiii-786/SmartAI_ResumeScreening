let errorLabel = document.querySelectorAll('.errorLabel')
let inputs = document.querySelectorAll('.FieldInputs')
let form = document.getElementById('Login')
let alertContent=document.querySelector('.alertContent')
let alertdiv=document.querySelector('.alert')

let requestFor=""
function CheckEmpty() {
  let count = 0
  const formData = new URLSearchParams();

  for (let i = 0; i < inputs.length; i++) {
    if (inputs[i].value == "") {
      errorLabel[i].innerText = "Field Shoud not be Empty"
    }
    else {
      key = inputs[i].getAttribute('name')
      formData.append(key, inputs[i].value)
      errorLabel[i].innerText = ""
      count = count + 1
    }
  }
  console.log(formData)
  HandledFrom(formData, count)
}

function HandledFrom(formData, count) {
  if ((inputs.length == 3 && count == 3) || (inputs.length == 2 && count == 2)) {
    if (inputs.length == 3) {
      formData.append('check','register')
      requestFor='register'
    }
    else {
      formData.append('check','login')
      requestFor='login'
    }
    HandledRequest('/checkUserInDB', formData)
  }
}

function HandledRequest(url, formData) {
  let checkExist = checkLogin_AndRegister_Crediential(url, formData)
}

async function checkLogin_AndRegister_Crediential(url, formData) {
  console.log(url)
  const res = await fetch(url, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    method: "POST",
    body: formData
  })

  const result = await res.text()
  console.log(result)
  if (result == "null" && requestFor=="login" ){
      alertContent.innerText='InValid Username or Password'
      alertdiv.style.display="block"
  }

  else if (result=="notNull" && requestFor=="register"){
     alertContent.innerText='Username Already Registered'
    // alertContent.innerText='InValid Username or Password'
      alertdiv.style.display="block"
  }
  else{
    console.log(form)
    form.submit()
  }
}

function hideAlert(){
   alertdiv.style.display="none"
}


