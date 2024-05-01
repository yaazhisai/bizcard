import easyocr 
import streamlit as st
from PIL import Image
import re
import numpy as np
import pandas as pd
import mysql.connector

def extract(result):
    # EXTRACTING CARD DETAILS
    states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 
            'Haryana','Hyderabad', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
            'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 
            'Rajasthan', 'Sikkim', 'TamilNadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
    
    data={"companyname":[],"website":[],"email":[],"cardholdername":[],"designation":[],"phonenumber":[],"pincode":[],"area":[],"city":[],"state":[]}
    # TO GET NAME AND DESIGNATION AND COMPANY NAME
    for i,j in enumerate(result):
        if i==0:
            data["cardholdername"].append(j)
        elif i==1:
            data["designation"].append(j)
        elif i!=0 and i!=1 and '-' not in j and 'St' not in j:
            if re.match(r'^[A-Za-z]',j) and "@" not in j and "com" not in j and "www" not in j.lower() and not any(char.isdigit() for char in j):
                data['companyname'].append(j)

        # TO GET EMAIL AND URL ADDRESS
        for x in j.split("."):
            if '@' in j and x=="com":
                data['email'].append(j.lower())
        for x in j.split():
            if "www" in j.lower() or ".com" in x and '@' not in x:
                data['website'].append(x.lower())

        # TO GET PHONENUMBER AND PINCODE DETAILS
        for x in j.split(" "):
            if j.startswith("+") or  '-' in j:
                data["phonenumber"].append(j)
            elif x.isdigit() and len(x)>=6:
                data["pincode"].append(x)

        # TO GET AREA AND CITY DETAILS
        for x in j.split(","):
            if 'St' in x:
                data['area'].append(x)
                j=j.replace(",,",",")
                j=j.replace(";",",")
                for i1,s in enumerate(j.split(",")):
                    if i1==1:
                        data['city'].append(s)
        # TO GET STATE DETAILS    
        for x in j.split(" "):
            x=x.replace(',',"")
            x=x.replace(";","")
            if x in states:
                data['state'].append(x)
        


    for key,value in data.items():
        if len(value)>0:
            j=" ".join(value)
            data[key]=[j]
        else:
            value="NOT AVAIABLE"
            data[key]=[value]

    return data


# Convert images or files data to binary format
def convert_data(file_name):
    with open(file_name, 'rb') as file:
        binary_data = file.read()
        return binary_data
        
# MYSQL CONNECTION
def db_connect(filename, data):
    connection = mysql.connector.connect(host='localhost',
                                        user='root',
                                        password='')
    mycursor = connection.cursor()
    # Create database
    # mycursor.execute("CREATE database biz")

    try:
        mycursor.execute("USE biz")
        connection.commit()
        #mycursor.execute("CREATE TABLE bizdata (id INT NOT NULL AUTO_INCREMENT,name TEXT,designation TEXT,phone TEXT,website TEXT,email TEXT,area TEXT,city TEXT,state TEXT,pincode int(10),image LONGBLOB NOT NULL)")
        # print("Table created Successfully")

        query = """INSERT INTO bizdata(name,designation,phone,website,email,area,city,state,pincode,image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # Convert image to Binary to upload as BLOB
        picture = convert_data(filename)

        # Insert extracted information to database
        mycursor.execute(query, (data['cardholdername'][0],
                                        data['designation'][0],
                                        data['phonenumber'][0],
                                        data['website'][0],
                                        data['email'][0],
                                        data['area'][0],
                                        data['city'][0],
                                        data['state'][0],
                                        data['pincode'][0],
                                        picture))
        # Commit the data
        connection.commit()
    
    # Print error if occured
    except mysql.connector.Error as error:
        print(format(error))
    
    # Close open connections
    finally:
        if connection.is_connected():
            mycursor.close()
            connection.close()

# Upload GUI and return details of the uploaded image
def upload():
    up_file=st.file_uploader("UPLOAD YOUR BUSINESS CARD:",type=['jpg', 'png'])
    st.warning("Make sure you image is in JPG/PNG Format.")
    if up_file is not None:
        filename = up_file.name
        img=Image.open(up_file)
        img_array=np.array(img)
        st.session_state['image']=img_array     # Save the image as a session state
        st.session_state['filename']=filename   # Save the filename as a session state
        return img_array,filename
    else:
        return None, None

# Data modification GUI
def modify(id,name):
    connection = mysql.connector.connect(host='localhost',
                                        user='root',
                                        password='')
    mycursor = connection.cursor()
    mycursor.execute('USE biz')
    mycursor.execute(f"SELECT * from bizdata where name='{name}' and id='{id}'")
    myresult = mycursor.fetchall()
    df1=pd.DataFrame(myresult,columns=("id","name","designation","phone","website","email","area","city","state","pincode","image"))
    st.dataframe(df1[["id","name","designation","phone","website","email","area","city","state","pincode"]])
    
    # Get the modified data from GUI 
    m_name=st.text_input("name:",df1['name'].item())
    m_desig=st.text_input("designation:",df1['designation'].item())
    m_phone=st.text_input("phonenumber:",df1['phone'].item())
    m_web=st.text_input("website:",df1['website'].item())
    m_email=st.text_input("email:",df1['email'].item())
    m_area=st.text_input("area:",df1['area'].item())
    m_city=st.text_input("city:",df1['city'].item())
    m_state=st.text_input("state:",df1['state'].item())
    m_pincode=st.text_input("pincode:",df1['pincode'].item())

    # Update the modified data to database
    mycursor.execute("UPDATE bizdata SET name=%s,designation=%s,\
                     phone=%s,website=%s,email=%s,area=%s,city=%s,\
                     state=%s,pincode=%s WHERE id=%s",\
                    (m_name,m_desig,m_phone,m_web,m_email,m_area,m_city,m_state,m_pincode,id))
    
    # Show button
    edit_bt=st.button("SAVE THE EDITED INFO TO DB")
    if edit_bt:
        connection.commit()
        st.success("EDITED INFO UPDATED SUCESSFULLY")

# Data deletion GUI
def delete_data(id,name):
    connection = mysql.connector.connect(host='localhost',
                                        user='root',
                                        password='')
    mycursor = connection.cursor()
    mycursor.execute('USE biz')
    mycursor.execute(f"DELETE from bizdata WHERE bizdata.name='{name}' and id='{id}'")
    connection.commit()
    st.success("DATA DELETED SUCESSFULLY")

# Fetch the list of id and name from database to display in Modify/Delete GUI
def select_data():
    connection = mysql.connector.connect(host='localhost',
                                        user='root',
                                        password='')
    mycursor = connection.cursor()
    mycursor.execute('USE biz')
    mycursor.execute(f"SELECT concat(id,'.',name) from bizdata")
    myresult=mycursor.fetchall()
    output = list()
    #Add first element of list as blanks to show empty selection in the Modify/Delete data drop down
    output.append(' ')
    # myresult gives tuple value hence below conversion to list done
    output += [list(x)[0] for x in myresult]
    return output

def view_data():
    connection = mysql.connector.connect(host='localhost',
                                        user='root',
                                        password='')
    mycursor = connection.cursor()
    mycursor.execute('USE biz')
    query="SELECT * FROM bizdata"
    result_df=pd.read_sql(query,connection,columns=("id","name","designation","phone","website","email","area","city","state","pincode","image"))
    st.dataframe(result_df[["id","name","designation","phone","website","email","area","city","state","pincode"]])
    connection.close()



# Display streamlit title
st.title("BizCardX: Extracting Business Card Data with OCR")

# Display a select box with the list of options
option=st.selectbox('Choose your activity',['','UPLOAD THE IMAGE','EXTRACT THE CARD DETAILS','SAVE TO MYSQL','VIEW ALL','MODIFY THE CARD DETAILS','DELETE THE CARD DETAILS'])
filename = ''

# Upload image
if option=='UPLOAD THE IMAGE':
    im,f1=upload()
    if im is not None and f1 is not None:
        st.image(im)
        st.write("Image Uploaded Successfully")
elif option=='EXTRACT THE CARD DETAILS':
    # READING IMAGE USING OCR
    if 'image' in st.session_state.keys():
        if st.session_state['image'] is not None and st.session_state['filename'] is not None:
            reader = easyocr.Reader(['en'],gpu=False)
            result = reader.readtext(st.session_state['image'],slope_ths=0.5,detail=0)
            
            # Extract the details from the easyocr result
            data = extract(result)
            st.session_state['extracted_data']=data

            # CREATING DATAFRAME
            df=pd.DataFrame.from_dict(data)
            df=df.transpose()
            st.write("EXTRACTED DETAILS IN TABLE FORMAT")
            st.write(df)
            st.image(st.session_state['image'])
        else:
            st.write("No image uploaded!!!")
    else:
        st.write("No image uploaded!!!")
elif option=='SAVE TO MYSQL':
    if 'extracted_data' in st.session_state.keys():
        if st.session_state['extracted_data'] is not None:
            db_connect(st.session_state['filename'], st.session_state['extracted_data'])
            st.success("SAVED TO MYSQL SUCESSFULLY")
            st.session_state['extracted_data']=None
            st.session_state['filename']=None
            st.session_state['image']=None
        else:
            st.write("No info available for upload!!!")
    else:
        st.write("No info available for upload!!!")
elif option=='VIEW ALL':
    view_data()
elif option=='MODIFY THE CARD DETAILS':
    st.header("select the name to modify the details")
    names_list = select_data()
    opt = st.selectbox('select the name:',names_list)
    if opt != ' ':
        name = opt.split('.')[1]
        id=opt.split(".")[0]
        modify(id,name)
    
elif option=='DELETE THE CARD DETAILS':
    st.header("select the name of cardholder to delete")
    names_list = select_data()
    opt = st.selectbox('select the name:',names_list)
    if opt != ' ':
        name = opt.split('.')[1]
        id=opt.split(".")[0]
        r=st.radio(f"ARE YOU SURE TO DELETE {id}.{name} FROM DB???",["YES","NO"],index=None)
        if r=='YES':
            delete_data(id,name)
        elif r=='NO':
            st.write("NO RECORDS DELETED FROM DB")
    


        
     

    
