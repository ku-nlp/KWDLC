# Kyoto University Web Document Leads Corpus #

### Overview ###

This is a Japanese text corpus that consists of lead three sentences
of web documents with various linguistic annotations. By collecting
lead three sentences of web documents, this corpus contains documents
with various genres and styles, such as news articles, encyclopedic
articles, blogs and commercial pages. It comprises approximately 5,000
documents, which correspond to 15,000 sentences.

The linguistic annotations consist of annotations of morphology, named
entities, dependencies, predicate-argument structures including zero
anaphora, coreferences, and discourse. All the annotations except
discourse annotations were given by manually modifying automatic
analyses of the morphological analyzer JUMAN and the dependency, case
structure and anaphora analyzer KNP. The discourse annotations were
given using crowdsourcing.


### Notes ###

This corpus consists of linguistically annotated Web documents that
have been made publicly available on the Web at some time. The corpus
is released for the purpose of contributing to the research of natural
language processing.

Since the collected documents are fragmentary, i.e., only the lead
three sentences of each Web document, we have not obtained permission
from copyright owners of the Web documents and do not provide source
information such as URL. If copyright owners of Web documents request
addition of source information or deletion of these documents, we will
update the corpus and newly release it. In this case, please delete
the downloaded old version and replace it with the new version.


### Notes on annotation guidelines ###

The annotation guidelines for this corpus are written in the manuals
found in "doc" directory. The guidelines for morphology and
dependencies are described in syn_guideline.pdf, those for
predicate-argument structures and coreferences are described in
rel_guideline.pdf, and those for discourse relations are described in
disc_guideline.pdf. The guidelines for named entities are available at
the IREX web site (http://nlp.cs.nyu.edu/irex/).


### Distributed files ###

* knp/ : the corpus annotated with annotations of morphology, named entities, dependencies, predicate-argument structures, and coreferences
* disc/ : the corpus annotated with discourse relations
* org/ : the raw corpus
* doc/ : annotation guidelines
* {train,test}.files : the file lists for evaluation

Note that the encoding of the corpus data is UTF-8.


### Format of the corpus annotated with annotations of morphology, named entities, dependencies, predicate-argument structures, and coreferences ###

Annotations of this corpus are given in the following format.

```
# S-ID:w201106-0000010001-1
* 2D
+ 3D
太郎 たろう 太郎 名詞 6 人名 5 * 0 * 0
は は は 助詞 9 副助詞 2 * 0 * 0
* 2D
+ 2D
京都 きょうと 京都 名詞 6 地名 4 * 0 * 0
+ 3D <ne type="ORGANIZATION" target="京都大学"/>
大学 だいがく 大学 名詞 6 普通名詞 1 * 0 * 0
に に に 助詞 9 格助詞 1 * 0 * 0
* -1D
+ -1D <rel type="ガ" target="太郎" sid="w201106-0000010001-1" id="0"/><rel type="ニ" target="大学" sid="w201106-0000010001-1" id="2"/>
行った いった 行く 動詞 2 * 0 子音動詞カ行促音便形 3 タ形 10
EOS
```

The first line represents the ID of this sentence. In the subsequent
lines, the lines starting with "*" denote "bunsetsu," the lines starting
with "+" denote basic phrases, and the other lines denote morphemes.

The line of morphemes is the same as the output of the morphological
analyzers, JUMAN and Juman++. This information includes surface
string, reading, lemma, part of speech (POS), fine-grained POS,
conjugate type, and conjugate form. "*" means that its field is not
available. Note that this format is slightly different from KWDLC 1.0,
which adopted the same format as Kyoto University Text Corpus 4.0.

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
the following four attributes: type, target, sid, and id, which mean
the name of a relation, the string of the counterpart, the sentence ID
of the counterpart, and the basic phrase ID of the counterpart,
respectively. If a basic phrase has multiple tags of the same type, a
"mode" attribute is also assigned, which has one of "AND," "OR," and
"？." The details of these attributes are described in the annotation
guidelines (rel_guideline.pdf).


### Format of the corpus annotated with discourse relations ###

In this corpus, a clause pair is given a discourse type and its probability as follows.

```
# A-ID:w201106-0001998536
1 今日とある企業のトップの話を聞くことが出来た。
2 経営者として何事も全てビジネスチャンスに変えるマインドが大切だと感じた。
3 生きていく上で追い風もあれば、
4 逆風もある。
1-2 関係なしまたは弱い関係:0.999915 対比:3.6e-05 根拠:1.5e-05 原因・理由:8e-06 目的:7e-06
3-4 対比:0.999986 その他根拠:3e-06

```

The first line represents the ID of this document, the subsequent
block denotes clause IDs and clauses, and the last block denotes
discourse relations for clause pairs and their probabilities. These
discourse relations and probabilities are the results of the second
stage of crowdsourcing. Each line is the list of a discourse relation
and its probability in order of probability. For the discourse
relation with the highest probability, the discourse direction is
annotated; if it is reverse order, "(逆方向)" is added to the
discourse relation. The details of these probabilities and discourse
relations are described in [Kawahara et al., 2014] and the annotation
guidelines (disc_guideline.pdf).


### References ###

* Masatsugu Hangyo, Daisuke Kawahara and Sadao Kurohashi. Building a Diverse Document Leads Corpus Annotated with Semantic Relations, In Proceedings of the 26th Pacific Asia Conference on Language Information and Computing, pp.535-544, 2012. http://www.aclweb.org/anthology/Y/Y12/Y12-1058.pdf
* 萩行正嗣, 河原大輔, 黒橋禎夫. 多様な文書の書き始めに対する意味関係タグ付きコーパスの構築とその分析, 自然言語処理, Vol.21, No.2, pp.213-248, 2014. https://doi.org/10.5715/jnlp.21.213
* Daisuke Kawahara, Yuichiro Machida, Tomohide Shibata, Sadao Kurohashi, Hayato Kobayashi and Manabu Sassano. Rapid Development of a Corpus with Discourse Annotations using Two-stage Crowdsourcing, In Proceedings of the 25th International Conference on Computational Linguistics, pp.269-278, 2014. http://www.aclweb.org/anthology/C/C14/C14-1027.pdf


### Acknowledgment ###

The creation of this corpus was supported by JSPS KAKENHI Grant Number 24300053 and JST CREST "Advanced Core Technologies for Big Data Integration." The discourse annotations were acquired by crowdsourcing under the support of Yahoo! Japan Corporation. We deeply appreciate their support.


### Contact ###

If you have any questions or problems about this corpus, please send an email to nl-resource at nlp.ist.i.kyoto-u.ac.jp. If you have a request to add source information or to delete a document in the corpus, please send an email to this mail address.
