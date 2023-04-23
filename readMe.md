# Introduction

I have taken the help of following modules to scrape the data from github
https://pypi.org/project/github-email-scraper/

## Folder structure -

```bash
├── data
│   ├── keepsake.txt
│   └── mlflow.txt
├── email
│   ├── keepsake.csv
│   └── mlflow.csv
├── readMe.md
├── requirements.txt
├── scrapper.js
└── test.py
```

## Code (Execute on Terminal)

You can run the following command to get the email id of the single user

You have limited requested using this command.

```bash
github-email-scraper -u AkshilVT -a
```

You can use the following command to get the email id of the single user using github token (allows 5000 requests per hour)

```bash
github-email-scraper -u AkshilVT -a --auth-user YOUR_GITHUB_USERNAME --token YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
```

You can create a .txt file and add the list of users in the file and run the following command to get the email id of the users

```bash
github-email-scraper -U ./data/mlflow.txt --all --auth-user YOUR_GITHUB_USERNAME --token YOUR_GITHUB_PERSONAL_ACCESS_TOKEN >> ./email/mlflow2.csv
```

I modified the code a little bit to do write operations directly in the destination file. It is named as test.py

```bash
py test.py -U ./data/keepsake.txt --all --auth-user YOUR_GITHUB_USERNAME --token YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
```

I have also tested getting emails using github public api. The code for that is in scrapper.js

## How to get Personal Access Token?

go to github -> settings -> developer settings -> personal access token -> generate new token -> select all the scopes (here you need only user and email but having all scopes is not a necessity) -> generate token -> copy the token and use it in the above command
