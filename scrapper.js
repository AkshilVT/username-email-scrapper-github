// Octokit.js
// https://github.com/octokit/core.js#readme
const { Octokit } = require('@octokit/core');
var fs = require('fs');
const octokit = new Octokit({
  auth: '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',
});

// Requiring the module
const reader = require('xlsx');

// Reading our test file
const file = reader.readFile('./data/keepsake.xlsx');

const sheets = file.SheetNames;

// for (let i = 0; i < sheets.length; i++) {
//   const temp = reader.utils.sheet_to_json(file.Sheets[file.SheetNames[i]]);
//   temp.forEach((res) => {
//     getEmails(res.ID);
//   });
// }

async function getEmails(user) {
  await octokit
    .request(`GET /${user}/public_emails`, {
      headers: {
        'X-GitHub-Api-Version': '2022-11-28',
      },
    })
    .then((response) => {
      for (let i = 0; i < response.data.length; i++) {
        console.log(response.data[i].email);
        fs.appendFileSync(
          './email/keepsake.csv',
          response.data[i].email + '\n',
          (err) => {
            if (err) throw err;
            console.log('Data written to file');
          }
        );
      }
      return response.data;
    })
    .catch((error) => {
      console.log(error);
      return [];
    });
}
getEmails('AkshilVT');
