// popup.js - PhishGuard AI Chrome Extension

chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const currentUrl = tabs[0].url;

    // Get all UI elements
    const status = document.getElementById('status');
    const resultBox = document.getElementById('result-box');
    const verdict = document.getElementById('verdict');
    const scoreVal = document.getElementById('score-val');

    // ─── Skip scanning internal browser pages ───────────────────────
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

    // ─── Show scanning message ───────────────────────────────────────
    let hostname = "";
    try {
        hostname = new URL(currentUrl).hostname;
    } catch (e) {
        hostname = currentUrl;
    }
    status.innerText = "🔍 Scanning: " + hostname;

    // ─── Call the PhishGuard backend API ────────────────────────────
    fetch("https://phish-guard-ml-udcl.vercel.app/api/main/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: currentUrl })
    })
        .then(function (response) {
            if (!response.ok) {
                // HTTP errors like 404, 500
                throw new Error("Server returned status " + response.status);
            }
            return response.json();
        })

        .then(function (data) {
            // ── Debug: see full API response in DevTools console ──────────
            console.log("PhishGuard API Response:", data);

            // ── Handle missing or error risk_score ────────────────────────
            if (
                !data ||
                data.risk_score === undefined ||
                data.risk_score === null ||
                data.risk_score === -1
            ) {
                status.innerText = "Scan Failed ❌";
                resultBox.style.display = "block";
                scoreVal.innerText = "N/A";
                verdict.innerText = data && data.error
                    ? "Error: " + data.error
                    : "Unable to analyze site";
                resultBox.style.backgroundColor = "#f1f5f9";
                resultBox.style.color = "#475569";
                return;
            }

            // ── Successfully got risk_score ────────────────────────────────
            const score = data.risk_score; // number 0–100
            resultBox.style.display = "block";
            scoreVal.innerText = score + "%";
            status.innerText = "✅ Scan Complete";

            // ── Reset inline styles before applying new ones ───────────────
            resultBox.style.backgroundColor = "";
            resultBox.style.color = "";

            // ── Colour-code by risk level ──────────────────────────────────
            if (score >= 70) {
                // HIGH RISK
                resultBox.className = "result-box high";
                verdict.innerText = "🚨 HIGH RISK — Do NOT proceed!";

            } else if (score >= 40) {
                // MEDIUM / SUSPICIOUS
                resultBox.className = "result-box medium";
                resultBox.style.backgroundColor = "#fef9c3";
                resultBox.style.color = "#854d0e";
                verdict.innerText = "⚠️ SUSPICIOUS — Proceed with caution";

            } else {
                // SAFE
                resultBox.className = "result-box low";
                verdict.innerText = "✅ Site looks safe";
            }
        })

        .catch(function (error) {
            // ── Network error or server down ───────────────────────────────
            console.error("PhishGuard fetch error:", error);
            status.innerText = "Connection Failed ❌";
            resultBox.style.display = "block";
            scoreVal.innerText = "N/A";
            verdict.innerText = "Cannot reach PhishGuard server";
            resultBox.style.backgroundColor = "#f1f5f9";
            resultBox.style.color = "#475569";
        });
});