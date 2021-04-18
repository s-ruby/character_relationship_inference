# Character Relationship Inference

This repository is the for the COMS 4995 Final Project. The project aims to automatically infer character relationships in fiction novels and output character arc visualizaitons. The project uses a variety of techniques in information extraction including snowball tchniques and [SpanBert](https://github.com/gkaramanolakis/SpanBERT).


## Install Requirements

```
pip3 install -U pip setuptools wheel
pip3 install -U spacy
python3 -m spacy download en_core_web_lg
pip3 install -r requirements.txt
```

## [Optionally] Download the fine-tuned SpanBERT model run:


`bash download_finetuned.sh`

If the `bash` command results in an error, try `brew install wget`


## Training the custom SpanBert Model:

1. Create Training Data run `python3 run_data_generator.py` and manually annotate the relationship in each sentence. You can use a keyboard interrupt to stop generating training data at any time (control + c)

2. Fine-Tune the SpanBert

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

## To Run

```
# Optionally pass custom span bert model
python3 main.py --model_dir=span_bert_training_output --min_conf=0.45
```

