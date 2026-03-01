async function getSignal() {
    const inputEl = document.getElementById("symbol");
    const resultEl = document.getElementById("result");

    let symbol = inputEl.value.trim();

    if (!symbol) {
        resultEl.innerHTML = "⚠️ Enter stock symbol";
        return;
    }

    // ✅ normalize symbol (user can type bel / BEL / bel.ns)
    symbol = symbol.replace(".NS", "").toUpperCase();

    resultEl.innerHTML = "⏳ Analyzing...";

    try {
        const response = await fetch(
            `https://trading-ai-app-7dol.onrender.com/analyze?symbol=${symbol}`
        );

        // ✅ VERY IMPORTANT — handle server errors
        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();

        // ✅ safe display helper
        const safe = (val) => (val === null || val === undefined ? "N/A" : val);

        resultEl.innerHTML = `
            Stock: ${safe(data.stock)}<br>
            Signal: ${safe(data.signal)}<br>
            Current Price: ₹${safe(data.current_price)}<br>
            Buy Near: ₹${safe(data.buy_price)}<br>
            Target: ₹${safe(data.target_price)}<br>
            Risk: ${safe(data.risk)}<br>
            Date & Time (IST): ${safe(data.date_time_ist)}
        `;
    } catch (error) {
        console.error("Fetch error:", error);
        resultEl.innerHTML = "❌ Failed to connect to server";
    }
}