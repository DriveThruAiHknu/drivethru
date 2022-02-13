var cols = document.querySelectorAll('#buttons .input_update_btn');
[].forEach.call(cols, function(col){
  col.addEventListener("click" , click , false );
});

function click(e){
  window.alert("update");
}