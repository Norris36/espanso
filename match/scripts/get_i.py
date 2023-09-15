import pandas as pd
path = r'C:\Users\jbay\AppData\Roaming\espanso\match\scripts\i_codes.csv'

df = pd.read_csv(path)

print(r'.\aws --profile production-eng ssm start-session --region us-east-1 --target ' + str(df.loc[0, df.columns[0]]) +' --document-name AWS-StartPortForwardingSessionToRemoteHost --parameters host="dotcom.ccxrngmoosoq.us-east-1.rds.amazonaws.com",portNumber="5432",localPortNumber="55432"')