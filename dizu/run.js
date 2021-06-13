const exec = require('child_process').exec;

class Commander {
  async execCommand(cmd) {
    return new Promise((resolve) => {
      exec(cmd, (error) => {
        if (error) {
          console.error(`exec error: ${error}`);
        }

        resolve();
      });
    });
  }
}

const commander = new Commander();

(async () => {
  const accountId = `46294080253`;
  const accountUsername = `and_rson_fel_pe`;

  for (let i = 1; i <= 50; i++) {
    await commander.execCommand(`npx @babel/node dizu/getTask.js ${accountId} ${accountUsername}`);
  }
})();
