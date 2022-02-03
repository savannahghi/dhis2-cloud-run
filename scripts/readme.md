### backup.sh reads

**What to change**
- Set the correct values for your variables
- Check that you have set the correct path to your bucket i.e gs://...


**How to run the script**
- Copy the file to your VM dir; */home/some_user/backup.sh*
- Make the file executable by running *sudo chmod +x /home/some_user/backup.sh*
- Run the file by the cmd *sudo /home/some_user/backup.sh*


**Set periodic execution of the file, every 3.30pm**
 - Run the cmd *crontab -e*; this will open cron file.
 - Edit the file by adding the line;
   *30 3 * * * sudo /home/some_user/backup.sh*
 - Save the file and exit.
 - Restart cron job by executing; *sudo service cron restart*


**Read resources**
	// bash introduction
• https://linuxconfig.org/bash-scripting-tutorial-for-beginners
	// cron job timing cheet sheet
• https://www.codementor.io/@akul08/the-ultimate-crontab-cheatsheet-5op0f7o4r


