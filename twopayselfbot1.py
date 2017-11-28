# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient() 
client._qrLogin("line://au/q/")
#client._tokenLogin ( " EnBzV4x1B9FhSS5yhKg3.sFKXCRJiHLAd3s1hZlUgeW.QEow6GtkChOtEHLyZs2+aTbcNAWLC7UCWHj3AG+0m2Y=" )

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + "\nSalken..")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

#def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
#    try:
 #       sendMessage(op.param1, #client.getContact(op.param2).displayName + "\n  🔰WELCOME TO MY FAMS🔰\n\n👉 No Baper\n👉 No Rusuh\n👉 No Ngeyel\n👉 No Nakal\n👉 Kita smua saudara ok..!!\n👉 Silahkan baca note")
  #  except Exception as e:
    #    print e
    #    print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
   #     return

#tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

#def NOTIFIED_KICKOUT_FROM_GROUP(op):
 #   try:
   #     sendMessage(op.param1, #client.getContact(op.param3).displayName + "\n\n🔰Selamat Tinggal🔰")
 #   except Exception as e:
 #       print e
  #      print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
  #      return

#tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

#def NOTIFIED_LEAVE_GROUP(op):
 #   try:
#        sendMessage(op.param1, #client.getContact(op.param2).displayName + " \n😱😱😱😱")
#    except Exception as e:
 #       print e
  #      print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
#        return

#tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "[Group Name]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[Group Picture]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nInvitationURL: Permitted\n"
                    else: md += "\n\nInvitationURL: Refusing\n"
                    if group.invitee is None: md += "\nMembers: " + str(len(group.members)) + "人\n\nInviting: 0People"
                    else: md += "\nMembers: " + str(len(group.members)) + "People\nInvited: " + str(len(group.invitee)) + "People"
                    sendMessage(msg.to,md)
                if "gname:" in msg.text:
                    key = msg.text[22:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"Group Name"+key+"Canged to")
                if msg.text == "url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "open":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "already open")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Open")
                if msg.text == "close":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "already close")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL close")
                if "kick" in msg.text:
                    key = msg.text[5:]
                    client.kickoutFromGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"😁😁")
                if "nk: " in msg.text:
                    key = msg.text[3:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if key in Names:
                        kazu = Names.index(key)
                        sendMessage(msg.to, "Bye Sayank..")
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+" Sorry")
                    else:
                        sendMessage(msg.to, "wtf?")
                if msg.text == "cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "No one is inviting.")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Done")
                if "invite" in msg.text:
                    key = msg.text[-33:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"\nMasuk Kaka 😊😊")
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "show:" in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"'s contact")
                if msg.text == "time":
                    sendMessage(msg.to, "Current time is" + datetime.datetime.today().strftime('%Y年%m月%d日 %H:%M:%S') + "is")
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "intip":
                    sendMessage(msg.to, "Cek tukang ngintip")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "ciduk":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "🌟Dibaca oleh🌟 %s\n\n🌟Tukang ngintip🌟\n%s🔥Moga panuan\n🔥Kurapan\n🔥Kudisan\n🔥Aminn.....\n\n🌟Tercatat sejak🌟\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "Ketik dulu Boss...\n「intip」Baru ciduk Dasar pikun...😆😆")
                else:
                    pass
#--------------------------------------------------------------
                if msg.text == "Lari":
                    print "ok"
                    _name = msg.text.replace("Lari","")
                    gs = client.getGroup(msg.to)
                    sendMessage(msg.to,"Kick By TWOPAY BOT\nSory group loe nyampah harus di basmi\nTerimakasih")
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        sendMessage(msg.to,"error")
                    else:
                        for target in targets:
                            try:
                                klist=[client]
                                kicker=random.choice(klist)
                                kicker.kickoutFromGroup(msg.to,[target])
                                print (msg.to,[g.mid])
                            except:
                                sendText(msg.to,"error")        
#--------------------------------------------------------                                                              
#-------------------------------------------------------------			
		if msg.text == "Cek":
                    start = time.time()
                    sendMessage(msg.to, "Cek Anu Boss.........")
                    elapsed_time = time.time() - start
                    sendMessage(msg.to, "%s 🕑 Km/jam" % (elapsed_time))
#-------------------------------------------------------------
                if msg.text == "Sepi":
                    sendMessage(msg.to,"No Baper")
                    sendMessage(msg.to,"No Rusuh")
                    sendMessage(msg.to,"No Ngeyel")
                    sendMessage(msg.to,"No Bulshit")
                    sendMessage(msg.to,"No Byk Alasan")
                    sendMessage(msg.to,"No Nakal")
                    sendMessage(msg.to,"Keep Enjoy")
                    sendMessage(msg.to,"Just Happy")
                    sendMessage(msg.to,"Sekedar Hiburan Jgn Dimasukin Hati")
                    sendMessage(msg.to,"Jaga Kekompakan")
                    sendMessage(msg.to,"Jaga Solideritas Teman")
                    sendMessage(msg.to,"“Menghargai” itu Sifat paling hebat!")
                    sendMessage(msg.to,"Ekpresikanlah Kreatifitasmu")
                    sendMessage(msg.to,"Jadi Org Jujurlah dari sekarang juga, Jujur pada Porsinya")
                    sendMessage(msg.to,"Selesai.............")
                    sendMessage(msg.to,"Created By : Mr 2pay")
                    sendMessage(msg.to,"Don't panix, just relax, it's ok wae ya... wasyik!!!!!!")
                                       
#-------------------------------Jurus Twopay Mulai --------------------------------#
                if msg.text == "Jurus Twopay":
                    sendMessage(msg.to,"Ku mengejar bus yang mulai berjalan")
                    sendMessage(msg.to,"Ku ingin ungkapkan kepada dirimu")
                    sendMessage(msg.to,"Kabut dalam hatiku telah menghilang")
                    sendMessage(msg.to,"Dan hal yang penting bagiku pun terlihat")
                    sendMessage(msg.to,"Walaupun jawaban itu sebenarnya begitu mudah")
                    sendMessage(msg.to,"Tetapi entah mengapa diriku melewatkannya")
                    sendMessage(msg.to,"Untukku menjadi diri sendiri")
                    sendMessage(msg.to,"Ku harus jujur, pada perasaanku")
                    sendMessage(msg.to,"Ku suka dirimu ku suka")
                    sendMessage(msg.to,"Ku berlari sekuat tenaga")
                    sendMessage(msg.to,"Ku suka selalu ku suka")
                    sendMessage(msg.to,"Ku teriak sebisa suaraku")
                    sendMessage(msg.to,"Ku suka dirimu ku suka")
                    sendMessage(msg.to,"Walau susah untukku bernapas")
                    sendMessage(msg.to,"Tak akan ku sembunyikan")
                    sendMessage(msg.to,"Oogoe daiyamondo~")
                    sendMessage(msg.to,"Saat ku sadari sesuatu menghilang")
                    sendMessage(msg.to,"Hati ini pun resah tidak tertahankan")
                    sendMessage(msg.to,"Sekarang juga yang bisa ku lakukan")
                    sendMessage(msg.to,"Merubah perasaan ke dalam kata kata")
                    sendMessage(msg.to,"Mengapa sedari tadi")
                    sendMessage(msg.to,"Aku hanya menatap langit")
                    sendMessage(msg.to,"Mataku berkaca kaca")
                    sendMessage(msg.to,"Berlinang tak bisa berhenti")
                    sendMessage(msg.to,"Di tempat kita tinggal, didunia ini")
                    sendMessage(msg.to,"Dipenuhi cinta, kepada seseorang")
                    sendMessage(msg.to,"Ku yakin ooo ku yakin")
                    sendMessage(msg.to,"Janji tak lepas dirimu lagi")
                    sendMessage(msg.to,"Ku yakin ooo ku yakin")
                    sendMessage(msg.to,"Akhirnya kita bisa bertemu")
                    sendMessage(msg.to,"Ku yakin ooo ku yakin")
                    sendMessage(msg.to,"Ku akan bahagiakan dirimu")
                    sendMessage(msg.to,"Ku ingin kau mendengarkan")
                    sendMessage(msg.to,"Oogoe daiyamondo~")
                    sendMessage(msg.to,"Jika jika kamu ragu")
                    sendMessage(msg.to,"Takkan bisa memulai apapun")
                    sendMessage(msg.to,"Ungkapkan perasaanmu")
                    sendMessage(msg.to,"Jujurlah dari sekarang juga")
                    sendMessage(msg.to,"Jika kau bersuar")
                    sendMessage(msg.to,"Cahaya kan bersinar")
                    sendMessage(msg.to,"Ku suka dirimu ku suka")
                    sendMessage(msg.to,"Ku berlari sekuat tenaga")
                    sendMessage(msg.to,"Ku suka selalu ku suka")
                    sendMessage(msg.to,"Ku teriak sebisa suaraku")
                    sendMessage(msg.to,"Ku suka dirimu ku suka")
                    sendMessage(msg.to,"Sampaikan rasa sayangku ini")
                    sendMessage(msg.to,"Ku suka selalu ku suka")
                    sendMessage(msg.to,"Ku teriakkan ditengah angin")
                    sendMessage(msg.to,"Ku suka dirimu ku suka")
                    sendMessage(msg.to,"Walau susah untuk ku bernapas")
                    sendMessage(msg.to,"Tak akan ku sembunyikan")
                    sendMessage(msg.to,"Oogoe daiyamondo~")
                    sendMessage(msg.to,"Katakan dengan berani")
                    sendMessage(msg.to,"Jika kau diam kan tetap sama")
                    sendMessage(msg.to,"Janganlah kau merasa malu")
                    sendMessage(msg.to,"“Suka” itu kata paling hebat!")
                    sendMessage(msg.to,"“Suka” itu kata paling hebat!")
                    sendMessage(msg.to,"“Suka” itu kata paling hebat!")
                    sendMessage(msg.to,"Ungkapkan perasaanmu")
                    sendMessage(msg.to,"Jujurlah dari sekarang juga..")
                    sendMessage(msg.to,"Anugerah terindah adalah ketika kita masih diberikan waktu untuk berkumpul bersama orang-orang yang kita sayangi.")
                    sendMessage(msg.to,"Cuma dirimu seorang yang bisa meluluhkan hati ini. Kamulah yang terindah dalam hidupku.")
                    sendMessage(msg.to,"Aku ingin meraih kembali cintamu menjadi kenyataan. Saat diriku dalam siksaan cinta, dirimu melenggang pergi tanpa pernah memikirkan aku.")
                    sendMessage(msg.to,"Tak ada yang salah dengan CINTA. Karena ia hanyalah sebuah kata dan kita sendirilah yang memaknainya.")
                    sendMessage(msg.to,"Mencintaimu adalah inginku. memilikimu adalah dambaku. meski jarak jadi pemisah, hati tak akan bisa terpisah.")
                    sendMessage(msg.to,"Dalam cinta ada bahagia, canda, tawa, sedih, kecewa, terluka, semua itu tidak akan terlupakan dalam hal cinta, itu yang artinya cinta.")
                    sendMessage(msg.to,"Seseorang yang berarti, tak akan dengan mudah kamu miliki. Jika kamu sungguh mencintai, jangan pernah berhenti berusaha untuk hati.")
                    sendMessage(msg.to,"Jika esok pagi menjelang, akan aku tantang matahari yang terbangun dari tidur lelap nya.")
                    sendMessage(msg.to,"Ketulusan cinta hanya dapat dirasakan mereka yang benar-benar mempunyai hati tulus dalam cinta.")
                    sendMessage(msg.to,"Kamu tak perlu menjadikan dirimu cantik/ganteng untuk bisa memilikiku, kamu hanya perlu menunjukkan bahwa aku membutuhkanmu.")
                    sendMessage(msg.to,"Ada seribu hal yang bisa membuatku berpikir ununtuk meninggalkanmu, namun ada satu kata yang membuatku tetap disini. Aku Cinta Kamu.")
                    sendMessage(msg.to,"Aku pernah jatuhkan setetes air mata di selat Sunda. Di hari aku bisa menemukannya lagi, itulah waktunya aku berhenti mencintaimu.")
                    sendMessage(msg.to,"Cinta adalah caraku bercerita tentang dirimu, caraku menatap kepergian mu dan caraku tersenyum, saat menatap indah wajahmu.")
                    sendMessage(msg.to,"Datang dan pergi seperti angin tidak beraturan dan arah merasakan cinta dalam kehidupan kadang ku bahagia kadang ku bersedih.")
                    sendMessage(msg.to,"Cinta adalah caraku bercerita tentang dirimu, caraku menatap kepergian mu dan caraku tersenyum, saat menatap indah wajahmu.")
                    sendMessage(msg.to,"Saat jarak memisahkan, satu yang harus kamu ketahui. Akan aku jaga cinta ini ununtukmu.")
                    sendMessage(msg.to,"Bersandarlah di pundaku sampai kau merasakan kenyamanan, karena sudah keharusan bagiku ununtuk memberikanmu rasa nyaman.")
                    sendMessage(msg.to,"Air mata merupakan satu-satunya cara bagimana mata berbicara ketika bibir tidak mampu menjelaskan apa yang membuatmu terluka.")
                    sendMessage(msg.to,"Hidup tidak bisa lebih baik tanpa ada cinta, tapi cinta dengan cara yang salah akan membuat hidupmu lebih buruk.")
                    sendMessage(msg.to,"Mencintaimu hanya butuh waktu beberapa detik, namun untuk melupakanmu butuh waktu seumur hidupku.")
                    sendMessage(msg.to,"Hidup tidak bisa lebih baik tanpa ada cinta, tapi cinta dengan cara yang salah akan membuat hidupmu lebih buruk.")
                    sendMessage(msg.to,"Mencintaimu hanya butuh waktu beberapa detik, namun ununtuk melupakanmu butuh waktu seumur hidupku.")
                    sendMessage(msg.to,"Cinta merupakan keteguhan hati yang ditambatkan pada kemanusiaan yang menghubungkan masa lalu, masa kini dan masa depan.")
                    sendMessage(msg.to,"Ketika mencintai seseorang, cintailah apa adanya. Jangan berharap dia yang sempurna, karena kesempurnaan adalah ketika mencinta tanpa syarat.")
                    sendMessage(msg.to,"Cinta bukanlah tentang berapa lama kamu mengenal seseorang, tapi tentang seseorang yang membuatmu tersenyum sejak kamu mengenalnya.")
                    sendMessage(msg.to,"Ketika mereka bertanya tentang kelemahanku, aku ingin mengatidakan bahwa kelemahanku itul adalah kamu. Aku merindukanmu di mana-mana dan aku sanagat mencintaimu.")
                    sendMessage(msg.to,"Kehadiranmu dalam hidupku, aku tahu bahwa aku bisa menghadapi setiap tantangan yang ada di hadapanku, terima kasih telah menjadi kekuatanku.")
                    sendMessage(msg.to,"Meneriakkan namamu di deras hujan, memandangmu dari kejauhan, dan berdo’a di hening malam. Cinta dalam diam ini lah yang mampu kupertahankan.")
                    sendMessage(msg.to,"Perempuan selalu menjaga hati orang yang dia sayangsehingga hati dia sendiri tersiksa. inilah pengorbanan perempuan ununtuk lelaki yang tidak pernah sadar.")
                    sendMessage(msg.to,"Ketika kau belum bisa mengambil keputusan ununtuk tetap bertahan dengan perasaan itu, sabarlah, cinta yang akan menguatkanmu.")
                    sendMessage(msg.to,"Aku tidak akan pernah menjajikan ununtuk sebuah perasaan, tapi aku bisa menjanjikan ununtuk sebuah kesetiaan.")
                    sendMessage(msg.to,"Cinta yang sebenarnya tidak buta, cinta yaitu adalah hal yang murni, luhur serta diharapkan. Yang buta itu jika cinta itu menguasai dirimu tanpa adanya suatu pertimbangan.")
                    sendMessage(msg.to,"Aku tercipta dalam waktu, ununtuk mengisi waktu, selalu memperbaiki diri di setiap waktu, dan semua waktu ku adalah ununtuk mencintai kamu.")
                    sendMessage(msg.to,"Cinta akan indah jika berpondasikan dengan kasih sang pencipta. Karena sesungguhnya Cinta berasal dari-Nya Dan cinta yang paling utama adalah cinta kepada Yang Kuasa.")
                    sendMessage(msg.to,"Bagi aku, dalam hidup ini, hidup hanya sekali, cinta sekali dan matipun juga sekali. Maka tidak ada yang namanya mendua.")
                    sendMessage(msg.to,"Tuhan..jagalah ia yang jauh disana, lindungi tiap detik hidup yang ia lewati,sayangi dia melebihi engkau menyayangiku.")
                    sendMessage(msg.to,"Kapan kau akan berhenti menyakitiku, lelah ku hadapi semua ini tapi aku tidak bisa memungkiri aku sangat mencintaimu.")
                    sendMessage(msg.to,"Ketidakutan terbesar dalam hidupku bukan kehilanganmu, tapi melihat dirimu kehilangan kebahagiaanmu.")
                    sendMessage(msg.to,"Cinta yang sesungguhnya akan mengatidakan aku butuh kamu karna aku siap ununtuk mencintaimu dan menjalani suka duka bersamamu")
                    sendMessage(msg.to,"Seseorang pacar yang baik adalah dia yang JUJUR dan tidak pernah membuat kamu selalu bertanya-tanya atau selalu mencurigai dia")
                    sendMessage(msg.to,"Cinta bukanlah sebuah kata cinta, yang sebenarnya adalah cinta yang menyentuh hati dan perasaan")
                    sendMessage(msg.to,"Kau datang di saat ke egoisan akan cinta tengah mendera. Membawa cahaya dan kedamaian, membuatku tidak mudah menyerah ununtuk merengkuh kisah cinta bersamamu")
                    sendMessage(msg.to,"Aku sangat menyukai kebersamaan karena kebersamaan mengajarkan kita tentang suka dan duka di lalui bersama")
                    sendMessage(msg.to,"Mungkin Tuhan sengaja memberi kita berjumpa dengan orang yang salah sebelum menemui insan yang betul supaya apabila kita akhirnya menemui insan yang betul, kita akan tahu bagaimana ununtuk bersyukur dengan pemberian dan hikmah di balik pemberian tersebut.")
                    sendMessage(msg.to,"Getaran di hatiku yang lama haus akan belaianmu seperti saat dulu dan kau bisikan kata ‘aku cinta padamu’ aku merindukannya")
                    sendMessage(msg.to,"Terkadang air mata adalah tanda kebahagiaan yang tidak terucapkan. Dan senyuman adalah tanda sakit yang mencoba ununtuk kuat")
                    sendMessage(msg.to,"Dicintai dan disayangi kamu adalah anugerah terindah yang tuhan berikan padaku.")
                    sendMessage(msg.to,"Mencintai kamu butuh waktu beberapa detik, Namun melupakanmu butuh waktu ku seumur hidup.")
                    sendMessage(msg.to,"Datang dan pergi seperti angin tidak beraturan dan arah merasakan cinta dalam kehidupan kadang aku bahagia dan juga kadang aku bersedih.")
                    sendMessage(msg.to,"Air mata merupakan satu-satunya cara bagimana mata berbicara ketika bibir tidak mampu lagi menjelaskan apa yang membuatmu terluka.")
                    sendMessage(msg.to,"Jauh sebelum bertemu denganmu, aku telah mengenalmu dalam doaku.")
                    sendMessage(msg.to,"Mungkin dia tidak sadar bahwa aku itu cemburu dan mungkin juga dia tidak merasa bahwa aku sangat terluka, tidak mendengar bahwa hatiku sedang menangis.")
                    sendMessage(msg.to,"Kehadirmu membawa cinta, memberi bahagia, dan juga rasa rindu yang tiada pernah ada akhirnya.")
                    sendMessage(msg.to,"Aku nngak mau jadi wakil rakyat, aku maunya jadi wali murid yang ngambil raport anak kita besok.")
                    sendMessage(msg.to,"Seperti hujan yang turun di tanah yang tandus, seperti itulah arti hadirmu dengan cinta dan kasih sayang untukku.")
                    sendMessage(msg.to,"Tanda-tanda cinta adalah ketika anda merasa bahwa kebahagiaan orang tersebut lebih penting daripada kebahagiaanmu sendiri.")
                    sendMessage(msg.to,"Cinta tidak hanya apa yang anda rasakan, tetapi apa yang harus anda lakukan.")
                    sendMessage(msg.to,"Cinta adalah sebuah kekuatan untuk melihat kesamaan dan tidak kesamaan.")
                    sendMessage(msg.to,"Cinta adalah pengalaman penuh emosi yang dirasakan banyak orang tetapi hanya beberapa orang saja yang bisa menikmatinya.")
                    sendMessage(msg.to,"Cinta adalah berbagi. Karena walau ada di dua raga yang berbeda, setiap pasangan hanya memiliki satu hati.")
                    sendMessage(msg.to,"Saat kita berjauhan, sebenarnya hanya raga kitalah yang jauh. Namun hati kita selalu dekat, karena hatiku ada di hatimu.")
                    sendMessage(msg.to,"Cinta datang dengan pengorbanan yang akan memberikan petunjuk siapa diri kita yang sebenarnya.")
                    sendMessage(msg.to,"Cinta begitu lembut dan merdu, namun jangan kau gunankan untuk merayu. Karena rayuan hanyalah akan mengosongkan makna kecintaan yang sesungguhnya.")
                    sendMessage(msg.to,"Cinta bukanlah penuntutan, penguasaan, pemaksaan, dan pengintimidasian. Tak lain itu hanyalah cara manusia mendefinisikannya. Karena cinta adalah perjuangan, pengorbanan, tanggungjawab, kejujuran, dan keikhlasan.")
                    sendMessage(msg.to,"Derajat cinta hanya bisa diukur dengan seberapa besar “Pemberian” yang kita korbankan.")
#---------------------------Jurus Twopay finis---------------------------#

  #-------------Fungsi Tag All Start---------------#
            if msg.text in ["Hadir","Anu",".","💃"]:
                  group = client.getGroup(msg.to)
                  nama = [contact.mid for contact in group.members]

                  cb = ""
                  cb2 = ""
                  strt = int(0)
                  akh = int(0)
                  for md in nama:
                      akh = akh + int(6)

                      cb += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(md)+"},"""

                      strt = strt + int(7)
                      akh = akh + 1
                      cb2 += "@nrik \n"

                  cb = (cb[:int(len(cb)-1)])
                  msg.contentType = 0
                  msg.text = cb2
                  msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+cb+']}','EMTVER':'4'}

                  try:
                      client.sendMessage(msg)
                  except Exception as error:
                      print error
    #-------------Fungsi Tag All Finish---------------#
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
