# Character Relationship Inference

This respository is a fork from [SpanBert](https://github.com/gkaramanolakis/SpanBERT) which adapted the SpanBERT scripts from Facebook Research to support relation extraction from general documents beyond the TACRED dataset.


# Install Requirements

`pip3 install -U pip setuptools wheel` \
`pip3 install -U spacy`\
`python3 -m spacy download en_core_web_lg`\
`pip3 install -r requirements.txt`\

# To download the fine-tuned SpanBERT model run:


`bash download_finetuned.sh`

If the `bash` command results in an error, try `brew install wget`

# To Run

`python3 main.py`
