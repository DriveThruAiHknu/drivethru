

/* 메인 */
var menu_list = new Array();
var op_list = new Array();
var user_op_list = new Array();
var db_op_list = new Array();
var price_list = new Array(); //상품 1개 가격*수량 + 옵션
var ea_list = new Array();
var morpheme_list = new Array();
var morpheme_str = "";
var menu_price = 0;
var total_price = 0;

var txt = document.getElementById("ai_say");
var forms = document.getElementById("content");
var forms_txt = '';
var total_real = document.getElementById("total_real");


var menu_default = "\n";
var op_default = "✔️ice ✔️시럽 X ✔️샷 2<br>✔️우유 기본 ✔️휘핑 X ✔️드리즐 X";
var price_default = "0 원\n";
var ea_default = "1\n";
var total_default = "0 원\n";

txt.innerHTML = "🌿어서오세요! 스타벅스입니다🌿";

window.onload = function () {
    setTimeout(() => {
        order();
    }, 1000);
}

/* 데이터베이스 가져오기 */
var db_str = '{{ prods|escapejs }}';
var db_list = db_str.slice(1, -1);
db_list = db_list.split('),');

//데이터베이스 - 전체(db)
var db = new Array();
for (var i = 0; i < db_list.length; i++) {
    db.push(db_list[i].replace(/\'|\"|\(|\)| /g, "").split(','));
}

//데이터베이스 - 메뉴(db_menu)
var db_menu = new Array();
for (var j = 0; j < db.length; j++) {
    db_menu.push(db[j][2]);
}

//데이터베이스 - 가격(db_price)
var db_price = new Array();
for (var k = 0; k < db.length; k++) {
    db_price.push(db[k][3]);
}

/* fetch로 view에 있는 분석기로 문장 보내는 함수 */
function stem_analyzer(resText) {
    var url = "http://localhost:8000/client/analyzer?resText=" + resText
    return fetch(url, {
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify(this.obj)
    }).then(response => response.json())
        .then(res => {//console.log("객체",res);
            var str = JSON.stringify(res);
            var str_slice = str.slice(1, -1).replace(/\'|\"|\\/g, '');
            str_slice = str_slice.split(',');
            morpheme_list = str_slice;
            morpheme_str = str_slice;
            //console.log('리스트:', morpheme_list);
            //console.log('문자:', morpheme_str);
            return morpheme_str;
        })
}

/* 실제 비동기 처리 코드 */
async function order() {
    var audio_once = false; //한번이라도 주문했는지

    try {
        var audio1 = await tts("어서오세요. 스타벅스입니다!");

        txt.innerHTML = "주문을 원하시는 메뉴나 번호를 말씀해주세요💚";
        var audio2 = await tts("주문을 원하시는 메뉴나 번호를 말씀해주세요!");

        txt.innerHTML = "인식 중 ...!"; //로딩 애니메이션 들어가면 좋을 거 같음

        var audio_once = true;

        while (true) {
            if (audio_once) // 주문한적 X
            {
                console.log("주문한 적 X");
                var stt1 = await speech_to_text();

                if (stt1.length > 1) //한 글자 이상 들어오면
                {

                    txt.innerHTML = "✅" + stt1;

                    /* 형태소 분석기 실행 */
                    var stt_morpheme = await stem_analyzer(stt1);
                    //console.log("return: ",stt_morpheme); -> 아메리카노,하나
                    console.log("전역 호출: ", morpheme_list); //-> [아메리카노,하나]
                    //console.log("전역 호출 문자: ", morpheme_str); -> 아메리카노,하나


                    /* DB에 있는지 메뉴 조회 */
                    for (var x = 0; x < morpheme_list.length; x++) {
                        for (var y = 0; y < db_menu.length; y++) {
                            if (morpheme_list[x] == db_menu[y]) {
                                console.log('메뉴 인식 완료 : ');
                                menu_list.push(db_menu[y]);
                                menu_price = db_price[y]; //가격 옵션이랑 수량 다 해서 price_list에 push 해야됨.
                                //6 hot_cold, 7 caf_amount, 8 syrup, 9 shot, 10 milk, 11 whip, 12 java_chip, 13 driz, 14 sales_rate
                                db_op_list.push([db[y][6], db[y][7], db[y][8], db[y][9], db[y][10], db[y][11], db[y][12], db[y][13], db[y][14]]);

                                break;
                            }
                            else //메뉴 인식 못함
                            {
                                //...
                            }
                        }
                    }


                    /* 사용자가 말한 옵션 */
                    var user_hot_cold = "";
                    var user_caf_amount = "";
                    var user_syrup = "";
                    var user_shot = "";
                    var user_milk = "";
                    var user_whip = "";
                    var user_java_chip = "";
                    var user_driz = "";
                    var user_sales_rate = "";
                    var user_size = "";


                    for (var z = 0; z < morpheme_list.length; z++) {
                        /* 사용자가 말한 메뉴 옵션!! */
                        //!!!!!!!!!!!!!!!!! 나중에 임베딩 연결하면 case 값 바꾸기

                        //1. 온도
                        if (morpheme_list[z] == '핫') {
                            user_hot_cold = "H";
                        }
                        else if (morpheme_list[z] == '아이스') {
                            user_hot_cold = "C";
                        }

                        //2. 카페인 조절
                        if (morpheme_list[z] == '카페인') {
                            user_caf_amount = 'CC';
                        }
                        else if (morpheme_list[z] == '디카페인') {
                            user_caf_amount = 'CD';
                        }
                        else if (morpheme_list[z] == '하프디카페인') {
                            user_caf_amount = 'CH';
                        }

                        //3. 시럽 조절


                        //4. 샷 조절


                        //5. 우유 조절


                        //6. 휘핑 조절


                        //7. 자바칩 조절


                        //8. 드리즐 조절


                        //9. 사이즈
                        if (morpheme_list[z] == '숏') {
                            user_size = "S";
                        }
                        else if (morpheme_list[z] == '톨') {
                            user_size = "T";
                        }
                        else if (morpheme_list[z] == '그란데') {
                            user_size = "G";
                        }


                    }

                    //user_op_list = (온도)H/C, (카페인)CC/CH/CD, (시럽), (샷), (우유), (휘핑), (자바칩), (드리즐), (사이즈) S/T/G

                    //user_op_list에 추가!
                    user_op_list.push([user_hot_cold, user_caf_amount, user_syrup, user_shot, user_milk, user_whip,
                        user_java_chip, user_driz, user_size]);

                    console.log("사용자가 추가한 옵션 : ", user_op_list);



                    var audio3 = await tts(menu_list[menu_list.length - 1] + "\n메뉴를 선택하셨습니다!");

                    console.log('추가된 메뉴', menu_list);
                    console.log('메뉴 가격', menu_price);
                    console.log('추가된 옵션', db_op_list);

                    /* 실제 옵션 */
                    var hot_cold = "";
                    var caf_amount = "";
                    var syrup = "";
                    var shot = "";
                    var milk = "";
                    var whip = "";
                    var java_chip = "";
                    var driz = "";
                    var sales_rate = "";
                    var size = "";

                    //if () //html에 옵션
                    //hot_cold = db_op_list[0][0];
                    //caf_amount = db_op_list[0][1];
                    //syrup = db_op_list[0][2];
                    //shot = db_op_list[0][3];
                    //milk = db_op_list[0][4];
                    //whip = db_op_list[0][5];
                    //java_chip = db_op_list[0][6];
                    //driz = db_op_list[0][7];
                    //sales_rate = db_op_list[0][8];
                    //size = user_op_list[0][8]


                    //0. size -> 숏, 톨, 그란데
                    switch (user_op_list[user_op_list.length - 1][8]) {
                        case 'T':
                            size = "Tall";
                            break;

                        case 'S':
                            size = "Short";
                            break;

                        case 'G':
                            size = "Grande";
                            break;

                        default: //기본은 중간사이즈로
                            size = "Tall";
                    }

                    //1. hot_cold -> case 3: hot/cold 둘 다 다 될 땐 어떻게 할 건지 디폴트 값 정하기!!
                    switch (Number(db_op_list[db_op_list.length - 1][0])) {
                        case 0:
                            hot_cold = "food";
                            break;
                        case 1:
                            hot_cold = "hot";
                            break;
                        case 2:
                            hot_cold = "ice";
                            break;
                        case 3:
                            hot_cold = "O"; //hot/ice 둘다 됨
                            break;
                    }

                    /* === 여기 해야됨 === */
                    /* hot, ice 둘 다 되는데 */
                    if (hot_cold == "O") {
                        hot_cold = "ice"; //고객이 따로 옵션 말 안했으면 일단 기본값 ice로

                        if (user_op_list[user_op_list.length - 1][0] == "C") //차가운 거 달라고 말했으면 ice
                        {
                            hot_cold = "ice";
                        }
                        else if (user_op_list[user_op_list.length - 1][0] == "H") //뜨거운 거 달라고 말했으면
                        {
                            hot_cold = "hot";
                        }
                    }
                    else //둘 다 안되는 음식이거나, 둘 중 하나만 되는 경우
                    {
                        //예외처리 어케할지 고민. (차가운 거만 되는데 따뜻한 거 시킨다고 말했다거나...)
                    }

                    //2. caf_amount
                    switch (db_op_list[db_op_list.length - 1][1]) {
                        case 'False':
                            caf_amount = "";
                            break;
                        case 'True':
                            caf_amount = "O";
                            break;
                    }

                    /* === 여기 해야됨 === */
                    /* 카페인 조절 되는데 고객이 따로 옵션 말 안했으면 */
                    if (caf_amount == "O") {
                        caf_amount = "O"; // 1/2디카페인 △, 디카페인 X, 블론드 O로 표시
                        //조절 아예 안되면 "" 공백!

                        if (user_op_list[user_op_list.length - 1][1] == "CC") //(카페인-카페인)카페인 있는 거 달라고 말하면
                        {
                            caf_amount = "O";
                        }
                        else if (user_op_list[user_op_list.length - 1][1] == "CH") //(카페인-하프디카페인)카페인 반 있는 거 달라고 하면
                        {
                            caf_amount = "△";
                        }
                        else if (user_op_list[user_op_list.length - 1][1] == "CD") //(카페인-디카페인) 카페인 없는 거 달라고 하면
                        {
                            caf_amount = "X";
                        }
                    }
                    else //조절 안되면
                    {
                        //예외처리 (카페인 조절 안되는데 해달라고 하는 경우)
                    }

                    //3. syrup
                    switch (Number(db_op_list[db_op_list.length - 1][2])) {
                        case 0:
                            syrup = "X";
                            break;
                        case 1:
                            syrup = "O"; //바닐라 1~9, 헤이즐넛 1~9, 카라멜 1~9
                            break;
                    }

                    /* === 여기 해야됨 === */
                    /* 시럽 조절 되는데 고객이 따로 옵션 말 안했으면 */
                    if (syrup == "O") {
                        syrup = "X";


                        //바닐라인지 헤이즐넛인지 카라멜인지도 구분해야함.
                        if (user_op_list[user_op_list.length - 1][2] != "") //따로 말했으면
                        {
                            //syrup = "바닐라 1"; 이런식으로 들어가게 하기!
                        }

                    }
                    else //조절 안되면
                    {
                        //예외처리 (시럽 조절 안되는데 해달라고 하는 경우)
                    }


                    //4. shot -> 디카페인은 조절 안되는 메뉴 = 샷이 없어야함 = ""
                    switch (db_op_list[db_op_list.length - 1][3]) {
                        case 'False':
                            shot = "X"; //샷 조절 안되는 디카페인 메뉴
                            break;
                        case 'True':
                            shot = "O"; //조절 되는 메뉴
                            break;
                    }

                    /* === 여기 해야됨 === */
                    /* 샷 조절 되는데 고객이 따로 옵션 말 안했으면 */
                    if (shot == "O") {
                        shot = "1"; // 1~9에서 1이 디폴트

                        if (user_op_list[user_op_list.length - 1][3] != "") //따로 말했으면
                        {
                            //shot = "1"; 이런식으로 들어가게 하기!
                        }
                    }
                    else //조절 안되면
                    {
                        //예외처리 (샷 조절 안되는데 해달라고 하는 경우)
                    }

                    //5. milk -> 우유 
                    switch (db_op_list[db_op_list.length - 1][4]) {
                        case 'False':
                            milk = "X"; //우유 조절 안되는 메뉴
                            break;
                        case 'True':
                            milk = "O"; //조절 되는 메뉴
                            break;
                    }

                    /* === 여기 해야됨 === */
                    /* 우유 조절 되는데 고객이 따로 옵션 말 안했으면 */
                    if (milk == "O") {
                        milk = "일반"; // 일반이 디폴트, 이외에 저지방, 무지방, 두유, 오트(귀리)

                        if (user_op_list[user_op_list.length - 1][4] != "") //따로 말했으면
                        {
                            //milk = "귀리, 오트, ..."; 이런식으로 들어가게 하기!
                        }
                    }
                    else //조절 안되면
                    {
                        //예외처리 (우유 조절 안되는데 해달라고 하는 경우)
                    }

                    //6. whip
                    switch (db_op_list[db_op_list.length - 1][5]) {
                        case 'False':
                            whip = "X"; //휘핑 조절 안되는 메뉴
                            break;
                        case 'True':
                            whip = "O"; //조절 되는 메뉴
                            break;
                    }

                    /* === 여기 해야됨 === */
                    /* 휘핑 조절 되는데 고객이 따로 옵션 말 안했으면 */
                    if (whip == "O") {
                        whip = "X"; // 일반 적게/보통/많이, 에스프레소휘핑 적게/보통/많이

                        if (user_op_list[user_op_list.length - 1][5] != "") //따로 말했으면
                        {
                            //whip = "일반 적게, 일반 많이, ..."; 이런식으로 들어가게 하기!
                        }
                    }
                    else //조절 안되면
                    {
                        //예외처리 (휘핑 조절 안되는데 해달라고 하는 경우)
                    }

                    //7. java_chip
                    switch (db_op_list[db_op_list.length - 1][6]) {
                        case 'False':
                            java_chip = "X"; //자바칩 조절 안되는 메뉴
                            break;
                        case 'True':
                            java_chip = "O"; //조절 되는 메뉴
                            break;
                    }

                    /* === 여기 해야됨 === */
                    /* 자바칩 조절 되는데 고객이 따로 옵션 말 안했으면 */
                    if (java_chip == "O") {
                        java_chip = "X"; // 일반, 통자바칩 토핑, 자바칩&토핑

                        if (user_op_list[user_op_list.length - 1][6] != "") //따로 말했으면
                        {
                            //java_chip = "일반 자바칩, ..."; 이런식으로 들어가게 하기!
                        }
                    }
                    else //조절 안되면
                    {
                        //예외처리 (자바칩 조절 안되는데 해달라고 하는 경우)
                    }


                    //8. driz
                    switch (db_op_list[db_op_list.length - 1][7]) {
                        case 'False':
                            driz = "X"; //자바칩 조절 안되는 메뉴
                            break;
                        case 'True':
                            driz = "O"; //조절 되는 메뉴
                            break;
                    }

                    /* === 여기 해야됨 === */
                    /* 드리즐 조절 되는데 고객이 따로 옵션 말 안했으면 */
                    if (driz == "O") {
                        driz = "X"; // 카라멜 적게, 카라멜 보통, 카라멜 많이, 초콜릿 적게, 초콜릿 보통, 초콜릿 많이

                        if (user_op_list[user_op_list.length - 1][6] != "") //따로 말했으면
                        {
                            //driz = "카라멜 적게, ..."; 이런식으로 들어가게 하기!
                        }
                    }
                    else //조절 안되면
                    {
                        //예외처리 (드리즐 조절 안되는데 해달라고 하는 경우)
                    }

                    //!!!!!!!최종 옵션 리스트
                    /*var hot_cold = "";
                    var caf_amount = "";
                    var syrup = "";
                    var shot = "";
                    var milk = "";
                    var whip = "";
                    var java_chip = "";
                    var driz = "";
                    var sales_rate = "";
                    var size = "";*/

                    op_list.push([hot_cold, caf_amount, syrup, shot, milk, whip, java_chip, driz, size]);

                    /* 수량 계산 */
                    for (var x = 0; x < morpheme_list.length; x++) {
                        for (var num = 1; num < 10; num++)
                            if (morpheme_list[x].indexOf(String(num)) == 0) //1~9가 속하는 문자열이 있으면 0
                            {
                                console.log("수량: ", Number(morpheme_list[x]));
                                ea_list.push(Number(morpheme_list[x]));
                                //수량 인식 못했을 때 에러 처리
                                break;
                            }
                    }

                    price_list.push(menu_price * ea_list[ea_list.length - 1]); //옵션도 더해야함
                    total_price += Number(price_list[price_list.length - 1]);

                    /* 결제 리스트에 추가 */


                    // db_op_list는 사이즈가 포함 X. 대신, sales_rate가 있음
                    // user_op_list는 사용자가 말한 옵션 저장리스트라 sale_rate 대신 사이즈도 포함 (결국 개수는 같음)
                    // op_list는 DB와 사용자 조합해서 최종 옵션 리스트로 사이즈도 포함 (위와 동일)

                    if (hot_cold == "food") //음식인 경우
                    {
                        forms_txt += '<div class="row">\
                            <div class="col-md-3" id="border"> \
                                <h4 id="list_txt" class="menu">'+ menu_list[menu_list.length - 1] + '</h4>\
                            </div>\
                            <div class="col-md-4" id="border">\
                                <h5 id="op_txt" class="op">✔️'+ hot_cold + '</h5>\
                            </div>\
                            <div class="col-md-2" id="border"> \
                                <h4 id="list_txt" class="price">'+ menu_price + ' 원</h4>\
                            </div>\
                            <div class="col-md-1" id="border"> \                                    <h4 id="list_txt" class="ea">'+ ea_list[ea_list.length - 1] + '</h4>\
                                </div>\
                            <div class="col-md-2" id="border"> \
                                <h4 id="list_txt">'+ price_list[price_list.length - 1] + ' 원</h4>\
                            </div>\
                            </div>';
                    }
                    else //음료인 경우
                    {
                        if (caf_amount == "") //카페인 조절 가능 불가능하면 아예 옵션에 안넣기 (카페인, 샷 둘 다)
                        {
                            forms_txt = '<div class="row">\
                                <div class="col-md-3" id="border"> \
                                    <h4 id="list_txt" class="menu">'+ menu_list[menu_list.length - 1] + '</h4>\
                                </div>\
                                <div class="col-md-4" id="border">\
                                    <h5 id="op_txt" class="op">✔️'+ hot_cold + '✔️사이즈 ' + size + ' ✔️시럽 ' + syrup + '<br>✔️우유 ' + milk + ' ✔️휘핑 ' + whip + ' ✔️드리즐 ' + driz + '</h5>\
                                </div>\
                                <div class="col-md-2" id="border"> \
                                    <h4 id="list_txt" class="price">'+ menu_price + ' 원</h4>\
                                </div>\
                                <div class="col-md-1" id="border"> \
                                    <h4 id="list_txt" class="ea">'+ ea_list[ea_list.length - 1] + '</h4>\
                                </div>\
                                <div class="col-md-2" id="border"> \
                                    <h4 id="list_txt">'+ price_list[price_list.length - 1] + ' 원</h4>\
                                </div>\
                                </div>';
                        }
                        else //카페인 조절 가능하면 넣기!
                        {

                            forms_txt = '<div class="row">\
                                <div class="col-md-3" id="border"> \
                                    <h4 id="list_txt" class="menu">'+ menu_list[menu_list.length - 1] + '</h4>\
                                </div>\
                                <div class="col-md-4" id="border">\
                                    <h5 id="op_txt" class="op">✔️'+ hot_cold + '✔️사이즈 ' + size + ' ✔️카페인 ' + caf_amount + ' ✔️시럽 ' + syrup + ' ✔️샷 ' + shot + '<br>✔️우유 ' + milk + ' ✔️휘핑 ' + whip + ' ✔️드리즐 ' + driz + '</h5>\
                                </div>\
                                <div class="col-md-2" id="border"> \
                                    <h4 id="list_txt" class="price">'+ menu_price + ' 원</h4>\
                                </div>\
                                <div class="col-md-1" id="border"> \
                                    <h4 id="list_txt" class="ea">'+ ea_list[ea_list.length - 1] + '</h4>\
                                </div>\
                                <div class="col-md-2" id="border"> \
                                    <h4 id="list_txt">'+ price_list[price_list.length - 1] + ' 원</h4>\
                                </div>\
                                </div>';
                        }
                    }

                    forms.innerHTML = forms_txt;
                    total_real.innerHTML = total_price + ' 원';

                    txt.innerHTML = '결제 또는 추가할 메뉴를 말씀해주세요❗';
                    var audio4 = await tts("결제 또는 추가할 메뉴를 말씀해주세요!");

                    audio_once = false;

                }
                else //한 글자도 안 들어오면
                {
                    txt.innerHTML = "✔️ 인식하지 못했습니다. 다시 한번 말씀해주세요!";
                    var audio5 = await tts("인식하지 못했습니다. 다시 한번 말씀해주세요!");
                }
            }


            else // 1메뉴 이상 주문 O
            {
                console.log("한번 이상 주문");
                txt.innerHTML = '📌 "결제"라고 말씀하시면 주문이 종료됩니다.';

                var stt2 = await speech_to_text();

                if (stt2.length > 1) //한 글자 이상 들어오면
                {
                    if (stt2 == "결제" | stt2 == "결재" | stt2 == "첫째") //결제 원하면
                    {
                        console.log("주문 종료");
                        txt.innerHTML = "✔️ 결제 안내를 도와드리겠습니다";
                        var audio5 = await tts("결제 안내를 도와드리겠습니다!");
                        await new Promise((resolve, reject) => setTimeout(resolve, 1300));
                        break;
                    }
                    else //계속 메뉴 받고 싶으면
                    {
                        txt.innerHTML = "✅" + stt2;

                        /* 형태소 분석기 실행 */
                        var stt_morpheme = await stem_analyzer(stt2);
                        console.log("전역 호출: ", morpheme_list); //-> [아메리카노,하나]



                        /* DB에 있는지 메뉴 조회 */
                        for (var x = 0; x < morpheme_list.length; x++) {
                            for (var y = 0; y < db_menu.length; y++) {
                                if (morpheme_list[x] == db_menu[y]) {
                                    console.log('메뉴 인식 완료 : ');
                                    menu_list.push(db_menu[y]);
                                    menu_price = db_price[y]; //가격 옵션이랑 수량 다 해서 price_list에 push 해야됨.
                                    //6 hot_cold, 7 caf_amount, 8 syrup, 9 shot, 10 milk, 11 whip, 12 java_chip, 13 driz, 14 sales_rate
                                    db_op_list.push([db[y][6], db[y][7], db[y][8], db[y][9], db[y][10], db[y][11], db[y][12], db[y][13], db[y][14]]);

                                    break;
                                }
                                else //메뉴 인식 못함
                                {
                                    //...
                                }
                            }
                        }


                        /* 사용자가 말한 옵션 */
                        var user_hot_cold = "";
                        var user_caf_amount = "";
                        var user_syrup = "";
                        var user_shot = "";
                        var user_milk = "";
                        var user_whip = "";
                        var user_java_chip = "";
                        var user_driz = "";
                        var user_sales_rate = "";
                        var user_size = "";


                        for (var z = 0; z < morpheme_list.length; z++) {
                            /* 사용자가 말한 메뉴 옵션!! */
                            //!!!!!!!!!!!!!!!!! 나중에 임베딩 연결하면 case 값 바꾸기

                            //1. 온도
                            if (morpheme_list[z] == '핫') {
                                user_hot_cold = "H";
                            }
                            else if (morpheme_list[z] == '아이스') {
                                user_hot_cold = "C";
                            }

                            //2. 카페인 조절
                            if (morpheme_list[z] == '카페인') {
                                user_caf_amount = 'CC';
                            }
                            else if (morpheme_list[z] == '디카페인') {
                                user_caf_amount = 'CD';
                            }
                            else if (morpheme_list[z] == '하프디카페인') {
                                user_caf_amount = 'CH';
                            }

                            //3. 시럽 조절


                            //4. 샷 조절


                            //5. 우유 조절


                            //6. 휘핑 조절


                            //7. 자바칩 조절


                            //8. 드리즐 조절


                            //9. 사이즈
                            if (morpheme_list[z] == '숏') {
                                user_size = "S";
                            }
                            else if (morpheme_list[z] == '톨') {
                                user_size = "T";
                            }
                            else if (morpheme_list[z] == '그란데') {
                                user_size = "G";
                            }


                        }

                        //user_op_list = (온도)H/C, (카페인)CC/CH/CD, (시럽), (샷), (우유), (휘핑), (자바칩), (드리즐), (사이즈) S/T/G

                        //user_op_list에 추가!
                        user_op_list.push([user_hot_cold, user_caf_amount, user_syrup, user_shot, user_milk, user_whip,
                            user_java_chip, user_driz, user_size]);

                        console.log("사용자가 추가한 옵션 : ", user_op_list);



                        var audio3 = await tts(menu_list[menu_list.length - 1] + "\n메뉴를 선택하셨습니다!");

                        console.log('추가된 메뉴', menu_list);
                        console.log('메뉴 가격', menu_price);
                        console.log('추가된 옵션', db_op_list);


                        /* 실제 옵션 */
                        var hot_cold = "";
                        var caf_amount = "";
                        var syrup = "";
                        var shot = "";
                        var milk = "";
                        var whip = "";
                        var java_chip = "";
                        var driz = "";
                        var sales_rate = "";

                        //if () //html에 옵션
                        //hot_cold = db_op_list[0][0];
                        //caf_amount = db_op_list[0][1];
                        //syrup = db_op_list[0][2];
                        //shot = db_op_list[0][3];
                        //milk = db_op_list[0][4];
                        //whip = db_op_list[0][5];
                        //java_chip = db_op_list[0][6];
                        //driz = db_op_list[0][7];
                        //sales_rate = db_op_list[0][8];
                        //size = user_op_list[0][8]

                        //0. size -> 숏, 톨, 그란데
                        switch (user_op_list[user_op_list.length - 1][8]) {
                            case 'T':
                                size = "Tall";
                                break;

                            case 'S':
                                size = "Short";
                                break;

                            case 'G':
                                size = "Grande";
                                break;

                            default: //기본은 중간사이즈로
                                size = "Tall";
                        }

                        //1. hot_cold -> case 3: hot/cold 둘 다 다 될 땐 어떻게 할 건지 디폴트 값 정하기!!
                        switch (Number(db_op_list[db_op_list.length - 1][0])) {
                            case 0:
                                hot_cold = "food";
                                break;
                            case 1:
                                hot_cold = "hot";
                                break;
                            case 2:
                                hot_cold = "ice";
                                break;
                            case 3:
                                hot_cold = "O"; //hot/ice 둘다 됨
                                break;
                        }

                        /* === 여기 해야됨 === */
                        /* hot, ice 둘 다 되는데 */
                        if (hot_cold == "O") {
                            hot_cold = "ice"; //고객이 따로 옵션 말 안했으면 일단 기본값 ice로

                            if (user_op_list[user_op_list.length - 1][0] == "C") //차가운 거 달라고 말했으면 ice
                            {
                                hot_cold = "ice";
                            }
                            else if (user_op_list[user_op_list.length - 1][0] == "H") //뜨거운 거 달라고 말했으면
                            {
                                hot_cold = "hot";
                            }
                        }
                        else //둘 다 안되는 음식이거나, 둘 중 하나만 되는 경우
                        {
                            //예외처리 어케할지 고민. (차가운 거만 되는데 따뜻한 거 시킨다고 말했다거나...)
                        }

                        //2. caf_amount
                        switch (db_op_list[db_op_list.length - 1][1]) {
                            case 'False':
                                caf_amount = "";
                                break;
                            case 'True':
                                caf_amount = "O";
                                break;
                        }

                        /* === 여기 해야됨 === */
                        /* 카페인 조절 되는데 고객이 따로 옵션 말 안했으면 */
                        if (caf_amount == "O") {
                            caf_amount = "O"; // 1/2디카페인 △, 디카페인 X, 블론드 O로 표시
                            //조절 아예 안되면 "" 공백!

                            if (user_op_list[user_op_list.length - 1][1] == "CC") //(카페인-카페인)카페인 있는 거 달라고 말하면
                            {
                                caf_amount = "O";
                            }
                            else if (user_op_list[user_op_list.length - 1][1] == "CH") //(카페인-하프디카페인)카페인 반 있는 거 달라고 하면
                            {
                                caf_amount = "△";
                            }
                            else if (user_op_list[user_op_list.length - 1][1] == "CD") //(카페인-디카페인) 카페인 없는 거 달라고 하면
                            {
                                caf_amount = "X";
                            }
                        }
                        else //조절 안되면
                        {
                            //예외처리 (카페인 조절 안되는데 해달라고 하는 경우)
                        }

                        //3. syrup
                        switch (Number(db_op_list[db_op_list.length - 1][2])) {
                            case 0:
                                syrup = "X";
                                break;
                            case 1:
                                syrup = "O"; //바닐라 1~9, 헤이즐넛 1~9, 카라멜 1~9
                                break;
                        }

                        /* === 여기 해야됨 === */
                        /* 시럽 조절 되는데 고객이 따로 옵션 말 안했으면 */
                        if (syrup == "O") {
                            syrup = "X";


                            //바닐라인지 헤이즐넛인지 카라멜인지도 구분해야함.
                            if (user_op_list[user_op_list.length - 1][2] != "") //따로 말했으면
                            {
                                //syrup = "바닐라 1"; 이런식으로 들어가게 하기!
                            }

                        }
                        else //조절 안되면
                        {
                            //예외처리 (시럽 조절 안되는데 해달라고 하는 경우)
                        }


                        //4. shot -> 디카페인은 조절 안되는 메뉴 = 샷이 없어야함 = ""
                        switch (db_op_list[db_op_list.length - 1][3]) {
                            case 'False':
                                shot = "X"; //샷 조절 안되는 디카페인 메뉴
                                break;
                            case 'True':
                                shot = "O"; //조절 되는 메뉴
                                break;
                        }

                        /* === 여기 해야됨 === */
                        /* 샷 조절 되는데 고객이 따로 옵션 말 안했으면 */
                        if (shot == "O") {
                            shot = "1"; // 1~9에서 1이 디폴트

                            if (user_op_list[user_op_list.length - 1][3] != "") //따로 말했으면
                            {
                                //shot = "1"; 이런식으로 들어가게 하기!
                            }
                        }
                        else //조절 안되면
                        {
                            //예외처리 (샷 조절 안되는데 해달라고 하는 경우)
                        }

                        //5. milk -> 우유 
                        switch (db_op_list[db_op_list.length - 1][4]) {
                            case 'False':
                                milk = "X"; //우유 조절 안되는 메뉴
                                break;
                            case 'True':
                                milk = "O"; //조절 되는 메뉴
                                break;
                        }

                        /* === 여기 해야됨 === */
                        /* 우유 조절 되는데 고객이 따로 옵션 말 안했으면 */
                        if (milk == "O") {
                            milk = "일반"; // 일반이 디폴트, 이외에 저지방, 무지방, 두유, 오트(귀리)

                            if (user_op_list[user_op_list.length - 1][4] != "") //따로 말했으면
                            {
                                //milk = "귀리, 오트, ..."; 이런식으로 들어가게 하기!
                            }
                        }
                        else //조절 안되면
                        {
                            //예외처리 (우유 조절 안되는데 해달라고 하는 경우)
                        }

                        //6. whip
                        switch (db_op_list[db_op_list.length - 1][5]) {
                            case 'False':
                                whip = "X"; //휘핑 조절 안되는 메뉴
                                break;
                            case 'True':
                                whip = "O"; //조절 되는 메뉴
                                break;
                        }

                        /* === 여기 해야됨 === */
                        /* 휘핑 조절 되는데 고객이 따로 옵션 말 안했으면 */
                        if (whip == "O") {
                            whip = "X"; // 일반 적게/보통/많이, 에스프레소휘핑 적게/보통/많이

                            if (user_op_list[user_op_list.length - 1][5] != "") //따로 말했으면
                            {
                                //whip = "일반 적게, 일반 많이, ..."; 이런식으로 들어가게 하기!
                            }
                        }
                        else //조절 안되면
                        {
                            //예외처리 (휘핑 조절 안되는데 해달라고 하는 경우)
                        }

                        //7. java_chip
                        switch (db_op_list[db_op_list.length - 1][6]) {
                            case 'False':
                                java_chip = "X"; //자바칩 조절 안되는 메뉴
                                break;
                            case 'True':
                                java_chip = "O"; //조절 되는 메뉴
                                break;
                        }

                        /* === 여기 해야됨 === */
                        /* 자바칩 조절 되는데 고객이 따로 옵션 말 안했으면 */
                        if (java_chip == "O") {
                            java_chip = "X"; // 일반, 통자바칩 토핑, 자바칩&토핑

                            if (user_op_list[user_op_list.length - 1][6] != "") //따로 말했으면
                            {
                                //java_chip = "일반 자바칩, ..."; 이런식으로 들어가게 하기!
                            }
                        }
                        else //조절 안되면
                        {
                            //예외처리 (자바칩 조절 안되는데 해달라고 하는 경우)
                        }


                        //8. driz
                        switch (db_op_list[db_op_list.length - 1][7]) {
                            case 'False':
                                driz = "X"; //자바칩 조절 안되는 메뉴
                                break;
                            case 'True':
                                driz = "O"; //조절 되는 메뉴
                                break;
                        }

                        /* === 여기 해야됨 === */
                        /* 드리즐 조절 되는데 고객이 따로 옵션 말 안했으면 */
                        if (driz == "O") {
                            driz = "X"; // 카라멜 적게, 카라멜 보통, 카라멜 많이, 초콜릿 적게, 초콜릿 보통, 초콜릿 많이

                            if (user_op_list[user_op_list.length - 1][6] != "") //따로 말했으면
                            {
                                //driz = "카라멜 적게, ..."; 이런식으로 들어가게 하기!
                            }
                        }
                        else //조절 안되면
                        {
                            //예외처리 (드리즐 조절 안되는데 해달라고 하는 경우)
                        }


                        //!!!!!!!최종 옵션 리스트
                        /*var hot_cold = "";
                        var caf_amount = "";
                        var syrup = "";
                        var shot = "";
                        var milk = "";
                        var whip = "";
                        var java_chip = "";
                        var driz = "";
                        var sales_rate = "";
                        var size = "";*/

                        op_list.push([hot_cold, caf_amount, syrup, shot, milk, whip, java_chip, driz, size]);


                        /* 수량 계산 */
                        for (var x = 0; x < morpheme_list.length; x++) {
                            for (var num = 1; num < 10; num++)
                                if (morpheme_list[x].indexOf(String(num)) == 0) //1~9가 속하는 문자열이 있으면 0
                                {
                                    console.log("수량: ", Number(morpheme_list[x]));
                                    ea_list.push(Number(morpheme_list[x]));
                                    //수량 인식 못했을 때 에러 처리
                                    break;
                                }
                        }

                        price_list.push(menu_price * ea_list[ea_list.length - 1]); //옵션도 더해야함
                        total_price += Number(price_list[price_list.length - 1]);


                        /* 결제 리스트에 추가 */


                        // db_op_list는 사이즈가 포함 X. 대신, sales_rate가 있음
                        // user_op_list는 사용자가 말한 옵션 저장리스트라 sale_rate 대신 사이즈도 포함 (결국 개수는 같음)
                        // op_list는 DB와 사용자 조합해서 최종 옵션 리스트로 사이즈도 포함 (위와 동일)


                        if (hot_cold == "food") //음식인 경우
                        {
                            forms_txt += '<div class="row">\
                                <div class="col-md-3" id="border"> \
                                    <h4 id="list_txt" class="menu">'+ menu_list[menu_list.length - 1] + '</h4>\
                                </div>\
                                <div class="col-md-4" id="border">\
                                    <h5 id="op_txt" class="op">✔️'+ hot_cold + '</h5>\
                                </div>\
                                <div class="col-md-2" id="border"> \
                                    <h4 id="list_txt" class="price">'+ menu_price + ' 원</h4>\
                                </div>\
                                <div class="col-md-1" id="border"> \
                                    <h4 id="list_txt" class="ea">'+ ea_list[ea_list.length - 1] + '</h4>\
                                </div>\
                                <div class="col-md-2" id="border"> \
                                    <h4 id="list_txt">'+ price_list[price_list.length - 1] + ' 원</h4>\
                                </div>\
                                </div>';
                        }
                        else //음료인 경우
                        {

                            if (caf_amount == "") //카페인 조절 가능 불가능하면 아예 옵션에 안넣기 (카페인, 샷 둘 다)
                            {
                                forms_txt += '<div class="row">\
                                    <div class="col-md-3" id="border"> \
                                        <h4 id="list_txt" class="menu">'+ menu_list[menu_list.length - 1] + '</h4>\
                                    </div>\
                                    <div class="col-md-4" id="border">\
                                        <h5 id="op_txt" class="op">✔️'+ hot_cold + '✔️사이즈 ' + size + ' ✔️시럽 ' + syrup + '<br>✔️우유 ' + milk + ' ✔️휘핑 ' + whip + ' ✔️드리즐 ' + driz + '</h5>\
                                    </div>\
                                    <div class="col-md-2" id="border"> \
                                        <h4 id="list_txt" class="price">'+ menu_price + ' 원</h4>\
                                    </div>\
                                    <div class="col-md-1" id="border"> \
                                        <h4 id="list_txt" class="ea">'+ ea_list[ea_list.length - 1] + '</h4>\
                                    </div>\
                                    <div class="col-md-2" id="border"> \
                                        <h4 id="list_txt">'+ price_list[price_list.length - 1] + ' 원</h4>\
                                    </div>\
                                    </div>';
                            }
                            else //카페인 조절 가능하면 넣기!
                            {

                                forms_txt += '<div class="row">\
                                    <div class="col-md-3" id="border"> \
                                        <h4 id="list_txt" class="menu">'+ menu_list[menu_list.length - 1] + '</h4>\
                                    </div>\
                                    <div class="col-md-4" id="border">\
                                        <h5 id="op_txt" class="op">✔️'+ hot_cold + '✔️사이즈 ' + size + ' ✔️카페인 ' + caf_amount + ' ✔️시럽 ' + syrup + ' ✔️샷 ' + shot + '<br>✔️우유 ' + milk + ' ✔️휘핑 ' + whip + ' ✔️드리즐 ' + driz + '</h5>\
                                    </div>\
                                    <div class="col-md-2" id="border"> \
                                        <h4 id="list_txt" class="price">'+ menu_price + ' 원</h4>\
                                    </div>\
                                    <div class="col-md-1" id="border"> \
                                        <h4 id="list_txt" class="ea">'+ ea_list[ea_list.length - 1] + '</h4>\
                                    </div>\
                                    <div class="col-md-2" id="border"> \
                                        <h4 id="list_txt">'+ price_list[price_list.length - 1] + ' 원</h4>\
                                    </div>\
                                    </div>';
                            }

                        }

                        forms.innerHTML = forms_txt;
                        total_real.innerHTML = total_price + ' 원';

                        txt.innerHTML = '"결제" / "추가할 메뉴"를 말씀해주세요❗';
                        var audio4 = await tts("결제 또는 추가할 메뉴를 말씀해주세요~");
                    }
                }
                else //한 글자도 안 들어오면
                {
                    txt.innerHTML = "✔️ 인식하지 못했습니다. 다시 한번 말씀해주세요!";
                    var audio5 = await tts("인식하지 못했습니다. 다시 한번 말씀해주세요!");
                }



                //location.href="/client/end"; -> 풀기!!!!!!!!!!!!!!!
            }
        }
    }

    catch (error) {
        console.log(error);
    }

}

/* STT */
var isRecognizing = false;

try {
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();
}
catch (e) {
    console.error(e);
}

recognition.lang = 'ko-KR';
recognition.interimResults = false;
recognition.maxAlternatives = 50; //클수록 발음대로 안적고 문장 적합도로.
recognition.continuous = false; //음성인식 안끝나고 계속됨

async function speech_to_text() {
    var resText = "";
    var txt = document.getElementById("ai_say");
    recognition.start();
    isRecognizing = true;

    recognition.onstart = function () {
        console.log("------------------------음성인식 시작------------------------");
    }

    recognition.onresult = function (event) {
        resText = event.results[0][0].transcript;
        txt.innerHTML = resText;

        if (resText == "결제" | resText == "결제.") {
            console.log("결제라고 말함");
            return "결제";
        }

        console.log('STT 반환:', resText);

    };

    await new Promise(resolve =>
        recognition.onend = e => {
            {
                console.log("------------------------음성인식 종료------------------------");
                resolve();
            }
        })

    recognition.stop();

    resText = resText.replace(".", "");
    return resText;
}


/* TTS */
var voices = [];


function setVoiceList() {
    voices = window.speechSynthesis.getVoices();
}
if (window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = setVoiceList;
}


async function tts(txt) {
    var end = false;

    if (!window.speechSynthesis) {
        alert("음성 재생을 지원하지 않는 브라우저입니다. 크롬, 파이어폭스 등의 최신 브라우저를 이용하세요");
        return;
    }

    var lang = 'ko-KR';
    var utterThis = new SpeechSynthesisUtterance(txt);

    utterThis.text = txt;
    utterThis.lang = lang;
    utterThis.pitch = 1;
    utterThis.rate = 1; //속도

    //기존
    utterThis.onerror = function (event) {
        console.log('error', event);
    };

    var voiceFound = false;

    for (var i = 0; i < voices.length; i++) {
        if (voices[i].lang.indexOf(lang) >= 0 || voices[i].lang.indexOf(lang.replace('-', '_')) >= 0) {
            utterThis.voice = voices[i];
            voiceFound = true;
        }
    }
    if (!voiceFound) {
        alert('voice not found');
        return;
    }

    await new Promise(function (resolve) {
        utterThis.onend = resolve;
        window.speechSynthesis.speak(utterThis);
    });
}