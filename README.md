# trelloautoassign
Trello Auto Assign.

Automatically assigns all cards on a Trello board to a user, and unassigns them if they're in a list labelled 'Done.'
Set your environment variables (defined at the top of the script) before running this.
Only applies to boards with a given organization name (defined in an environment variable).
I recommend automating this with cron.

Trello lets you view all of your cards sorted by due date, but only if they are assigned to you. This works well
in a team setting; however, if you use personal Trello boards for your own individual productivity, seeing all
cards by due date would require you to manually assign each card to yourself. Furthermore, if you have a list
called 'Done', you probably don't want to see its cards on a list of due dates; you would need to unassign it
manually.

This script removes the need for manual assignments/reassignments in the above scenario.
