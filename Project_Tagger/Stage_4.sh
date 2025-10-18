# Delete the v0 tag from the local repository;
# Delete the v0 tag from the remote repository;
# For your most recent commit, create the annotated tag 0.1.0 with the message Day name functionality;
# Push the tag to the remote's main branch.

git tag -d v0
git push origin --delete v0
git tag -a 0.1.0 -m "Day name functionality"
git push origin 0.1.0
