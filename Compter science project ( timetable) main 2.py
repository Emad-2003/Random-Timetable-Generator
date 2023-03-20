# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 10:11:14 2020

@author: Emad Shoaib
"""

#______________________________________________________________________________

# Inbuilt Functions
import mysql.connector as sq
import random

# connection Statements
c=sq.connect(host='localhost',user='root',passwd='emad',charset='utf8',database='project4')
cursor=c.cursor()

#______________________________________________________________________________

# Functions

#______________________________________________________________________________

# Basic Functions ( To set up the program)

def create_list():
    l=[]
    for i in range(5):
        r=[]
        for j in range(9):
            r+=['--------']
        l+=[r]
        
    return l

def create_newlist():
    nl=[]
    for i in range(9):
        r=[]
        for j in range(5):
            r+=['--------']
        nl+=[r]
        
    return nl

def store_max_sub(sub):
    n=[]
    print(sub)
    print()
    for i in sub:
        # maximum no of periods in a week
        maxsub=int(input('Enter maximum classes for '+i+ ': '))
        n+=[maxsub]
    return n

def sum_max(n):
    s=0
    for i in n:
       s+=i
    return s

#______________________________________________________________________________

# Functions of set_timetable() [ functions used inside set_timetable()]

def transpose_matrix(l,nl):
    # iterate through rows
    for i in range(len(l)):
    
        # iterate through columns
        for j in range(len(l[0])):
            nl[j][i] = l[i][j]
    
    return nl
    
def store_mysql(nl,grade,div,tname):
    # inserting records in mysql
    for i in nl:
        i=tuple(i)
        
        # entering the query
        query='insert into '+tname+grade+div+' values'+str(i)
        
        cursor.execute(query)
        c.commit()
    

def check_if_exist(grade,div,tname):
    # entering the query
    query='select * from '+tname+grade+div
    cursor.execute(query)
    data=cursor.fetchall()
    
    # check condition
    if len(data)==1:
        print('timetable already created')
        return True

def reset_timetable(grade,div,tname):
    query='delete from '+tname+grade+div
    cursor.execute(query)
    c.commit()          

def sub_set(grade,sub,l,n,subsum):
    
    # dsiplaying a sub heading
    sub_Heading2(subsum)
    
    # running loop to iterate every subject
    for i in range(len(sub)):
        
        maxsub=n[i]
        for j in range(maxsub):
            
            # running loop to avoid overlap
            while True:
                
                # check condition for assembly
                if i=='Assembly':
                    pos_sub=0
                    
                    # creation of parameter day_sub
                    if grade in ['Kg1','Kg2']:
                        day_sub=1
                        
                    elif grade in ['1','2','3','4','5']:
                        day_sub=4
                        
                    elif grade in ['6','7','8']:
                        day_sub=2
                        
                    elif grade in ['9','10']:
                        day_sub=3
                        
                    elif grade in ['11','12']:
                        day_sub=3
                        
                else:
                    pos_sub=random.randint(0,8)
                    # assigning day of the week
                    day_sub=random.randint(0,4)
                    
                # checking for empty position
                if l[day_sub][pos_sub]=='--------':
                    l[day_sub][pos_sub]=sub[i]
                    break
    return l         
  
def sub_Heading2(subsum):
    print('''
Below u will be asked to give the maximum periods a subject can have in a week
give in such an order such that the sum of all of it is ''' + str(subsum) + '''
(or) the program may not execute                                               ''')

#______________________________________________________________________________

# Functions to be called based on choice value in main()

def set_timetable(l,nl,grade,div,tname,sub):
    
    if check_if_exist(grade,div,tname)==True:
        reset_timetable(grade,div,tname)
    
    Result=True
    
    # list of maximum periods of subjects
    n=store_max_sub(sub)
    
    # sum of elements in n
    subsum=sum_max(n)
    
    # avoiding error
    if grade in ['kg1','kg2']:
        
        if subsum==25:
            # calling sub func
            l=sub_set(grade,sub,l,n,subsum)
        
        else:
            print('sorry , the program did not run because the sum of maximum periods was not 25')
            Result=False
    
    elif grade in ['1','2','3','4','5']:
        
        if subsum==40:
            # calling sub func
            l=sub_set(grade,sub,l,n,subsum)
        
        else:
            print('sorry , the program did not run because the sum of maximum periods was not 40')
            Result=False
    
    elif grade in ['6','7','8','9','10','11','12']:
        
        if subsum==45:
            # calling sub func
            l=sub_set(grade,sub,l,n,subsum)
        
        else:
            print('sorry , the program did not run because the sum of maximum periods was not 45')
            Result=False
    
    else:
        Result=True
    
               
    # To transpose the matrix l
    nl=transpose_matrix(l,nl)

    # To store the tuples in mysql
    store_mysql(nl,grade,div,tname)
    
    # conclusion statement
    if Result==True:
        print()
        print('!!! Timetable set !!!')
        print()
    
def assign_teacher(grade,div,tname,sub):
    
    if check_if_exist(grade, div, tname):
        reset_timetable(grade, div, tname)
    
    # entering the query
    query='select * from tt'+grade+div
    
    cursor.execute(query)
    data=cursor.fetchall()
    
    tl=create_newlist()
    
    for i in sub:
        tn=input('Enter name of teacher who teaches '+i+': ')
        # running for loop
        for a in range(9):
            for b in range(5):
                if data[a][b]==i:
                    tl[a][b]==tn
        
def display_timetable(grade,div,tname):
    global cursor
    
    # entering the query
    query='select * from '+tname+grade+div
    
    cursor.execute(query)
    data=cursor.fetchall()
    
    # dsiplaying the heading
    print('      Timetable ('+grade+'/'+div+')') 
    print()
    print('______________________________________________')
    print('|'+'_Sunday_'+'|'+'_Monday_'+'|'+'Tuesday_'+'|'+'Wedneday'+'|'+'Thursday'+'|')
    print('______________________________________________')
    for i in data:
        for j in range(len(i)):
            if j==0:
                print('|'+i[j],end='|')
            else:
                print(i[j],end='|')
                
        print()
        print('______________________________________________')

def search_class(grade,div,tname):
    global cursor
    
    # asking what period the user wants to know
    if tname=='tt':
        sp=input('what subject you want to know period of ? ')
    elif tname=='ttt':
        sp=input('Which teacher do you want to know class of ? ')
        
    day=input('On which day ? (sun/mon/Tue/Wed/Thurs) : ')
    days=['sun','mon','tue','wed','thu']
    
    # entering the query
    query='select * from '+tname+grade+div
    
    cursor.execute(query)
    data=cursor.fetchall()    
    
    # temporary list
    temp=[]
    for i in range(len(data)):
        for j in range(5):
            if str(days[j]).lower()==day: 
                if data[i][j]==sp:
                    temp+=[i]
    
    # printing the output
    if len(temp)!=0:
        print(sp+' class is at ')
        for k in temp:
            print(str(k+1)+' period')
    else:
        print('No '+sp+'period on '+day)

def Edit_table(grade,div,tname):
    global cursor
    
    # asking new teachers and old teachers name
    ue=input('Enter new teachers name: ')
    re=input('Replacing which teacher ? : ')
    
    for i in ['Sunday','Monday','Tuesday','Wednesday','Thursday']:
        # entering the query
        query='update '+tname+grade+div+' set '+i+'='+ue+' where '+i+'='+re
        cursor.execute(query)
        c.commit()
#______________________________________________________________________________

# Functions Of main() [ functions used inside main()]

def check_science(sub):
    
    # checking if maths or Bio
    mb=input('Math or Bio ? : ')
    
    # checking if maths stream
    if mb.lower() in 'maths':
        pc=input('Psychology or Computer science ? :')
        
        # checking maths with psychology
        if pc.lower() in 'psychology':
            # removing computer science subject 
            sub.pop(7)
        # checking maths with computer science
        elif pc.lower() in 'Computer Science':
            # removing psycology subject
            sub.pop(6)
                
        # removing Biology subject
        sub.pop(5)
    
                
    # checking if Biology stream
    elif mb.lower() in 'biology':
        pm=input('Maths or psychology or computer science ? :  ')
        
        # checking if Biology with maths
        if pm.lower() in 'maths':
            # removing psychology and Computer Science subject
            sub.pop(6)
            sub.pop(6)
            
        # checking if biology with psychology
        elif pm.lower() in 'psychology':
            # removing maths and computer science subject
            sub.pop(2)
            sub.pop(6)
            
        # checking if biology with Computer science
        elif pm.lower() in 'computer science':
            #removing maths and psychology
            sub.pop(2)
            sub.pop(5)
    # returning the subject list
    return sub

def check_commerce(sub):
    
    # checking if Ip or Maths
    immp=input('Informatics Practices/maths/Marketing/psychology ? : ')
    
    # checking if maths stream
    if immp.lower() in 'maths':
        sub.pop(5)
        sub.pop(5)
        sub.pop(6)
        
    # checking if Informatics practices stream
    if immp.lower() in 'informatics practices':
        sub.pop(2)
        sub.pop(4)
        sub.pop(6)
    
    # checking if Marketing stream
    if immp.lower() in 'marketing':
        sub.pop(2)
        sub.pop(5)
        sub.pop(6)
        
    # checking if psychology stream
    if immp.lower() in 'psychology':
        sub.pop(2)
        sub.pop(4)
        sub.pop(4)
    
    return sub

def create_table():
    
    # running the counting loop
    for i in ['kg1','kg2','1','2','3','4','5','6','7','8','9','10','11','12']:
        if i in ['9','10','11','12']:
            for j in ['a','b','c','d']:
                
                # entering the query
                query='create table tt'+i+j+'(Sunday char(20),Monday char(20),Tuesday char(20),Wednesday char(20),Thursday char(20))'
                cursor.execute(query)
                
                # entering the query
                query='create table ttt'+i+j+'(sunday char(20),Monday char(20),Tuesday char(20),Wednesday char(20),Thursday char(20))'
                cursor.execute(query)
        
        elif i in ['kg1','kg2']:
            for j in ['a','b','c']:
                
                # entering the query
                query='create table tt'+i+j+'(Sunday char(20),Monday char(20),Tuesday char(20),Wednesday char(20),Thursday char(20))'
                cursor.execute(query)
                
                # entering the query
                query='create table ttt'+i+j+'(sunday char(20),Monday char(20),Tuesday char(20),Wednesday char(20),Thursday char(20))'
                cursor.execute(query)
        
        else:
            for j in ['a','b','c','d','e']:
                
                # entering the query
                query='create table tt'+i+j+'(Sunday char(20),Monday char(20),Tuesday char(20),Wednesday char(20),Thursday char(20))'
                cursor.execute(query)
                
                # entering the query
                query='create table ttt'+i+j+'(sunday char(20),Monday char(20),Tuesday char(20),Wednesday char(20),Thursday char(20))'
                cursor.execute(query)
        
def drop_table():
    
    # running the counting loop
    for i in ['kg1','kg2','1','2','3','4','5','6','7','8','9','10','11','12']:
        if i in ['9','10','11','12']:
            for j in ['a','b','c','d']:
                
                # entering the query
                query='drop table tt'+i+j
                cursor.execute(query)
                
                # entering the query
                query='drop table ttt'+i+j
                cursor.execute(query)
        
        elif i in ['kg1','kg2']:
            for j in ['a','b','c']:
                
                # entering the query
                query='drop table tt'+i+j
                cursor.execute(query)
                
                # entering the query
                query='drop table ttt'+i+j
                cursor.execute(query)
        
        else:
            for j in ['a','b','c','d','e']:
                
                # entering the query
                query='drop table tt'+i+j
                cursor.execute(query)
                
                # entering the query
                query='drop table ttt'+i+j
                cursor.execute(query)
                
def exit_prog():
    # asking to be patient
    print('Please wait this may take some time (about a minute)')
    
    # calling func that drops all tables in mysql
    drop_table()
    
    # conclusion statements
    print()
    print('Thank you for using this program ')
    print()
    
def Heading():
    print('''
 
  _____   __    _   _     _   __    _   ___      ____   _          _       ____   ____
 |  _  \ |  \  | \ | |   | | |  \  | | |  _|    /  __| | |        / \     /  __| /  __|
 | | | | |   \ | | | |   | | |   \ | | | |_     | |    | |       / _ \    | |__  | |__
 | | | | | |\ \| | | |   | | | |\ \| | |  _|    | |    | |      / /_\ \   |___ | |__  |
 | |_| | | | \   | | |__ | | | | \   | | |_     | |__  | |__   / _____ \   __| |  __| |
 \_____| \_|  \__| |____||_| |_|  \__| |___|    \____| |____| /_/     \_\ |____/ |____/
              
 _____   _   ___    ___   ____   _____     _       _____   _     ___            
/_   _| | | |   \  /   | |  __| /_   _|   / \     |  _  \ | |   |  _\                    
  | |   | | | |\ \/ /| | | |__    | |    / _ \    | |_| / | |   | |_                       
  | |   | | | | \  / | | |  __|   | |   / /_\ \   |  _ |  | |   |  _|                      
  | |   | | | |  \/  | | | |__    | |  / _____ \  | |_| \ | |__ | |_                    
  |_|   |_| |_|      |_| |____|   |_| /_/     \_\ |_____/ |____||___/                        


_____________________________________________________________________________________  
  
  INSTRUCTIONS ( before use ):
      
1. The following Program deals with operations that can be done involving timetables
2. Choose any of the options below whichever you want
3. go as per the statements that follow ahead without any hurry or rush
4. write answers as specific as given in brackets without much deviation
5. The option for exit is the letter e in lower case instead of regular numbers
6. Once the program is exited all timetables created will be deleted  

NOTE : After this point , it may take some time to load , so please wait
_____________________________________________________________________________________
                                                                                            ''')    

def Heading2():
    print('''  
 TIMETABLES (to operate on)
         
1. Students Timetable
2. Teachers Timetable 
3. Exit
                                                                            ''')

def Heading3(tname):
    # Displaying the operations that can be done involving timetable
    print(''' 
OPERATIONS
              
1. Create Timetable
2. Display Timetable
3. Search class at a certain period                                    ''')

    if tname=='ttt':
        print('4. Edit Timetable')
    
    print('e. Exit')

def sub_Heading():
    # accepting grade and division
    print('''
Below you will be asked grade , division and stream of class(if needed)
Please kindly fill those  
 
                                                                        ''')

#______________________________________________________________________________

# The super functions of all above functions

# func that will be used in main()
def sub_main(grade,div,tname,sub):
    
    # setting basic lists 
    l=create_list()
    nl=create_newlist()
    
    # main program menu loop
    while True:
        
        # displaying Heading3()
        Heading3(tname)
        
        # accepting choice
        if tname=='tt':
            ch=input('Enter Choice (1/2/3): ')
        elif tname=='ttt':
            ch=input('Enter Choice (1/2/3/4): ')
            
        # condition based on user's choice
        if ch=='1':
            # checking if student or teacher timetable
            if tname=='tt':

                # calling func that sets students timetable in mysql
                set_timetable(l,nl,grade,div,tname,sub)
            
            elif tname=='ttt':
                # calling func that sets teachers timetable in mysql
                assign_teacher(grade, div, tname, sub)
                
        elif ch=='2':
            # calling function that displays timetable
            display_timetable(grade,div,tname)
            
        elif ch=='3':
            # calling function that searches for period
            search_class(grade,div,tname)
        
        elif tname=='ttt':
            if ch=='4':
                Edit_table(grade, div, tname)
                
        elif ch=='e':
            # conclusion statements
            if tname=='tt':
                print('Thank you for using student Timetable')
            elif tname=='ttt':
                print('Thank you for using Teachers Timetable')
            
            # exiting while loop
            break
        
        
        else:
            print('Please give any one of the options given above ')
        
        # condition to continue again
        ans=input('Do you want to continue with Online class timetable (y/n) ?  ')
        
        # condition to break from loop
        if ans.lower()=='n':
            # conclusion statements
            if tname=='tt':
                print('Thank you for using student Timetable')
            elif tname=='ttt':
                print('Thank you for using Teachers Timetable')
            
            # exiting while loop
            break

# func that will be used in super_main()
def main():
    
    # nested list of all subject streams
    sublist=[['English_','Maths___','EVS_____','GeneralA',],
            ['Assembly','English_','Maths___','EVS_____','2nd_Lang','3rd_Lang','Art_____','M/D_____','PE______','WorkExp_','ValueEd'],
            ['Assembly','English_','Maths___','Science','2nd_Lang','3rd_Lang','SocialSc','M/D/A_____','PE______','WorkExp_','ValueEd_'],
            ['Assembly','English_','Maths___','2nd_Lang','Physics_','Chem____','Biology_','Geo_____','Eco_____','History__','Civics__','A/M/D___','PE______','WorkExp_','ValueEd_'],
            ['Assembly','English_','Maths___','Physics_','Chem____','Biology_','Psy_____','CompSci_','WorkExp_','PE______'],
            ['Assembly','English_','Maths___','Buss_Stu','Eco_____','Market__','IP______','WorkExp_','Psy_____','PE______']]
    
    # displaying one sub heading
    sub_Heading()
    
    grade=input('Enter grade on which you want to do the below operations (kg1 to 12) : ')
    div=input('Enter section: ')
    div=div.lower()
    
    # creation of parameter sub
    if grade in ['kg1','kg2']:
        sub=sublist[0]
            
    elif grade in ['1','2','3','4','5']:
        sub=sublist[1]
            
    elif grade in ['6','7','8']:
        sub=sublist[2]
        
    elif grade in ['9','10']:
        sub=sublist[3]
        
    elif grade in ['11','12']:
        
        # Entering stream
        stream=input('Enter stream (Science/Commerce) :')
                
        # checking different streams
        if stream.lower() in 'science':
            sub=sublist[4]
            sub=check_science(sub)
            
        elif stream=='commerce':
            sub=sublist[5]
            sub=check_commerce(sub)
    
    # Displaying Heading2()
    Heading2()
    
    pch=input('Choose any of the options above (1/2) : ')
    
    # checking if students timetable
    if pch=='1':
        tname='tt'
    # checking if teachers timetable
    elif pch=='2':
        tname='ttt'
    # avoiding unnesscessary error
    else:
        print('please choose an option out of the above given')
        return None
        
    # calling function
    sub_main(grade,div,tname,sub)

# final function that has all the the above functions

def super_main():
    
    # Displaying the main Heading
    Heading()
    
    # creating all the tables
    create_table()
    
    while True:
        main()
        
        # asking if the user wants to do the program for a different class
        ans=input('do you want to do the above operations for a different class (y/n) ? : ')
        
        # condition to break from while loop
        if ans.lower()=='n':
            
            # function having some conclusion statements
            exit_prog()
            break
#______________________________________________________________________________

# executing the program
super_main()


