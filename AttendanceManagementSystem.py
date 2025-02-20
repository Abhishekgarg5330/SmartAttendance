import Encoding

# Generating Encodings for Known Images
uniqueIds, classNames, encodeListKnown = Encoding.generateEncoding()
print('Encoding Completed')

# opening Camera, recognizing face and marking attendance
# first value:-> list of encodings
# second value:-> list of Names parallel to encoding
# third value: -> number of times camera frame will be captured (optional)
# fourth value:-> strictness of face recognition (optional) range-> (0,1)
import RecognitionAndAttendance
RecognitionAndAttendance.RecognitionAndAttendance(uniqueIds, classNames, encodeListKnown, 0, 200, 7, 0.5)
print('Attendance Marked')

import Email

# sending mails to absentees
Email.emailToAbsentees({{email_address}}, 'xkvkydlwnsqixmwm')
print('Email sent to Absentees')

# sending mails to admins
Email.emailToAdmin({{email_address}}, 'xkvkydlwnsqixmwm', '09-04-2023', '09-06-2023')
print('Email Sent to Admins')
#
#
import SMS
# sending SMS to absentees
SMS.smsToAbsentees()
print('sms sent to absentees')






