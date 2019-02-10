import boto3
from datetime import datetime
import dateutil.tz
import json
import ast


# ==========================================================

GROUP_LIST = "@@exclusiongroup"
SERVICE_ACCOUNT_NAME = '@@serviceaccount'
#MASK_ACCESS_KEY_LENGTH = ast.literal_eval('@@maskaccesskeylength')
# ==========================================================

# Character length of an IAM Access Key
#ACCESS_KEY_LENGTH = 20
KEY_STATE_ACTIVE = "Active"
KEY_STATE_INACTIVE = "Inactive"

# ==========================================================
#check to see if the MASK_ACCESS_KEY_LENGTH has been misconfigured
#if MASK_ACCESS_KEY_LENGTH > ACCESS_KEY_LENGTH:
#    MASK_ACCESS_KEY_LENGTH = 16

# ==========================================================
def tzutc():
    return dateutil.tz.tzutc()


def key_age(key_created_date):
    tz_info = key_created_date.tzinfo
    age = datetime.now(tz_info) - key_created_date

    print('key age {0}'.format(age))

    key_age_str = str(age)
    if 'days' not in key_age_str:
        return 0

    days = int(key_age_str.split(',')[0].split(' ')[0])

    return days

#def mask_access_key(access_key):
#    return access_key[-(ACCESS_KEY_LENGTH-MASK_ACCESS_KEY_LENGTH):].rjust(len(access_key), "*")

#def lambda_handler(event, context):
    # print('*****************************')
    # print('RotateAccessKey {0}: starting...'format(BUILD_VERSION))
    # print('*****************************'))

# Connect to AWS APIs
client = boto3.client('iam')

users = {}
data = client.list_users()
print(data)

userindex = 0
#print("------------------------------")

for user in data['Users']:
    userid = user['UserId']
    username = user['UserName']
    users[userid] = username

    users_report1 = []
    users_report2 = []


for user in users:
    userindex += 1
    user_keys = []

    print('---------------------')
    print('userindex {0}'.format(userindex))
    print('user {0}'.format(user))
    username = users[user]
    print('username {0}'.format(username))

    # test is a user belongs to a specific list of groups. If they do, do not invalidate the access key
    print("Test if the user belongs to the exclusion group")
    user_groups = client.list_groups_for_user(UserName=username)
    skip = False
    for groupName in user_groups['Groups']:
        if groupName['GroupName'] == GROUP_LIST:
            print('Detected that user belongs to '), GROUP_LIST
            skip = True
            continue

        if skip:
            print("Do invalidate Access Key")
            continue

    # check to see if the current user is a special service account
    if username == SERVICE_ACCOUNT_NAME:
        print('detected special service account {0}, skipping account...'.format(username))
        continue

    access_keys = client.list_access_keys(UserName=username)['AccessKeyMetadata']
    for access_key in access_keys:
        print(access_key)
        access_key_id = access_key['AccessKeyId']

#        masked_access_key_id = mask_access_key(access_key_id)
#        print('AccessKeyId {0}'.format(masked_access_key_id))

        existing_key_status = access_key['Status']
        print(existing_key_status)

        key_created_date = access_key['CreateDate']
    #    print('key_created_date {0}'.format(key_created_date))

        age = key_age(key_created_date)
        print('age {0}'.foramt(age))
