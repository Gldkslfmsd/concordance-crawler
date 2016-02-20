
samples = [

#"my hovercraft is full of eels",

"""I decided to make my own English detector, a function that decides, whether
an input text is English or not. It will use cosine similarity of vector of
frequencies of n-grams and thresholding.
""", 

# http://www.bbc.com/news/world-europe-35618389
"""Hundreds of migrants living in part of a camp in the French port of
Calais known as the Jungle have been ordered to leave or face eviction.""",

"""The area has become a cultural hub for many of the migrants. It has
shops, a school and religious structures.

The authorities said up to 1,000 people could be affected but volunteers on
the ground estimated that at least twice that number lived in the area.
""",

# http://www.bbc.com/news/technology-35614335
"""On his blog, Prof Woodward noted there had not been a similar increase in
.onion sites in the history of the Tor network.

"Something unprecedented is happening, but at the moment that is all we
know," he told the BBC.

"It is hard to know for certain what the reason is for the jump because one
of the goals of Tor is to protect people's privacy by not disclosing how
they are using Tor," said Dr Steven Murdoch at University College London.

Another curiosity described by Prof Woodward was the fact that, despite the
rise of hidden addresses, traffic on the network has not seen a comparable
spike.""",

# 
"""I'm selfish, impatient and a little insecure.
""",

"""Be yourself; everyone else is already taken.""",

"""“Two things are infinite: the universe and human stupidity; and I'm not
sure about the universe.”
― Albert Einstein""",

"""“You've gotta dance like there's nobody watching,
Love like you'll never be hurt,
Sing like there's nobody listening,
And live like it's heaven on earth.”
― William W. Purkey""",

#"""“God has no religion.” """,

# http://www.karaoketexty.cz/texty-pisni/adele/hello-717629
#"""Hello, it's me, I was wondering""",
#"""If after all these years you'd like to meet""",
#"""To go over everything""",
"""
Hello from the outside
At least I can say that I've tried
To tell you I'm sorry for breaking your heart
But it don't matter
It clearly doesn't tear you apart anymore""",

# https://en.wikipedia.org/wiki/Cosine_similarity
"""The cosine of two vectors can be derived by using the Euclidean dot
product formula:
Given two vectors of attributes, A and B, the cosine similarity, cos(θ),
is represented using a dot product and magnitude as


The resulting similarity ranges from −1 meaning exactly
opposite, to 1 meaning exactly the same, with 0 indicating
orthogonality (decorrelation), and in-between values indicating
intermediate similarity or dissimilarity.

For text matching, the attribute vectors A and B are usually the
term frequency vectors of the documents. The cosine similarity
can be seen as a method of normalizing document length during
comparison.

In the case of information retrieval, the cosine similarity of
two documents will range from 0 to 1, since the term frequencies
(tf-idf weights) cannot be negative. The angle between two term
frequency vectors cannot be greater than 90°.

If the attribute vectors are normalized by subtracting the
vector means (e.g., A - \bar{A}), the measure is called centered
cosine similarity and is equivalent to the Pearson Correlation
Coefficient.
Angular similarity

The term "cosine similarity" has also been used on occasion to
express a different coefficient, although the most common use is
as defined above. Using the same calculation of similarity, the
normalised angle between the vectors can be used as a bounded
similarity function within [0,1], calculated from the above
definition of similarity by:


in a domain where vector coefficients may be positive or
negative, or

in a domain where the vector coefficients are always
positive.

Although the term "cosine similarity" has been used for
this angular distance, the term is oddly used as the
cosine of the angle is used only as a convenient
mechanism for calculating the angle itself and is no
part of the meaning. The advantage of the angular
similarity coefficient is that, when used as
a difference coefficient (by subtracting it from 1) the
resulting function is a proper distance metric, which is
not the case for the first meaning. However, for most
uses this is not an important property. For any use
where only the relative ordering of similarity or
distance within a set of vectors is important, then
which function is used is immaterial as the resulting
order will be unaffected by the choice.
Confusion with "Tanimoto" coefficient

The cosine similarity may be easily confused with the
Tanimoto metric - a specialised form of a similarity
coefficient with a similar algebraic form:

T(A,B) = {A \cdot B \over \|A\|^2 +\|B\|^2 - A \cdot
B}

In fact, this algebraic form was first defined by
Tanimoto as a mechanism for calculating the Jaccard
coefficient in the case where the sets being
compared are represented as bit vectors. While the
formula extends to vectors in general, it has quite
different properties from cosine similarity and
bears little relation other than its superficial
appearance.
Ochiai coefficient

This coefficient is also known in biology as Ochiai
coefficient, or Ochiai-Barkman coefficient, or
Otsuka-Ochiai coefficient:[3][4]

K =\frac{n(A \cap B)}{\sqrt{n(A) \times n(B)}}

Here, A and B are sets, and n(A) is the number
of elements in A. If sets are represented as bit
vectors, the Ochiai coefficient can be seen to
be the same as the cosine similarity.
Properties

Cosine similarity is related to Euclidean
distance as follows. Denote Euclidean distance
by the usual \|A - B\|, and observe that


by expansion. When A and B are normalized to
unit length, \|A\|^2 = \|B\|^2 = 1 so the
previous is equal to


Null distribution: For data which can be
negative as well as positive, the null
distribution for cosine similarity is
the distribution of the dot product of
two independent random unit vectors.
This distribution has a mean of zero and
a variance of 1/n (where n is the number
of dimensions), and although the
distribution is bounded between -1 and
+1, as n grows large the distribution is
increasingly well-approximated by the
normal distribution.[5][6] For other
types of data, such as bitstreams
(taking values of 0 or 1 only), the null
distribution will take a different form,
and may have a nonzero mean.[7]
								""",

]
