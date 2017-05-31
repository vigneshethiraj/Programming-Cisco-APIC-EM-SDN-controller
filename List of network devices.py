#import modules
import requests
import json
import datetime
import re
#Disable warnings
requests.packages.urllib3.disable_warnings()

# enter your APIC-EM SDN controller URL or IP below
apic_em_ip = "https://sandboxapic.cisco.com/api/v1"

def get_token(url):
    '''
    This function is used to get the authentication token for APIC-EM SDN controller
    '''

    #Define API Call
    api_call ="/ticket"

    #Payload contains authentication information
    payload = { "username": "devnetuser", "password": "Cisco123!" }

    #Header information
    headers = {"content-type" : "application/json"}

    #Combine URL, API call and parameters variables
    url +=api_call

    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False).json()

    # Return authentication token from respond body
    return response["response"]["serviceTicket"]



def get_networkip(token, url):

    '''
    this fuction returns the list of network devices connected to the SDN controller
    and also provides its IP
    '''
    
    # Define API Call. Get configuration for all network devices.    
    api_call = "/network-device"

    # Header information
    headers = {"X-AUTH-TOKEN": token}

#    # Combine URL, API call variables
    url += api_call
#
    response = requests.get(url, headers=headers, verify=False).json()
    idx = 0
    ip_list = []
    for item in response["response"]:
                idx+=1
                ip_list.append([idx,item["hostname"],item["managementIpAddress"]])
    api_call = "/host"
##
#    # Header information
    headers = {"X-AUTH-TOKEN": token}

  # Combine URL, API call variables
    url = "https://sandboxapic.cisco.com/api/v1/host"

    responses = requests.get(url, headers=headers, verify=False).json()
    print ("s.no" , "   ", "hostname", "          ", "IP")
    for item in responses["response"]:
                idx+=1
                ip_list.append([idx,item["hostIp"],item["hostType"]])
    for i in range (0,len(ip_list),1):
        print ((ip_list[i]))

    
    return ip_list 
#Assign obtained authentication token to a variable. Provide APIC-EM's URL address
auth_token = get_token(apic_em_ip)

#Provide authentication token, APIC-EM's URL address
get_networkip(auth_token, apic_em_ip)