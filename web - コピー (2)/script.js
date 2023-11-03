const words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "game", "typing", "humareuka", "inunorei", "fumareuka", "pc", "club"];
let currentWordIndex = 0;
let currentLetterIndex = 0;
let score = 0;

const wordDisplay = document.getElementById("word");
const inputStatus = document.getElementById("input-status");
const scoreDisplay = document.getElementById("score");

function startGame() {
    if (currentWordIndex < words.length) {
        const currentWord = words[currentWordIndex];
        wordDisplay.innerHTML = ""; // 単語をクリア
        for (let i = 0; i < currentWord.length; i++) {
            const span = document.createElement("span");
            span.innerText = currentWord[i];
            if (i < currentLetterIndex) {
                span.classList.add("completed");
            } else if (i === currentLetterIndex) {
                span.classList.add("in-progress");
            }
            wordDisplay.appendChild(span);
        }
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
            currentLetterIndex++;
            if (currentLetterIndex === currentWord.length) {
                currentWordIndex++;
                currentLetterIndex = 0;
                increaseScore();
                startGame();
            }
        }
        startGame();
    }
});

startGame();
