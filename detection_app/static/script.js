// static/script.js
function updateStats() {
    fetch("/stats/").then(res => res.json()).then(data => {
        let html = "";
        for (let key in data) {
            html += `<p><strong>${key}</strong>: ${data[key]}</p>`;
        }
        document.getElementById("stats").innerHTML = html;
    });
}
setInterval(updateStats, 1000);
