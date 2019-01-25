import numpy as np
import pandas as pd
import random


food = pd.read_csv('/Users/Tomoya_Iwasaki/Desktop/food.csv')

iteration = 100;
n = 4;



df_food = pd.DataFrame(food)
food_name = df_food['食品名']
df_food.index = food_name
df_food = df_food.drop('食品名', axis=1)
col = df_food.columns.values
df_score = pd.Series(0, index=food_name)



order = []
group = None
current_foods_name = [];
current_foods_values = [];
current_best_answer_names = [];
current_best_distance = 0;
kcal = 0;
money = 0;
kcal_limit = 1800;
money_limit = 600;
t = 0;

def init():

    global df_food
    global order
    global current_foods_name
    global current_foods_values
    global current_best_answer_names
    global current_best_distance
    global kcal
    global money

    t = 0
    order = [1,2,3,4];
    current_foods_name = [];
    current_foods_values = [];
    current_best_answer_names = [];
    kcal = 0;
    money = 0;

    return

def decideOrder(arg):
    np.random.shuffle(arg)
    return arg;


def selectFoods(order_list):

    global group

    group = order_list[0]
    order_list.pop(0)


    if group == 1:
        foods = df_food['第一群'].sort_values(ascending=False);
        foods = pd.Series(foods[0:4])


    elif group == 2:
        foods = df_food['第二群'].sort_values(ascending=False);
        foods = pd.Series(foods[0:4])


    elif group == 3:
        foods = df_food['第三群'].sort_values(ascending=False);
        foods = pd.Series(foods[0:4])


    elif group == 4:
        foods = df_food['第四群'].sort_values(ascending=False);
        foods = pd.Series(foods[0:4])



    return foods;


def selectAfood(foods, num):

    global df_food
    global df_score

    score_list = []


    fourFoods = foods.index.values
    for i in range(len(foods)):
        score_list.append(df_score.loc[foods.index[i]])
    score_list = pd.Series(score_list, index = fourFoods)
    score_list = score_list.sort_values(ascending=False)



    dice = random.random()

    if dice < 0.7:
        answer = str(score_list.index[0])
        df_food.loc[score_list.index[0], ['第一群','第二群','第三群','第四群']] = 0;
        return answer

    elif dice >= 0.7 and dice < 0.85:
        answer = str(score_list.index[1])
        df_food.loc[score_list.index[0], ['第一群','第二群','第三群','第四群']] = 0;
        return answer

    elif dice >= 0.85 and dice < 0.95:
        answer = str(score_list.index[2])
        df_food.loc[score_list.index[0], ['第一群','第二群','第三群','第四群']] = 0;
        return answer

    elif dice >= 0.95:
        answer = str(score_list.index[3])
        df_food.loc[score_list.index[0], ['第一群','第二群','第三群','第四群']] = 0;
        return answer


def checkCondition(ans):

    global money
    global kcal
    global current_foods_name
    global current_foods_values
    global current_best_answer_names
    global current_best_distance

    money += df_food.loc[ans]['値段']
    kcal += df_food.loc[ans]['カロリー']

    if kcal >= kcal_limit:
        print(current_foods_name)
        print(str(kcal) + " It's over")
        return current_foods_name

    elif money >= money_limit:
        print(current_foods_name)
        print(str(money) + " It's over")
        return current_foods_name

    else:
        current_foods_name.append(ans)
        return True


def evaluate(answer):

    global current_foods_name
    global current_foods_values
    global current_best_answer_names
    global current_best_distance

    group1 = 0;
    group2 = 0;
    group3 = 0;
    group4 = 0;



    for i in range(len(answer)):
        group1 += abs(df_food.loc[answer[i]]['第一群']-3)
        group2 += abs(df_food.loc[answer[i]]['第二群']-3)
        group3 += abs(df_food.loc[answer[i]]['第三群']-3)
        group4 += abs(df_food.loc[answer[i]]['第四群']-3)

    distance = group1 + group2 + group3 + group4

    if distance >= current_best_distance:



        current_best_distance = distance;
#         print(current_best_distance)


        df_score.loc[current_foods_name] += float(distance)
#         print(df_score)

        current_best_answer_names = current_foods_name;
        return current_foods_name

def oneTrial():

    global order
    global t

    if len(order) == 0:
        order = [1,2,3,4]
        decideOrder(order)
    foods = selectFoods(order)
    answer = selectAfood(foods,group)
    check = checkCondition(answer)
    if check == True:
        oneTrial()
    else:
        evaluate(check);

        return


def chooseGroup(num):
    if num == 1:
        return "第一群"
    elif num == 2:
        return "第二群"
    elif num == 3:
        return "第三群"
    elif num == 4:
        return "第四群"



if __name__ == "__main__":
    global iteration

    i = 0
    while i < iteration:
        init()
        oneTrial()
        print("TRIAL " + str(i) +" the best distance is " + str(current_best_distance))
        print("TRIAL " + str(i) +" the best foods are " + str(current_best_answer_names))
        i += 1
        df_food = pd.DataFrame(food)
        food_name = df_food['食品名']
        df_food.index = food_name
        df_food = df_food.drop('食品名', axis=1)
        col = df_food.columns.values
    print("best is " + str(current_best_answer_names))
    print(str(kcal) + " kcal  It's over")
    print(str(money) + "yen  It's over")

    
