import pandas as pd


class ClassifierTable:

    def __init__(self, file_path):
        self.dict = self.read_classifier_table(file_path)

    def read_classifier_table(self, file_path: str) -> dict:
        df = pd.read_csv(file_path)
        my_dict = pd.Series(df['Classification'].values, index=df['Character']).to_dict()
        my_dict['\n'] = my_dict.pop('\\n')  
        my_dict['\"'] = my_dict.pop('\\"')  
        return my_dict
    
    def getClassification(self, character: str):
        return self.dict.get(character, None)


class Transitiontable:

    def __init__(self, file_path:str):
        self.dict = self.read_transition_table(file_path)

    def read_transition_table(self, file_path: str) -> dict:
        df = pd.read_csv(file_path)
        my_dict = df.groupby('Start_State').apply(lambda group: group.set_index('On')['End_State'].to_dict()).to_dict()
        return my_dict

    def getTransition(self, state:str, transition:str):
        result = self.dict.get(state, None)
        if result is None:
            return None
        return result.get(transition, None)


class TokenTypeTable:
    def __init__(self, file_path:str):
        self.dict = self.read_token_type_table(file_path)

    def read_token_type_table(self, file_path: str) -> dict:
        df = pd.read_csv(file_path)
        my_dict = pd.Series(df['Type'].values, index=df['State']).to_dict()  
        return my_dict
    
    def getTokenType(self, state):
        return self.dict.get(state, None)