# Create a script with the name main.py and with the content below
#from datetime import datetime
#
#
#def get_day_name():
#    date_obj = datetime.utcnow()
#    day_name = date_obj.strftime('%A')
#    return day_name
#
# Add the changes to the staging area;
# Make your first commit with the commit message feat: Day name function.

echo -e "from datetime import datetime\n\n" > main.py
echo "def get_day_name():" >> main.py
echo -e "\tdate_obj = datetime.utcnow()" >> main.py
echo -e "\tday_name = date_obj.strftime('%A')" >> main.py
echo -e "\treturn day_name" >> main.py
git add main.py
git commit -m "feat: Day name function"
