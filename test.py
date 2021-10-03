from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
serial = Serializer('12379=)ç&{([!:?.:ytdexhajwfw')
token = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYzMzI5NjMzNiwiZXhwIjoxNjMzMjk5OTM2fQ.eyJpZCI6Nn0.eby9BMaZqp01frMiTB6alz7tbc3rkLxXA-kmQnmslgy5OEMjvUn7qNQ6ib-G95m2cQa4oeTunK5ur08ALderoQ'
print(token)
print(serial.loads(token))