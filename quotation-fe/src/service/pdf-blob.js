let pdfObject = {};

import Email from "emailjs-com";

import { OutputType } from "jspdf-invoice-template";

function setProps(propsFile, jsPDFInvoiceTemplate, outputType) {
  let props = propsFile;

  props["outputType"] = OutputType.Blob;
  console.log(props["outputType"]);
  ejecutarDescarga(jsPDFInvoiceTemplate, props);
}

function generatePdf(jsPDFInvoiceTemplate, props) {
  pdfObject = jsPDFInvoiceTemplate(props);

  console.log("Object created", pdfObject);

  let blob = new Blob([pdfObject.blob], { type: "application/pdf" });

  sendEmail();
}

function ejecutarDescarga(jsPDFInvoiceTemplate, props) {
  generatePdf(jsPDFInvoiceTemplate, props);
}

//index.js
function sendEmail() {
  Email.send({
    Host: "mail.macrisrefrigeracion.com",
    Username: "admin@macrisrefrigeracion.com",
    Password: "Sancastel7",
    To: "mghernandezcastillo@gmail.com",
    From: "admin@macrisrefrigeracion.com",
    Subject: "Test",
    Body: "Test",
  }).then((message) => alert("mail sent successfully"));
}

// export functions
export const pdfBlob = {
  setProps,
};
