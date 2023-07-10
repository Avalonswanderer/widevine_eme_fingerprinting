# Device Fingerprinting through EME Widevine

This project shows how the [W3C EME API](https://www.w3.org/TR/encrypted-media/) can be used to perform fingerprinting of devices using the [Widevine DRM system](https://www.widevine.com/). It collects Widevine Client ID when in clear, and open persistent sessions within the OS file system to provide both stateful and stateless user tracking to curious origins.

## How does it work?

This PoC uses the EME API from compatible web browsers to communicate with the underlying Widevine DRM system. In its usual workflow, Widevine generates license key requests to the license server in order to get media content keys to play protected assets. Under the opaque protocol of Widevine, such messages can be filled with distinctive identifiers leading to potential user tracking issues raised by the EME recommendation. Such distinctive identifiers can range from build info, CPU architecture, Widevine version up to device unique certificate hash.

Our PoC uses a JavaScript file to request a license key response from the Widevine integration test server and redirects the actual request to a rogue server in charge of collecting fingerprints.

Full details can be found in our [research paper](https://people.irisa.fr/Gwendal.Patat/assets/pdf/your_drm_can_watch_you_too.pdf).

## Setup of the Proof-of-Concept

To set up a working environment, you need to provide the `index.html` and `script_eme_full.js` to a webpage through HTTPS.
Replace the rogueUrl variable within the JS script to the url of the server in charge to collect the fingerprints.

### Docker Setup

The `Docker` directory host a docker compose file to build a test environment on `localhost`. This docker setup an Apache server serving both `index.html` and `script_eme_full.js` files over HTTPs, allowing EME usage for both Firefox and Chrome-based browsers. 

To build and start:
```bash
$ cd Docker
$ docker compose up -d
```
You can visit https://localhost on your favorite EME-compatible web browser. The gathered Widevine request will be send to the default rogue server being our local Apache one itself.

To check network logs and extract fingerprints run the following command:
```bash
$ docker logs docker-emefingerprint-1 2>&1 | grep request -A1 | awk '{print $15}' | tr -d '\n' | awk -F ':' '{print $NF}' | cut -d'"' -f2 | xargs python3 ../utils/get_device_info.py
```

And expected output for a Google Pixel 6 running Firefox:
```bash
Cert Serial Number: XXXXXXXXXXXXeb24ab4d9025ae96f928bc7cf3169f965946XXXXXXXXXXXXXXXX
Client Info:
	Application Name: org.mozilla.firefox
	Package Cert Hash: p4tipRZbRJSy/q2edqKA0i2Tf+5iUa7OWZRGsuoxmwQ=
	Company Name: Google
	Model Name: Pixel 6
	Architecture Name: arm64-v8a
	Device Name: oriole
	Product Name: oriole
	Build Info: google/oriole/oriole:12/SD1A.210817.015.A4/7697517:user/release-keys
	Widevine CDM Version: 16.1.0
	OEM Crypto Build Info: OEMCrypto Level3 Code 22594 May 28 2021 16:59:07
	OEM Crypto SPL: 0

```
And for a Linux desktop:
```bash
Cert Serial Number: 4f017ea9a6b5a9f23e7715ddf92ac856
Client Info:
	Company Name: Google
	Model Name: ChromeCDM
	Architecture Name: x86-64
	Widevine CDM Version: 4.10.2557.0
```


## Disclaimer & Responsible Disclosure

This PoC was made in the context of a scientific study and is meant to be used only for academic and educational purposes. Our findings have been timely communicated to all concerned parties following responsible disclosure process. 

