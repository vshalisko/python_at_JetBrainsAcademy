# Switch to the 0.2.x-dev branch: this is your development branch, where new features should be integrated. 
# Ensure that you are working from this branch before proceeding;
# Cherry-pick the last commit from the main branch: use the appropriate command to transfer the most recent 
# commit from main to 0.2.x-dev. This will allow the feature to be correctly integrated into the development branch.
# After cherry-picking the commit, return to the main branch to prepare for the reset;
# Reset the main branch to its original state: reset the main branch to the state it was in before the last merge, 
# leaving only the initial commit (feat: Initial).

git log --oneline
git checkout 0.2.x-dev
git cherry-pick e3b92a7
git checkout main
git reset --soft HEAD~3
git log --oneline
