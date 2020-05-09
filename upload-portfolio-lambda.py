import boto3
import io
import zipfile
import mimetypes
s3 = boto3.resource('s3')
portfolio_bucket = s3.Bucket('fortson.guru')
build_bucket = s3.Bucket('build.fortson.guru')

portfolio_zip = io.BytesIO()
build_bucket.download_fileobj('1563f35e-3114-4d95-a138-3402f5288249/buildFortsonGuru.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist(): 
        obj = myzip.open(nm) 
        mime_type = mimetypes.guess_type(nm)[0]  
        portfolio_bucket.upload_fileobj(obj, nm,  ExtraArgs={'ContentType': str(mime_type)})  
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')