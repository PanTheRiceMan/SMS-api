#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 14:19:46 2018

@author: oliver
"""

import requests
import datetime
import time
import json

class SMSInterface():
    
    def __init__(self, host="192.168.9.1", headers=None):
        self.host = host
        if not headers:    
            self.headers = {"Referer" : "http://{}/home.htm".format(host)}
        else:
            self.headers = headers
        self.gsm_encode = self.encodeISO88591Hex
    
    @staticmethod
    def dec2hexstr(num):
        return str(hex(num).strip("0x")).upper()
    
    def encodeISO88591Hex(self, message):
        #for whatever reason the webserver takes iso 8859 1 but utf-8 seems to work
#        message = message.encode("utf-8").decode("iso-8859-1")
        ret = ""
        for char in message:
            hexdigest = self.dec2hexstr(ord(char))
            if len(hexdigest) == 1:
                hexdigest = hexdigest + "0"
            while len(hexdigest) < 4:
                hexdigest ="0" +  hexdigest
            ret += hexdigest
        return ret
            
    @staticmethod
    def timems():
        return int(round(time.time()*1000))
    
    @staticmethod
    def smstime():
        return datetime.datetime.now().strftime("%y;%m;%d;%H;%M;%S;+1")

    def status(self):
        url = r"http://{}/goform/goform_get_cmd_process".format(self.host)
        data = {"cmd":"sms_received_flag,sms_remind,ppp_status,msisdn,signalbar,modem_main_state,simcard_roam,pinnumber,puknumber,pin_status,upgrade_result,activate_flag,sim_active_result,sim_imsi,sim_iccid,realtime_tx_thrpt,realtime_rx_thrpt,total_tx_bytes,total_rx_bytes,realtime_time,total_time,system_uptime,network_provider_fullname,network_provider,rmcc,rmnc,network_type,domain_stat",
                "multi_data":"1",
                "sms_received_flag_flag":"0",
                "_":str(self.timems())
                }
        r = requests.get(url, params=data, headers=self.headers)
        return json.loads(r.text)
    
    def send(self, number, message):
        url = "http://{}/goform/goform_set_cmd_process?_={}".format(self.host, self.timems())
        data = {"goformId":"SEND_SMS",
                "Number": str(number),
                "sms_time": self.smstime(),
                "MessageBody" : self.gsm_encode(message),
                "ID":"-1",
                "encode_type":"GSM7_default",
                }
        
        r = requests.post(url, data, headers=self.headers)
        
        return json.loads(r.text)
    
    def send_multiple(self, numbers, message):
        ret = {}
        for number in numbers:
            try:
                rcode = self.send(number, message)
            except:
                print("message could not be sent to {}".format(number))
                rcode = "error"
            ret[number] = rcode
        return ret
                
    def modem_status(self):
        url = "http://{}/goform/goform_get_cmd_process".format(self.host)
        data = {"cmd":"modem_main_state",
                "_":str(self.timems())
                }
        r = requests.get(url, params=data, headers=self.headers)
        return json.loads(r.text)
    
    def get_sms_count(self):
        url = "http://{}/goform/goform_get_cmd_process".format(self.host)
        data = {"cmd" :'sms_capacity_info',
                "_" : str(self.timems())
                }
        r = requests.get(url, params=data, headers=self.headers)
        print(r.text)
        
    def outbox(self):
        return self._get_sms_from(2)
    
    def inbox(self):
        return self._get_sms_from(1)
    
    def dustbin(self):
        return self._get_sms_from(4)
    
    def deleteSMS(self, smsid):
        #not working at the moment
        if type(smsid) == list:
            smsid = ";".join([str(i) for i in smsid])
        url = "http://{}/goform/goform_get_cmd_process?cmd=sms_cmd_status_info&sms_cmd=6".format(self.host)
        data = {"goformId" : "DELETE_SMS",
                "msg_id" : str(smsid) + ";"
                }
        r = requests.post(url, data, headers=self.headers)
        return json.loads(r.text)
    
    def _get_sms_from(self, itype = 2, nPageNum=1, nNumberMessagesPerPage=1000):
        """
        For further documentation see GetSMSMessages from the webinterface.
        """
        if itype in [1,5]:
            tag = 12
        elif itype in [2,6]:
            tag = 2
        elif itype in [3,7]:
            tag = 11
        else:
            tag = 10
        url = "http://{}/goform/goform_get_cmd_process".format(self.host)
        data = {"cmd" : "sms_page_data",
                "page": str(nPageNum - 1),
                "data_per_page" : nNumberMessagesPerPage,
                "mem_store" : "1",
                "tags": str(tag),
                "order_by" : "order by id desc"
                }
        r = requests.get(url, params=data, headers=self.headers)
        return json.loads(r.text)


def load_contacts_db(path="contacts.json"):
    with open(path, "r") as f:
        return json.load(f)

def store_contacts_db(db, path="contacts.json"):
    with open(path, "w") as f:
        json.dump(db, f, indent=4)

if __name__ == "__main__":
    contacts = load_contacts_db()
    numbers = [item[1] for item in contacts]
    sms = SMSInterface()
    ret = sms.send_multiple(numbers, "Hello World, Test vom raspberry PI-Ersatz" )
    print(ret)
