import math
import pandas as pd

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
        #conditions to make leaf node
        if len(df[y_val].unique())==1:
            self.value = df[y_val].unique()[0]
            return
        if len(df[self.feature].unique())==1:
            self.value = df[y_val].value_counts().idxmax()
            return
        if len(df)<=50 and len(df[df[y_val]==0])!=len(df[df[y_val]==1]):
            self.value = df[y_val].value_counts().idxmax()
            return
        if len(df)<=50:
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
            #p- proportion of y-values equal to 1 comapred to all y-values
            y_val = df_filtered.columns[-1]
            p = len(df_filtered[df_filtered[y_val]==1])/len(df_filtered) if len(df_filtered)!=0 else 0
            small = 0.000000000000001
            entropy = - p*math.log(p+small,2) - (1-p)*math.log((1-p)+small,2)
            return entropy
    
        entropies = {}
    
        for col in list(df.columns)[:-1]:
            #calculate dependent variable entropy for explanatory feature being possitive/negative
            if col == previos_best:
                continue
            elif len(df[col].unique())>1:
                p_exmp = df[df[col]==1]
                n_exmp = df[df[col]==0]
                p_entropy = calculate_entropy(p_exmp) 
                n_entropy = calculate_entropy(n_exmp)
                p = len(p_exmp)/len(df) if len(p_exmp)!=0 else 0
                avg_entropy = p*p_entropy + (1-p)*n_entropy
                # if avg_entropy <= 0:
                #     quit()
            else:
                avg_entropy = calculate_entropy(df)
            entropies[col] = avg_entropy
        #fix this so it gets a random feature if more than one min features.
        return sorted(entropies.items(),key=lambda x: x[1])[0][0]



def test(): 
    df = pd.read_csv('market_data.csv')
    df_train = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][:int(len(df)*0.8)]
    df_test = df[['Held_Open','Trend_bool','RVOL_bool','Gap_bool','ExCl','D2']][int(len(df)*0.8):].values.tolist()
    # print(df_train['ExCl'].value_counts().idxmax())
    feature = Tree.pick_best_feature(df_train,None)
    root = Tree(feature)
    root.build_tree(df_train)
    print(root.__class__)
    print(root.left_child)
test()


