# terra-to-aws
Functions and documentation for copying data from the Terra GCP platform to AWS


**Environment**

- This script is designed to be executed on a compute instance on the [Terra Platform](https://app.terra.bio/), with a configured project billing project. Documentation for Terra can be found here: https://support.terra.bio/hc/en-us/categories/360001399872-Documentation

- Python3 is required to run this script, which should come pre-installed on your Terra Instance.

- In addition, you must configure your AWS credentials by installing the [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). 
  
Terra instances do not grant you sudo privlidges, so please follow the instructions for installing without sudo(making sure to change these paths to locations you have access to on your instance):
```
$ ./aws/install -i /usr/local/aws-cli -b /usr/local/bin
```

From here, your AWS CLI must be configured in order to access your AWS bucket. Instructions for Strides account users at Sage are as follows:
```
    Ensure that you have AWS CLI v2 installed

    You can check with: aws --version

    Install the awscli-saml Python package
    Install the SAML Response Chrome extension (or this Firefox extension)

    If you’re using a different browser, you’ll need to identify an extension that captures the base64-encoded SAML assertion

    Add the snippet below to your AWS config

    On macOS and Linux, it’s located at ~/.aws/config

    Test by logging in as follows:

    Log into JumpCloud
    Click on the AWS icon for strides-ampad-workflows-towerviewer
    Click on the Chrome extension (look for the blue key) and copy the base64-encoded SAML assertion. In my case, the extension window is very narrow, but I’m still able to click and copy the text from the first box (see screenshot).
    Run aws-saml --profile ampad at the command line
    Paste the SAML assertion and press Enter

    Test by accessing one of your buckets with:

    aws --profile ampad s3 ls s3://<some-project>-tower-bucket/ 
```

AWS config snippet:
```
[profile ampad]
saml.role_arn = arn:aws:iam::751556145034:role/strides-ampad-workflows-towerviewer
saml.idp_arn = arn:aws:iam::751556145034:saml-provider/strides-ampad-workflows-towerviewer
saml.session_duration = 28800
```

**Required Inputs**

The following input parameters are required:

-input_file: a local path to a text file that contains a list of gcp objects that you want to copy. This can be generated using the `gsutil ls` command. Example: `"/home/jupyter/commit/smalltest.txt"`

-s3_prefix: a prefix that will define the path that objects will be copied to on your S3 bucket. Example: `"rnaseq_cram"` 

-s3_bucket: The name of the S3 bucket that you are copying data to. Example: `"strides-ampad-project-tower-bucket"`

-gcs_project: the GCS project ID for your Terra instance. This can be found by running `export $GOOGLE_PROJECT` on your Terra instance. Example: `"terra-a9763d"`


**Special Considerations**
- At Sage and other AWS environments, your AWS access token will expire after 8 hours. This will require you to restart the data transfer, taking care to pickup after the last file that was succesfully copied. 
- It is highly recommended to check the fidelity of your data transfer by comparing the file size or md5sums (if available) of the gcp and s3 objects following completion of the data transfer
- Choice of instance configuration (cpus, memory, network bandwidth, etc.) may increase the speed of your data transfer, but this script is relatively slow for copying large amounts of data. 
- Future development efforts will include better error handling and parallelization of the data transfer



