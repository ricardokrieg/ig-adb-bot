const fs = require('fs');
const DizuAPI = require('./DizuAPI');
const debug = require('debug')('bot:dizu:confirmTask');
const { sleep } = require('../old_src/v2/utils/sleep');

const accountUsername = process.argv[2];

(async () => {
  try {
    const content = fs.readFileSync(`${accountUsername}_actions.txt`, 'utf8');
    const submitted = [];

    for (let line of content.split('\n')) {
      if (line.length) {
        const [username, taskId, accountId] = line.split(';');

        if (submitted.includes(username)) {
          debug(`${username} already submitted. skipping.`);
          continue;
        }

        debug(`Submitting ${line}...`);

        // await sleep(60000);
        await (new DizuAPI()).submitTask(taskId, accountId);

        submitted.push(username);
      }
    }

    debug(`Submitted ${submitted.length} tasks`);
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
})();
