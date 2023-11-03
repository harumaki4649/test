function openModal() {
    const modal = document.querySelector('.modal');
    modal.classList.add('active');
}

function closeModal() {
    const modal = document.querySelector('.modal');
    modal.classList.remove('active');
    modal.classList.add('fade-out');
    setTimeout(() => {
        modal.classList.remove('fade-out');
        modal.style.display = 'none';
    }, 500); // フェードアウト完了後に非表示に
    document.querySelector('.mode-selection').style.display = 'block';
}

window.addEventListener('load', openModal);

document.querySelector('.modal').addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        closeModal();
    }
});

document.querySelector('.modal-content').addEventListener('click', () => {
    closeModal();
});


// ページが読み込まれた後にポップアップを表示する
window.addEventListener('load', openModal);

// ポップアップ領域をクリックしたときにフェードアウトする
document.querySelector('.modal').addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        closeModal();
    }
});

// モーダルコンテンツ（modal-content）をクリックしたときにもフェードアウト
document.querySelector('.modal-content').addEventListener('click', (event) => {
    if (event.target.classList.contains('modal-content')) {
        closeModal();
    }
});



function redirectToMode(mode) {
    switch (mode) {
        case 'mode1':
            window.location.href = 'http://127.0.0.1/typing/small'; // モード1のURL
            break;
        case 'mode2':
            window.location.href = 'http://127.0.0.1/typing/default'; // モード2のURL
            break;
        case 'mode3':
            window.location.href = 'http://127.0.0.1/typing/default2'; // モード3のURL
            break;
        default:
            break;
    }
}