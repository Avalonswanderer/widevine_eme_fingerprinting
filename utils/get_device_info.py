import sys
import base64

def usage(prog_name):
    print("Usage: " + prog_name + " CLIENTID\nwhere CLIENTID is the base64 of the Widevine Client ID", file=sys.stderr)

def findTLV(raw_clientid, tag_name):
    tag = raw_clientid.find(tag_name)
    if (tag == -1):
        return b''
    size = raw_clientid[tag + len(tag_name) + 1]
    start = tag + len(tag_name) + 2
    value = raw_clientid[start: start + size]
    return value

def get_serial_number(raw_clientid):
    serial_number_tag = raw_clientid.find(b'\x08\x02\x12')
    if (serial_number_tag == -1):
        print("No Serial Number tag, Client ID might be encrypted.", file=sys.stderr)
        exit()
    start = serial_number_tag + 4
    end = start + raw_clientid[start - 1]
    return raw_clientid[start: end].hex()

def build_device_info(raw_clientid):
    attributes = {
        "Application Name": "application_name",
        "Package Cert Hash": "package_certificate_hash_bytes",
        "Company Name": "company_name",
        "Model Name": "model_name",
        "Architecture Name": "architecture_name",
        "Device Name": "device_name",
        "Product Name": "product_name",
        "Build Info": "build_info",
        "Widevine CDM Version": "widevine_cdm_version",
        "OEM Crypto Build Info": "oem_crypto_build_information",
        "OEM Crypto SPL": "oem_crypto_security_patch_level"
    }

    device_info = "Client Info:"
    for attr in attributes.keys():
        value = findTLV(raw_clientid, str.encode(attributes[attr]))
        if value != b'':
            device_info += "\n\t" + attr + ": " + value.decode('utf-8')
    return device_info

def main(clientid):
    raw_clientid = base64.b64decode(clientid)
    serial_number = get_serial_number(raw_clientid)
    print("\n------RESULTS---------\n")
    print("Cert Serial Number: " + serial_number + "\n" + build_device_info(raw_clientid))

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        usage(sys.argv[0])
        exit()
    main(sys.argv[1])
