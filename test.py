import sys
import argparse

import requests


def get_url(url: str, auth: tuple):
    """Get a GitHub URL and check for rate limits and errors"""
    if auth:
        req = requests.get(url, auth=auth)
    else:
        req = requests.get(url)
    if not req.ok:
        if req.headers["x-ratelimit-remaining"] == "0":
            print("Rate limit exceeded")
            sys.exit(1)
        else:
            return []
            # print("Unknown error:")
            # print(req.headers)
            # print(req.status_code)
            # sys.exit(1)
    else:
        return req.json()


def main():
    """Scrapes GitHub users for their emails"""
    parser = argparse.ArgumentParser()
    parser.description = "Scrape GitHub for email addresses associated with a username. Choose to search through public events (--events), commits in the user's repositories (--commits), or both (--all). Specify users on the command line (-u) or load a file with one user per line (-U)."
    user_parse_group = parser.add_mutually_exclusive_group(required=True)
    user_parse_group.add_argument(
        "-u", "--user", action="append", help="Target GitHub username")
    user_parse_group.add_argument("-U", "--user-list", type=argparse.FileType("r"),
                                  help="File containing list of target GitHub usernames, or - for stdin")
    parser.add_argument("-c", "--commits", action="store_true",
                        help="Look through user's commits in their repos")
    parser.add_argument("-e", "--events", action="store_true",
                        help="Look through user's public events")
    parser.add_argument("-a", "--all", action="store_true",
                        help="Commits and events")
    parser.add_argument("-o", "--other-users", action="store_true",
                        help="Include emails from commits not associated with the GitHub user. This may find other email addresses beloning to the user that they haven't manually associated with their GitHub account, but may also contain a lot of emails from other accounts if the repo is a fork or has multiple contributors.")
    parser.add_argument("-n", "--name", action="store_true",
                        help="Show commit/event author name")
    parser.add_argument("-r", "--repo", action="store_true",
                        help="Show repo the email was (first) found in")
    parser.add_argument("-l", "--auth-user",
                        help="Your GitHub username to use for authentication; use with --token")
    parser.add_argument("-t", "--token",
                        help="Your GitHub personal access token; use with --auth-user")

    args = parser.parse_args()

    if args.all:
        args.commits = True
        args.events = True
    elif not args.commits and not args.events:
        # Must have commits and/or events flag set
        print("Specify an action")
        parser.print_usage()
        sys.exit(1)

    # Make sure auth_user and token are either both set or not
    if (args.auth_user and not args.token) or (args.token and not args.auth_user):
        print("Specify a username and a token to perform authentication")
        parser.print_usage()
        sys.exit(1)

    # Setup authentication header
    if args.auth_user and args.token:
        auth = (args.auth_user, args.token)
    else:
        auth = None

    # Load command-line users or users from specified file
    fp = open("./email/keepsake2.csv", "a")
    users = []
    if args.user:
        users = args.user
    elif args.user_list:
        with args.user_list as f:
            users = f.read().splitlines()
        args.user_list.close()

    # Loop over each user
    for user in users:
        user_emails = set()

        # Loop over public events
        if args.events:
            events = get_url(
                f"https://api.github.com/users/{user}/events/public", auth)
            for event in events:
                try:
                    for commit in event["payload"]["commits"]:
                        try:
                            if args.name:
                                if (commit["author"]["email"], commit["author"]["name"]) not in user_emails:
                                    user_emails.add(
                                        (commit["author"]["email"], commit["author"]["name"]))
                                    # print(
                                    #     f'{commit["author"]["email"]} ({commit["author"]["name"]}){(" [" + event["repo"]["name"] + "]" if args.repo else "")}')
                                    fp.write(f'{commit["author"]["email"]} ({commit["author"]["name"]}){(" [" + event["repo"]["name"] + "]" if args.repo else "")} \n')
                            else:
                                if commit["author"]["email"] not in user_emails:
                                    user_emails.add(
                                        commit["author"]["email"])
                                    # print(
                                    #     f'{commit["author"]["email"]}{(" [" + event["repo"]["name"] + "]" if args.repo else "")}')
                                    fp.write(f'{commit["author"]["email"]}{(" [" + event["repo"]["name"] + "]" if args.repo else "")} \n')
                        except KeyError:
                            continue
                except KeyError:
                    continue

        # Loop over repos and commits
        if args.commits:
            repos = get_url(f"https://api.github.com/users/{user}/repos", auth)
            for repo in repos:
                if args.other_users:
                    commits = get_url(f'{repo["url"]}/commits', auth)
                else:
                    commits = get_url(
                        f'{repo["url"]}/commits?author={user}', auth)
                for commit in commits:
                    try:
                        if args.name:
                            if (commit["commit"]["author"]["email"], commit["commit"]["author"]["name"]) not in user_emails:
                                user_emails.add(
                                    (commit["commit"]["author"]["email"], commit["commit"]["author"]["name"]))
                                # print(
                                #     f'{commit["commit"]["author"]["email"]} ({commit["commit"]["author"]["name"]}){(" [" + repo["full_name"] + "]" if args.repo else "")}')
                                fp.write(f'{commit["commit"]["author"]["email"]} ({commit["commit"]["author"]["name"]}){(" [" + repo["full_name"] + "]" if args.repo else "")} \n')
                        else:
                            if commit["commit"]["author"]["email"] not in user_emails:
                                user_emails.add(
                                    commit["commit"]["author"]["email"])
                                # print(
                                #     f'{commit["commit"]["author"]["email"]}{(" [" + repo["full_name"] + "]" if args.repo else "")}')
                                fp.write(f'{commit["commit"]["author"]["email"]}{(" [" + repo["full_name"] + "]" if args.repo else "")} \n')
                    except KeyError:
                        continue
        fp.flush()
    fp.close()


if __name__ == "__main__":
    main()
