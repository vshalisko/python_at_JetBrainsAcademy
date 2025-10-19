# Switch to the main branch. This is the branch where the production-ready version of the project is stored.
# Merge feature/math into the main. This will integrate the new file containing the new feature into the main codebase.
# Delete the feature/math branch as it's no longer needed. This helps keep the repository clean and avoids clutter from unused branches.

git checkout main
git merge feature/math
git branch -d feature/math
