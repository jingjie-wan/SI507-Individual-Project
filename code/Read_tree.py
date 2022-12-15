import pandas as pd
import webbrowser

def main():
    with open("tree.json", 'r') as f:
        tree = loadTree(f)
    print("Welcome to the movie recommendation system! We will recommend movies from the TOP 250 movies based on your answers to several questions. Now let\'s begin!")
    play(tree)
    while True:
        answer = input('Would you like to play again?')
        if answer == 'yes' or answer == 'Yes':
            play(tree)
        else:
            break
    print('Hope you have found the movie to watch in the winter break! Bye!')

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

def play(tree):
    if tree[1] == None and tree[2] == None:
        if tree[0] == 'None':
            print("We can\'t find movies meeting your requirements among TOP 250 movies. You can change your options and try again.")
        else:
            movies = tree[0].split('/')[:-1]
            imdb_list = []
            plot_list = []
            title_list = []
            info_list = []
            for movie in movies:
                imdb_number, movie = movie.split(" ", 1)
                imdb_list.append(imdb_number)
                split = movie.split('***')
                if len(split) == 1: plot_list.append('No plot available for this movie.')
                else: plot_list.append(split[1])
                
                movie = split[0]
                title, info = movie.split(', ', 1)
                title_list.append(title)
                info_list.append(info)
            
            answer = input('Enter 1 for seeing the list of recommendated movies in simple mode, 2 for detailed mode.')
            i = 1
            if answer == '1':
                print('Here are the recommended movies:')
                for item in title_list:
                    print('Movie ' + str(i) + ': ')
                    print(item)
                    print('---------------------------------------------------------------------------------------------')
                    i += 1
            else:
                print('Here are the recommended movies:')
                for j in range(len(title_list)):
                    print('Movie ' + str(i) + ': ')
                    print(title_list[j] + ', ' + info_list[j])
                    print('---------------------------------------------------------------------------------------------')
                    i += 1
                
            
            while True:
                answer = input('Enter 1 for the plot of movies and 2 for the link of the movies.Enter exit if no more infomation is needed: ')
                if answer == 'exit':
                    break
                elif answer == '1':
                    number = input('Enter the number of the movie (e.g. 1 for Movie 1) from the above movies to check its plot: ')
                    if number.isnumeric() == True:
                        number = int(number)
                        if (number < 1) or (number > i-1):
                            print('Invalid number, please try again')
                        else:
                            print(title_list[number-1] + ':\n' + plot_list[number-1])
                elif answer == '2':
                    number = input('Enter the number of the movie (e.g. 1 for Movie 1) from the above movies to go to its imdb website: ')
                    if number.isnumeric() == True:
                        number = int(number)
                        if (number < 1) or (number > i-1):
                            print('Invalid number, please try again')
                        else:
                            url = 'https://www.imdb.com/title/' + imdb_list[number-1]
                            print('Launching\n' + url +'\nin web browser...\n')
                            webbrowser.open_new_tab(url)
        #print(tree[0])
    else:
        answer = input(tree[0])
        if answer == 'yes' or answer == 'Yes':
            play(tree[1])
        elif answer == 'no' or answer == 'No':
            play(tree[2])
        else:
            print("Please answer 'yes' or 'no'")
            play(tree)

if __name__ == '__main__':
    main()


# In[ ]:




