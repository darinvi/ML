import pdb
import math
import pandas as pd
import numpy as np


class Tree:
    def __init__(self,feature,value=None):
        self.feature = feature
        print(self.feature ,'da')
        self.value = value
        self.left_child = None
        self.right_child = None
    

    def buld_tree(self,df):
        # p- positive, n- negative
        if len(df['D2'].unique())==1:
            #make leaf node
            self.value = df['D2'].unique()[0]
            return
        n_subset = df[df[self.feature]==0]
        p_subset = df[df[self.feature]==1]
        n_best = Tree.pick_best_feature(n_subset)
        print(n_best)
        p_best = Tree.pick_best_feature(p_subset)
        print(p_best)
        self.left_child = Tree(n_best)
        self.right_child = Tree(p_best)

    @staticmethod
    def pick_best_feature(df_tr):
        def calculate_entropy(test_df,el):
            print(el)
            p = len(test_df[test_df['D2']==1])/len(test_df)
            entropy = - p*math.log(p,2) - (1-p)*math.log((1-p),2)
            return entropy
        
        entropyes = {}
    
        for el in list(df_tr.columns)[:-1]:
            #calculate dependent variable entropy for explanatory feature being possitive/negative
            p_exmp = df_tr[df_tr[el]==1]
            # print(el)
            n_exmp = df_tr[df_tr[el]==0]
            print(len(p_exmp))
            print(p_exmp.head())
            print(len(n_exmp))
            print(n_exmp.head())
            p_entropy = calculate_entropy(p_exmp,el)
            n_entropy = calculate_entropy(n_exmp,el)
            avg_entropy = len(p_exmp)/len(df_tr)*p_entropy + len(n_exmp)/len(df_tr)*n_entropy
            entropyes[el] = avg_entropy
        #fix this so it gets a random feature if more than one min features.
        return sorted(entropyes.items(),key=lambda x: x[1])[0][0]



def test(): 
    df = pd.read_csv('market_data.csv')
    df_train = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][:int(len(df)*0.8)]
    df_test = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][int(len(df)*0.8):].values.tolist()

    feature = Tree.pick_best_feature(df_train)
    root = Tree(feature)
    root.buld_tree(df_train)
    print(root.__class__)
    print(root.left_child.feature)

test()



# class Tree:
#     def __init__(self,key):
#         self.key = key
#         self.left_child = None
#         self.right_child = None

#     def insert(self,data):
#         if self.key is None:
#             self.key = data
#             return
#         if self.key == data:
#             return
#         if self.key > data:
#             if self.left_child:
#                 self.left_child.insert(data)
#             else:
#                 self.left_child = Tree(data)
#         else:
#             if self.right_child:
#                 self.right_child.insert(data)
#             else:
#                 self.right_child = Tree(data)

# root = Tree(None)

# example_list = [34,25,67,65,3,1,23,4,5,67,89,10]
# for example in example_list:
#     root.insert(example)
