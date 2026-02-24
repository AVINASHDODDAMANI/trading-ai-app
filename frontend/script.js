async function getSignal() {
  const symbol = document.getElementById("symbol").value;

  const response = await fetch(
    https://trading-ai-app-7dol.onrender.com/analyze?symbol=" + symbol
  );

  const data = await response.json();

  document.getElementById("result").innerHTML =
    `Stock: ${data.stock}<br>
     Signal: ${data.signal}<br>
     Risk: ${data.risk}`;
}