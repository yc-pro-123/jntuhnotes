import json , requests ,os
import datetime ,time
from flask import Flask , request ,Response
app=Flask('__name__')
BOT_TOKEN=os.getenv("BOT_TOKEN")
api=f'https://api.telegram.org/bot{BOT_TOKEN}'
def fetchfile(sem):
    e=open("fileinfo.json","r")
    v=json.loads(e.read())
    return v.get(sem)
#Functions Used in documt process
def is_admin(chat_id):        
    chat_id=str(chat_id)
    admin_previlage=False
    f=open("superadmin.json","r")
    e=json.loads(f.read()).keys()
    f.close()
    if chat_id in list(e):
            admin_previlage=True        
    return admin_previlage

def addfile(file_name,file_id):
    e=open("file.json","r")
    v=json.loads(e.read())
    e.seek(0)
    v.update({file_name:file_id})
    e.write(json.dumps(v))
    e.close()
    print("file added in File.json")
    return True          

def fetchfileid(file_name):
    e=open("file.json","r")
    v=json.loads(e.read())
    file_id=v.get(file_name)
    #print(json.dumps(v,indent=3))
    return file_id
def remfile(file_name):
    e=open("file.json","r")
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
    print("Document Sent for",chat_id)
    return r.text
    

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


def fetchfail(chat_id):
    
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
            if " " in text:
                Dualstatus=True
                text,text1=text.split(" ",1)
            else:
                Dualstatus=False
            print("Dual Status :",Dualstatus)
            print(chat_id)
            #print(type(chat_id))
            if text == '/start':                
                
                stage_0(chat_id)
                print("Stage Completed")
                return Response(status=200) 
#----------------Code for MAIN_MENU-------------                       
            if text =="MAIN_MENU":               
                stage_0(chat_id)    
#---------------Code for Back---------------------                                
            if text == "BACK":
                stage_0(chat_id)
#-------1st stage processing............          
                
                
            if ((text=="3-2" and Dualstatus==False)or(text=="3-1" and Dualstatus==False)or(text=="2-2" and Dualstatus==False)or(text=="2-1" and Dualstatus==False)):
                button=button_(text)
                temp={"keyboard":[  [{"text":button[0]},{"text":button[1]}],  [{"text":button[2]},{"text":button[3]}] ,[{"text":button[4]},{"text":button[5]} ]],'resize_keyboard':True}
                stage_1(chat_id,temp)
                return Response(status=200)




                                      
            
            if (Dualstatus == False and (text in _2_1_sub))or(Dualstatus == False and (text in _2_2_sub))or(Dualstatus == False and(text in _3_1_sub))or(Dualstatus == False and (text in _3_2_sub))or(Dualstatus == False and (text in _4_1_sub))or(Dualstatus == False and(text in _4_2_sub)):
                #print(text+" SPECTRUM\n" ,text+" JNTUH_NOTES\n",text+" NOTES")
                temp={"keyboard":[  [{"text":text+" SPECTRUM"}],  [{"text":text+" JNTUH_ADDA"}] ,[{"text":text+" NOTES"},{"text":"MAIN_MENU"}]],'resize_keyboard':True}
                stage_1(chat_id,temp)
                return Response(status=200)
             
            if Dualstatus==True:
                
                
                
                if text in _2_1_sub:
                    sem="2-1"
                    sub=text
                elif text in _2_2_sub:
                    sem="2-2"
                    sub=text
                elif text in _3_1_sub:
                    sem="3-1"
                    sub=text
                elif text in _3_2_sub:
                    sem="3-2"
                    sub=text
                elif text in _4_1_sub:
                    sem="4-1"
                    sub=text
                elif text in _4_2_sub:
                    sem="4-2"
                    sub=text
                else:
                    pass
                
                file_inf=fetchfile(sem)
                lt=file_inf.get(sub).get(text1)
                print(lt)   
                    #resp={'chat_id':chat_id,"text":("Available number of files : ", json.loads(type(list)))}
#                    send_mess(resp)
                if not lt:
                    resp={'chat_id':chat_id,"text":"Sorry ! It seems like there's no files in this section.....\nwe will add them in upcoming days , will be pleased if you help to add files......"}
                    send_mess(resp)
                for each in lt:                        
                    f_id=fetchfileid(each)
                    #print(f_id)
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
    f="BQACAgUAAxkBAAICfWSFjAAB2QzhjYN4jKk9Qch20Il5wwAChQkAAqKNKVQT01Fp0fzzvS8E"
    #senddoc(chat_id,f)
    file_inf=fetchfile("3-2")
    lt=file_inf.get("VLSI").get("SPECTRUM")
    
    e=open("/storage/emulated/0/Documents/Pronote/file.json","r+")
    v=json.loads(e.read())
    
    print(json.dumps(v,indent=5))
    print(lt[0])
    file_id=v[str(lt[0])]
    print(file_id)
    '''
    for each in lt:
        f_id=fetchfileid(each)
        print(f_id)
        senddoc(chat_id,str(f_id))'''
