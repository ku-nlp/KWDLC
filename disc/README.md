### Files ###

* `disc_crowdsourcing.txt` annotation file annotated by crowd workers.
* `disc_expert.txt` annotation file annotated by experts.
* `make_knp_file_with_discourse_annotation.py` python script to convert annotation files to KNP-format files.

### Note ###

If you want to use same format as "the corpus annotated with morphology, named entities, dependencies, predicate-argument structures, and coreferences", please run the following command. 

```
$ python make_knp_file_with_discourse_annotation.py
```

That command outputs two files.

* `disc_crowdsourcing.knp` annotation file annotated by crowd workers.
* `disc_expert.knp` annotation file annotated by experts.

#### Options ####

```
usage: make_knp_file_with_discourse_annotation.py [-h] [-g] [--remove_duplicate_from_expert] [--remove_duplicate_from_crowd]

optional arguments:
  -h, --help            show this help message and exit
  -g, --gold_knp        use the corpus annotated with morphology, named entities, dependencies, predicate-argument structures, and coreferences
  --remove_duplicate_from_expert
                        Remove duplicate documents from annotation file annotated by experts.
  --remove_duplicate_from_crowd
                        Remove duplicate documents from annotation file annotated by crowd workers.
```

