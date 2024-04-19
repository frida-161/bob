window.onload = function() {
    // Select the anchor tag by its ID
    var link = document.getElementById('link');

    // Create a div to hold the QR code
    var qrCodeElement = document.getElementById('qr-code');
    
    // Read the href attribute from the link
    var url = link.href;

    // Initialize the QR code generator
    new QRCode(qrCodeElement, {
        text: url,
        width: 512,
        height: 512,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
    });
    qrCodeElement.childNodes()
}