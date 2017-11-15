import cPickle

def save_session(session):
	with open('session.txt', 'wb') as f:
		cPickle.dump(session.headers, f)
		cPickle.dump(session.cookies,get_dict(), f)
		print '[+] write session into file: session.txt'
		
def load_session():
	with open ('session.txt', 'rb') as f:
		headers = cPickle.load(f)
		cookies = cPickle.load(f)
	return headers, cookies