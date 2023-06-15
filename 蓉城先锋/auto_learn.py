import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from tqdm import tqdm
from update_webdriver import UpdateEdge

# 初始化网站
def browser_initial():
    options = Options()
    options.add_argument('--log-level=3')
    # 浏览器静音
    options.add_argument("--mute-audio")
    # 关闭cmd窗口的输出信息
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 尝试传参
    s = Service("msedgedriver.exe")
    browser = webdriver.Edge(service=s,options=options)
    page_url = 'https://new.cddyjy.com/login/qr'
    browser.get(page_url) # 打开网站
    browser.maximize_window() #最大化窗口
    print("请用微信扫码登录！\n")
    # 实现登录后页面跳转
    time.sleep(10)# 等待扫码
    wait = WebDriverWait(browser,60)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'ivu-card-body')))
    print("完成登录！\n")
    # # 最小化浏览器
    # browser.minimize_window()
    #点击公务员培训，进入对应网页
    train_page = browser.find_element(By.XPATH, '//*[@id="lhyj-content"]/div[2]/div/div[2]/div[2]/div/div[1]/span[1]').click()#点击跳转
    # 切换browser到公务员培训页面
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
    print("进入公务员培训！\n")
    if model == 1:
        print("1.开始学习必修课！\n")
        print('必修课已学完！！！\n')
        print("2.开始学习选修课！\n")
    # # 获取当前所有打开的窗口句柄
    # all_windows = browser.window_handles
    # print(all_windows)
    # # 获取当前窗口句柄
    # main_windows = browser.current_window_handle
    # print(main_windows)
    return browser 

# 选择视频，自动学习
def browser_learning(browser,model):
    # 点击必修课列表
    if model == 0:
        print("1.开始学习必修课！\n")
        required_courses = browser.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[3]/div/div[1]/div[1]/div[2]/div/div/div/div[2]').click()
    # 计数器
    num = 0 
    # 获取本地缓存数据，learned表示已完成多少个视频，并赋值给num
    if learned != 0:
        num = learned
    # 使用死循环，使下面的程序一直运行，通过break结束。
    while(1):
        # 点击选修课列表
        if model == 1:
            elective_courses = browser.find_element(By.XPATH,'//*[@id="app"]/div/div[2]/div[3]/div/div[1]/div[1]/div[2]/div/div/div/div[3]').click()
        time.sleep(3)
        # 获取全部按钮，通过buttons确认当前页面视频总数
        buttons = browser.find_elements(By.TAG_NAME,'button')
        # print(buttons)
        if browser.current_url == "https://new.cddyjy.com/member-education/civil":          
            # 开始学习
            if len(buttons)-2 != num:
                # 点击重新加载按钮，刷新页面
                button0 = buttons[1].click()
                # 通过num确认需要从第几个视频开始学习。
                button = buttons[num+2].click()
                print('正在检查第 {}/{} 个视频......'.format(num+1,len(buttons)-2))
                # 切换到视频页面
                windows = browser.window_handles
                browser.switch_to.window(windows[-1])
                # 等待进入视频播放状态
                time.sleep(5)
                wait_play = WebDriverWait(browser,15)
                play_element = wait_play.until(EC.element_to_be_clickable((By.CLASS_NAME,'ivu-card-body')))
                # 获取视频总时长，转换为秒，用于设计进度条
                total_time_text= browser.find_element(By.XPATH,'//*[@id="my-player"]/div[4]/div[4]/span[2]').get_attribute('textContent')
                total_time_text = total_time_text.strip()
                if len(total_time_text) < 6:
                    m1, s1 = total_time_text.split(':') 
                    total_time = int(m1)*60 + int(s1) #int()函数转换成整数运算获得时间
                else:
                    h1,m1,s1 = total_time_text.split(':') 
                    total_time = int(h1)*3600+int(m1)*60 + int(s1)
                # 设置视频状态，video_statue，0代表没看完，1代表已看完。
                video_statue = 0
                time_start = time.time() #开始计时
                bar_format='当前视频进度:{percentage:.2f}%|{bar}|[{n_fmt}/{total_fmt}{postfix}]'
                with tqdm(total=total_time,leave=False,maxinterval=10,mininterval=2,colour=color,bar_format = bar_format) as _tqdm:
                    update_time = 0
                    while(video_statue == 0):
                        time.sleep(1)
                        # 获取已学习时长，并转换为秒
                        learned_time_text= browser.find_element(By.XPATH,'//*[@id="wrap-box"]/div/div[2]/div/div[1]/div[1]/span[4]').get_attribute('textContent')[-15::].strip()
                        m,s = learned_time_text.split('分钟')
                        if '秒' in s:
                            s = s.split('秒')[0]
                        else:
                            s = 0
                        if '小时' in m:
                            h,m = m.split('小时')
                        else:
                            h = 0
                        learned_time = int(h)*3600+int(m)*60 + int(s)
                        # 更新进度条
                        time_end = time.time()    #结束计时
    
                        update_time = learned_time-update_time
                        seconds = total_time-learned_time
                        m2, s2 = divmod(seconds, 60)
                        remaining_time = "%02d:%02d" % (m2, s2)

                        spend_time = time_end - time_start
                        m3, s3 = divmod(spend_time, 60)
                        spend_time = "%02d:%02d" % (m3, s3)

                        _tqdm.set_postfix(Remaining_time = remaining_time,Spending_time = spend_time)
                        _tqdm.update(update_time)
                        # 获取视频播放进度
                        a = browser.find_element(By.XPATH,'//*[@id="my-player"]/div[4]/div[5]/div').get_attribute('aria-valuenow')
                        # 播放进度满了，学习时长不够，点击继续播放按钮
                        if a == "100.00" and total_time != learned_time:
                            time.sleep(5)
                            try:
                                continue_button = browser.find_elements(By.TAG_NAME,'button')[-1].click()
                            except:
                                continue_button1 = browser.find_elements(By.XPATH,'//*[@id="my-player"]/button')[0].click()
                        # 以学习时长作为判断完成标准
                        if total_time == learned_time:
                            # 更新data
                            file = open('data.txt', 'w')
                            file.seek(0)
                            file.truncate()
                            file.write(str(model)+"/"+str(num+1))
                            file.close()
                            # 更新视频状态
                            video_statue = 1
                            browser.close() # 学习完成，关闭当前页
                            browser.switch_to.window(windows[1]) # 返回选择页面
                        update_time = learned_time
                        time.sleep(1)# 1s检测一次
                _tqdm.close()
                num += 1
                print("已学完第 {} 个视频!\n".format(num))
            else:
                if model == 0:
                    print('必修课已学完！！！\n')
                    model = 1
                    num = 0
                    print("2.开始学习选修课！\n")
                    # 更新data
                    file = open('data.txt', 'w')
                    file.seek(0)
                    file.truncate()
                    file.write(str(model)+"/"+str(num))
                    file.close()
                else:
                    print('选修课已学完！！！\n')
                    browser.quit() # 关闭浏览器
                    input("按回车键结束学习！！！\n")
                    break
    
    
if __name__ =='__main__':
    os.chdir(os.path.dirname(__file__))
    # 更新/安装驱动
    source_dir = os.path.dirname(__file__)
    up = UpdateEdge(source_dir)
    up.update_edge()
    # 设置初始数据
    print("*****蓉城先锋网课自动化*****\n")
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    model = 0
    learned = 0

    # 读取本地缓存数据，/前面的数字表示必修课（0）或者选修课（1），/后面的数字表示当前模式下已完成的视频数量
    if os.path.exists('data.txt'):
        file = open('data.txt', 'r')
        data = file.read().split('/')
        model = int(data[0])
        learned = int(data[1])
        file.close()
    else:
        file = open('data.txt', 'w')
        file.write("0/0")
        file.close()
        print('请保证蓉城先锋可以微信扫描登陆！！！\n')
        print("首次使用将初始化生成data文本文件（请勿随意修改）\n")
        # print('示例：0/1\n/前面的数字：0表示必修课，1表示选修课\n/后面的数字表示当前模式下已完成的视频数\n')
        time.sleep(5)

    # 初始化浏览器,扫码登陆
    browser=browser_initial()
    time.sleep(1)

    # 学习
    browser_learning(browser,model)




