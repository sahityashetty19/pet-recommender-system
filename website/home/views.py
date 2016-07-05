from django.shortcuts import render, get_object_or_404
# from django.views import generic
from django.http.response import Http404, JsonResponse
import json
import math

# Load the data
doggies = json.loads(open('../data/dog_features.json').read())

def weather_tolerance(dog, answer):
    # The temperature affects the cold and heat tolerance levels of the dog
    penalty = 0
    score = 0
    cold_rescale = {1:5,2:3,3:1,4:1,5:1}
    hot_rescale = {1:1,2:1,3:1,4:3,5:5}
  
    cold_weight = 0 if answer >= 3 else 1
    hot_weight = 0 if answer <= 3 else 1
    if doggies[dog]['cold_ok'] <= cold_rescale[answer]:
        penalty += (cold_weight * (cold_rescale[answer]-doggies[dog]['cold_ok'])**2)
    else:
        score += (cold_weight * math.sqrt(doggies[dog]['cold_ok']-cold_rescale[answer])) 
        
    if doggies[dog]['hot_ok'] <= hot_rescale[answer]:
        penalty += (hot_weight * (hot_rescale[answer]-doggies[dog]['hot_ok'])**2)
    else:
        score += (hot_weight * math.sqrt(doggies[dog]['hot_ok']-hot_rescale[answer]))    
    return score - penalty

def house_size(dog, answer):
    # The house size is strongly linked to the size of the dog, exercise needs and its suitability to apartment living and weakly links to the barking level

    penalty = 0
    score = 0    
    
    # How house size affects the size of the dog
    size_penalty = 0
    size_weight = 0.5
    if doggies[dog].has_key('size') and doggies[dog]['size'] > answer:
        size_penalty = size_weight * (doggies[dog]['size']-answer)
    penalty += size_penalty
    
    
    bark_penalty = 0
    bark_weight = 0.5
    if doggies[dog].has_key('bark') and doggies[dog]['bark'] > answer:
        bark_penalty = bark_weight * (doggies[dog]['bark']-answer)
    penalty += bark_penalty
  

    apt_penalty = 0
    apt_weight = 1
    if doggies[dog].has_key('apt_ok') and (6-doggies[dog]['apt_ok']) > answer:
        apt_penalty = apt_weight * ((6-doggies[dog]['apt_ok'])-answer)
    penalty += apt_penalty

    return score - penalty

def money_influence(dog, answer):
    
    penalty = 0
    score = 0 
    
    groom_weight = 0.5
    if doggies[dog].has_key('groom_ease'):
        if (6-doggies[dog]['groom_ease']) > answer:
            penalty += groom_weight * ((6-doggies[dog]['groom_ease'])-answer)
        else:
            score += groom_weight  * math.sqrt((answer - (6-doggies[dog]['groom_ease'])))
    else:
        penalty+=1
    
    train_weight = 0.5
    if doggies[dog].has_key('train_ease'):
        if (6-doggies[dog]['train_ease']) > answer:
            penalty += train_weight * ((6-doggies[dog]['train_ease'])-answer)
        else:
            score += train_weight  * math.sqrt((answer - (6-doggies[dog]['train_ease'])))    
    else:
        penalty+=1
            
    health_weight = 1
    if doggies[dog].has_key('health'):
        if (6-doggies[dog]['health']) > answer:
            penalty += health_weight * ((6-doggies[dog]['health'])-answer)**2
        else:
            score += health_weight  * (answer - (6-doggies[dog]['health'])) 
    else:
        penalty+=4
            
    mouthy_weight = 0.5
    if doggies[dog].has_key('mouthy'):
        if doggies[dog]['mouthy'] > answer:
            penalty += mouthy_weight * (doggies[dog]['mouthy']-answer)
        else:
            score += mouthy_weight  * math.sqrt((answer - doggies[dog]['mouthy']))
    else:
        penalty+=1
            
    return score - penalty

def time_influence(dog, answer):
    
    penalty = 0
    score = 0 
    
    lone_weight = 1
    if doggies[dog].has_key('loneliness_ok'):
        if (6-doggies[dog]['loneliness_ok']) > answer:
            penalty += lone_weight * ((6-doggies[dog]['loneliness_ok'])-answer)**2
    else:
        penalty+=4
    
    train_weight = 0.25
    if doggies[dog].has_key('train_ease'):
        if (6-doggies[dog]['train_ease']) > answer:
            penalty += train_weight * ((6-doggies[dog]['train_ease'])-answer)
        else:
            score += train_weight  * math.sqrt((answer - (6-doggies[dog]['train_ease'])))    
    else:
        penalty+=0.5
            
            
    exercise_weight = 0.75
    if doggies[dog].has_key('exercise_need'):
        if doggies[dog]['exercise_need'] > answer:
            penalty += exercise_weight * (doggies[dog]['exercise_need']-answer)
        else:
            score += exercise_weight  * math.sqrt((answer - doggies[dog]['exercise_need']))
    else:
        penalty+=1.5
            
    return score - penalty

def outdoor(dog, answer):
    
    penalty = 0
    score = 0 
    
    intelligence_weight = 1
    energy_weight = 1
    intensity_weight = 1
    exercise_weight = 1
    playful_weight = 1
    wander_weight = 1
    prey_weight = 1
    size_weight = 1
    
    if answer == 1:
        if doggies[dog].has_key('intelligence'):
            score+=intelligence_weight*(doggies[dog]['intelligence'])

    if answer == 2:
        if doggies[dog].has_key('energy'):
            score+=energy_weight*(doggies[dog]['energy'])
        if doggies[dog].has_key('intensity'):
            score+=intensity_weight*(doggies[dog]['intensity'])
        if doggies[dog].has_key('exercise_need'):
            score+=exercise_weight*(doggies[dog]['exercise_need'])

    if answer == 3:
        if doggies[dog].has_key('intelligence'):
            score+=intelligence_weight*(doggies[dog]['intelligence'])
        if doggies[dog].has_key('energy'):
            score+=energy_weight*(doggies[dog]['energy'])
        if doggies[dog].has_key('intensity'):
            score+=intensity_weight*(doggies[dog]['intensity'])
        if doggies[dog].has_key('exercise_need'):
            score+=exercise_weight*(doggies[dog]['exercise_need'])
        if doggies[dog].has_key('playful'):
            score+=playful_weight*(doggies[dog]['playful'])
        
    if answer == 4:
        if doggies[dog].has_key('intelligence'):
            score+=intelligence_weight*(doggies[dog]['intelligence'])
        if doggies[dog].has_key('energy'):
            score+=energy_weight*(doggies[dog]['energy'])
        if doggies[dog].has_key('exercise_need'):
            score+=exercise_weight*(doggies[dog]['exercise_need'])
        if doggies[dog].has_key('wander'):
            score+=wander_weight*(doggies[dog]['wander'])
        
    if answer == 5:
        if doggies[dog].has_key('intelligence'):
            score+=intelligence_weight*(doggies[dog]['intelligence'])
        if doggies[dog].has_key('energy'):
            score+=energy_weight*(doggies[dog]['energy'])
        if doggies[dog].has_key('exercise_need'):
            score+=exercise_weight*(doggies[dog]['exercise_need'])
        if doggies[dog].has_key('wander'):
            score+=wander_weight*(doggies[dog]['wander'])
        if doggies[dog].has_key('prey_drive'):
            score+=prey_weight*(doggies[dog]['prey_drive'])
        if doggies[dog].has_key('size'):
            score+=size_weight*(doggies[dog]['size'])
                
    return score - penalty

def neatfreak(dog, answer):
    
    penalty = 0
    score = 0 
    
    answer = 6-answer
    
    shed_weight = 1
    if doggies[dog].has_key('shed'):
        if doggies[dog]['shed'] > answer:
            penalty += shed_weight * (doggies[dog]['shed']-answer)
    else:
        penalty+=2

    drool_weight = 1
    if doggies[dog].has_key('drool'):
        if doggies[dog]['drool'] > answer:
            penalty += drool_weight * (doggies[dog]['drool']-answer)
    else:
        penalty+=2
            
    return score - penalty

def novice(dog, answer):

    penalty = 0
    score = 0 

    novice_weight = 1
    if answer == 1:
        if doggies[dog].has_key('novice_ease'):
                score+=novice_weight*(doggies[dog]['novice_ease']) 
        
    return score - penalty

def family(dog, answer):

    penalty = 0
    score = 0 

    kids_weight = 1
    if answer == 1:
        if doggies[dog].has_key('kid_ok'):
            score+=kids_weight*(doggies[dog]['kid_ok']) 

    family_weight = 1
    if answer == 1:
        if doggies[dog].has_key('family_ok'):
            score+=family_weight*(doggies[dog]['family_ok'])
      
    return score - penalty


questions = {
                "1":{
                    'id':1,
                    'question': 'What is the weather like where you live?',
                    'name': 'location',
                    'answer': False,
                    'options': [
                                {
                                    'text':'Freezing',
                                    'image':'http://static.businessinsider.com/image/52a8d0636bb3f72e2ea6b86d/image.jpg',
                                    'id':1
                                    },
                                {
                                    'text':'Cold',
                                    'image':'http://images.travelpod.com/tripwow/photos2/ta-03e2-c58a-03ad/wayanad-pass-road-in-december-with-cool-weather-5-wayanad-india+1152_13259913968-tpfil02aw-1500.jpg',
                                    'id':2
                                },
                                {
                                    'text':'Pleasant',
                                    'image':'http://www.boehmerwaldurlaub.com/web-content/Bilder/Willkommen%20allen%20Fruehlingsgaesten%20im%20Haus%20Sonne.jpg',
                                    'id':3
                                },                                
                                {
                                    'text':'Hot',
                                    'image':'http://images.techtimes.com/data/images/full/20426/extremely-hot-weather.jpg?w=600',
                                    'id':4
                                },
                                {
                                    'text':'Hell on Earth',
                                    'image':'http://previews.123rf.com/images/tomwang/tomwang1207/tomwang120700012/14349772-drought-land-and-hot-weather--Stock-Photo-desert.jpg',
                                    'id':5
                                    },                                                                
                                ],
                    'influence': weather_tolerance 
                    },
                "2":{
                    'id':2,
                    'question': 'How big is your house?',
                    'name': 'house',
                    'answer': False,
                    'options': [
                                {
                                    'text':'Tiny',
                                    'image':'http://i.telegraph.co.uk/multimedia/archive/02930/move01_2930119b.jpg',
                                    'id':1
                                    },
                                {
                                    'text':'Small',
                                    'image':'http://www.ramascreen.com/wp-content/uploads/2015/08/Edith-Macefield-e1440478393316.jpg',
                                    'id':2
                                },
                                {
                                    'text':'Standard',
                                    'image':'http://www.energysmartohio.com/uploads/content/typical%20cape%20cod%20home%20with%20knee%20wall%20attics-resized-600_1.jpg',
                                    'id':3
                                },                                
                                {
                                    'text':'Big',
                                    'image':'http://p-fst2.pixstatic.com/5086018ad9127e2f16000023._w.1500_s.fit_.jpg',
                                    'id':4
                                },
                                {
                                    'text':'Huge',
                                    'image':'http://i.dailymail.co.uk/i/pix/2012/12/28/article-2254258-16AC0E88000005DC-666_964x594.jpg',
                                    'id':5
                                    },                                                                
                                ],
                    'influence': house_size
                    },
                "3":{
                    'id':3,
                    'question': 'How much will you spend on a dog?',
                    'answer': False,
                    'name': 'money',
                    'options': [
                                {
                                    'text':'Little',
                                    'image':'https://learnmoreeveryday.files.wordpress.com/2013/05/some-pennies.jpg',
                                    'id':1
                                    },
                                {
                                    'text':'Some',
                                    'image':'http://sweetberries.com/wp-content/uploads/2013/07/dollar-bills.jpg?c90e1cg',
                                    'id':2
                                },
                                {
                                    'text':'Sufficient',
                                    'image':'http://virginiabeachonlinereport.com/wp-content/uploads/2014/08/us-money-bills.jpg',
                                    'id':3
                                },                                
                                {
                                    'text':'Lot',
                                    'image':'http://cdn.zmescience.com/wp-content/uploads/2015/08/money-7.jpg',
                                    'id':4
                                },
                                {
                                    'text':"Excessive",
                                    'image':'http://s3.amazonaws.com/churchplantmedia-cms/christ_covenant_knoxville/money.jpg',
                                    'id':5
                                    },                                                                
                                ],
                    'influence': money_influence
                    },
                "4":{
                    'id':4,
                    'question': 'How much time can you give a dog?',
                    'answer': False,
                    'name': 'time',
                    'options': [
                                {
                                    'text':'Little',
                                    'image':'http://thumbs.dreamstime.com/x/retro-alarm-clock-showing-one-hour-14192333.jpg',
                                    'id':1
                                    },
                                {
                                    'text':'Some',
                                    'image':'http://blog.art21.org/wp-content/uploads/2011/01/perfectloverse-e1296521830280.jpg',
                                    'id':2
                                },
                                {
                                    'text':'Sufficient',
                                    'image':'http://www.farrowdesign.com/galleries/scp-clocks/final_web_AllClocks.jpg',
                                    'id':3
                                },                                
                                {
                                    'text':'Lot',
                                    'image':'http://static1.squarespace.com/static/5193ac7de4b0f3c8853ae813/t/52d9284ce4b01b5207ed9c3e/1389963364365/many_clocks.gif',
                                    'id':4
                                },
                                {
                                    'text':"Excessive",
                                    'image':'http://previews.123rf.com/images/iqoncept/iqoncept1407/iqoncept140700080/30166479-Many-clocks-ticking-and-counting-down-the-seconds-minutes-and-hours-as-time-marches-on-and-moves-for-Stock-Photo.jpg',
                                    'id':5
                                    },                                                                
                                ],
                    'influence': time_influence
                    },
                "5":{
                    'id':5,
                    'question': 'What best describes you?',
                    'answer': False,
                    'name': 'time',
                    'options': [
                                {
                                    'text':'Nerd',
                                    'image':'http://cdn.playbuzz.com/cdn/1564c2b2-b839-4e8f-a69f-c9f6b0d7385c/4d6c33cb-eee1-44b1-84e3-10b163f04125.jpg',
                                    'id':1
                                    },
                                {
                                    'text':'Active',
                                    'image':'http://wac.450f.edgecastcdn.net/80450F/nj1015.com/files/2012/09/woman-jogger-630x504.jpg',
                                    'id':2
                                },
                                {
                                    'text':'Sporty',
                                    'image':'http://www.texastravesty.com/sites/default/files/field/image/frisbee-300x214.jpg',
                                    'id':3
                                },                                
                                {
                                    'text':'Thrill seeker',
                                    'image':'http://images.nationalgeographic.com/wpf/media-live/photos/000/753/cache/cliff-climber-oman-chin_75336_990x742.jpg',
                                    'id':4
                                },
                                {
                                    'text':"Hunter",
                                    'image':'http://www.rifleshootermag.com/files/2012/07/savage-bear-hunter-1.jpg',
                                    'id':5
                                    },                                                                
                                ],
                    'influence': outdoor
                    }, 

                "6":{
                    'id':6,
                    'question': 'How clean are you?',
                    'answer': False,
                    'name': 'time',
                    'options': [
                                {
                                    'text':"What's a shower?",
                                    'image':'http://cdn.playbuzz.com/cdn/1564c2b2-b839-4e8f-a69f-c9f6b0d7385c/4d6c33cb-eee1-44b1-84e3-10b163f04125.jpg',
                                    'id':1
                                    },
                                {
                                    'text':'I bathe occasionally',
                                    'image':'http://wac.450f.edgecastcdn.net/80450F/nj1015.com/files/2012/09/woman-jogger-630x504.jpg',
                                    'id':2
                                },
                                {
                                    'text':"I'm mostly clean",
                                    'image':'http://www.texastravesty.com/sites/default/files/field/image/frisbee-300x214.jpg',
                                    'id':3
                                },                                
                                {
                                    'text':'I shower twice a day!',
                                    'image':'http://images.nationalgeographic.com/wpf/media-live/photos/000/753/cache/cliff-climber-oman-chin_75336_990x742.jpg',
                                    'id':4
                                },
                                {
                                    'text':"I clean the vacuum cleaner",
                                    'image':'http://www.rifleshootermag.com/files/2012/07/savage-bear-hunter-1.jpg',
                                    'id':5
                                    },                                                                
                                ],
                    'influence': neatfreak,
                    },         
                "7":{
                    'id':7,
                    'question': 'Had a dog before?',
                    'answer': False,
                    'name': 'time',
                    'options': [
                                {
                                    'text':"Yes",
                                    'image':'https://upload.wikimedia.org/wikipedia/commons/8/87/Symbol_thumbs_up.svg',
                                    'id':1
                                    },
                                {
                                    'text':'No',
                                    'image':'https://openclipart.org/image/2400px/svg_to_png/192849/thumbs-down-left.png',
                                    'id':2
                                },                                                                
                                ],
                    'influence': novice,
                    },  
                "8":{
                    'id':8,
                    'question': 'Family?',
                    'answer': False,
                    'name': 'time',
                    'options': [
                                {
                                    'text':"Yes",
                                    'image':'https://upload.wikimedia.org/wikipedia/commons/8/87/Symbol_thumbs_up.svg',
                                    'id':1
                                    },
                                {
                                    'text':'No',
                                    'image':'https://openclipart.org/image/2400px/svg_to_png/192849/thumbs-down-left.png',
                                    'id':2
                                },                                                                
                                ],
                    'influence': family,
                    },   
             }


def get_closest_dogs():
    doggie_scores = {}
    
#     for dog in doggies:
    for dog in doggies:
        # initialize
        doggie_scores[dog] = 0
        
        sorted_questions = sorted(questions.keys())

        # Update for each question
        for question_num in sorted_questions:
            question = questions[question_num]

            # update if question is answered
            if question['answer']:
                answer = question['answer']
                score = question['influence'](dog, answer)

                doggie_scores[dog] += score  
    
    top12 = sorted(doggie_scores, key=doggie_scores.get, reverse=True)[:12]
    top_dogs = []
    for dog in top12:
        top_dogs.append({'url': doggies[dog]['url'], 'name': dog, 'image': doggies[dog]['image'], 'score': round(doggie_scores[dog],2)})

    bottom12 = sorted(doggie_scores, key=doggie_scores.get)[:12]
    bottom_dogs = []
    for dog in bottom12:
        bottom_dogs.append({'url': doggies[dog]['url'], 'name': dog, 'image': doggies[dog]['image'], 'score': round(doggie_scores[dog],2)})
    
    print doggie_scores["Sussex Spaniel"]
    
    return top_dogs, bottom_dogs   
                

def home(request):
    
    global questions
    
    if request.method == "GET" and request.is_ajax():
        answer = int(request.GET['selected'])
        question_id = str(request.GET['question_id'])
        questions[question_id]['answer'] = answer       
        top_dogs, bottom_dogs = get_closest_dogs()
        
        next_question = {}

        sorted_questions = sorted(questions.keys())
        for question_num in sorted_questions:
            if not questions[question_num]['answer']:
                next_question['question'] = questions[question_num]['question']
                next_question['id'] = questions[question_num]['id']
                next_question['options'] = questions[question_num]['options']
                break
        my_response = {
                    'question': next_question,
                    'recos': top_dogs,
                    'skip': bottom_dogs
                    }

        return JsonResponse(my_response)
        
    # Reset all questions to false
    for question_num in questions:
        questions[question_num]['answer'] = False
    
    default_question = questions["1"]
    default_top_dogs, default_bottom_dogs = get_closest_dogs()
    
    return render(request, template_name='home/index.html',context={'default_question': default_question, 'default_top_dogs': default_top_dogs,  'default_bottom_dogs': default_bottom_dogs })