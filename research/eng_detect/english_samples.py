# -*- coding: utf-8 -*-
samples = [

"my hovercraft is full of eels",

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

"""semiotician. He is best known for his groundbreaking 1980 historical
mystery novel Il nome della rosa (The Name of the Rose), an intellectual
mystery combining semiotics in fiction, biblical analysis, medieval studies
and literary theory. He later wrote other novels, including Il pendolo di
Foucault (Foucault's Pendulum) and L'isola del giorno prima (The Island of
the Day Before). His novel Il cimitero di Praga (The Prague Cemetery),
released in 2010, was a best-seller.

Eco also wrote academic texts, children's books and essays. He was founder
of the Dipartimento di Comunicazione (Department of Media Studies) at the
University of the Republic of San Marino, President of the Scuola Superiore
di Studi Umanistici (Graduate School for the Study of the Humanities),
University of Bologna, member of the Accademia dei Lincei and an Honorary
Fellow of Kellogg College, Oxford.""",

"""This definition, together with Peirce's definitions of correspondence and
determination, is sufficient to derive all of the statements that are
necessarily true for all sign relations. Yet, there is much more to the
theory of signs than simply proving universal theorems about generic sign
relations. There is also the task of classifying the various species and
subspecies of sign relations. As a practical matter, of course, familiarity
with the full range of concrete examples is indispensable to theory and
application both.

In Peirce's theory of signs, a sign is something that stands in
a well-defined kind of relation to two other things, its object and its
interpretant sign. Although Peirce's definition of a sign is independent of
psychological subject matter and his theory of signs covers more ground than
linguistics alone, it is nevertheless the case that many of the more
familiar examples and illustrations of sign relations will naturally be
drawn from linguistics and psychology, along with our ordinary experience of
their subject matters.

For example, one way to approach the concept of an interpretant is to think
of a psycholinguistic process. In this context, an interpretant can be
understood as a sign's effect on the mind, or on anything that acts like
a mind, what Peirce calls a quasi-mind. An interpretant is what results from
a process of interpretation, one of the types of activity that falls under
the heading of semiosis. One usually says that a sign stands for an object
to an agent, an interpreter. In the upshot, however, it is the sign's effect
on the agent that is paramount. This effect is what Peirce called the
interpretant sign, or the interpretant for short. An interpretant in its
barest form is a sign's meaning, implication, or ramification, and especial
interest attaches to the types of semiosis that proceed from obscure signs
to relatively clear interpretants. In logic and mathematics the most
clarified and most succinct signs for an object are called canonical forms
or normal forms.

Peirce argued that logic is the formal study of signs in the broadest sense,
not only signs that are artificial, linguistic, or symbolic, but also signs
that are semblances or are indexical such as reactions. Peirce held that
"all this universe is perfused with signs, if it is not composed exclusively
of signs",[3] along with their representational and inferential relations.
He argued that, since all thought takes time, all thought is in signs:

    To say, therefore, that thought cannot happen in an instant, but
		requires a time, is but another way of saying that every thought must be
		interpreted in another, or that all thought is in signs. (Peirce,
		1868[4])

		    Thought is not necessarily connected with a brain. It appears in the
				work of bees, of crystals, and throughout the purely physical world;
				and one can no more deny that it is really there, than that the
				colors, the shapes, etc., of objects are really there. Consistently
				adhere to that unwarrantable denial, and you will be driven to some
				form of idealistic nominalism akin to Fichte's. Not only is thought
				in the organic world, but it develops there. But as there cannot be
				a General without Instances embodying it, so there cannot be thought
				without Signs. We must here give "Sign" a very wide sense, no doubt,
				but not too wide a sense to come within our definition. Admitting
				that connected Signs must have a Quasi-mind, it may further be
				declared that there can be no isolated sign. Moreover, signs require
				at least two Quasi-minds; a Quasi-utterer and a Quasi-interpreter;
				and although these two are at one (i.e., are one mind) in the sign
				itself, they must nevertheless be distinct. In the Sign they are, so
				to say, welded. Accordingly, it is not merely a fact of human
				Psychology, but a necessity of Logic, that every logical evolution
				of thought should be dialogic. (Peirce, 1906[5] )
				""",

# American news (foxnews.com)
"""JERUSALEM –  Samuel Willenberg, the last survivor of Treblinka, the Nazi
death camp where 875,000 people were killed, has died at the age of 93.

Willenberg was among a group of Jews who in 1943 set fire to the camp and
headed to the woods. Hundreds fled, but most were killed by Nazi troops in
the surrounding mine fields or captured by Polish villagers.

The Nazis and their collaborators killed 6 million Jews during World War II.

He described to AP in 2010 how he was shot in the leg as he climbed over
bodies piled at the barbed wire fence and catapulted over. After the war he
made it to Israel.

His daughter said he died on Friday. He is survived by a daughter and
grandchildren.""",

# Australian news (http://www.abc.net.au)
"""'I've never heard anything as pitiful as that moaning'

Bruce Davies, who lives on the road, said he had just gone to bed when he
heard "a terrible bang".

"There was a hell of a noise. I came out and had a look and saw the police
come up behind and they stopped and they turned their headlights back on and
there was a body lying on the footpath," he said.

"I've never heard anything as pitiful as that moaning. They must have been
in some terrible pain.

"I didn't hear anything until the bang. I was wide awake, I'd only just gone
to bed. The only noise I heard was a bang and then the siren coming up the
street behind it."

Assistant Commissioner Clifford said the only way to describe the crash was
as "horrific".

"Three young people have lost their lives tonight and that's a tragedy," he
said.

"We are yet to piece together the circumstances of what occurred and the
matter will be put together for the coroner.

"The officers have been provided with a lot of support. As you can imagine
there's a lot of people who will be very much affected by what occurred
tonight, a lot of lives that will be changed forever."

Police are unable to confirm whether the driver was one of those killed in
the collision.
""",

"""Archbishop of Melbourne Denis Hart is supporting calls for an independent
investigation to find out who leaked details of a reported police
investigation into alleged abuse by Cardinal George Pell.
Key points:

Archbishop Hart supports inquiry call
Calls media leak "disturbing"
Says allegations "do not reflect" George Pell
Says leak designed to damage Cardinal Pell before his
testifies at royal commission

The Herald Sun newspaper published a report that said
a Victoria Police taskforce was investigating allegations of
abuse by Australia's most high-profile Catholic.

In a statement, Cardinal Pell vehemently denied the
allegations, calling them "undetailed", and said they had
not been raised with him.

Cardinal Pell called for a public inquiry into the source of
the leak and Archbishop Hart released a statement defending
the cardinal.""",

# Canadian news (http://www.cbc.ca)
"""A U.S. security decision that banned private Canadian aircraft from
flying through American airspace when travelling between cities in Canada
affected dozens of flights and cost thousands of dollars in extra fuel
before the decision was reversed, industry officials say.

The U.S. Federal Aviation Administration [FAA] issued a notice Dec.14 last
year warning private pilots that all foreign private planes now had to
obtain diplomatic clearance from the secretary of state before entering U.S.
airspace.

Neil Macdonald: Air Canada's reimbursement policy
Canada's electronic spy agency stops sharing data
Bombardier to cut up to 7,000 jobs

The situation persisted for a month and cost thousands of
dollars in increased fuel as planes had to be diverted.

Bernard Gervais president of the Canadian Owners and Pilots
Association [COPA] worries the situation could reoccur.

"I don't want this to happen again," Gervais told CBC News.
"It's a big issue for us. We need overfly there. There's no wall
between our countries. It's always been that way."

Rudy Toering, president of the Canadian Business Aviation
Association, says he wants reassurance from Transport Canada and
the FAA that both agencies will follow the proper protocol in
the future.

We want to know "that there will be direct communications
between Canada and the United States as far as what are the
impacts of this particular [decision]," Toering said.

"We're taking steps both from COPA and from ourselves to make
sure the proper communication protocol is in place. I'm sure on
the U.S. side the same thing is happening," he added.""",

"""
Wim Pretorius, News24
Deputy President Cyril Ramaphosa.

Deputy President Cyril Ramaphosa. (GCIS)

Multimedia   ·   User Galleries   ·   News in Pictures Send us your pictures
·  Send us your stories
Related Links

Ramaphosa's bodyguard injured in Cape Town crash
ANC will not play Zama Zama with people’s futures – Ramaphosa
Ramaphosa reflects on the year

Johannesburg – South Africa needed young people who resolved
differences through dialogue, not through vandalism, violence or
intimidation.

Deputy President Cyril Ramaphosa delivered this message at the
Youth Development and Career Expo held at the University of
Johannesburg on Saturday.

"We need young people that resolve differences through dialogue,
not through vandalism, violence or intimidation," he said.

Ramaphosa told students the government posted a list of the top
100 scarce skills in the country every two years and that they
should use this list when making career choices.

Dire shortages of certain skills

“We have a dire shortage of electrical, civil, mechanical,
industrial and chemical engineers,” Ramaphosa said."There are
many unfilled vacancies for quantity surveyors, project managers
and finance managers.

"We have a shortage of artisans. Many of these qualifications
can be acquired at TVET colleges. Government is investing
significantly in these colleges""",

]
