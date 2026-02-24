async function getSignal() {
  const symbol = document.getElementById("symbol").value;

  const response = await fetch(
    `http://10.133.23.174:8001/analyze?symbol=${symbol}`
  );

  const data = await response.json();

  document.getElementById("result").innerHTML =
    `Stock: ${data.stock}<br>
     Signal: ${data.signal}<br>
     Risk: ${data.risk}`;
}