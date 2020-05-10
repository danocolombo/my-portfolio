import boto3
import io
import zipfile
import mimetypes


def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic(
        'arn:aws:sns:us-east-1:226036691416:deployForstonGuruTopic')
    topic.publish(Subject="Fortson.Guru - redeployed",
                  Message="The fortson.guru site has been updated with the latest code from Github")
    s3 = boto3.resource('s3')
    portfolio_bucket = s3.Bucket('fortson.guru')
    build_bucket = s3.Bucket('build.fortson.guru')

    portfolio_zip = io.BytesIO()
    build_bucket.download_fileobj(
        '1563f35e-3114-4d95-a138-3402f5288249/buildFortsonGuru.zip', portfolio_zip)

    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            mime_type = mimetypes.guess_type(nm)[0]
            portfolio_bucket.upload_fileobj(
                obj, nm,  ExtraArgs={'ContentType': str(mime_type)})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
    print "Job done!"
    topic.publish(Subject="Fortson.Guru - redeployed",
                  Message="The fortson.guru site has been updated with the latest code from Github")
    return 'Hello from Lamb'
