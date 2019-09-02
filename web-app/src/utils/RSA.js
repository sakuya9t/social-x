import * as JsEncryptModule from 'jsencrypt';

const crypt = new JsEncryptModule.JSEncrypt();

class RSA{
    constructor(){
        fetch('http://localhost:5000/publickey')
        .then((res) => res.json())
        .then((body) => body.key)
        .then((key) => crypt.setKey(key));
    }

    encrypt = (body) => crypt.encrypt(body);
    decrypt = (body) => crypt.decrypt(body);
}
export default RSA;