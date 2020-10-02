from __future__ import print_function
import pickle
import os.path
import googletrans
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googletrans import Translator
from email.mime.text import MIMEText

translator = Translator()
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']
f = open('lastMsgId.txt')
lastid = f.read()
textWeWhantToTranslate="Don't bother me!!!"

print ('Last message id ='+str(lastid))

def detectAndTrans(msgText):
	message = textWeWhantToTranslate
	result = translator.detect(msgText['snippet'])
	message=translator.translate(message, dest=result.lang)
	return message.text

def lastMsgPos(lastMsgId, results):
	for i in range(1000):
		try:
			if (results['messages'][i]['id'] == lastMsgId):
				print("new messages found="+str(i))
				return i
		except:
			print("exeption// new messages found="+str(i))
			return i 
		print(results['messages'][i])
	print ('to many new letters or last messages was deleted')
	return 100

def create_message(sender, to, subject, message_text):
	try:
		message = MIMEText(message_text)
		message['to'] = to
		message['from'] = sender
		message['subject'] = subject

		return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
	except Exception :
		print	('Message error occurred: %s' % Exception)
		return 0

def send_message(service, user_id, message):

  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    print('letter was sended')
    return message
  except Exception :
    print ('An error occurred: %s' % Exception)
    print('letter was not sended')


def main():

	creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('gmail', 'v1', credentials=creds)
	
    # Call the Gmail API
	
	results = service.users().messages().list(userId='me', 
		labelIds=None, q=None, pageToken=None, maxResults=None, includeSpamTrash=None).execute()
	print(results)
	lastMsg=lastMsgPos(lastid, results)
	nLastId=results['messages'][0]['id']
		
	for i in range(lastMsg):
		msgText= service.users().messages().get(userId='me',
			id=results['messages'][i]['id'], format=None, metadataHeaders=None).execute()
		translated=detectAndTrans(msgText)
		
		if(msgText['payload']['headers'][5]['value']==service.users().getProfile(userId='me').execute()['emailAddress']):
			continue
		else:
			resivedEmail=msgText['payload']['headers'][7]['value'][1:len(msgText['payload']
				['headers'][7]['value'])-1]
		print(resivedEmail)
		message=create_message('me',resivedEmail,"don't bother me", translated)
		print(message)
		send_message(service=service,user_id='me', message=message)
	return nLastId
			
	
	
	
	
if __name__ == '__main__':
   lastid = main()
g = open('lastMsgId.txt', "w")
g.write(lastid)