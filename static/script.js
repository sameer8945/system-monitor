
async function updateStats() {

    const response = await fetch("/stats");

    const data = await response.json();

    document.getElementById("cpu").innerText =
        data.cpu + "%";

    document.getElementById("ram").innerText =
        data.ram + "%";

    document.getElementById("disk").innerText =
        data.disk + "%";
let hours =
    Math.floor(data.uptime / 3600);

let minutes =
    Math.floor((data.uptime % 3600) / 60);

document.getElementById("uptime").innerText =
    hours + "h " + minutes + "m";

document.getElementById("os").innerText =
    data.os;

document.getElementById("kernel").innerText =
    data.kernel;

document.getElementById("architecture").innerText =
    data.architecture;

    document.getElementById("upload").innerText =
    data.bytes_sent + " MB";

document.getElementById("download").innerText =
    data.bytes_recv + " MB";
    let coresHtml = "";

data.cpu_cores.forEach((usage, index) => {
    coresHtml += `
        <div>
            <p>Core ${index}: ${usage}%</p>
            <progress value="${usage}" max="100"></progress>
        </div>
    `;
});

document.getElementById("cpu-cores").innerHTML = coresHtml;
   const table = document.getElementById("process-table");

table.innerHTML = "";

data.processes.forEach(proc => {
    table.innerHTML += `
        <tr>
            <td>${proc.pid}</td>
    <td>${proc.name}</td>
    <td>${proc.cpu}</td>
    <td>${proc.memory}</td>
        </tr>
    `;
});
}

setInterval(updateStats, 2000);

updateStats();
