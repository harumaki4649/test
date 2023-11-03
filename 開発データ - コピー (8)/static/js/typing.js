let words = []; // words変数を空の配列として初期化
let currentWordIndex = 0;
let currentLetterIndex = 0;
let score = 0;
let timeLimit = 60; // 時間制限（秒）
let timeExtension = 5; // 文字をn回打つたびに追加される時間
let timeAdd = 60; // 何回打つたびに時間を追加するか
let typing_count = 0;
let isGameEnded = false; // ゲームが終了したかどうかを示すフラグ
let playTime = 0;
let onetimeper = true;

// 残り時間を表示する要素
const timeDisplay = document.getElementById("time-display");
timeDisplay.innerText = formatTime(timeLimit);

function countdown(seconds) {
    return new Promise(resolve => {
        const interval = setInterval(() => {
            if (seconds > 0) {
                if (seconds === 1){
                    wordDisplay_hira.innerText = "START";
                } else {
                    wordDisplay_hira.innerText = seconds-1;}
                seconds--;
            } else {
                if (onetimeper) {
                    onetimeper = false;
                    isGameEnded = false;
                    startGame();
                    startTimer();
                }
            }
        }, 1000); // 1秒ごとにカウントダウン
    });
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
}

function startTimer() {
    const timer = setInterval(() => {
        if (timeLimit > 0) {
            playTime++;
            timeLimit--;
            timeDisplay.innerText = formatTime(timeLimit);
        } else {
            clearInterval(timer);
            if (!isGameEnded) {
                endGame();
            }
        }
    }, 1000);
}

function increaseTime() {
    timeLimit += timeExtension;
    timeDisplay.innerText = formatTime(timeLimit);
}

const wordDisplay_moto = document.getElementById("word_moto");
const wordDisplay_hira = document.getElementById("word_hira");
const wordDisplay = document.getElementById("word_roma");
const inputStatus = document.getElementById("input-status");
const scoreDisplay = document.getElementById("score");
const h1_title = document.getElementById("h1_title");
const nickname = document.getElementById("nickname");

function startGame() {
    if (isGameEnded) {
        return;
    }
    if (currentWordIndex < words.length) {
        const currentWord = words[currentWordIndex];
        wordDisplay.innerHTML = ""; // 単語をクリア
        wordDisplay_hira.innerHTML = words[currentWordIndex];
        wordDisplay_moto.innerHTML = moto_words[currentWordIndex];
        for (let i = 0; i < keygraph.key_candidate().length; i++) {
            const span = document.createElement("span");
            span.innerText = keygraph.key_candidate()[i];
            if (i < currentLetterIndex) {
                //span.classList.add("completed");
            } else if (i === currentLetterIndex) {
                //span.classList.add("in-progress");
            }
            wordDisplay.appendChild(span);
        }
        if ("" === keygraph.key_candidate()) {
            alert("変換システムでエラーが発生しました");
            currentWordIndex++;
            currentLetterIndex = 0;
            increaseScore(); // 文字列を入力し終えた時にスコアを増やす
            keygraph.build(words[currentWordIndex]);
            //location.reload();
        } else {
            inputStatus.innerText = "次に入力すべき文字: " + keygraph.key_candidate()[0];
        }
    } else {
        alert("1000の文章入力お疲れ様でした！\nここまで来る人がいるとは思っていなかったのでうまく動作しません💦");
    }
}

function increaseScore() {
    score++;
    scoreDisplay.innerText = score;
    inputStatus.innerText = "";
}

document.body.addEventListener("keydown", e => {
    if (!isGameEnded && currentWordIndex < words.length) {
        const currentWord = words[currentWordIndex];
        if (keygraph.next(e.key)) {
            sound.play();
            currentLetterIndex++;
            typing_count++;
            if (typing_count === timeAdd){
                increaseTime()
                typing_count = 0;
            }
            if (keygraph.is_finished()) {
                currentWordIndex++;
                currentLetterIndex = 0;
                increaseScore(); // 文字列を入力し終えた時にスコアを増やす
                keygraph.build(words[currentWordIndex]);
                startGame();
            } else {
                increaseScore(); // 一文字入力するたびにスコアを増やす
            }
        }
        if (!isGameEnded && currentWordIndex < words.length) {
            startGame();
        }
    }
});

function GameStart() {
    isGameEnded = true;
    onetimeper = true;
    document.getElementById('nickname').style.display = 'none';
    document.getElementById('retry').style.display = 'none';
    document.getElementById('retry-mode').style.display = 'none';
    fetch('/get_random_sentence') // Flaskからランダムな文章を取得
    .then(response => response.json())
    .then(data => {
        // ランダムな文章を表示
        console.log(data); // 受け取ったリストをコンソールに表示
        words = data[0];
        moto_words = data[1];
        keygraph.build(words[currentWordIndex]);
        sound.init();
        countdown(4)
    });}

function endGame() {
    if (!isGameEnded) {
        isGameEnded = true; // ゲームが終了したことを示すフラグを設定
        //h1_title.innerText = "結果";
        let heikin = score/playTime;
        heikin = Math.ceil(heikin * 10) / 10;
        wordDisplay_hira.innerText = "終了";
        inputStatus.innerText = "";
        wordDisplay_moto.innerText = "";
        wordDisplay.innerText = "";
        timeDisplay.innerText = "平均タイピング速度：" + heikin + " 回/秒";
        document.getElementById('nickname').style.display = 'block';
        document.getElementById('retry').style.display = 'block';
        document.getElementById('retry-mode').style.display = 'block';
        }
}

// ボタンが押された際の処理
document.getElementById('nickname-form').addEventListener('submit', function(event) {
    let heikin = score/playTime;
    heikin = Math.ceil(heikin * 10) / 10;
    event.preventDefault(); // デフォルトの送信動作をキャンセル

    // ニックネームの入力値を取得
    const nickname = document.getElementById('nickname-input').value;
        document.getElementById('nickname').style.display = "none";

    // ここで取得したニックネームを使って必要な処理を行う（例：ランキングの表示）
    // この例では、ニックネームをコンソールに表示するだけです

    // ここにニックネームを使った追加の処理を記述
    // 例えば、ニックネームをサーバーに送信してランキングを取得するなどの処理が入ります
    fetch('/ranking', {
        method: 'POST', // POSTリクエストを送信するための指定
        headers: {
            'Content-Type': 'application/json' // 送信するデータのタイプ
        },
        body: JSON.stringify({ data: [nickname, score, heikin] }) // 送信するデータをJSON形式に変換
        })
    .then(response => response.json())
    .then(data => {
        console.log(data); // 受け取ったリストをコンソールに表示
    });
});


// ボタンが押された際の処理
document.getElementById('retry-form').addEventListener('submit', function(event) {
    event.preventDefault(); // デフォルトのイベントをキャンセル
    // 頑張ったけど再読み込みしないとうまくできなかったからとりあえずこれ
    var paramstr = document.location.search;
    const currentURL = window.location.href;
    window.location.href = currentURL;
});

// ボタンが押された際の処理
document.getElementById('retry-form-mode').addEventListener('submit', function(event) {
    event.preventDefault(); // デフォルトのイベントをキャンセル
    window.location.assign('http://127.0.0.1/typing')
});

GameStart();