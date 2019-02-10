import boto3

if __name__ == '__main__':
    session = boto3.Session(profile_name='barkay_wolfsohn')
    iam = session.resource('iam')

    for users in iam.users.all():
        print(users)
