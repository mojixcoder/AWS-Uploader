import os
import logging

import boto3
from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO)


def get_s3_resource(*, endpoint_url, aws_access_key_id, aws_secret_access_key):
    try:
        s3_resource = boto3.resource(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        return s3_resource
    except Exception as e:
        logging.info(e)
        

def get_base_name(path):
    try:
        base_name = os.path.basename(os.path.normpath(path))
        return base_name
    except Exception as e: 
        logging.error(e)
        

def get_directory(path):
    return os.path.dirname(path)


def create_directory(root, path):
    directory = f"{root}/{path}"
    os.makedirs(directory, exist_ok=True)
    return directory


def get_download_destination(*, key, download_path):
    if get_directory(key):
        destination = f"{download_path}/{get_directory(key)}/{get_base_name(key)}"
    else:
        destination = f"{download_path}/{get_base_name(key)}"
    return destination


def upload(*, bucket_name, s3_resource, directory, ACL):
    try:
        bucket = s3_resource.Bucket(bucket_name)
        base_name = get_base_name(directory)
        count = 0
        print()
        print(f"Uploading files to {bucket_name}...")
        print()
        for dirname, dirs, files in os.walk(directory):
            for filename in files:
                dirname = dirname if dirname.endswith("/") else dirname + "/"
                object_name = dirname.split(base_name)[-1][1:]
                file_path = dirname + filename
                object_name = object_name + filename
                with open(file_path, "rb") as file:
                    bucket.put_object(
                        ACL=ACL,
                        Body=file,
                        Key=object_name
                    )
                print(f"Uploaded '{object_name}'")
                count += 1
        print()
        print(f"{count} files uploaded.")
    except ClientError as e:
        logging.error(e)
        
        
def object_list(*, s3_resource, bucket_name):
    try:
        bucket = s3_resource.Bucket(bucket_name)
        return bucket.objects.all()
    except ClientError as e:
        logging.error(e)
        

def delete_many(object_list):
    print()
    print("Deleting files...")
    print()
    count = 0
    for object_ in object_list:
        key = object_.key
        object_.delete()
        print(f"Deleted '{key}'")
        count += 1
    print()
    print(f"{count} files deleted.")
    

def download_all(*, s3_resource, bucket_name, download_path):
    print()
    print("Downloading files...")
    print()
    
    bucket = s3_resource.Bucket(bucket_name)
    objects = object_list(s3_resource=s3_resource, bucket_name=bucket_name)
    
    count = 0
    for obj in objects:
        try:
            destination = get_download_destination(key=obj.key, download_path=download_path)
            create_directory(root=download_path, path=get_directory(obj.key))
            bucket.download_file(
                obj.key,
                destination,
            )
            print(f"'{obj.key}' downloaded.")
            count += 1
        except ClientError as e:
            logging.error(e)
    
    print()        
    print(f"{count} files downloaded.")
    

def main():
    endpoint_url = input("Endpoint URL: ")
    aws_access_key_id = input("AWS access key: ")
    aws_secret_access_key = input("AWS secret key: ")
    bucket_name = input("Bucket name: ")
    
    print()
    choice = input("""Menu:
    \r1) Upload files from directory:
    \r2) Delete all objects of a bucket:
    \r3) Download all objects of a bucket:
    \rEnter your choice: """)
    
    if choice == "1":
        directory = input("Directory: ")
        acl = input("ACL: ")
        s3_resource = get_s3_resource(
            endpoint_url=endpoint_url, 
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key,
        )
        upload(
            bucket_name=bucket_name,
            s3_resource=s3_resource, 
            directory=directory, 
            ACL=acl,
        )
    elif choice == "2":
        s3_resource = get_s3_resource(
            endpoint_url=endpoint_url, 
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key,
        )
        delete_many(object_list(s3_resource=s3_resource, bucket_name=bucket_name))
    elif choice == "3":
        s3_resource = get_s3_resource(
            endpoint_url=endpoint_url, 
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key,
        )   
        download_path = input("Enter download path: ")
        download_all(s3_resource=s3_resource, bucket_name=bucket_name, download_path=download_path)
    else:
        print("Wrong choice!")
    

if __name__ == "__main__":
    main()
    