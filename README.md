# trelloautoassign
Trello Auto Assign.

Automatically assigns all cards on a Trello board to a user, and unassigns them if they're in a list labelled 'Done.'
Set your environment variables (defined at the top of the script) before running this.
Only applies to boards with a given organization name (defined in an environment variable).
I recommend automating this with cron.

Trello doesn't allow automatically assigning a card to yourself, but this is required to view all of your cards sorted by due date. Additionally, you probably don't want to see the due dates of cards in a list called 'Done'. So, automate these issues away!
