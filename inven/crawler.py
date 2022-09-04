#-*- coding: utf-8 -*-
#2022/9/3 selenium version method 수정

from pickle import NONE
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import os
import re
import json
import sys
import copy


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(r"d:\Chromedriver.exe",options=options)
driver.get('https://uma.inven.co.kr/dataninfo/deckbuilder/')
driver.implicitly_wait(10)
# key = [ 100101,	100101,	100102,	100201,	100301,	100302,	100401,	100402,	100501,	100601,	100701,	100801,	100901,	101001,	101101,	101102,	101201,	101301,	101302,	101401,	101402,	101501,	101601,	101701,	101801,	101802,	102001,	102301,	102401,	102402,	102601,	102701,	103001,	103201,	103501,	103701,	103801,	104001,	104101,	104501,	104601,	105001,	105201,	105601,	105602,	105801,	106001,	106101,]
# //*[@id="deckBuilder"]/section[2]/dl[1]/dd/div/ul/li[1]/img
# deckBuilder > section.container > dl.item-list-type1.umamusume-list > dd > div > ul > li:nth-child(1)
# //*[@id="deckBuilder"]/section[2]/dl[1]/dd/div/ul/li[2]
# //*[@id="deckBuilder"]/section[2]/dl[1]/dd/div/ul/li[32]/span/span


rules = {}
raw_data = {}
data = {
  "Charactor": {
        "☆3": {},
        "☆2": {},
        "☆1": {}
    },
    "Support": {
        "SSR": {},
        "SR": {},
        "R": {}
    }, "Skill": {
        "ノーマル": [],
        "レア": [],
        "固有": [],
        "Buff": []
    }, "Race": {
        "G1": [],
        "G2": [],
        "G3": [],
        "OP": [],
        "Pre-OP": []
    }
}
races = {
    "G1": {},
    "G2": {},
    "G3": {},
    "OP": {},
    "Pre-OP": {}
}

with open(os.path.join(BASE_DIR, 'rules.json'), 'r', encoding='utf-8') as f:
        rules = json.load(f)

def cover(input):
    output = input
    for k in rules["replace"]:
        output = output.replace(k, rules["replace"][k])
    return output           

def toJson(data):
    with open(os.path.join(BASE_DIR, 'chra_event.json'), 'w+', encoding='utf-8') as json_file:
                 json.dump(data, json_file, indent=2, ensure_ascii=False)

# 『랜덤으로 『마장 상태 및 출장 레이스장과 관계있는 스킬』』??
# 이후 내용없는것(op: 공통:)도 패스하면 괜찮을듯?
# range(1,33) 2부터 시작?
# 2022/08/27 33+1 스마트팔콘
def Player():
    for r in range(33,34) :
        #deckBuilder > section.container > dl.item-list-type1.umamusume-list > dd > div > ul > li:nth-child(33) > span > span
        # //*[@id="deckBuilder"]/section[2]/dl[1]/dd/div/ul/li[1]/span/span
        #deckBuilder > section.container > dl.item-list-type1.umamusume-list > dd > div > ul > li:nth-child(6) > span > span
        element = driver.find_element(By.XPATH,'//*[@id="deckBuilder"]/section[2]/dl[1]/dd/div/ul/li['+ str(r) +']')
        driver.execute_script("arguments[0].click();", element)
        driver.get_screenshot_as_file('inven_screen.png')
        #//*[@id="deckBuilder"]/section[2]/dl[2]/dd/div/span
        driver.find_element(By.XPATH,'//*[@id="deckBuilder"]/section[2]')
        driver.get_screenshot_as_file('inven_screen2.png')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser' ,exclude_encodings='utf-8')
        co = soup.select('dl.item-list-type2')
        ti = soup.select('dl.item-list-type2 > dd > div > span')
        driver.find_element(By.XPATH,'//*[@id="deckBuilder"]/section[2]/dl[1]/dd/div/ul')
        
        p_rare = {"3": "☆3", "2": "☆2", "1": "☆1"}
        for n in co:
            code = n.get('data-code')
            if code is None : continue
            else : 
                print(code)
                # raw_data["id"] = code
            charaName = ti[0].text
            f_name = (charaName.find(']')+1)
            name = charaName[0:f_name]
            name = re.sub(r"\s", "", name)
            charaName = charaName[+(f_name+1):]
            charaName = re.sub(r"\s", "", charaName)
            charaName = name +' '+ charaName
            rare = '1'

            # print (name)
            # print (charaName)
            print (charaName)

            c_rare_a = ['26', '27', '28', '29', '30', '31', '32']
            c_rare_b = ['18', '19', '20', '21', '22', '23', '24', '25']
            c_rare_c = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']
            
            
            ra = str(r)
            for c in range(1,3) : 
                if  ra in c_rare_a :
                    rare = '1'
                elif ra in c_rare_b :
                    rare = '2'    
                elif ra in c_rare_c :
                    rare = '3'
                else : break
            

            print(p_rare[rare])
            
            

            #name갯수 35?
            raw_events = {}
            events= range(1,35)
            eventList = list()
            eventJSON = {}  
            for i in events :
                #deckBuilder > section.container > dl.item-list-type2.umamusume.selected > dd > ul > li.expanded > div.name
                # //*[@id="deckBuilder"]/section[2]/dl[2]/dd/ul/li[2]
                #deckBuilder > section.container > dl.item-list-type2.umamusume.selected > dd > ul > li:nth-child(2)
                name = soup.select('li:nth-child('+str(i)+') > div.name')
                name = str(name)[1:-1]
                name = re.sub('<.+?>','', name,0).strip()
                print ('name', name)
                if name == '' :
                    break
                
                p_event = {} 
                opts = list()
                print('eventList', i)
                choiceList = range(2,7) 
                for j in choiceList :
                    print ('opt', i,j)
                    #deckBuilder > section.container > dl.item-list-type2.umamusume.selected > dd > ul > li:nth-child(1) > div:nth-child(2) > div.word
                    opt_name = soup.select('li:nth-child('+str(i)+') > div:nth-child('+str(j)+') > div.word')
                    effects = soup.select('li:nth-child('+str(i)+') > div:nth-child('+str(j)+') > div.reward > div')
                    effect_str = ''
                    
                    opt_name = str(opt_name)[1:-1]
                    opt_name = re.sub('<.+?>','', opt_name,0).strip()
                    opt_name = re.sub('amp;','', opt_name,0).strip()
                    effects = str(effects)[1:-1]
                    effects = re.sub('<.+?>','', effects,0).strip() 
                    if effects.find('『') != -1: 
                        effects = re.sub(', ','\n',effects,0).strip()
                        

                    elif effects.find('힌트') != -1:
                        effect_str = effects.split(',')
                       
                        find_str = '힌트'
                        find_hint = [h for h in range(len(effect_str)) if find_str in effect_str[h]]
                        
                        hint = find_hint[0]
                        c_effect_str = effect_str[hint].split()
                        d_effect_str = ','.join(c_effect_str)
                       
                        s = (d_effect_str.find(find_str)-1)
                        skill= " 『"+d_effect_str[0:s]+"』" 
                        skill = re.sub(',',' ',skill)
                        
                        d_effect_str = d_effect_str.strip(d_effect_str[0:s])
                        d_effect_str = skill+d_effect_str
                        
                        c_effect_str = ','.join(d_effect_str)
                        c_effect_str = re.sub(',','',c_effect_str)
                        c_effect_str = re.sub('힌트','힌트 ',c_effect_str)
                        effect_str[hint] = c_effect_str
                        effects=",".join(effect_str)    
                        effects = re.sub(', ','\n',effects,0).strip()
                    else :
                        effects = re.sub(', ','\n',effects,0).strip()
                    
                    print('opt', len(opts))
                    print (opt_name)
                    effects = cover(effects).rstrip('\n')

                    if opt_name == '' :
                        opts = None
                        break
                    
                    tmp = {}
                    tmp["Option"] = opt_name
                    tmp["Effect"] = effects
                    opts.append(tmp)   
                    if opts != None :
                        p_event[name] = opts
                        raw_events = p_event 
                        print (p_event)
                  
                
                
                if raw_events.keys() == NONE : continue 
                eventList.append(raw_events)
                # print('eventList', len(eventList))
                # print(raw_events[id].keys())
            eventJSON['Event'] = eventList
            data['Charactor'][p_rare[rare]][charaName] = eventJSON

#subname 사라짐? 오페라오 subname ! 확인필요

def Support():
    # child(119) 1,120
    for rs in range(1,120) :
        #deckBuilder > section.container > div > dl.support-card-list > dd > div.scroll-wrap > ul > li:nth-child(1)
        #deckBuilder > section.container > div > dl.support-card-list > dd > div.scroll-wrap > ul > li:nth-child(9)
        #deckBuilder > section.container > div > dl.support-card-list > dd > div.scroll-wrap > ul > li:nth-child(119)
        # //*[@id="deckBuilder"]/section[2]/div/dl[2]/dd/div[2]/ul/li[1]
        driver.find_element(By.XPATH,'//*[@id="deckBuilder"]/section[2]/div/dl[2]/dd/div[2]/ul/li['+ str(rs) +']').click()
        print('r:', rs)
        driver.find_element(By.XPATH,'//*[@id="deckBuilder"]/section[2]')
        driver.get_screenshot_as_file('inven_screen2.png')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser' ,exclude_encodings='utf-8')
        #deckBuilder > section.container > dl.item-list-type2.support-card.selected
        co = soup.select('dl.item-list-type2.support-card.selected')
        #deckBuilder > section.container > dl.item-list-type2.support-card.selected > dd > div > span
        ti = soup.select('dl.item-list-type2.support-card.selected > dd > div > span')
        driver.find_element(By.XPATH,'//*[@id="deckBuilder"]/section[2]/dl[3]/dd/ul')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser' ,exclude_encodings='utf-8')
       
        for ns in co:
            code = ns.get('data-code')
            if code is None : continue
            else : 
                print(code)
                # raw_data["id"] = code
            charaName = ti[0].text
            print(code[0])
            if code[0] == str(1) :
                rare = 'R'
            elif code[0] == str(2) :
                rare = 'SR'
            elif code[0] == str(3) :
                rare = 'SSR'
                
            print('rare: ', rare)
            print(charaName)
            
            #name갯수 35?
            raw_events = {}
            events= range(1,35)
            event = {}
            eventList = list()
            eventJSON = {}  
            bu = '#deckBuilder > section.container > dl.item-list-type2.support-card.selected > dd > ul >'
            for si in events :
                event['id'] = si
                name = soup.select(bu+'li:nth-child('+str(si)+') > div.name')
                name = str(name)[1:-1]
                name = re.sub('<.+?>','', name,0).strip()
                event['name'] = name
                print ('name', name)
                if name == '' :
                    break
                
                s_event = {} 
                opts = list()
                choiceList = range(2,7) 
                for sj in choiceList :
                    opt_name = soup.select(bu+'li:nth-child('+str(si)+') > div:nth-child('+str(sj)+') > div.word')
                    effects = soup.select(bu+'li:nth-child('+str(si)+') > div:nth-child('+str(sj)+') > div.reward > div')
                    print ('opt', si,sj)
                    print ('optname', opt_name)
                    effect_str = ''
                    
                    opt_name = str(opt_name)[1:-1]
                    opt_name = re.sub('<.+?>','', opt_name,0).strip()
                    opt_name = re.sub('amp;','', opt_name,0).strip()
                    effects = str(effects)[1:-1]
                    effects = re.sub('<.+?>','', effects,0).strip() 
                    if effects.find('『') != -1: 
                        effects = re.sub(', ','\n',effects,0).strip()
                        

                    elif effects.find('힌트') != -1:
                        effect_str = effects.split(',')
                       
                        find_str = '힌트'
                        find_hint = [h for h in range(len(effect_str)) if find_str in effect_str[h]]
                        
                        hint = find_hint[0]
                        c_effect_str = effect_str[hint].split()
                        d_effect_str = ','.join(c_effect_str)
                       
                        s = (d_effect_str.find(find_str)-1)
                        skill= " 『"+d_effect_str[0:s]+"』" 
                        skill = re.sub(',',' ',skill)
                        
                        d_effect_str = d_effect_str.strip(d_effect_str[0:s])
                        d_effect_str = skill+d_effect_str
                        
                        c_effect_str = ','.join(d_effect_str)
                        c_effect_str = re.sub(',','',c_effect_str)
                        c_effect_str = re.sub('힌트','힌트 ',c_effect_str)
                        effect_str[hint] = c_effect_str
                        effects=",".join(effect_str)    
                        effects = re.sub(', ','\n',effects,0).strip()
                    else :
                        effects = re.sub(', ','\n',effects,0).strip()
                    
                    print('opt', len(opts))
                    print (opt_name)
                    effects = cover(effects).rstrip('\n')

                
                    if opt_name == '' :
                        opts = None
                        break
                    
                    tmp = {}
                    tmp["Option"] = opt_name
                    tmp["Effect"] = effects
                    opts.append(tmp)
                    print('opts : ',len(opts))
                    if opts != None :
                        s_event[name] = opts
                        raw_events = s_event
                
                if raw_events.keys() == NONE : continue
                eventList.append(raw_events)
                # print(raw_events[id])
                # print(raw_events[id].keys())
                # print(eventList)
                print('eventList : ',len(eventList))
            eventJSON['Event'] = eventList
            data['Support'][rare][charaName] = eventJSON

def Races():
    global raw_data
    global gametora
    with open(os.path.join(BASE_DIR, 'race.json'), 'r', encoding='utf-8') as f:
        gametora = json.load(f)

    

    for race in gametora['raceUra'] :
        id = race['id']
        if (id.isalpha()) == True : continue
        else :
            detail = race['details']
            r_year = {1 :'주니어 ', 2 :'클래식 ', 3:'시니어 '}
            r_month = (str(race['month']) + "월")
            r_half = {1:' 전반', 2:' 후반'}
            r_rank = { 100:'G1', 200:'G2', 300:'G3',400:'OP',700:'Pre-OP'}
            grade = detail['grade']
            rank = r_rank[grade]
            if detail.get('name_ko') is None : continue
            name = detail['name_ko']
            year = race['year']
            half = race['half']
            date = r_year[year] +r_month+ r_half[half]

            item= {}
            item['Name'] = name


        


        print(id.isalpha(), rank, id, name)
        print(date, )

        # rank[grade]

# Player()  
Support()
# Races()   소스 수정필요(전반 후반으로 셀 색상 바뀜)
toJson(data)
driver.close()
