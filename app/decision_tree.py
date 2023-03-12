import math
import pandas as pd

class Node:
    def __init__(self,feature=None,left=None,right=None,value=None):
        self.feature = feature
        self.left_child = left
        self.right_child = right
        #for leaf nodes
        self.value = value

class Tree:
    def __init__(self,df):
        self.root = self.buld_tree(df)
    
    @staticmethod
    def pick_best_feature(df):
        def calculate_entropy(test_df):
            p = len(test_df[test_df['D2']==1])/len(test_df)
            entropy = - p*math.log(p,2) - (1-p)*math.log((1-p),2)
            return entropy
        
        entropyes = {}
    
        for el in list(df.columns)[:-1]:
            p_exmp = df[df[el]==1]
            n_exmp = df[df[el]==0]
            print(el)
            p_entropy = calculate_entropy(p_exmp)
            n_entropy = calculate_entropy(n_exmp)
            avg_entropy = len(p_exmp)/len(df)*p_entropy + len(n_exmp)/len(df)*n_entropy
            entropyes[el] = avg_entropy

        return sorted(entropyes.items(),key=lambda x: x[1])[0][0]

    def buld_tree(self,df):
        if len(df['D2'].unique())==1:
            print(type(df['D2'].unique()))
            print(len(df['D2'].unique()))
            return Node(value=df_train['D2'].unique()[0])
        else:
            print('yeea')
            best_feature = Tree.pick_best_feature(df)
            # print(best_feature)
            # print(df[df[best_feature]==1])
            n_subset = df[df[best_feature]==0]
            p_subset = df[df[best_feature]==1]
            return Node(best_feature,left=self.buld_tree(n_subset),right=self.buld_tree(p_subset))

df = pd.read_csv('market_data.csv')
df_train = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][:int(len(df)*0.8)]
df_test = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][int(len(df)*0.8):].values.tolist()
print(df)
# test = Tree(df_train)
# print(test.root.left_child)