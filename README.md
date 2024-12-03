```
 ________________________________________________________
|\______                                          ______/|
|%%%%%%%\______                            ______/%%%%%%%|
|%%%%%%%%%%%%%%\______              ______/%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%\_____  _____/%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%\/%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
|%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%|
 _________   __     _   _______   _________   ___
|___   ___| |  \   | | /  ____/  |___   ___| |   \
    | |     |   \  | | | /____       | |     | |\ \
    | |     | |\ \ | | \_____ \      | |     | |_\ \
    | |     | | \ \| | __    \ \     | |     | ____ \
 ___| |___  | |  \   | \ \___/ /     | |     | |   \ \
|_________| |_|   \__|  \_____/      |_|     |_|    \_\

 __    __   ___        _________   _
|  \  /  | |   \      |___   ___| | |
|   \/   | | |\ \         | |     | |
| |\  /| | | |_\ \        | |     | |
| | \/ | | | ____ \       | |     | |
| |    | | | |   \ \   ___| |___  | |_____
|_|    |_| |_|    \_\ |_________| |_______|
```
```
An Instagram Bot that checks your emails, summarises them using ChatGPT, and sends you the summaries
via your Instagram inbox

Uses the Gmail API, OpenAI API, and a library for accessing Instagram called Instagrapi
Also uses pystray to run as a tray application

Has a batch file in the startup folder that runs it in the background so I dont have to open it
when I turn on my computer. checks the 10 most recent emails on startup, just in case it missed
some while it wasnt running.
```

```
Created By Matthew Shanahan
Contact Me
    Instagram:  _hi_its_matt
    Discord:    hi_its_matt
    Email:      hi.its.ma77@gmail.com
```

```
Want to use it for yourself? You've got two options:
```

```
   1. Contact me, I can add your username to the program running on my computer and
      you will start receiving email updates through instagram with no effort on your
      behalf.

      I charge $5/month for this service as a baseline but depending on the volume
      of emails I may charge more - this is because OpenAI API calls cost real money,
      so the price will scale depending on how many calls have to be made.
      consider unsubscribing from spam emails to reduce the overhead cost so I can
      give you a fair price.
```

```
   2. Run this program locally on your own computer. This github repository is missing
      some important files because they are secret information and I dont want it on the
      internet.
      You will need to provide these files yourself for the program to work locally:

         Program/OpenAI_API_Key.txt
            The key to your OpenAI account. so OpenAI know who to charge for the API
            calls.

         Program/credentials.json
            The credentials for accessing your Gmail Account.
            Generated by logging into Google Cloud Console and adding the Gmail Api
            to a new project.

         Program/token.json
            Generated automatically once authorised with Gmail
            Allows the program access to your emails and allows the program to generate
            a new token when the current one expires

         Program/.env - contains the username and password for the account that you
            want to recieve messages from

            Contents should look like this:
            INSTA_USERNAME=Your_Bot_Account_Username
            INSTA_PASSWORD=Your_Bot_Account_Password

      Feel free to contact me for support if you need help! I'm usually available on Instagram @_hi_its_matt
```
