from django.shortcuts import render
# from django.http import HttpResponse
from django.http import JsonResponse
import os
import glob
import boto3
import smtplib
def flvtomp4(req):
    os.system('aws s3 sync s3://new-image-profile /home/rohtash/flv --exclude "*" --include "*.flv"')
    for name in glob.glob('/home/rohtash/flv/*'):
        print(name)
        os.system('ffmpeg -i '+name+' -f mp4 -vcodec mpeg4 -acodec libmp3lame /home/rohtash/mp4/'+name+'.mp4')
        s3 = boto3.client('s3')
        s3.upload_file(
        '/home/rohtash/mp4/'+name+'.mp4', 'new-image-profile', name+'.mp4',
        ExtraArgs={'ACL': 'public-read'}
        )
        os.system('rm /home/rohtash/mp4/'+name+'.mp4')
        os.system('rm /home/rohtash/flv/'+name+'.mp4')
        message = "submite"
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("rraghav476@gmail.com","password")
        s.sendmail("rraghav476@gmail.com","rraghav476@gmail.com",message)
        s.quit()
        print("msg send")
    return JsonResponse({"msg":"success","data":"convert to mp4"})