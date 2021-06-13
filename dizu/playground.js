const DizuAPI = require('./DizuAPI');
const debug = require('debug')('bot:dizu:playground');
const inquirer = require('inquirer');

const accountId = '46294080253';

(async () => {
  try {
    const tasks = [];
    for (let i = 1; i <= 3; i++) {
      debug(`#${i}`);
      const data = await (new DizuAPI()).getTask(accountId);
      tasks.push(data);

      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    for (let task of tasks) {
      console.log(task.username);
    }

    const { message } = (await inquirer.prompt([
      {
        type: 'input',
        name: 'message',
        message: 'Pronto?',
      },
    ]));

    for (let task of tasks) {
      await (new DizuAPI()).submitTask(task.connectFormId, task.accountIdAction);
    }
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
})();
