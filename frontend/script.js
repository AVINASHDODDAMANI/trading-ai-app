async function getSignal() {
    const symbol = document.getElementById("symbol").value.trim();

    if (!symbol) {
        document.getElementById("result").innerHTML = "⚠️ Enter stock symbol";
        return;
    }

    document.getElementById("result").innerHTML = "⏳ Analyzing...";

    try {
        const response = await fetch(
            `https://trading-ai-app-7dol.onrender.com/analyze?symbol=${symbol}`
        );

        const data = await response.json();

        document.getElementById("result").innerHTML = `
            Stock: ${data.stock}<br>
            Signal: ${data.signal}<br>
            Risk: ${data.risk}<br>
            Date & Time (IST): ${data.date_time_ist}
        `;
    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML =
            "❌ Failed to connect to server";
    }
}