import pandas as pd

df=pd.read_csv("glassdoor_jobs.csv")
#salary parsing

df=df[df['Salary Estimate'] != '-1']
salary=df['Salary Estimate'].apply(lambda x : x.split('(')[0])
minus_kd=salary.apply(lambda x : x.replace('K','').replace('$',''))
rem_hourly=minus_kd.apply(lambda x : x.lower().replace('per hour','').replace('employer provided salary:',''))
df['min_salary']=rem_hourly.apply(lambda x : int(x.split('-')[0]))
df['max_salary']=rem_hourly.apply(lambda x : int(x.split('-')[1]))
df['avg_salary']=(df.min_salary+df.max_salary)/2

#Company name text only
df['Company_txt']=df.apply(lambda x : x['Company Name'] if x['Rating'] < 0 else x['Company Name'][: -3] , axis = 1)

#state field
df['Job_State']=df['Location'].apply(lambda x : x.split(',')[1])
df['Head_Location']=df['Headquarters'].apply(lambda x : x.split(',')[-1])
df['same_state']=df.apply(lambda x : 1 if x.Job_State == x.Head_Location else 0 , axis = 1)

#age of company
df['Company_Age']=df.apply(lambda x : '-1' if x.Founded == -1 else ( 2021 - x.Founded) , axis = 1)

#parsing of job description (python , etc.)
df['Job Description'][0]
df['python_yn']=df['Job Description'].apply(lambda x : 1 if 'python' in x.lower() else 0)
df['rstudio_yn']=df['Job Description'].apply(lambda x : 1 if 'r studio' in x.lower() or 'r-studio' in x.lower()  else 0 )
df['spark_yn']=df['Job Description'].apply(lambda x : 1 if 'spark' in x.lower() or 'apache' in x.lower()  else 0 )
df['aws_yn']=df['Job Description'].apply(lambda x : 1 if 'aws' in x.lower() or 'amazon web service' in x.lower()  else 0 )
df['excel_yn']=df['Job Description'].apply(lambda x : 1 if 'excel' in x.lower() or 'ms-excel' in x.lower()  else 0 )

df.columns
df_out=df.drop(['Unnamed: 0'] , axis = 1)
df_out.to_csv('salary_data_cleaned.csv' , index= False)
