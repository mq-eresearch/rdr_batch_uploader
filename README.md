# MQ RDR Batch Uploader

Batch upload of research metadata to the Macquarie University Research Data Repository

## Description

The Macquarie University [Research Data Repository](https://figshare.mq.edu.au) (RDR) allows researchers to upload, publish and share research data. The _MQ RDR Batch Uploader_ facilitates the upload of metadata records by allowing researchers to supply a CSV file containing multiple metadata entries, and uploading these to the RDR in a single batch operation.

## Getting Started

### Dependencies

- pandas
- getpass
- requests

```
$ pip install pandas
$ pip install getpass
$ pip install requests
```

### Creating the CSV file

Create a csv file (make sure your file ends in _.csv_) and make sure the minimum column headings are included (see Example files)

- How/where to download your program
- Any modifications needed to be made to files/folders

### Executing program

- Execute the batch uploader by running:

```
$ python rdr_batch_uploader myfile.csv
```

- You will be prompted for your RDR API token. See below for instructions on how to generate and access your API token.

## Help/Contact

Please contact Gerry Devine, Macquarie University for any help or advice in using this software:
[gerry.devine@mq.edu.au](mailto:gerry.devine@mq.edu.au)

## Authors

Gerry Devine
Digitally Enabled Research
Macquarie University  
[gerry.devine@mq.edu.au](mailto:gerry.devine@mq.edu.au)

## Features History

- July 2021
  - Initial Release
  - csv file upload of metadata information only

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details
