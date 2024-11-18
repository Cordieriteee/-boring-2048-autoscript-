import webbrowser
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

#game over
def game_over(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    game_over_text = soup.find('div', {'class': 'game-message game-over'})
    if game_over_text and 'Game over!' in game_over_text.text:
        return True
    return False

#获取游戏状态
def get_game_state(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    grid_container = soup.find('div', {'class': 'tile-container'})
    return str(grid_container)

# 确定文件路径
file_path = os.path.join(os.path.dirname(__file__), 'best_score.txt')
print("Best score file path:", file_path)

# 确保文件存在，如果不存在则创建
if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        f.write('0')

#检查并储存最高分
def best_score(driver, current_score):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    #find local best score
    try:
        with open(file_path, 'r') as f:
            best_score = f.read().strip()
            
            #确保当文件为空时以当前分数为最高分
            if best_score:
                best_score = int(best_score)
            else:
                best_score = current_score
    
    except FileNotFoundError:
        best_score = current_score
    
    #检查当前分数是否高于最高分
    if current_score > best_score:
        with open(file_path, 'w') as f:
            f.write(str(current_score))
        print('New Best Score:', current_score)
    else:
        print('Best Score:', best_score)

#获取当前分数
def get_current_score(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    score_container = soup.find('div', {'class': 'score-container'})
    score_text = score_container.contents[0].strip()
    print('Final Score:', score_text)
    return int(score_text)


#设置实例
driver = webdriver.Edge()

# Open 2048
driver.get("https://www.2048.org/")

# Wait for the page to load
time.sleep(3)

# Find the game body
body = driver.find_element(By.TAG_NAME, 'body')

#all actions that will be taken
actions = [Keys.LEFT, Keys.DOWN, Keys.RIGHT, Keys.DOWN]

#loop
game_end = False
while not game_end:
    
    #获得游戏最初状态
    state_before = get_game_state(driver)

    #循环动作
    for action in actions:
        body.send_keys(action)
        time.sleep(0.5) #调整此行，改变2048移动速度

        #确保动作后游戏未结束
        if game_over(driver):
            print('Game Over!')
            game_end = True

            #检查并储存最高分
            current_score = get_current_score(driver)
            best_score(driver, current_score)
            break
    
    #若未结束，获取动作后的状态并判断是否有变化
    if not game_end:
        state_after = get_game_state(driver)
        if state_before == state_after:

            #若无变化，向上移动
            body.send_keys(Keys.UP)

        #确保动作后游戏未结束
        if game_over(driver):
            print('Game Over!')
            game_end = True

            #检查并储存最高分
            current_score = get_current_score(driver)
            best_score(driver, current_score)

            break
    
    else:
        break
