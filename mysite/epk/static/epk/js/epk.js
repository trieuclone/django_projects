document.addEventListener('DOMContentLoaded',() => {
  document.querySelector('.waitingList').onclick = () => clikOnCustomerList("waitingList");
  document.querySelector('.workingList').onclick = () => clikOnCustomerList("workingList");
});


function clikOnCustomerList(url) {
  const customerNameList = document.querySelector(".customerNameList");
  const customerInfo = document.querySelector(".CustomerInfo");

  // Clear previous content
  customerNameList.innerHTML = "";
  customerInfo.innerHTML = "";

    fetch(url)
    .then(response => response.json())
    .then(customerList => {
      for (let key in customerList) {
        const customer = customerList[key];

        // Create <p> for name
        let nameP = document.createElement("p");
        nameP.textContent = customer.name;
        nameP.style.cursor = "pointer";

        nameP.addEventListener("click", () => {
          // Clear and show status when name is clicked
          customerInfo.innerHTML = "";

          let statusP = document.createElement("p");
          statusP.textContent = customer.status;
          statusP.style.cursor = "pointer";

          statusP.addEventListener("click", () => {
            alert(`Status clicked: ${customer.status}`);
          });

          customerInfo.appendChild(statusP);
        });

        customerNameList.appendChild(nameP);
      }
    })
    .catch(err => {
      console.error("Failed to load customer list:", err);
    });
}

function printCustomerHistory(format = 'a4') {
  const element = document.querySelector('#customerClinicalInput');
  if (!element) {
    alert('Customer history not found.');
    return;
  }

  const opt = {
    margin:       0.5,
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2 },
    jsPDF:        { unit: 'in', format: format, orientation: 'portrait' }
  };

  // Generate PDF and open in new tab for printing
  html2pdf()
    .set(opt)
    .from(element)
    .outputPdf('bloburl')
    .then((pdfUrl) => {
      // Open PDF in new window/tab
      const win = window.open(pdfUrl, '_blank');
      if (win) {
        win.focus();
        // Optional: Prompt user to print after slight delay
        setTimeout(() => {
          win.print();
        }, 1000); // Wait to ensure it's rendered
      } else {
        alert('Pop-up blocked. Please allow pop-ups for this site.');
      }
    });
}