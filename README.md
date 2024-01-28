# Conlang organizer for my Computer Science IA
Welcome to my product! This is my first time dealing with Flask and Python, so there could be large number of bugs. Please report them to me if there are. Furthermore, it is specifically designed to organize *Dukhrit*, which means that some phonemes and inflection features (such as prefix-based inflections rather than suffix, verb classes etc.) would be missing. 
 
 # Installation guide
 Download a release, then unzip the file.
 Then, either:
 - Install Python from the Microsoft Store
 - or install Python from https://www.python.org/downloads/release/python-3120/. Then, go to Settings > Manage App Execution Aliases, and disable the default Python shortcuts.

Right-click the folder, and press "Open in Terminal". Now type:
```
cd <paste your file path here>
```
Then, type:
```
venv\Scripts\Activate
```
Once that's done, enter the following:
```
pip install flask flask_migrate flask_sqlalchemy flask_wtf
```
With that, you can now use the application~

# Running the application
At the moment, the only method to run the application is:
- Right-click the folder, and press "Open in Terminal".
- Type `venv\Scripts\Activate`
- Type `python -m flask run`
- Go to `localhost:5000` in your browser.

# Updating the programme
When you download a new version of the programme, simply copy and paste the `app.db` file from the previous folder into the new folder. Replace the existing mock database.
