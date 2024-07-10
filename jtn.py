from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from configparser import ConfigParser
from email.mime.text import MIMEText
from selenium import webdriver
import smtplib
import time

# ==================== ==================== ==================== ====================
# Function Send E-Mail 
def send_email(sender, receiver, subject, content):
    
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    config = ConfigParser()
    config.read('./conf.ini')
    email = config['gmail']['email']
    pswrd = config['gmail']['pswrd']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, pswrd)

    server.sendmail(sender, receiver, msg.as_string())
    server.quit()



# ==================== ==================== ==================== ====================
# Get Event ID Array From Text File
txtArr = []
with open('./jtn.txt', 'rt') as f:
    for line in f:
        txtArr.append(line.strip('\n'))


# ==================== ==================== ==================== ====================
# Protecting Close Browser
chrome_options = Options()
chrome_options.add_argument("headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"


# Creaete Chrome Driver
driver = webdriver.Chrome(options=chrome_options)
driver.get(url='https://www.jtnevent.com/event/vindex.php')



# Explicitly Wait DOM Loaded
wait = WebDriverWait(driver, 5)
evt_proceed = wait.until(EC.visibility_of_element_located((By.ID, 'evt_proceed')))
liArr = evt_proceed.find_elements(By.TAG_NAME, 'li')
now = "[" + time.strftime('%Y-%m-%d %H:%M:%S') + "]"


# Loop List
newArr = []
isUpdt = False
for li in liArr:
    href = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
    text = li.find_element(By.CLASS_NAME, 'tit').text
    contnet_id = href.split('=')[1]
    newArr.append(contnet_id + "\n")

    # Send E-Mail New Content
    if contnet_id not in txtArr:
        isUpdt = True
        print('[Log]' + now + ' Uploded New Content')
        send_email('gks83123@gmail.com', 'gks831@kakao.com', '[JTN][신규이벤트]', text)

    # Write New File
    with open('./jtn.txt', 'w') as f:
        f.writelines(newArr)


if isUpdt == False:
    print('[Log]' + now + ' Nothing Changed Contents')


# End
driver.quit()