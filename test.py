from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
serial = Serializer('12379=)ç&{([!:?.:ytdexhajwfw', expires_in=20)
token = serial.dumps({'id': 2}).decode('utf-8')
print(token)
print(serial.loads(token))