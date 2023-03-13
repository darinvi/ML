import pandas as pd
import numpy as np
import math

def calculate_r_values(train_data,feature,features):
    train_data = pd.DataFrame(train_data,columns=[*features,'target'])
    #split into two datasets, positive examples and negative examples
    p_exmp, n_exmp = train_data[train_data['target']==1], train_data[train_data['target']==0]
    #compute the R values for each combination feature-outcome; Laplace correction
    r11_val = (len(p_exmp[p_exmp[feature]==1])+1)/(len(p_exmp)+2)
    r01_val = 1 - r11_val
    r10_val = (len(n_exmp[n_exmp[feature]==1])+1)/(len(n_exmp)+2)
    r00_val = 1 - r10_val
    log_val = list(map(lambda x: math.log(x,10),[r11_val,r01_val,r10_val,r00_val]))
    return {'positive':{1:log_val[0],0:log_val[1]},'negative':{1:log_val[2],0:log_val[3]}}

def handle_score_computations(row,scores,is_positive):
    #The score is calculated using r-values. It is used to make a prediction. 1 if S(1)>S(0) else 0
    score = 0
    for i,name in enumerate(list(scores.keys())):
        curr_score = scores[name]['positive'][row[i]] if is_positive else scores[name]['negative'][row[i]]
        score += curr_score
    return score

def cross_valiadtion(scores,test_data):
    # print(test_data.shape)
    # print(type(test_data))
    right_answers = 0
    for el in test_data:
        score_positive = handle_score_computations(el,scores,True)
        score_negative = handle_score_computations(el,scores,False)
        expected = 1 if score_positive > score_negative else 0
        actual = el[-1]
        if expected == actual:
            right_answers += 1
    right_answers /= len(test_data)
    return right_answers

#This is a data set I created during an university homework, split into 10 parts
#I will only use a couple of boolean features trying to explain 'D2'- also bool
df = pd.read_csv('market_data.csv')[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']]
features = list(df.columns)[:-1]
df = np.array_split(np.array(df),10)
correct_predictions = 0

for i in range(len(df)):
    #using list-comprehensions and numpy.concatenate in order to cross-validate and get an average idea of the error term
    df_train = np.concatenate([el for indx,el in enumerate(df) if indx != i])
    df_test = np.array(*[el for indx,el in enumerate(df) if indx == i])
    scores = {feature:calculate_r_values(df_train,feature,features) for feature in features}
    correct_predictions += cross_valiadtion(scores,df_test)

correct_predictions /= len(df)
print(f'Average error = {(1 - correct_predictions)*100:.2f}% => {correct_predictions*100:.2f}% correct predictions')

