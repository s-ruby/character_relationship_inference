[NeuralCoref](https://github.com/huggingface/neuralcoref) was used for anaphora resolution. 

Approach:
- Temporarily removed punctuation from conversations (inside quotations) in order to not lose subject
- Resolve text at sentence level 
- Resolve text using prior sentence for additional context
- Added code to handle possession since NeuralCoref does not i.e `Harry and his wand` would resolve to `Harry and Harry wand`
  - Added `['s]` to mark where a possessive pronoun was (his, her, their), if pronoun was resolved, concatenate `'s` to subject, then delete the added `['s]`
