# Kyoto University Web Document Leads Corpus #

### Overview ###

This is a Japanese text corpus that consists of lead three sentences
of web documents with various linguistic annotations. It comprises
5,000 documents (15,000 sentences) with annotations of morphology,
named entities, dependencies, predicate-argument structures including
zero anaphora, and coreferences. These annotations were given by
manually modifying automatic analyses of the morphological analyzer
JUMAN and the dependency, case structure and anaphora analyzer
KNP. This corpus also includes 10,000 documents (30,000 sentences)
with discourse relations between clauses manually assigned via
crowdsourcing.


### Distributed files ###

* knp/ : the corpus annotated with annotations of morphology, named entities, dependencies, predicate-argument structures, and coreferences
* doc/ : annotation guidelines

Note that the encoding of the corpus data is UTF-8.


### Format of the corpus annotated with annotations of morphology, named entities, dependencies, predicate-argument structures, and coreferences ###

Annotations of this corpus are given in the following format.

```
# S-ID:w201106-0000010001-1
* 2D
+ 3D
太郎 たろう * 名詞 人名 * * 
は は * 助詞 副助詞 * *
* 2D
+ 2D
京都 きょうと * 名詞 地名 * *
+ 3D <ne type="ORGANIZATION" target="京都大学"/>
大学 だいがく * 名詞 普通名詞 * *
に に * 助詞 格助詞 * *
* -1D
+ -1D <rel type="ガ" target="太郎" sid="w201106-0000010001-1" tag="0"/><rel type="ニ" target="大学" sid="w201106-0000010001-1" tag="2"/>
行った いった 行く 動詞 * 子音動詞カ行促音便形 基本形
EOS
```

The first line represents the ID of this sentence. In the subsequent
lines, the lines starting with "*" denote "bunsetsu," the lines starting
with "+" denote basic phrases, and the other lines denote morphemes.

The line of morphemes is based on the output the morphological
analyzer, JUMAN.  This information includes surface string, reading,
lemma ("*" if it does not conjugate), part of speech (POS),
fine-grained POS, conjugate type, and conjugate form.

The line starting with "*" represents "bunsetsu," which is a
conventional unit for dependency in Japanese. "Bunsetsu" consists of
one or more content words and zero or more function words. In this
line, the first numeral means the ID of its depending head. The subsequent alphabet
denotes the type of dependency relation, i.e., "D" (normal
dependency), "P" (coordination dependency), "I" (incomplete
coordination dependency), and "A" (appositive dependency).

The line starting with "+" represents a basic phrase, which is a unit
to which various relations are annotated. A basic phrase consists of
one content word and zero or more function words. Therefore, it is
equivalent to a bunsetsu or a part of a bunsetsu. In this line, the
first numeral numeral means the ID of its depending head. The subsequent alphabet is
defined in the same way as bunsetsu. The remaining part of this line
includes the annotations of named entity and various relations.

Annotations of named entity are given in <ne> tags. <ne> has the
following four attributes: type, target, possibility, and
optional_type, which mean the class of a named entity, the string of
a named entity, possible classes for an OPTIONAL named entity, and a
type for an OPTIONAL named entity, respectively. The details of these
attributes are described in the IREX annotation guidelines.

Annotations of various relations are given in <rel> tags. <rel> has
the following four attributes: type, target, sid, and tag, which mean
the name of a relation, the string of the counterpart, the sentence ID
of the counterpart, and the basic phrase ID of the counterpart,
respectively. If a basic phrase has multiple tags of the same type, a
"mode" attribute is also assigned, which has one of "AND," "OR," and
"？." The details of these attributes are described in the annotation
guidelines (rel_guideline.pdf).


### References ###

* Masatsugu Hangyo, Daisuke Kawahara and Sadao Kurohashi. Building a Diverse Document Leads Corpus Annotated with Semantic Relations, In Proceedings of the 26th Pacific Asia Conference on Language Information and Computing, pp.535-544, 2012. http://www.aclweb.org/anthology/Y/Y12/Y12-1058.pdf
* Daisuke Kawahara, Yuichiro Machida, Tomohide Shibata, Sadao Kurohashi, Hayato Kobayashi and Manabu Sassano. Rapid Development of a Corpus with Discourse Annotations using Two-stage Crowdsourcing, In Proceedings of the 25th International Conference on Computational Linguistics, pp.269-278, 2014. http://www.aclweb.org/anthology/C/C14/C14-1027.pdf