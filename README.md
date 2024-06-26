                                      BizCardX: Extracting Business Card Data with OCR



TECHNOLOGIES USED: OCR,streamlit GUI, SQL,Data Extraction,pandas.
                  
                   pandas: Used to create DataFrames for data manipulation and storage.
                  
                   mysql.connector: Used to store and retrieve data from a MySQL database.
                  
                   streamlit: Used to create a graphical user interface for users.
                  
                   easyocr: Used for text extraction from business card images.


BizCardX project that allows users to upload an image of a business card and extract relevant information from it using easy Optical Character Recognition (OCR).OCR is a Python package that developers to effortlessly perform Optical Character Recognition.It is a Python library for Optical Character Recognition (OCR) that allows you to easily extract text from images and scanned documents.The extracted information includes the company name, card holder name, designation, mobile number, email address, website, area, city, state, and pin code.The extracted information would be displayed in a clean and organized manner.
The users can save it to a database.Once saved, Users can also view , update, and delete the stored data through the streamlit dashboard.

STEP-BY-STEP APPROACH:
1. Install the required packages: You will need to install Python, Streamlit,easyOCR, and a database management system like SQLite or MySQL.
2. Design the user interface: Create a simple and intuitive user interface usingStreamlit that guides users through the process of uploading the business
card image and extracting its information. 
3. Implement the image processing and OCR: Use easyOCR to extract therelevant information from the uploaded business card image. You can useimage processing techniques like resizing, cropping, and thresholding toenhance the image quality before passing it to the OCR engine.
4. Display the extracted information: Once the information has been extracted,display it in a clean and organized manner in the Streamlit GUI. 
5. Implement database integration: Use MySQL to store the extracted information along with the uploadedbusiness card image. You can use SQL queries to create tables, insert data,and retrieve data from the database, Update the data and Allow the user todelete the data through the streamlit UI
6. Testing and optimising the code whereever it is needed

Functions used in this project:
            1.extract()-->To extract info from the card using ocr 
            2.convert_data()--->convert the image file to binary
            3.db_connection()--->establish the mysql connection
            4.upload()--->To upload the image in the dashboard
            5.modify()---->This allow the user to modify the data and save it to db
            6.delete_data()--->This allow the user to delete the data from db
            7.select_data()-->This allow the user to select the data to modify or delete from db
            8.view_data()--->This allow the user to view the data saved in the db

Overall, the result of this project would be a useful tool for businesses and individuals who need to manage business card information efficiently.

