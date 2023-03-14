import pdb
import math
import pandas as pd
import numpy as np

class Tree:

    def __init__(self,feature,value=None):
        self.feature = feature
        self.left_child = None
        self.right_child = None
        #if val then it's leaf node
        self.value = value

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
        if len(df)<=20:
            self.value = 0
            return
        n_subset = df[df[self.feature]==0]
        p_subset = df[df[self.feature]==1]
        n_best = Tree.pick_best_feature(n_subset,self.feature)
        p_best = Tree.pick_best_feature(p_subset,self.feature)
        self.left_child = Tree(n_best).build_tree(n_subset)
        self.right_child = Tree(p_best).build_tree(p_subset)

    @staticmethod
    def pick_best_feature(df,previos_best):

        def calculate_entropy(df_filtered):
            p = len(df_filtered[df_filtered[df_filtered.columns[-1]]==1])/len(df_filtered) if len(df_filtered)!=0 else 0
            entropy = - p*math.log(p+0.000001,2) - (1-p)*math.log((1-p)+0.000001,2)
            return entropy
    
        entropyes = {}
    
        for col in list(df.columns)[:-1]:
            #calculate dependent variable entropy for explanatory feature being possitive/negative
            if col == previos_best:
                continue
            p_exmp = df[df[col]==1]
            n_exmp = df[df[col]==0]
            p_entropy = calculate_entropy(p_exmp) 
            n_entropy = calculate_entropy(n_exmp)
            p = len(p_exmp)/len(df) if len(p_exmp)!=0 else 1/2
            avg_entropy = p*p_entropy + (1-p)*n_entropy
            entropyes[col] = avg_entropy
        #fix this so it gets a random feature if more than one min features.
        print(entropyes)
        return sorted(entropyes.items(),key=lambda x: x[1])[0][0]



def test(): 
    df = pd.read_csv('market_data.csv')
    df_train = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][:int(len(df)*0.8)]
    df_test = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][int(len(df)*0.8):].values.tolist()
    # print(df_train['ExCl'].value_counts().idxmax())
    feature = Tree.pick_best_feature(df_train,None)
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