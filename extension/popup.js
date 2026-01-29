chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    let currentUrl = tabs[0].url;
    const status = document.getElementById('status');
    const resultBox = document.getElementById('result-box');
    const verdict = document.getElementById('verdict');
    const scoreVal = document.getElementById('score-val');

    status.innerText = "Analyzing: " + new URL(currentUrl).hostname;

    fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: currentUrl })
    })
        .then(response => response.json())
        .then(data => {
            resultBox.style.display = "block";
            scoreVal.innerText = data.risk_score + "%";

            // --- NEW SENSITIVITY LOGIC ---
            // We lower the threshold to 60% to catch sophisticated spoofing
            if (data.risk_score >= 60) {
                resultBox.className = "result-box high";
                verdict.innerText = "🚨 HIGH RISK DETECTED";
            } else if (data.risk_score >= 40) {
                // Optional: Adding a yellow "caution" state
                resultBox.className = "result-box";
                resultBox.style.backgroundColor = "#fef9c3"; // Yellow
                resultBox.style.color = "#854d0e";
                verdict.innerText = "⚠️ CAUTION: SUSPICIOUS";
            } else {
                resultBox.className = "result-box low";
                verdict.innerText = "✅ SITE LOOKS SAFE";
            }
            status.innerText = "Scan Complete";
        })
        .catch(error => {
            status.innerText = "Error: Is PhishGuard Server running?";
            console.error('Error:', error);
        });
});