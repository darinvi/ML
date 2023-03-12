import pandas as pd
import math

def calculate_r_values(df,feature):
    #split into two datasets, positive examples and negative examples
    p_exmp, n_exmp = df[df['D2']==1], df[df['D2']==0]
    #compute the R values for each combination feature-outcome; Laplace correction
    r11_val = (len(p_exmp[p_exmp[feature]==1])+1)/(len(p_exmp)+2)
    r01_val = 1 - r11_val
    r10_val = (len(n_exmp[n_exmp[feature]==1])+1)/(len(n_exmp)+2)
    r00_val = 1 - r10_val
    log_val = list(map(lambda x: math.log(x,10),[r11_val,r01_val,r10_val,r00_val]))
    return {'positive':{1:log_val[0],0:log_val[1]},'negative':{1:log_val[2],0:log_val[3]}}

def handle_score_computations(row,scores,is_positive):
    #Score
    score = 0
    for i,name in enumerate(list(scores.keys())):
        curr_score = scores[name]['positive'][row[i]] if is_positive else scores[name]['negative'][row[i]]
        score += curr_score
    return score

df = pd.read_csv('market_data.csv')

df_train = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][:int(len(df)*0.85)]
df_test = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][int(len(df)*0.85):].values.tolist()

def cross_valiadtion():
    right_answers = 0
    for el in df_test:
        score_positive = handle_score_computations(el,scores,True)
        score_negative = handle_score_computations(el,scores,False)
        expected = 1 if score_positive > score_negative else 0
        actual = el[-1]
        if expected == actual:
            right_answers += 1
    right_answers /= len(df_test)
    print(f'{right_answers*100:.2f}', '%')

features = list(df_train.columns)[:-1]
scores = {feature:calculate_r_values(df_train,feature) for feature in features}

cross_valiadtion()
