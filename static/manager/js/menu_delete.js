var cols = document.querySelectorAll('#buttons .input_delete_btn');
[].forEach.call(cols, function(col){
  col.addEventListener("click" , click , false );
});

function click(e){
  window.alert("❌메뉴 삭제 완료");
}