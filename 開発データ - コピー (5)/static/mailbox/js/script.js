// JavaScriptファイル（script.js）
document.addEventListener('DOMContentLoaded', function () {
    const emailList = document.getElementById('email-list');
    const emailSender = document.getElementById('email-sender');
    const emailDate = document.getElementById('email-date');
    const emailRecipient = document.getElementById('email-recipient');
    const emailSubject = document.getElementById('email-subject');
    const emailContent = document.getElementById('email-content-body'); // メールの内容を表示する要素

    let selectedEmailId = null;
    let data = []; // メールデータを格納する配列

    // メールデータを取得する関数
    function getEmails() {
        document.getElementById('loading-message').style.display = 'block'; // 取得中メッセージを表示

        fetch('/get_emails')
            .then(response => response.json())
            .then(result => {
                data = result; // メールデータを更新
                renderEmails(data); // メール一覧を表示
            })
            .finally(() => {
                document.getElementById('loading-message').style.display = 'none'; // 取得中メッセージを非表示
            });
    }

    // メール一覧を表示する関数
    function renderEmails(data) {
        emailList.innerHTML = '';

        data.forEach(email => {
            const listItem = document.createElement('li');
            listItem.dataset.id = email.id;
            listItem.innerHTML = `
                <a href="#">
                    <strong>${email.sender[0]}</strong> - ${email.subject}<br>
                    <small>${email.date}</small><br>
                    <small>To: ${email.recipient}</small>
                </a>
            `;
            emailList.appendChild(listItem);
        });
    }

    // ページ読み込み時に初回のメールデータを取得
    getEmails();

    // 更新ボタンをクリックした際の処理
    document.getElementById('update-button').addEventListener('click', function () {
        getEmails();
        clearEmailDetails();
    });

    // メールをクリックした際の処理
    emailList.addEventListener('click', function (event) {
        const listItem = event.target.closest('li');
        if (listItem) {
            selectedEmailId = listItem.dataset.id;
            const selectedEmail = findEmailById(selectedEmailId);
            if (selectedEmail) {
                emailSender.textContent = selectedEmail.sender[1];
                emailDate.textContent = selectedEmail.date;
                emailRecipient.textContent = `To: ${selectedEmail.recipient}`;
                emailSubject.textContent = selectedEmail.subject;
                
                if (selectedEmail.body_type === 'body_html') {
                    // HTML形式のメールの場合、内容をHTMLとして表示
                    emailContent.innerHTML = selectedEmail.body;
                } else {
                    // 通常のテキストメールの場合、内容をテキストとして表示
                    emailContent.textContent = selectedEmail.content;
                }
            }
        }
    });

    // メールIDを使ってメールを検索
    function findEmailById(id) {
        return data.find(email => email.id === parseInt(id));
    }

    // メール詳細をクリア
    function clearEmailDetails() {
        selectedEmailId = null;
        emailSender.textContent = '';
        emailDate.textContent = '';
        emailRecipient.textContent = '';
        emailSubject.textContent = '';
        emailContent.innerHTML = ''; // メールの内容をクリア
    }
});
