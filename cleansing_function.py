def clean_slang(text, slang_df):
    # turning values in alay and baku columns into key-pair value
    slang_dict = dict(zip(slang_df['alay'], slang_df['baku'])) 
    
    #create empty list
    temp = [] 
    
    for word in text.split(' '):
        # checking if word exist in dictionary key
        if word in slang_dict.keys():
            # if exists, reassign the word variable to be equal to slang[word]
            word = slang_dict[word] 
            temp.append(word) 
        else :
            # if it doesn't, then we pass the word into the empty list
            temp.append(word) 
            
    # rearranging the words in the temp list and turning it back into strings
    return ' '.join(temp) 
    
def clean_abusive(text, abusive_df):
    abusive_free = text
    for word in abusive_df['ABUSIVE']:
        if text == word:    
            abusive_free = ""
        else:
            pass
    return abusive_free
