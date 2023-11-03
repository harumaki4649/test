let words = []; // words変数を空の配列として初期化

let currentWordIndex = 0;
let currentLetterIndex = 0;
let score = 0;

const wordDisplay_moto = document.getElementById("word_moto");
const wordDisplay_hira = document.getElementById("word_hira");
const wordDisplay = document.getElementById("word_roma");
const inputStatus = document.getElementById("input-status");
const scoreDisplay = document.getElementById("score");

function startGame() {
    if (currentWordIndex < words[0].length) {
        const currentWord = words[currentWordIndex];
        wordDisplay.innerHTML = ""; // 単語をクリア
        wordDisplay_hira.innerHTML = words[1][currentWordIndex];
        wordDisplay_moto.innerHTML = words[0][currentWordIndex];
        for (let i = 0; i < keygraph.key_candidate().length; i++) {
            const span = document.createElement("span");
            span.innerText = keygraph.key_candidate()[i];
            if (i < currentLetterIndex) {
                span.classList.add("completed");
            } else if (i === currentLetterIndex) {
                span.classList.add("in-progress");
            }
            wordDisplay.appendChild(span);
        }
        inputStatus.innerText = "次に入力すべき文字: " + keygraph.key_candidate()[0];
    } else {
        wordDisplay.innerText = "ゲーム終了";
        inputStatus.innerText = "";
    }
}

function increaseScore() {
    score++;
    scoreDisplay.innerText = score;
    inputStatus.innerText = "";
}

document.body.addEventListener("keydown", e => {
    if (currentWordIndex < words.length) {
        const currentWord = words[currentWordIndex];
        if (keygraph.next(e.key)) {
            currentLetterIndex++;
            if (keygraph.is_finished()) {
                currentWordIndex++;
                currentLetterIndex = 0;
                increaseScore(); // 文字列を入力し終えた時にスコアを増やす
                keygraph.build(words[1][currentWordIndex]);
                startGame();
            } else {
                increaseScore(); // 一文字入力するたびにスコアを増やす
            }
        }
        startGame();
    }
});

fetch('/get_random_sentence')  // Flaskからランダムな文章を取得
    .then(response => response.json())
    .then(data => {
        // ランダムな文章を表示
        console.log(data); // 受け取ったリストをコンソールに表示
        words = data;
        keygraph.build(words[1][currentWordIndex]);
        startGame();
    });
