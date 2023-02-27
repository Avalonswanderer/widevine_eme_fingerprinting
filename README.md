# Device Fingerprinting through EME Widevine

This project shows how the [W3C EME API](https://www.w3.org/TR/encrypted-media/) can be used to perform fingerprinting of devices using the [Widevine DRM system](https://www.widevine.com/). It collects Widevine Client ID when in clear, and open persistent sessions within the OS file system to provide both statefull and stateless user tracking to curious origins.

## Setup of the Proof-of-Concept

To set up a working environment, you need to provide the `index.html` and `script_eme_full.js` to a webpage through HTTPS.
Replace the rogueUrl variable within the JS script to the url of the server in charge to collect the fingerprints.

## Disclaimer & Responsible Disclosure

This PoC was made in the context of a scientific study and is meant to be used only for academic and educational purposes. Our findings have been timely communicated to all concerned parties following responsible disclosure process. 

