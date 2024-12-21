import os
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen


def main():
    # Ask for start and end dates
    date_input = input("Enter start and end dates in the format 'YYYY MM DD YYYY MM DD': ").strip()
    try:
        start_year, start_month, start_day, end_year, end_month, end_day = map(int, date_input.split())
        start_date = datetime(start_year, start_month, start_day)
        end_date = datetime(end_year, end_month, end_day)
        if start_date > end_date:
            raise ValueError("Start date must be earlier than or equal to end date.")
    except ValueError as e:
        print(f"Invalid date input: {e}")
        return

    # Configuration dictionary for other parameters
    config = {
        "max_commits": 15,  # Maximum commits per day
        "frequency": 80,  # Percentage of days to commit
        "repository": None,  # Remote repository URL (set to None if not used)
        "user_name": "Your Name",  # Override Git user.name (set to None for default)
        "user_email": "youremail@example.com",  # Override Git user.email (set to None for default)
        "daily_start_time": 9,  # Start hour for daily commits (0-23)
        "daily_end_time": 17,  # End hour for daily commits (0-23)
    }

    daily_start_time = config["daily_start_time"]
    daily_end_time = config["daily_end_time"]
    if daily_start_time < 0 or daily_end_time > 23 or daily_start_time >= daily_end_time:
        raise ValueError("Invalid daily time range")

    # Directory and Git initialization
    directory = f"repository-{start_date.strftime('%Y-%m-%d')}"
    if config["repository"]:
        start = config["repository"].rfind("/") + 1
        end = config["repository"].rfind(".")
        directory = config["repository"][start:end]

    os.mkdir(directory)
    os.chdir(directory)
    run(["git", "init", "-b", "main"])

    if config["user_name"]:
        run(["git", "config", "user.name", config["user_name"]])
    if config["user_email"]:
        run(["git", "config", "user.email", config["user_email"]])

    # Generate commits
    curr_date = start_date
    while curr_date <= end_date:
        if randint(0, 100) < config["frequency"]:
            for commit_time in generate_commit_times(curr_date, daily_start_time, daily_end_time, config):
                contribute(commit_time)
        curr_date += timedelta(days=1)

    # Push to remote if specified
    if config["repository"]:
        run(["git", "remote", "add", "origin", config["repository"]])
        run(["git", "branch", "-M", "main"])
        run(["git", "push", "-u", "origin", "main"])

    print("\nRepository generation completed successfully!")


def contribute(date):
    with open(os.path.join(os.getcwd(), "README.md"), "a") as file:
        file.write(message(date) + "\n\n")
    run(["git", "add", "."])
    run(["git", "commit", "-m", f'"{message(date)}"', "--date", date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    Popen(commands).wait()


def message(date):
    return date.strftime("Contribution: %Y-%m-%d %H:%M")


def generate_commit_times(date, daily_start_time, daily_end_time, config):
    """Generate commit times for a specific date."""
    start_hour, end_hour = daily_start_time, daily_end_time
    commits = []
    
    # Generate a random number of commits within the allowed range
    num_commits = randint(1, config['max_commits'])
    
    for _ in range(num_commits):
        hour = randint(start_hour, end_hour)
        
        # Generate a random minute value within the valid range
        minute = randint(0, 59)
        
        # Add the commit time
        commits.append(date.replace(hour=hour, minute=minute, second=0))
    
    return commits


if __name__ == "__main__":
    main()
