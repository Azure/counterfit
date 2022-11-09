# Troubleshooting

This is a list of common issues when using Counterfit. For additional questions
or other issues, check the [Counterfit discussion ](https://github.com/Azure/counterfit/discussions).


### Problem: Resource stopwords not found

This issue is caused because the NLTK does not have the necessary libraries it
needs. Below is an example of the error you might see.

```
(counterfit) azure@LAPTOP:~/counterfit$ counterfit

Traceback (most recent call last):
  File " /home/azure/miniconda3/envs/counterfit/lib/python3.8/site-packages/nltk/corpus/util.py", line 84, in __load
    root = nltk.data.find(f"(self.subdir}/{zip_name}")
  File " /home/azure/miniconda3/envs/counterfit/lib/python3.8/site-packages/nltk/data.py", line 583, in find
    raise LookupError(resource_not_found)
LookupError:
*******************
  Resource stopwords not found.
  Please use the NLTK Downloader to obtain the resource:
  
  >>> import nltk
  >>> nltk.downLoad('stopwords")

```

The solution is to install the NLTK dependencies manually. This should be needed at most once per
installation
```bash
python -c "import nltk;  nltk.download('stopwords')"
```
