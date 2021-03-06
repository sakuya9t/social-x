import {server_ip} from '../config';
const forge = require('node-forge');

class RSA{
    constructor(){
        this.key = "";
        this.getKey();
    }

    getKey = async () => {
        let res = await fetch(`http://${server_ip}:5000/key`);
        res = await res.json();
        this.key = res.data;
    }

    encrypt = (body) => {
        const publicKey = forge.pki.publicKeyFromPem(this.key);
        const encrypted = publicKey.encrypt(body, "RSA-OAEP", {
            md: forge.md.sha256.create(),
            mgf1: forge.mgf1.create()
        });
        const base64 = forge.util.encode64(encrypted);
        return base64;
    }
}
export default RSA;