import pdb
import math
import pandas as pd
import numpy as np

class Tree:

    def __init__(self,feature,value=None):
        self.feature = feature
        self.value = value
        self.left_child = None
        self.right_child = None
        Tree.used_features.appendleft(self.feature)    

    def build_tree(self,df):
        y_val = df.columns[-1]
        # p- positive, n- negative
        if len(df[y_val].unique())==1:
            #make leaf node
            self.value = df[y_val].unique()[0]
            return
        if len(df)<=20 and len(df[df[y_val]==0])!=len(df[df[y_val]==1]):
            self.value = sorted(df[y_val].value_counts().idxmax())
            return
        n_subset = df[df[self.feature]==0]
        p_subset = df[df[self.feature]==1]
        n_best = Tree.pick_best_feature(n_subset)
        p_best = Tree.pick_best_feature(p_subset)
        self.left_child = Tree(n_best).build_tree(n_subset)
        self.right_child = Tree(p_best).build_tree(p_subset)

    @staticmethod
    def pick_best_feature(df_all):

        def calculate_entropy(df_all):
            p = len(df_all[df_all[df_all.columns[-1]]==1])/len(df_all)
            entropy = - p*math.log(p+0.000001,2) - (1-p)*math.log((1-p)+0.000001,2)
            return entropy
    
        entropyes = {}
    
        for el in list(df_all.columns)[:-1]:
            #calculate dependent variable entropy for explanatory feature being possitive/negative
            p_exmp = df_all[df_all[el]==1]
            n_exmp = df_all[df_all[el]==0]
            p_entropy = calculate_entropy(df_all) 
            n_entropy = calculate_entropy(df_all)
            p = len(p_exmp)/len(df_all)
            avg_entropy = p*p_entropy + (1-p)*n_entropy
            entropyes[el] = avg_entropy
        #fix this so it gets a random feature if more than one min features.
        print(entropyes)
        return sorted(entropyes.items(),key=lambda x: x[1])[0][0]



def test(): 
    df = pd.read_csv('market_data.csv')
    df_train = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][:int(len(df)*0.8)]
    df_test = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][int(len(df)*0.8):].values.tolist()
    # print(df_train['ExCl'].value_counts().idxmax())
    feature = Tree.pick_best_feature(df_train)
    root = Tree(feature)
    root.build_tree(df_train)
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

# a = np.array([1,0,0,1,1])
# b = np.array([0,1,0,0,1])
# print(a == b)