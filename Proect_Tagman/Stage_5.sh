# Add the get_month_name function to the main.py file
#from datetime import datetime
#
#
#def get_day_name():
#    date_obj = datetime.utcnow()
#    day_name = date_obj.strftime('%A')
#    return day_name
#
#
#def get_month_name():
#    date_obj = datetime.utcnow()
#    month_name = date_obj.strftime('%m')
#    return month_name
#
#
# Add changes to the staging area;
# Commit changes with the message feat: Month names;
# Create an annotated tag by increasing your last tag's minor version by one with the message Month name functionality;
# Push the modifications and tags to the remote's main branch.


echo -e "\n\n" >> main.py
echo "def get_month_name():" >> main.py
echo -e "\tdate_obj = datetime.utcnow()" >> main.py
echo -e "\tmonth_name = date_obj.strftime('%m')" >> main.py
echo -e "\treturn month_name" >> main.py
git add main.py
git commit -m "feat: Month names"
git tag -a 0.2.0 -m "Month name functionality"
git push origin main --tags
