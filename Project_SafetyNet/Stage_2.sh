# Create a new branch named feature/math from the existing 0.2.x-dev branch. 
# This branch will serve as the isolated environment where you will add new functionality. 
# Ensure that this new branch is active before proceeding to the next steps.
# In the newly created feature/math branch, create a file named math_operations.py 
# in the root directory of the project.
# The file should contain a basic mathematical function that performs the addition of two 
# integers and returns the result:
#
#def addition(a, b):
#    return a + b
#
# Stage and commit the changes with the commit message: feat: new function addition

git checkout -b feature/math
git add math_operations.py
git commit -m "feat: new function addition"
