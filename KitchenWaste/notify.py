import requests

def pushNotify(token,msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
 
    params = {"message": msg}
 
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  #200
    if r.status_code == 200 :
        return True
    return False
def pushNotify_Sticker(token,msg,stickerPackageId,stickerId):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    #https://developers.line.biz/en/docs/messaging-api/sticker-list/
    params = {"message": msg,"stickerPackageId":stickerPackageId,"stickerId":stickerId}
 
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  #200
    if r.status_code == 200 :
        return True
    return False