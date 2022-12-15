#year < 2000
#IMDB_votes (popular) > 50,0000
#box_office (profitable) > 4000,0000
#runtime > 120
#director
#contain Hollywood super stars
#language contains English
#country contains UK
#nominated oscar
#if R

import pandas as pd

question = ['Do you want an old movie?', 'Do you want a popular movie?', 'Do you want a grossing movie?', 'Do you want a long movie?', 'Do you want a movie directed by a famous director?', 'Do you want a movie acted by Hollywood super stars?', 'Do you want a movie in English?', 'Do you want a movie that has been nominated the Oscar Award?', 'Do you want an R-rated movie?', 
           'Do you want a crime movie?']
def main():
    df = pd.read_csv('collected_data.csv')
    super_star = ['Johnny Depp', 'Al Pacino', 'Robert De Niro', 'Kevin Spacey', 'Denzel Washington', 'Russell Crowe', 'Brad Pitt', 'Angelina Jolie', 'Leonardo DiCaprio', 'Tom Cruise', 'John Travolta', 'Arnold Schwarzenegger', 'Sylvester Stallone', 'Kate Winslet', 'Christian Bale', 'Morgan Freeman', 'Keanu Reeves', 'Nicolas Cage', 'Hugh Jackman', 'Edward Norton']
    df2 = df.copy()
    df2['if_old'] = [i < 2000 for i in df2['year']]
    df2['if_popular'] = [i > 500000 for i in df2['IMDB_votes']]
    df2['if_grossing'] = [i > 40000000 for i in df2['box_office']]
    df2['if_long'] = [i > 120 for i in df2['runtime']]
    df2['if_famous_director'] = [(i in df2['director'].value_counts().iloc[:20].index) for i in df2['director']]
    df2['if_super_star'] = [set(i.split(', '))&set(super_star) != set() for i in df2['stars']]
    df2['if_English'] = ['English' in i.split(', ') for i in df2['language']]
    df2['if_nominated'] = [i == True for i in df2['nominated_oscar']]
    df2['if_restricted'] = [i == 'R' for i in df2['rated']]
    df2['if_crime'] = ['Crime' in i.split(', ') for i in df2['genre']]
    lst_country = []
    for i in range(len(df2)):
        try:
            if 'United Kingdom' in df2.iloc[i]['country'].split(', '):
                lst_country.append(True)
            else: lst_country.append(False)
        except:
            lst_country.append(False)
    df2['if_UK'] = lst_country
    
    
    Initial_tree = (df2, None, None)
    tree = construct(Initial_tree, 0)
    with open("tree.json", 'w') as f:
    #print(json.dumps('Leaf'), file = treeFile)
        saveTree(tree, f)
    
def construct(tree, index):
    #print(index)
    #print(tree)
    if len(tree[0]) == 0: return None
    if (len(tree[0]) == 1) or (index == 10): return tree
    else:
        df = tree[0]
        return (question[index], construct((df[df.iloc[:,index+18] == True], None, None), index+1), construct((df[df.iloc[:,index+18] == False], None, None), index+1))
    
def saveTree(tree, f):
    text, left, right = tree
    if left is None and right is None:
        f.write('Leaf\n')
        write = ''
        for i in range(len(text)):
            row = text.iloc[i]
            try:
                write += row['IMDB_number'] + ' ' + row['title'] + ', ranking ' + str(row['place']) + ' among the top 250 movies. Its a ' + row['genre'] +' movie in ' + str(row['year']) + ', directed by ' + row['director'] + ', having a runtime of ' + str(row['runtime']) + 'min, and rated ' + row['rated'] + '.***The movie is about: ' + row['plot']+ '/'
            except:
                write += row['IMDB_number'] + ' ' + row['title'] + ', ranking ' + str(row['place']) + ' among the top 250 movies. Its a ' + row['genre'] +' movie in ' + str(row['year']) + ', directed by ' + row['director']+'./'
        f.write(write+'\n')
    else:
        f.write('Internal node\n')
        f.write(text+'\n')
        if left is not None:
            saveTree(left, f)
        else:
            f.write('Leaf\n')
            f.write('None\n')
        if right is not None:
            saveTree(right, f)
        else:
            f.write('Leaf\n')
            f.write('None\n')
        
def loadTree(treeFile):
    while True:
        line = treeFile.readline().strip()
        if line == '': break
        if line == 'Leaf':
            name = treeFile.readline().strip()
            return (name, None, None)
        elif line == 'Internal node':
            name = treeFile.readline().strip()
            return (name, loadTree(treeFile), loadTree(treeFile))

if __name__ == '__main__':
    main()


# In[ ]:




