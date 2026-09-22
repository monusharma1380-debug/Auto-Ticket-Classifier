function analyzeTickets() {
  const fileInput = document.getElementById("csvFile");
  const statusMsg = document.getElementById("statusMsg");

  if (!fileInput.files.length) {
    statusMsg.textContent = "Please choose a CSV file first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  statusMsg.textContent = "Analyzing...";

  fetch("/analyze", { method: "POST", body: formData })
    .then((res) => res.json())
    .then((data) => {
      statusMsg.textContent = "Done.";
      renderTable(data.tickets);
      document.getElementById("totalCount").textContent = data.total_tickets;
      document.getElementById("highCount").textContent = data.high_priority_count;
    })
    .catch((err) => {
      statusMsg.textContent = "Something went wrong.";
      console.error(err);
    });
}

function renderTable(tickets) {
  const tbody = document.getElementById("ticketTable");
  tbody.innerHTML = "";
  tickets.forEach((t) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${t.id}</td>
      <td>${t.text}</td>
      <td>${t.category}</td>
      <td>${t.priority}</td>
      <td>${t["route_to"] ?? t["Route To"]}</td>
    `;
    tbody.appendChild(row);
  });
}

document.getElementById("csvFile").addEventListener("change", function () {
  const label = document.getElementById("fileLabel");
  label.textContent = this.files.length ? this.files[0].name : "Choose file (CSV, Excel, or JSON)";
});