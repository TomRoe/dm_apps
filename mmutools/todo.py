# these should all be bilingual exports

### SMALLER ITEMS
# TODO Add confirmation step for deleting files
# TODO Add lending table to quantity, JS for having lent_to and other fields appear if "lent out" is selected as status
# TODO Create Location Table (with containers as locations)
# TODO Lend button beside quantities on item_detail --- form could ask how many, calculate difference etc
# TODO look into using ajax for popout close and refresh function -- talk to David -- see Travel app (urls, views, jsonresponse)
# TODO Be able to click on "Location" in _quantity and take to location_detail page to see address

### LARGER ITEMS - PRIORITY
# TODO Testing Units so Dev version can be deployed

### OTHER LARGER ITEMS
# TODO remake models with fields that make sense for lending and make items--supplier relation M2M
# TODO Add Historical model or some way to track history of inventory of each item (ie. track previous additions, subtractions, inventory control updates) --would need a description field for inveotry control comments (ie. "item missing")
# TODO Add Bulk Lending View to checkout (change to "lent out") status multiple items of various quantities all on one page -- how to sort so you can find all items you want also?
# TODO Bulk Check In View to check back in items -- should be easy enough to sort on a person's name and then bulk check back in items you have out


### SOLVED - I THINK
# TODO Fix quantity calculation error in views.py -- see error message there, need to create case for when no values entered yet -- I think I fixed this!~! WOOO
# TODO get file upload function to work properly -- I think I mostly solved this -- UpdateView not getting current "item"
# TODO add additional search features (i.e. for item location, size) --- can you have 2 different search filters on a page? (see itm_list.html page)
# TODO Figure out how to have Forms default fill in the field that is the PK with the pk of the current DetailView --in Views use def get_initial(self):
# TODO add edit button beside quantity
# TODO fix Quantity UpdateView to work with popouts in both item_detail and directly
# TODO file Model - return 'mmutools/{0}_{1}/{2}'.format(instance.item.item_name, instance.item.size, filename) === when size = N/A it reads the / as separator -- write a test for this