# Switch to the feature/case branch: create a local copy of feature/case from the remote repository.
# Restore case_operations.py to a previous state: using the commit 6b2ec72, restore the file case_operations.py 
# to its state from that commit. This will undo changes that were made from that point.
# Commit the changes: after restoring the file, stage and commit the changes with the following commit message: 
# refactor: restored case operations from 6b2ec72.
# Verify the branch: ensure that the feature/case branch contains the correct number of commits and that the 
# restored file matches the content from the 6b2ec72 commit.

git checkout feature/case
ls
git log --oneline
git checkout 6b2ec72 -- case_operations.py
git commit -m "refactor: restored case operations from 6b2ec72"
git log --oneline
git diff 6b2ec72 feature/case -- case_operations.py
