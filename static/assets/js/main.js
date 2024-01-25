let CsvCheckBox =  document.getElementById("checkBoxCsv");
let btnNext = document.getElementById("btnNext");
let btnSubmit = document.getElementById("btnSubmit");
let csvFileInput = document.getElementById("csvFileInput");

CsvCheckBox.addEventListener('change', (event)=>{
  
    if(event.target.value){
      btnNext.classList.add("d-none");
      btnSubmit.classList.remove("d-none");
    }

})

document.querySelectorAll(".")

