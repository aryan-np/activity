import os
import subprocess
from datetime import datetime, timedelta

# Function to run git commands
def run_git_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        exit(1)

# Path to your repository
REPO_DIR = "C:/Users/npary/OneDrive/Desktop/final/activity"  # Corrected path

# Name of the text file where dates will be appended
FILE_NAME = "commit_dates.txt"

# Start and End Dates
start_date = "2024-12-01"  # Example start date
end_date = "2024-12-10"    # Example end date

# Convert the string dates to datetime objects
start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")

# Change to the repository directory
os.chdir(REPO_DIR)

# Ensure the repository is initialized
if not os.path.isdir(".git"):
    print("This is not a Git repository!")
    exit(1)

# Loop through each date from start to end date
current_date = start_date
while current_date <= end_date:
    # Append the current date to the text file
    with open(FILE_NAME, "a") as f:
        f.write(current_date.strftime("%Y-%m-%d") + "\n")
    
    # Stage the changes (adding the file to Git)
    run_git_command(f"git add {FILE_NAME}")

    # Commit the changes with the date as the commit message
    commit_message = f"Commit on {current_date.strftime('%Y-%m-%d')}"

    # Set commit date dynamically
    commit_date = current_date.strftime("%Y-%m-%dT%H:%M:%S")

    # Run git commit with a custom date
    run_git_command(f"GIT_AUTHOR_DATE={commit_date} GIT_COMMITTER_DATE={commit_date} git commit -m \"{commit_message}\"")

    # Push the changes to the remote repository (to main branch)
    run_git_command("git push origin main")

    # Move to the next day
    current_date += timedelta(days=1)

print("Completed commits for all the days from start date to end date.")
