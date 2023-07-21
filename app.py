#Libraries
import os
import streamlit as st

#Model based Librabries
import openai
import time

st.set_page_config(layout="wide")
openai.api_key = st.secrets["openai_key"]

##App framework
st.image('logo_nbg.png', width = 100)
# st.title('Code:robot_face:')
st.markdown("<h1 style='font-size: 30px;'>Code Migration Bot</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size: 5px;'></h1>", unsafe_allow_html=True)
col1, col2, col3, side = st.columns([1,1,1,6])
with col2:
    summarize_flag = st.checkbox('Summarize')
with col1:
    debug_flag = st.checkbox('Debug')
with col3:
    convert_flag = st.checkbox('Convert')
    
prompt = st.text_area('Please enter the SAS code below', height = 200)
# exl_model='gpt-3.5-turbo'
exl_model='gpt-3.5-turbo-16k'


##Model-1 - Checking for Syntax Errors
def syntax_model(user_prompt):

    user_prompt_updated = '''Identify syntax errors in the below the SAS code:
    ''' + user_prompt

    bot_instructions = '''You are a code assistant, focussing on identifying and correcting syntax errors based on SAS programming language. You get a SAS code as input. You are going to identify syntax error and correct the SAS code. If there is no syntax error, let the user know about it. Do not explain what the code is doing. Do not summarize the code. Do not explain the functions used in the code.'''
                            
    
    sample_input1 = '''Identify syntax errors in the below the SAS code:
    /*Program to analyze/explore the data having customer infomation and 
flag indicating whether default on payment occured or not*/

/*Assign library where data will be stored*/

libname logit 'C:\Analytics\Logistic Regression';

*Using "proc import" to import csv file;
proc import 
datafile = "D:\Analytics\Logistic Regression\Default_On_Payment.csv"
out = logit.Default_On_Payment_1	dbms = csv	replace;
delimiter = ',';
getnames = yes;
run;'''
    sample_output1 = '''The provided SAS code contains a syntax error. The issue is with the libname statement and the datafile option of the proc import statement. The directory path in both statements uses backslashes (\) instead of forward slashes (/). Here is the corrected code:
/*Program to analyze/explore the data having customer information and flag indicating whether default on payment occurred or not*/

/*Assign library where data will be stored*/
libname logit 'C:/Analytics/Logistic Regression';

*Using "proc import" to import csv file;
proc import 
    datafile = "D:/Analytics/Logistic Regression/Default_On_Payment.csv"
    out = logit.Default_On_Payment_1
    dbms = csv
    replace;
    delimiter = ',';
    getnames = yes;
run;

In the corrected code, the directory path in both the libname statement and the datafile option of proc import now use forward slashes (/) instead of backslashes (\) for proper file path formatting.'''


    
    sample_input2 = '''Identify syntax errors in the below the SAS code:
                        *Content of data;
                        procc contents 
                        data = logit.Default_On_Payment;
                        run;'''
    sample_output2 = '''There is a syntax error in the provided SAS code. The correct procedure name is "proc" instead of "procc". Additionally, there are unnecessary spaces and indentation in the code. Here is the corrected code:
    
    *Content of data;
proc contents 
    data = logit.Default_On_Payment;
run;

In the corrected code, the "proc" statement is used to specify the procedure, followed by the "contents" keyword. The "data" statement is used to specify the dataset, "logit.Default_On_Payment" in this case. The code then ends with the "run" statement to execute the procedure.'''

    sample_input3 = '''Identify syntax errors in the below the SAS code:
                        *Bivariate Analysis of independent variable;
                        %macro mBivariate(var);
                        proc sql;
                        Create table &var._tab as 
                        select &var, count(*) as freq,
                        sum(Default_On_Payment) as Default_On_Payment 
                        from logit.Default_On_Payment
                        group by &var;
                        quit;
                        
                        data &var._tab;
                        set &var._tab;
                            Default_Rate = Default_On_Payment/freq;
                        run;
                        
                        proc print data = &var._tab; run;
                        %mend mBivariate;
                        %mBivariate(Status_Checking_Acc)
                        %mBivariate(Duration_in_Months);
                        %mBivariate(Credit_History);
                        %mBivariate(Purposre_Credit_Taken);'''
    sample_output3 = '''There is a syntax error in the provided SAS code. The macro invocation statements at the end are missing semicolons (;) after each invocation. Additionally, there are unnecessary spaces and indentation in the code. Here is the corrected code:
    *Bivariate Analysis of independent variable;
%macro mBivariate(var);
    proc sql;
        Create table &var._tab as 
        select &var, count(*) as freq,
        sum(Default_On_Payment) as Default_On_Payment 
        from logit.Default_On_Payment
        group by &var;
    quit;
    
    data &var._tab;
        set &var._tab;
        Default_Rate = Default_On_Payment/freq;
    run;
    
    proc print data = &var._tab; 
    run;
%mend mBivariate;
%mBivariate(Status_Checking_Acc);
%mBivariate(Duration_in_Months);
%mBivariate(Credit_History);
%mBivariate(Purposre_Credit_Taken);

In the corrected code, each macro invocation statement ends with a semicolon (;) after the macro name. The code also includes proper indentation for better readability.'''

    sample_input4 = '''Identify syntax errors in the below the SAS code:
    *Running proc logistic to predict probability of default;

proc logistics data=logit.Default_On_Payment_Train_v1  descending outest=betas covout;
  model Default_On_Payment= &VarList
               / selection=stepwise
                 slentry=0.01
                 slstay=0.005
                 details
                 lackfit;
  output out=Pred_Default_On_Payment_Train_v1 p=phat lower=lcl upper=ucl
         predprobs=(individual crossvalidate);
run;'''
    sample_output4 = '''There is a syntax error in the provided SAS code. The procedure name should be "logistic" instead of "logistics". Here is the corrected code:
    *Running proc logistic to predict probability of default;

proc logistic data=logit.Default_On_Payment_Train_v1 descending outest=betas covout;
  model Default_On_Payment = &VarList
               / selection=stepwise
                 slentry=0.01
                 slstay=0.005
                 details
                 lackfit;
  output out=Pred_Default_On_Payment_Train_v1 p=phat lower=lcl upper=ucl
         predprobs=(individual crossvalidate);
run;

In the corrected code, the procedure name is changed to "logistic".'''
    
    sample_input5 = '''Identify syntax errors in the below the SAS code:
    proc sql;
create table Gains_v1 as 
select Bin, count(*) as freq, sum(Default_On_Payment) as Actual,
sum(phat) as Predicted from Pred_Default_On_Payment_Train_v2
group by Bin;
quit;'''
    sample_output5 = '''The SAS code you provided contains a couple of syntax errors. Here's the corrected version:
    proc sql;
create table Gains_v1 as 
select Bin, count(*) as freq, sum(Default_On_Payment) as Actual,
sum(phat) as Predicted from Pred_Default_On_Payment_Train_v2
group by Bin;
quit;

Changes made:

The function add() used in add(Default_On_Payment) and add(phat) is not a valid SAS function. It has been changed to sum() to calculate the sum of the variables.
The corrected code uses sum() instead of add().
With these corrections, the code should execute without syntax errors.'''

    sample_input6 = '''Identify syntax errors in the below the SAS code:
    proc logistic data=logit.Default_On_Payment_Train_v1  descending outest=betas covout;
  model Default_On_Payment= &VarList
               / selection=stepwise
                 slentry=0.01
                 slstay=0.005
                 details
                 lackfit;
  output out=Pred_Default_On_Payment_Train_v1 p=phat lower=lcl upper=ucl
         predprobs=(individual crossvalidate);
run;'''
    sample_output6 = '''The SAS code consists of no syntax error.'''

    sample_input7 = '''data logit.Default_On_Payment_v1;
set logit.Default_On_Payment;

	/*Status_Checking_Acc*/	
	if Status_Checking_Acc eq 'A11' then Status_Checking_Acc_dummy_1 = 1; 
		else Status_Checking_Acc_dummy_1 = 0;
	if Status_Checking_Acc eq 'A12' then Status_Checking_Acc_dummy_2 = 1; 
		else Status_Checking_Acc_dummy_2 = 0;
	if Status_Checking_Acc eq 'A13' then Status_Checking_Acc_dummy_3 = 1; 
		else Status_Checking_Acc_dummy_3 = 0;
		
	/*Duration_in_Months*/
	if Duration_in_Months le 12 then Duration_in_Months_trans = 12;
	else if Duration_in_Months le 24 then Duration_in_Months_trans = 24;
	else if Duration_in_Months le 36 then Duration_in_Months_trans = 36;
	else if Duration_in_Months le 48 then Duration_in_Months_trans = 48;
	else if Duration_in_Months gt 48 then Duration_in_Months_trans = 60;
	
	/*Credit_History*/
	if Credit_History eq 'A30' then Credit_History_dummy_1 = 1; 
		else Credit_History_dummy_1 = 0;
	if Credit_History eq 'A31' then Credit_History_dummy_2 = 1; 
		else Credit_History_dummy_2 = 0;	
	if Credit_History eq 'A33' then Credit_History_dummy_3 = 1; 
		else Credit_History_dummy_3 = 0;
	if Credit_History eq 'A34' then Credit_History_dummy_4 = 1; 
		else Credit_History_dummy_4 = 0;	
		
	/*Purposre_Credit_Taken*/
	if Purposre_Credit_Taken eq 'A40' then Purposre_Credit_Taken_dummy_1 = 1; 
		else Purposre_Credit_Taken_dummy_1 = 0;
	if Purposre_Credit_Taken eq 'A41' then Purposre_Credit_Taken_dummy_2 = 1; 
		else Purposre_Credit_Taken_dummy_2 = 0;
	if Purposre_Credit_Taken eq 'A410' then Purposre_Credit_Taken_dummy_1 = 1; 
		else Purposre_Credit_Taken_dummy_1 = 0;
	if Purposre_Credit_Taken eq 'A42' then Purposre_Credit_Taken_dummy_3 = 1; 
		else Purposre_Credit_Taken_dummy_3 = 0;	
	if Purposre_Credit_Taken eq 'A45' then Purposre_Credit_Taken_dummy_4 = 1; 
		else Purposre_Credit_Taken_dummy_4 = 0;
	if Purposre_Credit_Taken eq 'A46' then Purposre_Credit_Taken_dummy_5 = 1; 
		else Purposre_Credit_Taken_dummy_5 = 0;	
	if Purposre_Credit_Taken eq 'A49' then Purposre_Credit_Taken_dummy_6 = 1; 
		else Purposre_Credit_Taken_dummy_6 = 0;
    run;'''
    sample_output7 = '''Provided SAS code appears to be free of syntax errors.'''

    sample_input8 = '''proc gplot data = ScoredLinReg;	Plot Customer_ID * Model1; 	run;'''
    sample_output8 = '''The SAS code you provided appears to be free of syntax errors.'''

    sample_input9 = '''proc freq 
data= logit.Default_On_Payment;
tables Default_On_Payment/list missing;
run;'''
    sample_output9 = '''The SAS code doesn't have any syntax error.'''

    response = openai.ChatCompletion.create(
        model = exl_model,
        messages=[
            {"role": "system", "content": bot_instructions},
            {"role": "system", "name":"example_user", "content": sample_input1},
            {"role": "system", "name": "example_assistant", "content": sample_output1},
            {"role": "system", "name":"example_user", "content": sample_input2},
            {"role": "system", "name": "example_assistant", "content": sample_output2},
            {"role": "system", "name":"example_user", "content": sample_input3},
            {"role": "system", "name": "example_assistant", "content": sample_output3},
            {"role": "system", "name":"example_user", "content": sample_input4},
            {"role": "system", "name": "example_assistant", "content": sample_output4},
            {"role": "system", "name":"example_user", "content": sample_input5},
            {"role": "system", "name": "example_assistant", "content": sample_output5},
            {"role": "system", "name":"example_user", "content": sample_input6},
            {"role": "system", "name": "example_assistant", "content": sample_output6},
            {"role": "system", "name":"example_user", "content": sample_input7},
            {"role": "system", "name": "example_assistant", "content": sample_output7},
            {"role": "system", "name":"example_user", "content": sample_input8},
            {"role": "system", "name": "example_assistant", "content": sample_output8},
            {"role": "system", "name":"example_user", "content": sample_input9},
            {"role": "system", "name": "example_assistant", "content": sample_output9},
            {"role": "user", "content": user_prompt_updated},
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]


##Model-2 - Code Summarization
def summary_model(user_prompt):
    bot_instructions = """You are a code summarization assistant. You get SAS code as input. You have to perform below tasks:
    1. Identify syntax error and write the correct SAS code. Skip this step if there is no syntax errors.
    2. Briefly explain what code is doing.
    
    Below are two examples:
    Example 1:
    User:
    procc contents 
    data = logit.Default_On_Payment;
    run;
    AI: There is a syntax error in the provided SAS code. The correct procedure name is "proc" instead of "procc". Here is the corrected code:
    
    *Content of data;
    proc contents 
    data = logit.Default_On_Payment;
    run;

    Summary: The code is using the PROC CONTENTS statement to obtain information about the variables in the dataset named "logit.Default_On_Payment".


    Example 2:
    User:
    proc contents 
    data = logit.Default_On_Payment;
    run;
    AI: The code is using the PROC CONTENTS statement to obtain information about the variables in the dataset named "logit.Default_On_Payment".
    """
    response = openai.ChatCompletion.create(
        model=exl_model,
        messages=[
            {"role": "system", "content": bot_instructions},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]


##Model-3 - Code Conversion
def conversion_model(user_prompt):
    bot_instructions = """You are a python code assistant. You get SAS code as an input and you write its equivalent python code which strictly follows python coding language syntax. Below are two examples:
    
    Example 1:
    User:
    %macro mBivariate(var);
    proc sql;
    Create table &var._tab as 
    select &var, count(*) as freq,
    sum(Default_On_Payment) as Default_On_Payment 
    from logit.Default_On_Payment
    group by &var;
    quit;

    data &var._tab;
    set &var._tab;
        Default_Rate = Default_On_Payment/freq;
    run;

    proc print data = &var._tab; run;
    %mend mBivariate;
    AI:
    import pandas as pd

    def mBivariate(var):
    # Creating &var._tab table
    data = pd.DataFrame({
        var: logit.Default_On_Payment[var],
        'freq': logit.Default_On_Payment.groupby(var).size(),
        'Default_On_Payment': logit.Default_On_Payment.groupby(var).sum()
    }).reset_index()

    # Adding Default_Rate column
    data['Default_Rate'] = data['Default_On_Payment'] / data['freq']

    # Printing the &var._tab table
    print(data)

    # Calling the mBivariate macro
    mBivariate(var)

    Example 2:
    User:
    data logit.Default_On_Payment_v1;
    set logit.Default_On_Payment;

	/*Status_Checking_Acc*/	
	if Status_Checking_Acc eq 'A11' then Status_Checking_Acc_dummy_1 = 1; 
		else Status_Checking_Acc_dummy_1 = 0;
	if Status_Checking_Acc eq 'A12' then Status_Checking_Acc_dummy_2 = 1; 
		else Status_Checking_Acc_dummy_2 = 0;
	if Status_Checking_Acc eq 'A13' then Status_Checking_Acc_dummy_3 = 1; 
		else Status_Checking_Acc_dummy_3 = 0;

    run;

    AI:
    import pandas as pd

    logit_Default_On_Payment_v1 = pd.DataFrame(logit_Default_On_Payment)
    logit_Default_On_Payment_v1['Status_Checking_Acc_dummy_1'] = (logit_Default_On_Payment['Status_Checking_Acc'] == 'A11').astype(int)
    logit_Default_On_Payment_v1['Status_Checking_Acc_dummy_2'] = (logit_Default_On_Payment['Status_Checking_Acc'] == 'A12').astype(int)
    logit_Default_On_Payment_v1['Status_Checking_Acc_dummy_3'] = (logit_Default_On_Payment['Status_Checking_Acc'] == 'A13').astype(int)

    """
    
    # sample_input1_cc = '''
    # %macro mBivariate(var);
    # proc sql;
    # Create table &var._tab as 
    # select &var, count(*) as freq,
    # sum(Default_On_Payment) as Default_On_Payment 
    # from logit.Default_On_Payment
    # group by &var;
    # quit;

    # data &var._tab;
    # set &var._tab;
    #     Default_Rate = Default_On_Payment/freq;
    # run;

    # proc print data = &var._tab; run;
    # %mend mBivariate;'''
    # sample_output1_cc = '''
    # import pandas as pd

    # def mBivariate(var):
    # # Creating &var._tab table
    # data = pd.DataFrame({
    #     var: logit.Default_On_Payment[var],
    #     'freq': logit.Default_On_Payment.groupby(var).size(),
    #     'Default_On_Payment': logit.Default_On_Payment.groupby(var).sum()
    # }).reset_index()

    # # Adding Default_Rate column
    # data['Default_Rate'] = data['Default_On_Payment'] / data['freq']

    # # Printing the &var._tab table
    # print(data)

    # # Calling the mBivariate macro
    # mBivariate(var)
    # '''

    response = openai.ChatCompletion.create(
        model=exl_model,
        messages=[
            {"role": "system", "content": bot_instructions},
            # {"role": "system", "name":"example_user", "content": sample_input1_cc},
            # {"role": "system", "name": "example_assistant", "content": sample_output1_cc},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]


##Defining Model functions:
def debug_function():
    progress_text = "Debugging, Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(1)
        my_bar.progress(percent_complete + 1, text=progress_text)
        response_syntax =  syntax_model(prompt)
        if type(response_syntax) == type('Check'):
            my_bar.progress(100)
            break

    st.markdown('\n:blue[Code debugging]')
    st.write(response_syntax)


def summary_function():    
    progress_text = "Summarizing, Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(1)
        my_bar.progress(percent_complete + 1, text=progress_text)
        response_summary = summary_model(prompt)
        if type(response_summary) == type('Check'):
            my_bar.progress(100)
            break

    st.markdown('\n:blue[Code Summarization]')
    st.write(response_summary)


def conversion_function():
    progress_text = "Converting, Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(1)
        my_bar.progress(percent_complete + 1, text=progress_text)
        response_conversion = conversion_model(prompt)
        if type(response_conversion) == type('Check'):
            my_bar.progress(100)
            break

    st.markdown('\n:blue[Python Code]')
    st.code(response_conversion, language = 'python')

##Show stuff to the sceen if there is a prompt
if st.button('Submit'):

    if prompt.strip() == '' or prompt is None:
        st.text("Please enter your SAS code.")

    elif debug_flag is not True and summarize_flag is not True and convert_flag is not True:
        st.text("Please select an option (Debug, Summarize or Convert) to proceed.")

    else:

        if debug_flag and summarize_flag and convert_flag:
            debug_function()
            summary_function()
            conversion_function()
        
        elif debug_flag and summarize_flag:
            debug_function()
            summary_function()
            
        elif debug_flag and convert_flag:
            debug_function()
            conversion_function()

        elif summarize_flag and convert_flag:
            summary_function()
            conversion_function()
        
        elif debug_flag:
            debug_function()
        
        elif summarize_flag:
            summary_function()
        
        else:
            conversion_function()

    
