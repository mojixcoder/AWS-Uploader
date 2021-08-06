## AWS-uploader  
Upload all files from a local directory to AWS S3.  

***Note:***

 - Only supports Linux and **doesn't** support Windows yet.
 - Tested on Ubuntu 20.04.2.
 

 ## Installation
First clone repository.  

	 $ git clone https://github.com/MojixCoder/AWS-uploader.git 
Go to cloned directory.  

    $ cd AWS-uploader/  
Now install `requirements.txt` and run `aws.py`.

    $ pip install -r requirements.txt && python aws.py

 ## Example
When you run `aws.py`  it receives 6 parameters.

 1. **Directory:** Absolute path to directory
 2. **Endpoint URL:** AWS endpoint URL
 3. **AWS access key:** AWS access key of your storage
 4. **AWS secret key:**  AWS secret key of your storage
 5. **ACL:** Access Control List like private, public-read, etc.
 6. **Bucket name:** Bucket name that you want to upload files on.  

Let's sat you have this directory.   

    .
    ├── directory
	│   ├── a.txt
	│   └── sub_dir1
	│   │   └── b.txt
	│   └── sub_dir2
	│       ├── c.txt
	│       └── sub_sub_dir
	│			└── d.txt

After it starts uploading files it uses the sub directories as separators.  

    Uploading files to {bucket_name}...

	Uploaded 'a.txt'
	Uploaded 'sub_dir1/b.txt'
	Uploaded 'sub_dir2/c.txt'
	Uploaded 'sub_dir2/sub_sub_dir/d.txt'
	
	4 files uploaded.
  
