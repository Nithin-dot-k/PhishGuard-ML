// popup.js - PhishGuard AI Chrome Extension

const API_ENDPOINTS = [
    "https://phish-guard-ml-udcl.vercel.app/api/main/analyze",
    "http://127.0.0.1:8000/api/analyze"
];

chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    if (!tabs || !tabs[0] || !tabs[0].url) return;
    const currentUrl = tabs[0].url;

    // Get UI elements
    const status = document.getElementById('status');
    const resultBox = document.getElementById('result-box');
    const verdict = document.getElementById('verdict');
    const scoreVal = document.getElementById('score-val');

    // Skip internal browser pages
    if (
        currentUrl.startsWith('chrome://') ||
        currentUrl.startsWith('chrome-extension://') ||
        currentUrl.startsWith('about:') ||
        currentUrl.startsWith('file://')
    ) {
        status.innerText = "Cannot scan this page";
        resultBox.style.display = "block";
        scoreVal.innerText = "N/A";
        verdict.innerText = "⚠️ Internal browser page";
        return;
    }

    let hostname = "";
    try {
        hostname = new URL(currentUrl).hostname;
    } catch (e) {
        hostname = currentUrl;
    }
    status.innerText = "🔍 Scanning: " + hostname;

    function fetchFromEndpoint(index) {
        if (index >= API_ENDPOINTS.length) {
            status.innerText = "Connection Failed ❌";
            resultBox.style.display = "block";
            scoreVal.innerText = "N/A";
            verdict.innerText = "Cannot reach PhishGuard server";
            resultBox.style.backgroundColor = "#f1f5f9";
            resultBox.style.color = "#475569";
            return;
        }

        const endpoint = API_ENDPOINTS[index];

        fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: currentUrl })
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Status " + response.status);
                }
                return response.json();
            })
            .then(function (data) {
                console.log("PhishGuard API Response from " + endpoint + ":", data);

                if (!data || data.risk_score === undefined || data.risk_score === null || data.risk_score === -1) {
                    status.innerText = "Scan Failed ❌";
                    resultBox.style.display = "block";
                    scoreVal.innerText = "N/A";
                    verdict.innerText = data && data.error ? "Error: " + data.error : "Unable to analyze site";
                    resultBox.style.backgroundColor = "#f1f5f9";
                    resultBox.style.color = "#475569";
                    return;
                }

                const score = data.risk_score;
                resultBox.style.display = "block";
                scoreVal.innerText = score + "%";
                status.innerText = "✅ Scan Complete";

                resultBox.style.backgroundColor = "";
                resultBox.style.color = "";

                if (score >= 70) {
                    resultBox.className = "result-box high";
                    verdict.innerText = "🚨 HIGH RISK — Do NOT proceed!";
                } else if (score >= 40) {
                    resultBox.className = "result-box medium";
                    resultBox.style.backgroundColor = "#fef9c3";
                    resultBox.style.color = "#854d0e";
                    verdict.innerText = "⚠️ SUSPICIOUS — Proceed with caution";
                } else {
                    resultBox.className = "result-box low";
                    verdict.innerText = "✅ Site looks safe";
                }
            })
            .catch(function (error) {
                console.warn("Endpoint failed (" + endpoint + "):", error);
                fetchFromEndpoint(index + 1);
            });
    }

    fetchFromEndpoint(0);
});