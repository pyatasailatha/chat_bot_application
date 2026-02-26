import http.client
import json
import urllib.parse

BASE = 'localhost:5000'

def req(method, path, data=None, headers=None):
    conn = http.client.HTTPConnection(BASE, timeout=10)
    body = None
    hdrs = headers or {}
    if data is not None:
        body = json.dumps(data)
        hdrs['Content-Type'] = 'application/json'
    conn.request(method, path, body=body, headers=hdrs)
    resp = conn.getresponse()
    text = resp.read().decode('utf-8')
    try:
        js = json.loads(text)
    except Exception:
        js = text
    return resp.status, js

def main():
    tests = []

    print('1) Health')
    s, j = req('GET', '/health')
    print(s, j)

    print('\n2) Get training data')
    s, j = req('GET', '/get-training-data')
    print(s, type(j))

    print('\n3) Chat - known question')
    s, j = req('POST', '/chat', {'message': 'what is admission process'})
    print(s, j)

    print('\n4) Get-answer for known question')
    s, j = req('POST', '/get-answer', {'question': 'what are the fees'})
    print(s, j)

    print('\n5) Add training data (public endpoint)')
    newq = 'test question xyz'
    s, j = req('POST', '/add-training-data', {'question': newq, 'answer': 'test answer', 'category':'test'})
    print(s, j)

    print('\n6) Chat - unknown phrase to trigger first_five or fallback')
    s, j = req('POST', '/chat', {'message': 'tell me about parking'})
    print(s, j)

    print('\n7) Admin login (use .env defaults)')
    s, j = req('POST', '/admin/login', {'username':'admin','password':'adminpass'})
    print(s, j)
    token = None
    if isinstance(j, dict) and j.get('token'):
        token = j.get('token')

    if token:
        hdr = {'Authorization': 'Bearer ' + token}
        print('\n8) Admin get questions')
        s, j = req('GET', '/admin/questions', headers=hdr)
        print(s, type(j))

        print('\n9) Admin add question')
        s, j = req('POST', '/admin/question', data={'question':'admin created q','answer':'admin created a','category':'admin'}, headers=hdr)
        print(s, j)

        # if add returned id, try update
        if isinstance(j, dict) and j.get('id'):
            qid = j.get('id')
            print('\n10) Admin update question')
            s, j = req('PUT', '/admin/question/' + qid, data={'answer':'updated answer'}, headers=hdr)
            print(s, j)

        print('\n11) Admin logout')
        s, j = req('POST', '/admin/logout', headers=hdr)
        print(s, j)

if __name__ == '__main__':
    main()
