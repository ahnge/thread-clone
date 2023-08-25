const alerts = htmx.findAll(".alert");

for (let i = 0; i < alerts.length; i++) {
  const alert = alerts[i];
  setTimeout(() => {
    alert.remove();
  }, i * 1000 + 5 * 1000);
}
