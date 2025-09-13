async function atualizar() {
    const res = await fetch('/sensor'); // ESP32 vai responder com JSON ou texto
    const data = await res.text();      // ou res.json()
    const container=document.getElementById('sensor').innerText = data;
    container.innerHTML = '';
    for (const key in data) {
            // cria uma "linha" para cada sensor
            const linha = document.createElement('p');
            linha.textContent = key + ': ' + data[key];
            container.appendChild(linha);
        }
}
setInterval(atualizar, 1000); // atualiza a cada 1s