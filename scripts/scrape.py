import os
import httplib2
import time
import random
import re
import pickle
from bs4 import BeautifulSoup
import json



def send_http_request(request_url):
    response,content = httplib2.Http().request(request_url)
    #Return content if successful
    if response['status'] == '200':
        return content
    else:
        return -1

def get_all_dog_links():
    breed_dict = {}
    
    base_url = "http://dogtime.com/dog-breeds"
    
    content = send_http_request(base_url)
    soup = BeautifulSoup(content, "lxml")
    dog_divs = soup.findAll('div',{'class':'group-letter'})
    
    
    for dog_div in dog_divs:
        
        doggies = dog_div.findAll('div',{'class':'group-list-item'})
        
        for doggy in doggies:
        
            anchor = doggy.h2.findAll("a")
            breed_dict[anchor[0].text] = anchor[0]['href']
             
            print "Just extracted breed %s"%anchor[0].text
             
            open('dogs.json','w').write(json.dumps(breed_dict, indent=4))
         
            time.sleep(0.25)
        

parent_child = {}

def pull_dog_info():
    
    dogs = {}
    
    breed_dict = json.loads(open("dogs.json").read())
    
    
    dog_names = breed_dict.keys()
    count = 0
    for doggy in dog_names:
#         print doggy
#         print breed_dict[doggy]
        print "Extracting %s"%doggy
        
        dogs[doggy] = {'url':breed_dict[doggy],'characteristics':{},'vital_stats':{}}
        
        content = send_http_request(breed_dict[doggy])
        soup = BeautifulSoup(content, "lxml")
        dog_boxes = soup.findAll('div',{'class':'inside-box'})
        
        attributes = dog_boxes[0]
        vital_stats = dog_boxes[1]
        
        # Pull all dog info
        all_chars = attributes.findAll('div',{'class':'star-by-breed'})
        
        current_parent = ''
        
        for characteristic in all_chars:
            if 'parent-characteristic' in characteristic['class']:
                title = characteristic.findAll('span',{'class':'characteristic item-trigger-title'})[0].text.strip()           
                stars = characteristic.findAll('span',{'class':'stars-column'})[0].findAll('span')[0]['class'][-1].split("-")[-1]
                
                current_parent = title
                
                dogs[doggy]['characteristics'][title] = {'overall':stars}
        
            if 'child-characteristic' in characteristic['class']:
                title = characteristic.findAll('span',{'class':'characteristic item-trigger-title'})[0].text.strip()           
                stars = characteristic.findAll('span',{'class':'stars-column'})[0].findAll('span')[0]['class'][-1].split("-")[-1]
                
                dogs[doggy]['characteristics'][current_parent][title] = stars           
        
        
        lines = vital_stats.text.strip().split('\n')[1:]
        
        try:
            line = lines[0].strip().split(':')
            attribute = line[0].strip()
            value = line[1].strip()
            
            dogs[doggy]['vital_stats'][attribute] = value
        except:
            pass
        
        try:
            line = lines[1].strip().split(':')
            attribute = line[0].strip()
            value = line[1].strip()
            
            dogs[doggy]['vital_stats'][attribute] = value.split(',')
        except:
            pass
        
        try:
            line = lines[2].strip().split(':')
            attribute = line[0].strip()
            value = line[1].strip().split()
        
            dogs[doggy]['vital_stats'][attribute] = {'min':value[0], 'max':value[2]}
        except:
            pass
        
        try:
            line = lines[3].strip().split(':')
            attribute = line[0].strip()
            value = line[1].strip().split()
            
            dogs[doggy]['vital_stats'][attribute] = {'min':value[0], 'max':value[2]}
        except:
            pass

#         from pprint import pprint 
#         
#         pprint(dogs)
        count+=1
#         time.sleep(0.1)
        
        print "%d remaining..."%(len(breed_dict) - count)
        open('dog_details.json','w').write(json.dumps(dogs, indent=4))

def tocsv():
    dog_details = json.loads(open("dog_details.json").read())
    
    meta = ['Name',
            'URL',
            'Dog Breed Group',
            'Life Span - Min',
            'Life Span - Max',
            "Weight - Min",
            "Weight - Max",
            "Height",
            "Height at Shoulder"          
            ]

    characteristics = [
                       'Health Grooming - overall',
                       'Health Grooming - Amount Of Shedding',
                       'Health Grooming - Easy To Groom',
                       'Health Grooming - Potential For Weight Gain',
                       'Health Grooming - Drooling Potential',
                       'Health Grooming - General Health',
                       'Health Grooming - Size',
                       'Trainability - overall',
                       'Trainability - Wanderlust Potential',
                       'Trainability - Intelligence',
                       'Trainability - Prey Drive',
                       'Trainability - Potential For Mouthiness',
                       'Trainability - Tendency To Bark Or Howl',
                       'Trainability - Easy To Train',
                       'Exercise Needs - overall',
                       'Exercise Needs - Potential For Playfulness',
                       'Exercise Needs - Energy Level',
                       'Exercise Needs - Exercise Needs',
                       'Exercise Needs - Intensity',
                       'Adaptability - overall',
                       'Adaptability - Tolerates Cold Weather',
                       'Adaptability - Good For Novice Owners',
                       'Adaptability - Sensitivity Level',
                       'Adaptability - Tolerates Hot Weather',
                       'Adaptability - Tolerates Being Alone',
                       'Adaptability - Adapts Well to Apartment Living',
                       'All Around Friendliness - overall',
                       'All Around Friendliness - Affectionate with Family',
                       'All Around Friendliness - Friendly Toward Strangers',
                       'All Around Friendliness - Kid Friendly',
                       'All Around Friendliness - Dog Friendly',
                       ]

    headers = meta + characteristics 
    
    out = open("dog_details.csv",'w')
    out.write(",".join(headers)+'\n')
    
    for dog in dog_details:
        line = []
        # add the name
        line.append(dog)
        # add the url
        line.append(dog_details[dog]['url'])
        # Add the vital stats
        if dog_details[dog]['vital_stats'].has_key('Dog Breed Group'):
            line.append(dog_details[dog]['vital_stats']['Dog Breed Group'])
        else:
            line.append("?")
        
        if dog_details[dog]['vital_stats'].has_key('Life Span'):
            line.append(dog_details[dog]['vital_stats']['Life Span']['min'])
            line.append(dog_details[dog]['vital_stats']['Life Span']['max'])
        else:
            line.append("?") 
            line.append("?")      
            
        if dog_details[dog]['vital_stats'].has_key('Weight'):
            if dog_details[dog]['vital_stats']['Weight']['min'] == 'Up':
                line.append("?")
                line.append(dog_details[dog]['vital_stats']['Weight']['max'])

            elif dog_details[dog]['vital_stats']['Weight']['min'] == 'Starts':
                line.append(dog_details[dog]['vital_stats']['Weight']['max']) 
                line.append("?")           
            else:
                line.append(dog_details[dog]['vital_stats']['Weight']['min'])
                line.append(dog_details[dog]['vital_stats']['Weight']['max'])
        else:
            line.append("?") 
            line.append("?")         

        if dog_details[dog]['vital_stats'].has_key('Height'):      
            line.append('/'.join(dog_details[dog]['vital_stats']['Height']))
            line.append(dog_details[dog]['vital_stats']['Height'][-1].strip())
        else:
            line.append("?") 
            line.append("?")  
    
        #load characteristics
        for character in characteristics:
            parent = character.split("-")[0].strip()
            child = character.split("-")[-1].strip()
            if dog_details[dog]['characteristics'][parent].has_key(child):
                line.append(dog_details[dog]['characteristics'][parent][child])
            else:
                line.append("?")
        print line
        out.write(','.join(line)+'\n') 

def pull_images():
    dog_details = json.loads(open("../data/dog_details.json").read()) 
    
    doggies = {}
    
    for dog in dog_details:
        url = dog_details[dog]['url']
        print url 
        
        content = send_http_request(url)
        soup = BeautifulSoup(content, "html.parser")
        dog_image = soup.findAll('div',{'class':'article-content'})[0].find('img')['src']
        
        print dog_image
        
        doggies[dog] = dog_details[dog]
        doggies[dog]['image'] = dog_image
        
        
        
    open('../data/doggies.json','w').write(json.dumps(doggies,indent=4))

# pull_images()



def flatten_details():
    
    shortname = {u'Adapts Well to Apartment Living': 'apt_ok',
             u'Affectionate with Family': 'family_ok',
             u'Amount Of Shedding': 'shed',
             u'Dog Friendly': 'dog_ok',
             u'Drooling Potential': 'drool',
             u'Easy To Groom': 'groom_ease',
             u'Easy To Train': 'train_ease',
             u'Energy Level': 'energy',
             u'Exercise Needs': 'exercise_need',
             u'Friendly Toward Strangers': 'stranger_ok',
             u'General Health': 'health',
             u'Good For Novice Owners': 'novice_ease',
             u'Intelligence': 'intelligence',
             u'Intensity': 'intensity',
             u'Kid Friendly': 'kid_ok',
             u'Potential For Mouthiness': 'mouthy',
             u'Potential For Playfulness': 'playful',
             u'Potential For Weight Gain': 'weight_gain',
             u'Prey Drive': 'prey_drive',
             u'Sensitivity Level': 'sensitive',
             u'Size': 'size',
             u'Tendency To Bark Or Howl': 'bark',
             u'Tolerates Being Alone': 'loneliness_ok',
             u'Tolerates Cold Weather': 'cold_ok',
             u'Tolerates Hot Weather': 'hot_ok',
             u'Wanderlust Potential': 'wander'}
    
    doggies = json.loads(open("../data/doggies.json").read())
    new_doggies = {}
    
    for doggy in doggies:
        new_doggies[doggy] = {}
        new_doggies[doggy]['url'] = doggies[doggy]['url']
        new_doggies[doggy]['image'] = doggies[doggy]['image']
        
        chars = doggies[doggy]["characteristics"]
        
        for charac in chars:
            for subchar in chars[charac]:
                if subchar == 'overall':
                    continue
                new_doggies[doggy][shortname[subchar]] = int(chars[charac][subchar])
    open("../data/dog_features.json",'w').write(json.dumps(new_doggies,indent=4))

# flatten_details()

# dog_details = json.loads(open("../data/dog_details.json").read())
# new_keys = {}
# chars = dog_details[dog_details.keys()[0]]["characteristics"]
# i = 10
# for characs in chars:
#     subchars = chars[characs].keys()
#     for subchar in subchars:
#         if subchar == 'overall':
#             continue
#         new_keys['empty_'+str(i)] = subchar
#         i+=1
#  
# from pprint import pprint
#  
# pprint(new_keys)
    
    


# questions = [
#                 {
#                     'q': 'This is the first question',
#                     'answered':False,
#                     'options':{'1': {
#                                      "text": "option1",
#                                      "image": "image1"
#                                      },
#                                '2': {
#                                      "text": "option2",
#                                      "image": "image2"
#                                      },
#                                }
#              
#                 },
#             ]
#         
import math
def custom_scorer(threshold,given):
    
    deviation = threshold - given
    
    if deviation > 0:
        deviation = math.sqrt(deviation)
    elif deviation < 0:
        deviation = deviation**2
    
    return deviation

print custom_scorer(5, 4)
print custom_scorer(3, 5)
print custom_scorer(3, 1)
print custom_scorer(3, 4)
print custom_scorer(3, 2)
print custom_scorer(2, 5)
print custom_scorer(1, 5)
