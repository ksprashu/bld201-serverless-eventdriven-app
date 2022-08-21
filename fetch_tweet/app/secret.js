const {SecretManagerServiceClient} = require('@google-cloud/secret-manager');
const client = new SecretManagerServiceClient();

async function displaySecrets() {
    const [secretResponse] = await client.listSecrets();

    // const [version] = await client.accessSecretVersion({
    //   name: name,
    // });
  
    // Extract the payload as a string.
    const payload = secretResponse.payload.data.toString();
  
    // WARNING: Do not print the secret in a production environment - this
    // snippet is showing how to access the secret material.
    console.info(`Payload: ${payload}`);
  }
  
//   accessSecretVersion();
module.exports = {
    displaySecrets: displaySecrets
};
