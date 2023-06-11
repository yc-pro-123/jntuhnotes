import json , requests
import datetime ,time
from flask import Flask , request ,Response
app=Flask('__name__')
BOT_TOKEN=os.getenv('BOT_TOKEN')
api=f'https://api.telegram.org/bot{BOT_TOKEN}'
def fetchfile():
    e=open("fileinfo.json","r+")
    v=json.loads(e.read())
    return v
#Functions Used in documt process
def is_admin(chat_id):        
    chat_id=str(chat_id)
    admin_previlage=False
    f=open("superadmin.json","r+")
    e=json.loads(f.read()).keys()
    f.close()
    if chat_id in list(e):
            admin_previlage=True        
    return admin_previlage

def addfile(file_name,file_id):
    e=open("file.json","r+")
    v=json.loads(e.read())
    e.seek(0)
    v.update({file_name:file_id})
    e.write(json.dumps(v))
    e.close()
    print("file added in File.json")
    return True          

def fetchfileid(file_name):
    e=open("file.json","r+")
    v=json.loads(e.read())
    file_id=v.get(file_name)
    return file_id
def remfile(file_name):
    e=open("file.json","r+")
    v=json.loads(e.read())
    e.seek(0)
    v.pop(file_name)

    e.write(json.dumps(v))
    e.close()   
    return True

#--------------'+₹+₹-₹#₹++---------

def action(chat_id):
    method='/sendChatAction'
    repo={'chat_id':chat_id,'action':'typing'}
    r=requests.post(url=api+method,params=repo)
    return r.status_code

def dltmsg(chat_id,msg_id):
    method='/deleteMessage'
    resp={'chat_id':chat_id,'message_id':msg_id}
    r=requests.post(url=api+method,params=resp)
    return r
    
    
def send_mess(resp):
    method='/sendMessage'
    #print(api+method)
    #print('Message Sent...')
    r=requests.post(url=api+method,params=resp)    
    return r
def editmes(chat_id,m,txt):
    method='/editMessageReplyMarkup'
    j={'keyboard':[[{'text':'4-2'},{'text':'4-1'}],    [{'text':'3-2'},{'text':'3-1'}], [{'text':'2-2'},{'text':'2-1'} ]  ],'resize_keyboard':True}
    resp={'chat_id':chat_id,'message_id':m,'text':"Select the Year"}
    #resp={'chat_id':chat_id,'message_id':m,'text':"Select the Year"}
    
    r=requests.post(url=api+method,data=resp)
    
    return r.text
        
def senddoc(chat_id,file_id):
    resp={'chat_id':chat_id,'document':file_id}
    method='/sendDocument'
    r=requests.post(url=api+method,data=resp)
    return r.status_code
    

def stage_2(chat_id):
    print("avccc")
    button=["JNTUH_ADDA","NOTES","SPECTRUM","BACK","MAIN_MENU"]
    
    j={'keyboard':[    [{ 'text':button[0]},{'text':button[1]} ],[button[2]],[{"text":button[3]},{"text":button[4]}]],'resize_keyboard':True}
    resp={'chat_id':chat_id,'text':"Here's the Main Menu",'one_time_keyboard':True,'is_persistent':True,'reply_markup': json.dumps(j)}
    r=send_mess(resp)
    t=json.loads(r.text)
    print(t)
    bmess_id=t["result"]["message_id"]
    return r.text,bmess_id
    
def stage_0(chat_id):
    button=["4-2","4-1","3-2","3-1","2-2","2-1"]
    
    temp={"keyboard":[[{"text":button[0]},{"text":button[1]}],  [{"text":button[2]},{"text":button[3]}], [{"text":button[4]},{"text":button[5]} ]  ],'is_persistent':True,'resize_keyboard':True,"one_time_keyboard":True}
    resp={'chat_id':chat_id,'text':"Select the Year",'reply_markup': json.dumps(temp)}
    r=send_mess(resp)
    
    return r
def stage_1(chat_id,temp):    
    resp={'chat_id':chat_id,'text':"Select the Year",'reply_markup': json.dumps(temp)}
    r=send_mess(resp)
    
    return r    

def send_err(chat_id):
    method='/sendMessage'
    #print(api+method)
    resp={'text':'Process Failed.....','chat_id':chat_id }   
    r=requests.post(url=api+method,params=resp)
    return r.status_code    
def parse_message(message):
   print(message)
   chat_id=message.get("message").get("chat").get("id")
   #txt=message["message"]["text"]
   date=message["message"]["date"]
   nameby=message["message"]["from"]
   msg_id=message["message"]["message_id"]
   
   print('Chat_ID :',chat_id,'\t',datetime.datetime.fromtimestamp(date))
   #print('User Id : '+nameby["username"]+'\t\t'+nameby["first_name"]+'\t'+nameby["last_name"])
   print('Message Id :',msg_id)
   return chat_id ,msg_id

def addstage(chat_id):
    s=open("/storage/emulated/0/Documents/Pronote/stage.json","r+")
    v=json.loads(s.read())
    s.seek(0)
    v.update({chat_id:{ "stage":0 , "s_sem":None,"s_sub":None,"select":None}})
    s.write(json.dumps(v))
    s.close()
    return True
    
def updatestage(chat_id,value,mode):
    s=open("stage.json","r+")
    v=json.loads(s.read())
    #print(v)
    chat_id=str(chat_id)
    if mode == 0:     
        s.seek(0)        
        v[chat_id]["stage"]=value
        json.dump(v,s)
    elif(mode == 1):        
        #v=json.loads(s.read())
        s.seek(0)
        v[chat_id]["s_sem"]=value
        s.write(json.dumps(v))
    elif(mode == 2):
        #v=json.loads(s.read())
        s.seek(0)        
        v[chat_id]["s_sub"]=value
        s.write(json.dumps(v))
    elif(mode == 3):
        #v=json.loads(s.read())
        s.seek(0)
        v[chat_id]["select"]=value
        s.write(json.dumps(v))
    else:
        s.close()
        return False
    s.close()
    print(v)
    return True
        
def fetchstage(chat_id):
    s=open("stage.json","r+")    
    v=json.loads(s.read())
    s.close()
    chat_id=str(chat_id)
    #print(v)
    r=v.get(chat_id)
    #print(r)
#    print("fetching startef")
    return r
def fetchfail():
    resp={'chat_id':"1262319137","text":f"Adding Stage Failedd.... for{chat_id}"}
    send_mess(resp)
def button_(sem):
    semin={'2-1':1,'2-2':2,'3-1':3,'3-2':4}
    semno=semin.get(sem)
    semno=semno-1
    button=[["PTSP","DSD","EDC","NATL","SS","BACK"],["LTNM","EMF","ECA","ADC","LICA","BACK"],["DCN","BEFA","CS","EMI","MPMC","BACK"],["AWP","ESD","VLSI","DSP","BST","BACK"],["SOCA","ESD","VLSI","DSP","BST","BACK"],["AWP","ESD","VLSI","DSP","BST","BACK"]]
    return button[semno]
@app.route('/',methods=["POST","GET"])
def index():
    if request.method == 'POST':
        msg = request.get_json()
       
        try:
            chat_id  ,msg_id = parse_message(msg)
        except:            
            return Response(status=200)
        _3_2_sub=["AWP","ESD","VLSI","DSP","BST"]
        _3_1_sub=["DCN","BEFA","CS","EMI","MPMC"]
        _2_1_sub=["DSD","SS","EDC","NATL","PTSP"]
        _2_2_sub=["ADC","EMF","ECA","LTNM","LICA"]
        _4_1_sub=["DIGITAL IMAGE PROCESSING","PYTHON PROGRAMMING","DBMS"]
        _4_2_sub=["DIGITAL IMAGE PROCESSING","PYTHON PROGRAMMING","DBMS"]
        _stage_2=["JNTUH_ADDA","NOTES","SPECTRUM"]
        
#to find the responae arrived is supported r not        
        is_supported=False
        supported=["photo","document","text"]
        format_list=list(msg["message"].keys())  
        for each in supported:
            if(each in format_list) == True:
                is_supported=True  
                type=each     
        if(is_supported==False):
            resp={'chat_id':chat_id,'text':'Invalid Command or Un-Supported format'}
            send_mess(resp)
            return Response(status=200)
        print("Supported format")
#..........text process
        if(type=='text'):
            text=msg["message"]["text"]
            print(chat_id)
            #print(type(chat_id))
            if text == '/start':
                try:
                    print("msmsm")
                    v=fetchstage(chat_id)
                    print(v)
                    #print(v[chat_id])
                    if(fetchstage(chat_id)== None):                           
                        print("fetchingg...entered")
                        addstage(chat_id)
                        print("New User adding him in Json Stage.....")
                except:
                    resp={'chat_id':"1262319137","text":f"Adding Stage Failedd.... for{chat_id}"}
                    send_mess(resp)
                    return Response(status=200)
                    
                stage_0(chat_id)
                print("Stage Completed")
                return Response(status=200) 
#----------------Code for MAIN_MENU-------------                       
            if text =="MAIN_MENU":
                try:
                    updatestage(chat_id,0,0)
                except:
                    return Response(status=200)
                stage_0(chat_id)    
#---------------Code for Back---------------------                                
            if text == "BACK":
                try:
                    t=fetchstage(chat_id)
                except:
                    fetchfail()
                    return Response(status=200)
                stage= int(t.get("stage"))                
                stage=stage-1
                sem=t.get("s_sem")
                #print("Later in st@ge num :",stage)
                try:
                    updatestage(chat_id,stage,0)
                except:
                    fetchfail()
                    return Response(status=200)
                if stage == 0:
                    stage_0(chat_id)
                if stage==1:
                    button=button_(sem)
                    temp={"keyboard":[  [{"text":button[0]},{"text":button[1]}],  [{"text":button[2]},{"text":button[3]}] ,[{"text":button[4]},{"text":button[5]} ]],'resize_keyboard':True}
                    stage_1(chat_id,temp)
                
#-------1st stage processing............          
                
                
            if ((text=="3-2")or(text=="3-1")or(text=="2-2")or(text=="2-1")):
                try:
                    updatestage(chat_id,1,0)
                except:
                    return Response(status=200)
                updatestage(chat_id,text,1)
                button=button_(text)
                temp={"keyboard":[  [{"text":button[0]},{"text":button[1]}],  [{"text":button[2]},{"text":button[3]}] ,[{"text":button[4]},{"text":button[5]} ]],'resize_keyboard':True}
                stage_1(chat_id,temp)
                   
            if text == "3-1":
                try:
                    updatestage(chat_id,1,0)
                except:
                    return Response(status=200)
                updatestage(chat_id,text,1)
                button=button_(text)
                temp={"keyboard":[  [{"text":button[0]},{"text":button[1]}],  [{"text":button[2]},{"text":button[3]}] ,[{"text":button[4]},{"text":button[5]}]],'resize_keyboard':True}
                stage_1(chat_id,temp)
# ______SEMI FINAL STAGE_______              
            if((text in _3_1_sub)or(text in _3_2_sub)or(text in _2_1_sub)or(text in _2_2_sub)or(text in _4_1_sub)or(text in _4_2_sub)):
                updatestage(chat_id,2,0)
                updatestage(chat_id,text,2)
               
                try:
                    print("stage checkingg startedd")
                    stage_2(chat_id)
                except:
                    return Response(status=200)
                print("dfdrf")
#_________FINAL STAGE__________            
            
            if(text in _stage_2):
                #jntuh_adda , spectrum ,notes
                updatestage(chat_id,text,3)
               
                #sem=3-1....SUB = DCN.........select = SPECTRUM
                if(text == "JNTUH_ADDA")or(text=="SPECTRUM")or(text=="NOTES"):
                    
                    temp=fetchstage(chat_id)
                    sem=temp.get("s_sem")
                    sem=str(sem)
                    choice=temp.get("select")
                    choice=str(choice)
                    sub=temp.get("s_sub")
                    sub=str(sub)
                    file_inf=fetchfile()
                    lt=file_inf.get(sem).get(sub).get(choice)
                    
                    #resp={'chat_id':chat_id,"text":("Available number of files : ", json.loads(type(list)))}
#                    send_mess(resp)
                    if not lt:
                        resp={'chat_id':chat_id,"text":"Sorry ! It seems like there's no files in this section.....\nwe will add them in upcoming days , will be pleased if you help to add files......"}
                        send_mess(resp)
                    for each in lt:                        
                        f_id=fetchfileid(each)
                        senddoc(chat_id,str(f_id))
                
                
                
                
                
                
                
                
                
                
                
                
                
#............document process    
        if(type=='document'):
            if(is_admin(chat_id) == False):
                resp={'chat_id':chat_id,'text':'Sorry ! Invalid Command'}
                send_mess(resp)
                return Response(status=200)
            print("Admin sent a Document")
            file_name=msg.get("message").get("document").get("file_name")
            file_id=msg.get("message").get("document").get("file_id")
            print(file_name,file_id)
            try:
                if(fetchfileid(file_name)==None):
                    k=addfile(file_name,file_id)
                    print(".......File added in File.json.......")
            except:
                send_err(chat_id)
                return Response(status=200)
            tt=f"File added Successfully !\n\nFile Name : <strong><code>{file_name}</code></strong>\n\nFile id : <code>{file_id}</code>"
            
            resp={'chat_id':chat_id,'text':tt,'reply_to_message_id':msg_id,'parse_mode':'HTML'}
            
            print(send_mess(resp))
            print("Sending message.........")
                        
            return Response(status=200)     
            
            
            
            
#.......photo   process        
        if type == 'photo':
            pass
            
        return Response(status=200)
    else:
        return '<h1>HII ..WORKING FOR PROVIDING B.TECH NOTES</h1>'
        
def main():
    
    chat_id='1262319137'
    tt=f"File Name : finame\n\nFileid :`file id`"
    resp={'chat_id':chat_id,'text':tt,'parse_mode':'Markdown'}
    #m=json.loads(send_mess(resp).text)
#    print(m)
#    msg_id=m["result"]["message_id"]
#    print(msg_id)
    #time.sleep(2)
    #print(dltmsg(chat_id,75).text)
    a=["abc","bcd"]
    #print(stage_2(chat_id))
    #addstage("chintu4gggg")
    #updatestage('1468745769',1,0)
    print("bcd" in a)
    #supported=["photo","document","text"]
#    format_list=["ggfg","gjg","hjk"]
#    #format_list=list(msg["message"].keys())
#    for each in supported:
#        if(each in format_list) == True:
#            type=True
#        else:
#            type=False
#    if type==True:
#        print("It is Supported")
#    else:
#        print("Un Supported")

    
    
    



