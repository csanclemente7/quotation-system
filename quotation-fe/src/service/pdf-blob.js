let pdfObject = {};

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
}

function ejecutarDescarga(jsPDFInvoiceTemplate, props) {
  generatePdf(jsPDFInvoiceTemplate, props);
}

// export functions
export const pdfBlob = {
  setProps,
};
