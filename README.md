# Mini-Cocktail DB
In hopes of increasing access to cocktail making, we are creating a platform that provides advanced cocktail recipe search, sharing, and saving. On our website, users can search available cocktails based on ingredients they have, drink category, and alcoholic content. Users can also share personal recipes and review others’ recipes. In a Pinterest-esque format, users can save cocktails to curated lists based on their liking (e.g. Summer drinks, classy drinks, for this weekend, etc). 

## Updates since Milestone 2

### Bryan
- Updated functionality for menus being added
- And helped with user login and authentication function

### Stuart
- Updated functionality of ingredients/bar cart
- Updated functionality of drinks page
- Created individual drink display page/template

### Cheryl
- Implemented front end UI, standardized design across website
- Updated how ingredients are linked to drinks 

### Ashir
- Update functionality of reviews (add rating, clear reviews, and get average ratings)

### Jaimie
- Implemented user registration, login, authentication and use of current user information throughout database
- Implemented bar cart so users can add drinks to cart.

## Original Project Info
Skeleton code for the CompSci 316 undergraduate course project.
This course project is intended as a 'standard option'.

Originally created by [Rickard Stureborg](http://www.rickard.stureborg.com) and [Yihao Hu](https://www.linkedin.com/in/yihaoh/) for Fall 2021.
Amended for Fall 2022.

We assume you are in your class VM.
If you have a different setup, your mileage with the following instructions may vary.

## Installing the Current Skeleton

1. Fork this repo by clicking the small 'Fork' button at the very top right on Gitlab.
   It's important that you fork first, because if you clone the directory directly you won't be able to push changes (save your progress) back to Gitlab.
   Name your forked repo as you prefer.
2. In your newly forked repo, find the blue "Clone" button.
   Copy the "Clone with SSH" text.
   In your terminal on the VM, you can now issue the command `git clone THE_TEXT_YOU_JUST_COPIED`.
   Make sure to replace 'THE_TEXT_YOU_JUST_COPIED' with the "Clone with SSH" text.
3. In your VM, change into the repository directory and then run `./install.sh`.
   This will install a bunch of things, set up an important file called `.flashenv`, and creates a simple PostgreSQL database named `amazon`.
4. If you are running a Google VM, to view the app in your browser, you may need to edit the firewall rules.
   The [Google VM instructions](https://courses.cs.duke.edu/fall22/compsci316d/instructions/gcp/) on the course page has instructions for how to add rules at the bottom.
   If those for some reason are outdated, here are [instructions provided by Google](https://cloud.google.com/vpc/docs/using-firewalls).
   Create a rule to open up port 5000, which flask will run on.

## Running/Stopping the Website

To run your website, in your VM, go into the repository directory and issue the following commands:
```
source env/bin/activate
flask run
```
The first command will activate a specialized Python environment for running Flask.
While the environment is activated, you should see a `(env)` prefix in the command prompt in your VM shell.
You should only run Flask while inside this environment; otherwise it will produce an error.

If you are running a local Vagrant VM, to view the app in your browser, you simply need to visit [http://localhost:5000/](http://localhost:5000/).
If you are running a Google VM, you will need to point your browser to `http://vm_external_ip_addr:5000/`, where `vm_external_ip_addr` is the external IP address of your Google VM.

To stop your website, simply press <kbd>Ctrl</kbd><kbd>C</kbd> in the VM shell where flask is running.
You can then deactivate the environment using
```
deactiviate
```

## Working with the Database

Your Flask server interacts with a PostgreSQL database called `amazon` behind the scene.
As part of the installation procedure above, this database has been created automatically for you.
You can access the database directly by running the command `psql amazon` in your VM.

For debugging, you can access the database while the Flask server is running.
We recommend you open a second shell on your VM to run `psql amazon`.
After you perform some action on the website, you run a query inside `psql` to see the action has the intended effect on the database.

The `db/` subdirectory of this repository contains files useful for (re-)initializing the database if needed.
To (re-)initialize the database, first make sure that you are NOT running your Flask server or any `psql` sessions; then, from your repository directory, run `db/setup.sh`.
* You will see lots of text flying by---make sure you go through them carefully and verify there was no errors.
  Any error in (re-)initializing the database will cause your Flask server to fail, so make sure you fix them.
* If you get `ERROR:  database "amazon" is being accessed by other users`, that means you likely have Flask or another `psql` still running; terminate them and re-run `db/setup.sh`.
  If you cannot seem to find where you are running them, a sure way to get rid of them is to restart your VM.

To change the database schema, modify `db/create.sql` and `db/load.sql` as needed.
Make sure you to run `db/setup.sh` to reflect the changes.

Under `db/data/`, you will find CSV files that `db/load.sql` uses to initialize the database contents when you run `db/setup.sh`.
Under `db/generated/`, you will find alternate CSV files that will be used to initialize a bigger database instance when you run `db/setup.sh generated`; these files are automatically generated by running a script (which you can re-run by going inside `db/data/generated/` and running `python gen.py`.
* Note that PostgreSQL does NOT store data inside these CSV files; it store data on disk files using an efficient, binary format.
  In other words, if you change your database contents through your website or through `psql`, you will NOT see these changes reflected in these CSV files (but you can see them through `psql amazon`).
* For safety, a database should never store password in plain text; instead it stores one-way hash of the password.
  This rule applies to the password value in the CSV files too.
  To see what hashed password value you should put in a CSV file, see `db/data/gen.py` for example of how compute the hashed value.

## Git Tips

These instructions seem long, but they aren't complicated.
If you've never worked with merge requests, make sure to read this thoroughly. 

To work on a gitlab project with many team members, you want to avoid working directly on the `main` branch as much as possible.
If multiple people work on this branch at the same time, you are likely to run into conflicts and be forced to restore old versions.
This is a mess.
Instead, use new branches every time you add a feature or make an edit, and then merge these into the main branch.
This is how to do it:

Let's imagine we want to create a new function to help with some specific query of the database. Before you begin, create and checkout a new branch for this feature.
1. `git branch query-feature` will create a branch named `query-feature`.
   You can change the name as you'd like.
   Then switch to this branch using `git checkout query-feature`.
2. Once you are on this branch, get to work.
   Make the edits you need to the files you want to work on.
3. Run the command `git status` to see what files have changed.
   Let's say you only edit the file `app/db.py` to add the new function along with some comments, and `README.md` to include some information about this feature.
   These files will then appear in red under the title `modified:`.
4. Now that you're done editing, you want to save your changes.
   Each save appears as a notification on gitlab in the form of a "commit".
   To be helpful, we save our edits in small chunks so that others can easily read these notifications and follow along which changes were made.
   Let's say we want to make two commits, one for `app/models/user.py` and another for `README.md`. 
   1. We make the first commit ready by adding the changes to `app/models/user.py` using the command `git add app/models/user.py`.
      Now, running `git status` will show this file in green, indicating it is being tracked.
   2. Now we can commit this change using the command `git commit -m "MESSAGE"`.
      We replace `MESSAGE` with a short description of what the change entailed.
      This is what shows up in the notification on gitlab. For example: `git commit -m "created a new function to find the total amount spent by a user"`
   3. Now repeat this process for the `README.md` file.
      That is: `git add README.md`, then `git commit -m "updated readme to include description of 'all-time spending' feature"`.
   4. You've saved your changes!
      But they're still only local (to your VM).
      To upload them to gitlab you need to run `git push --set-upstream origin query-feature`.
      By now you (and your teammates) should be able to see that you've made changes on the gitlab website.
      These changes appear in your repository under Repository -> Branches -> `query-feature`.
5. For others to add on top of your work, you want to open a "merge" request to merge your branch into the `main` branch.
   This request is an open invitation for your teammates to take a look at your code, make sure the changes look good to them, and then incorporate them onto the `main` branch for others to use.
   To open a merge request, click on "merge requests" in the left navigation bar on gitlab, and then hit the blue "New merge request" button at the top right.
   It will ask you to select a source branch.
   For our example above this would be the `query-feature` branch.
   For the target branch, leave it as `main`.
6. Once the merge request is created, ping your teammates to take a look at it.
   If they think it's acceptable, they just need to click "merge" and the code you've written gets incorporated.
   Now you can safely delete the `query-feature` branch on gitlab.
   Done!

## Note on Hiding Credentials

Use the file `.flaskenv` for passwords/secret keys---we are talking about passwords used to access your database server, for example (not user passwords for your website in CSV files described earlier).
This file is NOT tracked by git and it was automatically generated when you first ran `./install.sh` (from a template file).
You can change any credentials in this file.
Only share the contents of this file securely with your teammates, but don't check it into git because your credentials would be exposed to everybody on gitlab if you are not careful.
You can generate strong passwords with this tool: https://www.lastpass.com/password-generator

## Editing Files using VS Code

We recommend Visual Studio Code (VS Code).
You can download and install it for your laptop from [this link](https://code.visualstudio.com/Download).

If you use a local Vagrant VM, we recommending placing your project directory under `~/shared/` so you can edit files using VS Code running on your laptop.

If you use a Google VM, your files live on the Google VM and you have no direct access to them.
However, you can still set up VS Code to edit the files directly via SSH.
See `README-vscode.md` in this repository for setup instructions.
