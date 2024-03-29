# Regex replace  

I ran into issues mutliple times when my regexes were too complex to be handled by file editors (like Notepad++) to use them for batch processing of directories with many files.  
One way to solve the issue is to learn to write better regexes, I guess, but another way is to build a workaround.  
Therefore, I created a python script that simply performs a regex replace on a directory and all subdirectories.  

## Usage  

⚠️ CAUTION: Before using the script, you should always create a backup of your files! ⚠️ 

The script requires the usage of a JSON config file.  
The file contains information on the directory to perform the replacement on (`directory_path`), an optional filter based on the file extension (`file_extension`), and a list of regex patterns and their respective replacement pattern (`regex_patterns`).  
The regex patterns have to be provided as an object consisting of the search pattern as `search` and the replacement pattern as `replace`.  

Assuming the config file is named `config.json` and located in the current directory alongside the `replace.py` script, you can run the script with the following command:

```shell
python3 ./replace.py ./config.json
```

## Example config  

This config is built to identify a property area in a markdown file, that is not located at the top of the file.  
Then the property area will be moved to the top of the file, by replacing the _rest_ group 1 with the _property_ group 2.  

```json
{
    "directory_path": "/path/to/your/directory",
    "file_extension": ".md",
    "regex_patterns": [
        {
            "search": "((?:.|\\r|\\n)+?)(---(?:[\\r\\n]+\\w+:.+)+[\\r\\n]+---)",
            "replace": "\\2\r\n\\1"
        }
    ]
}
```

## Known issues  

This script is not intended to be perfect, it was only built to _function_ for two use-cases I had.  
It does not offer proper error handling!  
