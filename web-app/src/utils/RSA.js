const NodeRSA = require('node-rsa');

class RSA{
    constructor(){
        fetch('http://localhost:5000/publickey')
        .then((res) => res.json())
        .then((body) => body.key)
        .then((key) => this.key = new NodeRSA(key));
    }

    encrypt = (body) => this.key.encrypt(body, 'base64');
    decrypt = (body) => this.key.decrypt(body, 'base64');
}
export default RSA;