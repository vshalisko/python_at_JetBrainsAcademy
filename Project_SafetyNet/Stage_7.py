# Create a release branch (0.2.x): create a new branch named 0.2.x from the 0.2.x-dev branch. 
# This branch will serve as the release branch, containing the final version of the code that will be deployed to production;
# Fix the bug in the make_upper function: in the case_operations.py file, the make_upper function 
# currently prints the uppercase version of the text instead of returning it. Modify the function so that it returns the 
# uppercase text, as shown in the provided code snippet:
#
#def make_upper(text):
#    return text.upper()
#
#Commit the bug fix: after fixing the bug, commit the changes to the 0.2.x branch with the commit message: fix: bug-fix make_upper.
#Verify the repository: ensure that the 0.2.x branch contains the correct number of commits (9 commits in total, 
# including the bug fix), and that the make_upper function has been correctly updated.

git branch 0.2.x
git checkout 0.2.x
ls
git add .
git commit -m "fix: bug-fix make_upper"
git log --oneline
