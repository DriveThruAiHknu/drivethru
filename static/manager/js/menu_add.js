//메뉴 추가 버튼 누르면 입력 완료 알림
var cols = document.querySelectorAll('.submit');
[].forEach.call(cols, function(col){
  col.addEventListener("click" , click , false );
});

function click(e){
    window.alert("✔메뉴 추가 완료");
}

//추가한 이미지 섬네일
const reader = new FileReader();

reader.onload = (readerEvent) => {
    document.querySelector("#img_section").setAttribute("src", readerEvent.target.result);
    //파일을 읽는 이벤트가 발생하면 img_section의 src 속성을 readerEvent의 결과물로 대체함
};

document.querySelector(".file-upload-field").addEventListener("change", (changeEvent) => {
    //upload_file 에 이벤트리스너를 장착

    const imgFile = changeEvent.target.files[0];
    reader.readAsDataURL(imgFile);
    //업로드한 이미지의 URL을 reader에 등록
})

//이미지 파일명 출력하는 코드

$("form").on("change", ".file-upload-field", function(){
    $(this).parent(".file-upload-wrapper").attr("data-text",$(this).val().replace(/.*(\/|\\)/,''));
})


