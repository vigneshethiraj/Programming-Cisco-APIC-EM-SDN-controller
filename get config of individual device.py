
import requests
import json
import datetime
import re
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
    
    # Define API Call. Get all network devices.    
    api_call = "/network-device"

    # Header information
    headers = {"X-AUTH-TOKEN": token}

    # Combine URL, API call variables
    url += api_call
    response = requests.get(url, headers=headers, verify=False).json()
    idx = 0
    ip_list = []
    for item in response["response"]:
                idx+=1
                ip_list.append([idx,item["hostname"],item["managementIpAddress"]])
    print ("s.no" , "   ", "hostname", "          ", "IP")
    for i in range (0,len(ip_list),1):
        print ((ip_list[i]))
    return response 


def get_deviceconf(token, dev_id):
    '''
    Takes in token and device id as input and output the running configuration 
    of the selected device
    '''
    api_call = "/config"
    headers = {"X-AUTH-TOKEN": token}
    url = "https://sandboxapic.cisco.com/api/v1/network-device/"+dev_id+api_call
    print ("GET request URL:", url)
    response = requests.get(url, headers=headers, verify=False)
    print ("status: " , response)
    response_json = response.json()
    print (response_json["response"].replace("\r\n","\n"))
    return response


auth_token = get_token(apic_em_ip)  #Provide authentication token, APIC-EM's URL address
response= get_networkip(auth_token, apic_em_ip)
device = int(input ('Enter s.no of device to retrieve config: ' ))
dev_id = response['response'][device-1]['id']
get_deviceconf(auth_token, dev_id)