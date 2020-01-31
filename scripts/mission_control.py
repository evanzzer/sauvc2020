#!/usr/bin/env python
# ini kodingan buat atur kodingan misi mana yang jalan

import rospy
from sauvc2020.msg import Kontrol

statusmisi_pub = None

def misicallback(msg):
    statusSatu = msg.misiSatu_selesai
    statusDua = msg.misiDua_selesai
    statusTiga = msg.misiTiga_selesai
    kontrol = Kontrol()
    if(statusSatu == True and statusDua == False and statusTiga == False):
        kontrol.misiSatu_mulai = False
        kontrol.misiDua_mulai = True
        kontrol.misiTiga_mulai = False
        kontrol.misiEmpat_mulai = False
        statusmisi_pub.publish(kontrol)

    elif(statusSatu == True and statusDua == True and statusTiga == False):
        kontrol.misiSatu_mulai = False
        kontrol.misiDua_mulai = False
        kontrol.misiTiga_mulai = True
        kontrol.misiEmpat_mulai = False
        statusmisi_pub.publish(kontrol)

    elif(statusSatu == True and statusDua == True and statusTiga == True):
        kontrol.misiSatu_mulai = False
        kontrol.misiDua_mulai = False
        kontrol.misiTiga_mulai = False
        kontrol.misiEmpat_mulai = True
        statusmisi_pub.publish(kontrol)
    else:
        kontrol.misiSatu_mulai = True
        kontrol.misiDua_mulai = False
        kontrol.misiTiga_mulai = False
        kontrol.misiEmpat_mulai = False
        statusmisi_pub.publish(kontrol)

if __name__ == "__main__":
    rospy.init_node("mission_control")
    
    statusmisi_pub = rospy.Publisher("statusmisi_mulai", Kontrol, queue_size=10)
    statusmisi_sub = rospy.Subscriber("statusmisi_selesai", Kontrol, misicallback, queue_size=10)

    rospy.spin()