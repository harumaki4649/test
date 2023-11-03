const words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"];
let currentWordIndex = 0;
let currentLetterIndex = 0;
let score = 0;

const wordDisplay = document.getElementById("word");
const inputStatus = document.getElementById("input-status");
const scoreDisplay = document.getElementById("score");

function startGame() {
    if (currentWordIndex < words.length) {
        const currentWord = words[currentWordIndex];
        wordDisplay.innerText = currentWord;
        inputStatus.innerText = "次に入力すべき文字: " + currentWord[0];
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

document.addEventListener("keydown", function (e) {
    if (currentWordIndex < words.length) {
        const currentWord = words[currentWordIndex];
        if (e.key === currentWord[currentLetterIndex]) {
            if (currentLetterIndex === 0) {
                inputStatus.innerText = "入力した文字: " + e.key;
            } else {
                inputStatus.innerText += e.key;
            }

            currentLetterIndex++;
            if (currentLetterIndex === currentWord.length) {
                currentWordIndex++;
                currentLetterIndex = 0;
                increaseScore();
                startGame();
            }
        }
    }
});

startGame();
