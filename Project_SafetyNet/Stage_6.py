# Rebase the feature/case branch with 0.2.x-dev: before merging, to ensure that it includes the latest 
# changes from the development branch. This is necessary to avoid conflicts and ensure 
# that the feature branch is up to date.
# Switch to the 0.2.x-dev branch: after rebasing, switch to the 0.2.x-dev branch. This is the development 
# branch where the latest features are integrated.
# Merge the feature/case branch into 0.2.x-dev: perform the merge operation to integrate 
# the changes from the feature/case branch into the 0.2.x-dev branch. This will bring the new 
# feature into the development branch without creating 
# a separate merge commit.
# Delete the feature/case branch: once the merge is complete, delete the feature/case branch. 
# This helps keep the repository clean by removing branches that are no longer needed.
# Verify the repository state: ensure that the 0.2.x-dev branch now contains the commits 
# from the feature/case branch and that the feature/case branch has been successfully deleted.

git checkout 0.2.x-dev
git pull origin 0.2.x-dev
git checkout feature/case
git rebase 0.2.x-dev
git checkout 0.2.x-dev
git merge feature/case
git branch -D feature/case
git log --oneline
