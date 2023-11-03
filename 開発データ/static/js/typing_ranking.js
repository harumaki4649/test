function view(data) {
const rankingContainer = document.createElement('div');
    rankingContainer.classList.add('ranking-container');

    for (let i = 0; i < data[1].length; i++) {
        const rankItem = document.createElement('div');
        rankItem.classList.add('rank-item');

        const [nickname, score, avgSpeed] = data[1][i];

        // 自分の順位のランキングデータを強調表示
        if (i === data[0] - 1) {
            if (i === 0) {
                rankItem.classList.add('highlight_top1'); // 自分の順位を強調表示するためのクラス
            } else if (i === 1) {
                rankItem.classList.add('highlight_top2'); // 自分の順位を強調表示するためのクラス
            } else if (i === 2) {
                rankItem.classList.add('highlight_top3'); // 自分の順位を強調表示するためのクラス
            } else {
                rankItem.classList.add('highlight'); // 自分の順位を強調表示するためのクラス
            }
        }

        rankItem.innerHTML = `
            <p>${i + 1}位 ： ${nickname}</p>
            <p>スコア ： ${score}</p>
            <p>平均キータイプ数 ： ${avgSpeed} 回/秒</p>
        `;

        rankingContainer.appendChild(rankItem);
    }

    // ランキングデータを表示するコンテナをページに追加
    const gameContainer = document.querySelector('.game-container');
    gameContainer.appendChild(rankingContainer);
}

  // ランキングを表示する関数
function displayRanking() {
    fetch('/ranking', {
        method: 'POST', // POSTリクエストを送信するための指定
        headers: {
            'Content-Type': 'application/json' // 送信するデータのタイプ
        },
        body: JSON.stringify({}) // 送信するデータをJSON形式に変換
        })
    .then(response => response.json())
    .then(data => {
        view(data);
    });
}

window.addEventListener('load', function(){
			console.log("load：リソースファイルを全て読み込みました。");
			displayRanking();
		});
