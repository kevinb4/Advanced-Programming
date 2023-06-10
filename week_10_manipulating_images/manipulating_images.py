from functions.my_functions import *

# get required data from webpage
data = get_data('https://ool-content.walshcollege.edu/CourseFiles/IT/IT414/MASTER/Week10/WI20-Assignment/employees/index.php?ModPagespeed=off')

# process each image downloaded above and add the logo + name/title
process_images(data)

# zip the processed images
zip_images("images/output_images")