--------------------------------------------
MUSIC CLASSIFICATION ON THE BASIS OF MOOD
--------------------------------------------
The project tries to address a classification system that tags the moods for music,based on music
features. A Music classification system which has been built upon on a classification algorithm,
trained to predict the mood of songs based on song lyrics and the acoustic analysis data. The
final output of this experiment shows music corresponding to happy, angry, sad, relax mood. In
a nut shell it classifies music on mood with the help of lyrical and acoustic data and compares the
predictions of both classifiers.

-------------
CONTRIBUTORS
-------------
Prakash Ranjan Singh 
Prateek Singh Arya 
Prince Kumar Katiyar 
Vijay Prakash Chaurasia 

----------------
Getting Started
----------------
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

------------------
Files Description
------------------
-[additional_csv_files]:contains csv files that were used to get the final dataset.
-[MSD_text_database]:contains Million Song Dataset text files that were used to get the database of songs with artist name and song title.
-[Screenshots]:contains screenshots of output screen of project run and results.
-[support_python_files]:contains python files that were used to apply manipulations over database and code to get spotify acoustic features data in the process of creating the database.
-[VPN_setup_files]:contains VPN software exe.
-[a_fier.py]:Python file for acoustic feature based mood classifier.
-[t_fier_new.py]:Python file for lyrical feature based mood classifier.
-[f1combfinal2.csv]:CSV file dataset for acoustic and lyrical features based mood classifier.


--------------
Prerequisites
--------------
What things you need to install the software and how to install them.
Install these Python libraries and Packages:
1. spotipy
2. pandas 
3. json
4. Seaborn
4. matplotlib
5. Sklearn
6. pylyrics
7. NumPy
8. web browser
9. NLTK
10. wordcloud
11. beautifulsoup.


------
Steps
------
1.Setup Anaconda for Python3.6 and above

Installing on Windows
-Download the installer:
----link--https://anaconda.org/anaconda/python
----Miniconda installer for Windows.
----Anaconda installer for Windows.
-Double-click the .exe file.

-Follow the instructions on the screen.

-If you are unsure about any setting, accept the defaults. You can change them later.

-When installation is finished, from the Start menu, open the Anaconda Prompt.

-Test your installation.

2.Connect to VPN through available software.
3.Setup Spotify developer ID and get API key: https://beta.developer.spotify.com/
4.Open Anaconda Prompt on project folder and run a_fier.py (for acoustic based classifier)
5.And similarly run t_fier_new.py (for lyrical based classifier)

-----
CODE
----
github-https://github.com/prakashranjan/mmcl
