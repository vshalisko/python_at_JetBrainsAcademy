# Fix the bug in the main.py file;
# Add changes to the staging area;
# Commit changes with the message fix: Bug fix month name;
# Create an annotated tag by increasing your last tag's patch version by 1 and with the message Month name bug fix;
# Push the modifications and tags to the remote's main branch.


sed -i 's/%m/%B/g' main.py
git add main.py
git commit -m "fix: Bug fix month name"
git tag -a 0.2.1 -m "Month name bug fix"
git push origin main --tags
