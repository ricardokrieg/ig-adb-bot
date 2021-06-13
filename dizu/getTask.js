const fs = require('fs');
const DizuAPI = require('./DizuAPI');

const accountId       = process.argv[2];
const accountUsername = process.argv[3];

(async () => {
  try {
    const data = await (new DizuAPI()).getTask(accountId);
    fs.writeFileSync(`${accountUsername}_usernames.txt`, `${data.username}\n`, { flag: 'a+' });
    fs.writeFileSync(`${accountUsername}_actions.txt`, `${data.username};${data.connectFormId};${data.accountIdAction}\n`, { flag: 'a+' });
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
})();
