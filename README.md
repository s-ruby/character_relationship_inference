# Character Relationship Inference

This respository is a fork from [SpanBert](https://github.com/gkaramanolakis/SpanBERT) which adapted the SpanBERT scripts from Facebook Research to support relation extraction from general documents beyond the TACRED dataset.


## Install Requirements

`pip3 install -U pip setuptools wheel` \
`pip3 install -U spacy`\
`python3 -m spacy download en_core_web_lg`\
`pip3 install -r requirements.txt`

## To download the fine-tuned SpanBERT model run:


`bash download_finetuned.sh`

If the `bash` command results in an error, try `brew install wget`

## To Run

`python3 main.py`

## To Fine-Tune SpanBert

To fine-tune the SpanBert model with custom relations, you can add custom relations the the /data folder. Annotations should be derived from the Stanford NLP package. 

```
python3 run_train_spanbert.py \
  --do_train \
  --do_eval \
  --eval_test \
  --data_dir data \
  --model spanbert-base-cased \
  --train_batch_size 32 \
  --eval_batch_size 32 \
  --learning_rate 2e-5 \
  --num_train_epochs 10 \
  --max_seq_length 128 \
  --output_dir span_bert_training_output
```